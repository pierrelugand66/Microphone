import csv
import json
import os
from datetime import datetime, timedelta
from PySide6.QtWidgets import QFileDialog, QMainWindow, QDialog, QTableWidgetItem, QMessageBox, QInputDialog, QLineEdit

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from ihm_wifi import Ui_MainWindow
from dialog_params_reseau import Ui_DialogParamsReseau
from udp_worker import UDPWorker
from remote_worker import RemoteWorker
from trame_parser import parser_trame, parser_ack, parser_trame_binaire
from graph_manager import GraphManager
from data_manager import DataManager
from PySide6.QtCore import QTimer

# Couleurs par sévérité (fond de ligne)
_COULEUR_SEVERITE = {
    "critique": QColor("#7F1F1F"),   # rouge foncé
    "haute":    QColor("#7F4A00"),   # orange foncé
    "moyenne":  QColor("#5A5A00"),   # jaune foncé
    "basse":    QColor("#1A3A1A"),   # vert très foncé
}

PARAMS_DEFAUT = {
    "sps":        "1000 Hz",
    "fft":        "512",
    "udp":        "10 Hz",
    "resolution": "12 bits",
    "mode":       "Continu",
    "timeout":    "30 s",
    "val_max":    100.0,
    "val_min":    0.0,
    "rms_max":    50.0,
    "db_max":     90.0,
    "capteur_id": "",
    "capteur_nom":"",
    "carte":      "",
}

class MainController(QMainWindow):
    def __init__(self, mode="local", ip_distante=""):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Onglet Production grisé au démarrage
        self.ui.tabWidget.setTabEnabled(1, False)

        # Désactiver le scan en mode distant
        if mode == "distant":
            self.ui.btn_scan.setEnabled(False)
            self.ui.btn_scan.setToolTip("Scan indisponible en mode distant — connexion directe via IP")

        # Initialisation de la base de données
        self.db = DataManager()
        self.db.purger_alarmes_acquittees()   

        # Initialisation du worker UDP
        if mode == "distant":
            self.udp = RemoteWorker(ip_serveur=ip_distante)
        else:
            self.udp = UDPWorker(
                port_local=5001,
                port_dest=5002,
                broadcast="192.168.10.255",
                mode=mode,
                ip_distante=ip_distante,
            )
        self.udp.trame_recue.connect(self.traiter_trame)
        self.udp.ack_recu.connect(self.traiter_ack)
        try:
            self.udp.demarrer()
        except RuntimeError as e:
            QMessageBox.critical(self, "Erreur UDP", str(e))

        # Titre de fenêtre selon le mode 
        if mode == "distant":
            self.setWindowTitle(f"IHM Wi-Fi — Mode Distant ({ip_distante})")
        else:
            self.setWindowTitle("IHM Wi-Fi — Mode Local")

        # Connexion des signaux
        self.connecter_signaux()

        # Carte sélectionnée
        self.ip_carte_selectionnee = None

        # Initialisation des graphes
        self.graph_prod = GraphManager(
            self.ui.widget_prod_signal,
            self.ui.widget_prod_fft
        )
        self.graph_histo = GraphManager(
            self.ui.widget_courbe,
            self.ui.widget_fft
        )
        self._timer_graph = QTimer(self)
        self._timer_graph.timeout.connect(self._rafraichir_graphes)
        self._timer_graph.start(100)  # rafraîchissement 10Hz


        #compteur de trames MIC 
        self._compteur_mic = 0

        #initialisation min/max global pour affichage
        self._min_global = float('inf')
        self._max_global = float('-inf')
        self._last_mic_time = None

        # Compteur de séquence partagé pour toutes les commandes UDP
        self._seq = 0
        self._timestamps_envoi = {}
        self._paquets_recus = 0
        self._paquets_envoyes = 0
        self._timer_debit = QTimer(self)
        self._timer_debit.timeout.connect(self._maj_metriques)
        self._timer_debit.start(1000)  

        # Initialisation de l'onglet Historique
        self._init_historique()
        self._charger_capteurs_connus()
        self._init_params()

        # Initialisation de la table alarmes + chargement initial
        self._init_table_alarmes()

        # Peupler les filtres alarmes
        self.ui.combo_filtre_severite.addItems(["Toutes", "critique", "haute", "moyenne", "basse"])
        self.ui.combo_filtre_capteur.addItem("Tous les capteurs")
        self.ui.combo_filtre_severite.currentIndexChanged.connect(self.filtrer_alarmes)
        self.ui.combo_filtre_capteur.currentIndexChanged.connect(self.filtrer_alarmes)
        self.charger_alarmes()
        
    # ─────────────────────────────────────────────────────────
    # INITIALISATION
    # ─────────────────────────────────────────────────────────

    def _init_params(self):
        """Remplit les combos de l'onglet Paramètres et charge les valeurs sauvegardées."""
        self.ui.combo_params_sps.addItems(["100 Hz", "500 Hz", "1000 Hz", "5000 Hz", "10000 Hz"])
        self.ui.combo_params_fft.addItems(["128", "256", "512", "1024", "2048"])
        self.ui.combo_params_udp.addItems(["1 Hz", "5 Hz", "10 Hz", "50 Hz", "100 Hz"])
        self.ui.combo_params_resolution.addItems(["8 bits", "10 bits", "12 bits", "16 bits"])
        self.ui.combo_params_mode.addItems(["Continu", "Déclenché", "Mode éco"])
        self.ui.combo_params_timeout.addItems(["10 s", "30 s", "60 s", "120 s", "300 s"])

        params = self._charger_params_fichier()
        self._appliquer_params_ui(params)

    def _appliquer_params_ui(self, params):
        """Injecte un dict de params dans les widgets."""
        def set_combo(combo, val):
            idx = combo.findText(val)
            if idx >= 0:
                combo.setCurrentIndex(idx)

        set_combo(self.ui.combo_params_sps,        params["sps"])
        set_combo(self.ui.combo_params_fft,        params["fft"])
        set_combo(self.ui.combo_params_udp,        params["udp"])
        set_combo(self.ui.combo_params_resolution, params["resolution"])
        set_combo(self.ui.combo_params_mode,       params["mode"])
        set_combo(self.ui.combo_params_timeout,    params["timeout"])
        self.ui.spinbox_val_max.setValue(params["val_max"])
        self.ui.spinbox_val_min.setValue(params["val_min"])
        self.ui.spinbox_rms_max.setValue(params["rms_max"])
        self.ui.spinbox_db_max.setValue(params["db_max"])
        self.ui.input_capteur_id.setText(params["capteur_id"])
        self.ui.input_capteur_nom.setText(params["capteur_nom"])
        self.ui.combo_capteur_carte.setText(params["carte"])

    def _lire_params_ui(self):
        """Lit les valeurs actuelles des widgets et retourne un dict."""
        return {
            "sps":         self.ui.combo_params_sps.currentText(),
            "fft":         self.ui.combo_params_fft.currentText(),
            "udp":         self.ui.combo_params_udp.currentText(),
            "resolution":  self.ui.combo_params_resolution.currentText(),
            "mode":        self.ui.combo_params_mode.currentText(),
            "timeout":     self.ui.combo_params_timeout.currentText(),
            "val_max":     self.ui.spinbox_val_max.value(),
            "val_min":     self.ui.spinbox_val_min.value(),
            "rms_max":     self.ui.spinbox_rms_max.value(),
            "db_max":      self.ui.spinbox_db_max.value(),
            "capteur_id":  self.ui.input_capteur_id.text(),
            "capteur_nom": self.ui.input_capteur_nom.text(),
            "carte":       self.ui.combo_capteur_carte.text(),
        }

    def _charger_params_fichier(self):
        """Charge params.json si existant, sinon retourne les défauts."""
        if os.path.exists("params.json"):
            try:
                with open("params.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur chargement params : {e}")
        return dict(PARAMS_DEFAUT)

    def _sauvegarder_params_fichier(self, params):
        """Sauvegarde le dict params dans params.json."""
        try:
            with open("params.json", "w", encoding="utf-8") as f:
                json.dump(params, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde params : {e}")

    def _init_historique(self):
        """Initialise les widgets de l'onglet Historique au démarrage."""
        self.ui.combo_histo_periode.clear()
        self.ui.combo_histo_periode.addItems([
            "Dernière heure",
            "Dernières 6 heures",
            "Dernières 24 heures",
            "Dernière semaine",
            "Plage personnalisée",
        ])
        self.ui.combo_histo_periode.currentIndexChanged.connect(self._on_periode_changed)

        self.ui.combo_export_format.clear()
        self.ui.combo_export_format.addItems(["CSV", "JSON"])

        self.ui.combo_histo_capteur.clear()
        self.ui.combo_histo_capteur.addItem("Tous les capteurs", userData=None)

        maintenant = datetime.now()
        self.ui.datetime_histo_debut.setDateTime(maintenant - timedelta(hours=1))
        self.ui.datetime_histo_fin.setDateTime(maintenant)

        self._on_periode_changed(0)

        self.ui.table_logs.setColumnCount(3)
        self.ui.table_logs.setHorizontalHeaderLabels(["Heure", "Valeur", "Unité"])
        self.ui.table_logs.horizontalHeader().setStretchLastSection(True)
        self.ui.table_logs.setEditTriggers(self.ui.table_logs.EditTrigger.NoEditTriggers)
        self.ui.table_logs.setSelectionBehavior(self.ui.table_logs.SelectionBehavior.SelectRows)
        self.ui.table_logs.setAlternatingRowColors(True)

    def _init_table_alarmes(self):
        """Configure les colonnes de table_alarmes_historique."""
        t = self.ui.table_alarmes_historique
        t.setColumnCount(7)
        t.setHorizontalHeaderLabels([
            "ID", "Date/Heure", "Capteur", "Type", "Message", "Sévérité", "Statut"
        ])
        t.setColumnHidden(0, True)
        t.horizontalHeader().setStretchLastSection(True)
        t.setEditTriggers(t.EditTrigger.NoEditTriggers)
        t.setSelectionBehavior(t.SelectionBehavior.SelectRows)
        t.setAlternatingRowColors(True)
        t.setSortingEnabled(True)
        
    def _on_periode_changed(self, index):
        """Active/désactive les DateTimeEdit selon la période sélectionnée."""
        personnalise = (index == 4)
        self.ui.datetime_histo_debut.setEnabled(personnalise)
        self.ui.datetime_histo_fin.setEnabled(personnalise)

    def _periode_vers_timestamps(self):
        """Retourne (debut_ts, fin_ts) en secondes Unix selon la période sélectionnée."""
        index = self.ui.combo_histo_periode.currentIndex()
        maintenant = datetime.now()

        deltas = {
            0: timedelta(hours=1),
            1: timedelta(hours=6),
            2: timedelta(hours=24),
            3: timedelta(weeks=1),
        }

        if index in deltas:
            debut = maintenant - deltas[index]
            return int(debut.timestamp()), int(maintenant.timestamp())

        debut_ts = int(self.ui.datetime_histo_debut.dateTime().toSecsSinceEpoch())
        fin_ts = int(self.ui.datetime_histo_fin.dateTime().toSecsSinceEpoch())
        return debut_ts, fin_ts

    def _ajouter_capteur_combo(self, capteur_id):
        """Ajoute un capteur dans combo_histo_capteur s'il n'y est pas déjà."""
        if capteur_id is None:
            return
        for i in range(self.ui.combo_histo_capteur.count()):
            if self.ui.combo_histo_capteur.itemData(i) == capteur_id:
                return
        self.ui.combo_histo_capteur.addItem(f"Capteur {capteur_id}", userData=capteur_id)
        self._sauvegarder_capteurs_connus()

    def _sauvegarder_capteurs_connus(self):
        """Sauvegarde les capteurs connus dans params.json."""
        capteurs = []
        for i in range(1, self.ui.combo_histo_capteur.count()):  # skip "Tous les capteurs"
            capteurs.append(self.ui.combo_histo_capteur.itemData(i))
        params = self._charger_params_fichier()
        params["capteurs_connus"] = capteurs
        self._sauvegarder_params_fichier(params)

    def _charger_capteurs_connus(self):
        """Recharge les capteurs connus depuis params.json."""
        params = self._charger_params_fichier()
        for capteur_id in params.get("capteurs_connus", []):
            self._ajouter_capteur_combo(capteur_id)

    # ─────────────────────────────────────────────────────────
    # SIGNAUX
    # ─────────────────────────────────────────────────────────

    def connecter_signaux(self):
        # Accueil
        self.ui.btn_scan.clicked.connect(self.scanner_reseau)
        self.ui.btn_start.clicked.connect(self.demarrer_acquisition)
        self.ui.btn_stop.clicked.connect(self.arreter_acquisition)
        self.ui.btn_wake.clicked.connect(self.reveiller_capteur)
        self.ui.btn_network_settings.clicked.connect(self.ouvrir_params_reseau)
        self.ui.list_cartes.itemClicked.connect(self.afficher_ip_carte)
        self.ui.btn_export.clicked.connect(self.exporter_logs)

        # Maintenance
        self.ui.btn_send_cmd.clicked.connect(self.envoyer_commande)
        self.ui.btn_clear_terminal.clicked.connect(self.effacer_terminal)
        self.ui.btn_cmd_wake.clicked.connect(lambda: self.commande_rapide("WAKE"))
        self.ui.btn_cmd_start.clicked.connect(lambda: self.commande_rapide("START"))
        self.ui.btn_cmd_stop.clicked.connect(lambda: self.commande_rapide("STOP"))
        self.ui.btn_cmd_status.clicked.connect(lambda: self.commande_rapide("STATUS"))
        self.ui.btn_cmd_reset.clicked.connect(lambda: self.commande_rapide("RESET"))
        self.ui.btn_cmd_config.clicked.connect(lambda: self.commande_rapide("CONFIG"))
        self.ui.combo_params_mode.currentTextChanged.connect(self._on_mode_changed)

        # Alarmes
        self.ui.btn_acquit.clicked.connect(self.acquitter_selection)
        self.ui.btn_acquit_all.clicked.connect(self.acquitter_tout)
        self.ui.btn_export_alarmes.clicked.connect(self.exporter_alarmes)

        # Historique
        self.ui.btn_histo_load.clicked.connect(self.charger_historique)
        self.ui.btn_export_histo.clicked.connect(self.exporter_historique)

        # Paramètres
        self.ui.btn_params_appliquer.clicked.connect(self.appliquer_parametres)
        self.ui.btn_params_reset.clicked.connect(self.reinitialiser_parametres)
        self.ui.btn_params_reset_all.clicked.connect(self.reinitialiser_tout)

    # ─────────────────────────────────────────────────────────
    # RÉCEPTION TRAMES / ACK
    # ─────────────────────────────────────────────────────────

    def traiter_trame(self, trame, ip):
        self._ajouter_carte(ip)
        self._paquets_recus += 1
        
        #Paquets binaires MIC
        if isinstance(trame, (bytes, bytearray)):
            data = parser_trame_binaire(trame)
            if data is None:
                return
            self._traiter_mic(data, ip)
            return

        #Trame texte 
        # Afficher dans le terminal seulement si ce n'est PAS une trame MIC
        if "TYPE:MIC" not in trame:
            self.ui.text_terminal_output.append(f"← {trame}")

        data = parser_trame(trame)

        if data is None:
            self.ui.text_terminal_output.append("⚠ Trame invalide ou checksum incorrect")
            return

        val = None
        rms = None
        unit = ""
        capteur_id = data.get("ID")

        type_trame = data.get("TYPE", "")

        if type_trame in ["ADC"]:
            val = data.get("VAL", 0)
            unit = data.get("UNIT", "")
            capteur_id = data.get("ID")
            self._ajouter_capteur_table(capteur_id, type_trame, ip)

            self.ui.label_prod_val.setText(f"{val} {unit}")
            self.graph_prod.maj_signal(val)
            buffer = list(self.graph_prod.buffer_signal)
            rms = float(np.sqrt(np.mean(np.array(buffer)**2)))
            self.ui.label_prod_rms.setText(f"{rms:.3f} {unit}")
            self.ui.label_prod_min.setText(f"{min(buffer):.3f} {unit}")
            self.ui.label_prod_max.setText(f"{max(buffer):.3f} {unit}")
            rssi = data.get("RSSI")
            if rssi is not None:
                self.ui.label_rssi_val.setText(f"{rssi} dBm")

        elif type_trame == "FFT":
            data_fft = data.get("DATA", [])
            fmax = data.get("FMAX", 5000)
            self.graph_prod.maj_fft(data_fft, fmax)
            print(f"FFT reçue : {len(data_fft)} points")

        elif type_trame == "WAVE":
            data_wave = data.get("DATA", [])
            for val in data_wave:
                self.graph_prod.maj_signal(val)
            print(f"WAVE reçue : {len(data_wave)} points")


        elif type_trame == "ALRM":
            self.db.sauvegarder_alarme(
                capteur_id=data.get("ID", "inconnu"),
                type_alarme=data.get("CODE", "INCONNU"),
                message=data.get("MSG", ""),
                severite=data.get("SEV", "basse"),
            )
            self.charger_alarmes()
        
        # Vérification seuils alarmes
        params = self._charger_params_fichier()
        if val is not None and val> params["val_max"]:
            self.db.sauvegarder_alarme(capteur_id=capteur_id, type_alarme="VAL_MAX", message=f"Valeur {val} dépasse le max ({params['val_max']})", severite="haute")
            self.charger_alarmes()
        elif val is not None and val < params["val_min"]:
            self.db.sauvegarder_alarme(capteur_id=capteur_id, type_alarme="VAL_MIN", message=f"Valeur {val} sous le min ({params['val_min']})", severite="haute")
            self.charger_alarmes()
        if rms is not None and rms > params["rms_max"]:
            self.db.sauvegarder_alarme(capteur_id=capteur_id, type_alarme="RMS_MAX", message=f"RMS {rms:.3f} dépasse le max ({params['rms_max']})", severite="moyenne")
            self.charger_alarmes()

        if val is not None :
            self.db.sauvegarder_mesure(
                capteur_id=capteur_id,
                type_trame=type_trame,
                valeur=val,
                unite=unit,
                timestamp=data.get("TS", 0)
            )
            self._ajouter_capteur_combo(capteur_id)

    def _traiter_mic(self, data, ip):
        data_mic = data.get("DATA", [])
        if not data_mic:
            return

        self._compteur_mic += 1
        self.ui.tabWidget.setTabEnabled(1, True)
        self.ui.frame_wake_banner.setVisible(False)

        self.graph_prod.maj_signal_buffer(data_mic)
        self.graph_histo.maj_signal_buffer(data_mic)

        arr = np.array(data_mic)
        rms = float(np.sqrt(np.mean(arr**2)))
        val_max = float(np.max(np.abs(arr)))

        # RAW
        self.ui.label_prod_raw.setText(f"{int(val_max)} raw")

        # Latence
        now = datetime.now()
        if self._last_mic_time is not None:
            latence = (now - self._last_mic_time).total_seconds() * 1000
            self.ui.label_prod_latence.setText(f"Latence : {latence:.1f} ms")
            self.ui.label_latence_val.setText(f"{latence:.1f} ms")
        self._last_mic_time = now
        
        val_min = float(np.min(arr))
        val_max_arr = float(np.max(arr))

        if val_min < self._min_global:
            self._min_global = val_min
        if val_max_arr > self._max_global:
            self._max_global = val_max_arr

        self.ui.label_prod_min.setText(f"{self._min_global:.1f}")
        self.ui.label_prod_max.setText(f"{self._max_global:.1f}")

        self.ui.label_prod_rms.setText(f"{rms:.1f}")
        self.ui.label_prod_val.setText(f"{val_max:.1f}")

        if val_max > 0:
            db_spl = 20 * np.log10(val_max / 32768.0)
            self.ui.label_prod_db.setText(f"{db_spl:.1f} dB SPL")

        # FFT
        fft_data = np.abs(np.fft.rfft(arr))
        if np.max(fft_data) > 0:
            fft_data = fft_data / np.max(fft_data)
        self.graph_prod.maj_fft(fft_data.tolist(), 5000)
        self.graph_histo.maj_fft(fft_data.tolist(), 5000)

        # RSSI
        rssi = data.get("RSSI")
        if rssi is not None:
            self.ui.label_prod_rssi.setText(f"RSSI : {rssi} dBm")
            self.ui.label_rssi_val.setText(f"{rssi} dBm")

        self.db.sauvegarder_mesure(
            capteur_id="01",
            type_trame="MIC",
            valeur=float(rms),
            unite="raw",
            timestamp=int(datetime.now().timestamp())
        )
        self._ajouter_capteur_combo("01")


    def traiter_ack(self, ack, ip):
        """Traite un ACK reçu de la carte."""
        self.ui.text_terminal_output.append(f"✓ {ack}")
        self._ajouter_carte(ip)
        data = parser_ack(ack)
        if data is None:
            return

        statut = data.get("STATUS", "--")
        seq = data.get("SEQ", "--")

        self.ui.label_ack_status.setText(f"Statut : {statut}")
        self.ui.label_ack_seq.setText(f"SEQ : {seq}")

        if seq in self._timestamps_envoi:
            latence = (datetime.now() - self._timestamps_envoi.pop(seq)).total_seconds() * 1000
            self.ui.label_ack_latence.setText(f"Latence : {latence:.1f} ms")
            self.ui.label_latence_val.setText(f"{latence:.1f} ms")
            self.ui.label_prod_latence.setText(f"Latence : {latence:.1f} ms")

        if "WAKE" in ack and statut == "OK":
            self.ui.tabWidget.setTabEnabled(1, True)
            self.ui.frame_wake_banner.setVisible(False)
            print("Capteur réveillé → Production débloquée !")

        elif "SCAN" in ack and statut == "OK":
            carte_id = data.get("ID", "--")
            ip_carte = data.get("IP", "--")
            type_capteur = data.get("TYPE", "--")
            entree = f"[ID:{carte_id}]  {ip_carte}  —  {type_capteur}"
            self._ajouter_capteur_table(carte_id, type_capteur, ip_carte)
            existants = [
                self.ui.list_cartes.item(i).text()
                for i in range(self.ui.list_cartes.count())
            ]
            if entree not in existants:
                self.ui.list_cartes.addItem(entree)
                self._ajouter_capteur_combo(carte_id)
                print(f"Carte détectée : {entree}")

    def _ajouter_carte(self, ip):
        if not hasattr(self, 'cartes_connues'):
            self.cartes_connues = set()
        if ip not in self.cartes_connues:
            self.cartes_connues.add(ip)
            self.ui.list_cartes.addItem(f"Carte — IP: {ip}")
            self.ip_carte_selectionnee = ip  # ← sélection automatique
            self.ui.label_carte_cible_val.setText(f"Carte cible : {ip}")
            self.statusBar().showMessage(f"Carte sélectionnée : {ip}")
            self.setWindowTitle(f"IHM Wi-Fi — Microcontrôleur — {ip}")
            print(f"Nouvelle carte détectée : {ip}")

    def _ajouter_capteur_table(self, capteur_id, type_capteur, ip_carte, etat="Connecté"):
        """Ajoute ou met à jour un capteur dans table_capteurs."""
        t = self.ui.table_capteurs
        # Vérifier si déjà présent
        for row in range(t.rowCount()):
            if t.item(row, 0) and t.item(row, 0).text() == str(capteur_id):
                t.item(row, 3).setText(etat)
                return
        # Ajouter nouvelle ligne
        row = t.rowCount()
        t.insertRow(row)
        t.setItem(row, 0, QTableWidgetItem(str(capteur_id)))
        t.setItem(row, 1, QTableWidgetItem(str(type_capteur)))
        t.setItem(row, 2, QTableWidgetItem(str(ip_carte)))
        t.setItem(row, 3, QTableWidgetItem(etat))
        t.setItem(row, 4, QTableWidgetItem(""))
        t.resizeColumnsToContents()

    def afficher_ip_carte(self, item):
        self.ip_carte_selectionnee = item.text().replace("Carte — IP: ", "")
        self.ui.label_carte_cible_val.setText(f"Carte cible : {self.ip_carte_selectionnee}")
        self.statusBar().showMessage(f"Carte sélectionnée : {self.ip_carte_selectionnee}")

    # ─────────────────────────────────────────────────────────
    # ALARMES — PIPELINE PRINCIPAL
    # ─────────────────────────────────────────────────────────

    def charger_alarmes(self):
        """Charge toutes les alarmes depuis la DB et remplit table_alarmes_historique."""
        alarmes = self.db.charger_alarmes()
        t = self.ui.table_alarmes_historique

        t.setSortingEnabled(False)
        t.setRowCount(0)

        for alarme in alarmes:
            alarme_id, date_heure, capteur_id, type_a, message, severite, statut = alarme

            row = t.rowCount()
            t.insertRow(row)

            item_id = QTableWidgetItem(str(alarme_id))
            item_id.setData(Qt.ItemDataRole.UserRole, alarme_id)
            t.setItem(row, 0, item_id)

            t.setItem(row, 1, QTableWidgetItem(str(date_heure or "")))
            t.setItem(row, 2, QTableWidgetItem(str(capteur_id or "")))
            t.setItem(row, 3, QTableWidgetItem(str(type_a or "")))
            t.setItem(row, 4, QTableWidgetItem(str(message or "")))
            t.setItem(row, 5, QTableWidgetItem(str(severite or "")))
            t.setItem(row, 6, QTableWidgetItem(str(statut or "")))

            # Ajouter capteur dans le filtre si pas déjà présent
            if capteur_id:
                existants = [self.ui.combo_filtre_capteur.itemText(i) 
                            for i in range(self.ui.combo_filtre_capteur.count())]
                if str(capteur_id) not in existants:
                    self.ui.combo_filtre_capteur.addItem(str(capteur_id))

            if statut == "acquittee":
                couleur = QColor("#2A2A2A")
            else:
                couleur = _COULEUR_SEVERITE.get(str(severite).lower())

            if couleur:
                for col in range(t.columnCount()):
                    item = t.item(row, col)
                    if item:
                        item.setBackground(couleur)
        nb_actives = sum(
            1 for row in range(t.rowCount())
            if t.item(row, 6) and t.item(row, 6).text() != "acquittee"
        )
        self.ui.label_alarmes_count.setText(str(nb_actives))
        t.setSortingEnabled(True)
        t.resizeColumnsToContents()
        t.horizontalHeader().setStretchLastSection(True)
        print(f"Alarmes chargées : {t.rowCount()} ligne(s)")

    def filtrer_alarmes(self):
        """Filtre table_alarmes_historique selon sévérité et capteur."""
        severite = self.ui.combo_filtre_severite.currentText()
        capteur = self.ui.combo_filtre_capteur.currentText()

        t = self.ui.table_alarmes_historique
        for row in range(t.rowCount()):
            item_sev = t.item(row, 5)
            item_cap = t.item(row, 2)

            sev_ok = (severite == "Toutes") or (item_sev and item_sev.text() == severite)
            cap_ok = (capteur == "Tous les capteurs") or (item_cap and item_cap.text() == capteur)

            t.setRowHidden(row, not (sev_ok and cap_ok))

    # ─────────────────────────────────────────────────────────
    # ALARMES — ACQUITTEMENT
    # ─────────────────────────────────────────────────────────

    def acquitter_selection(self):
        """Acquitte l'alarme sélectionnée dans la table."""
        t = self.ui.table_alarmes_historique
        row = t.currentRow()

        if row < 0:
            QMessageBox.information(self, "Acquittement", "Sélectionnez une alarme dans la liste.")
            return

        item_id = t.item(row, 0)
        if item_id is None:
            print("ID alarme introuvable en colonne 0")
            return

        alarme_id = item_id.data(Qt.ItemDataRole.UserRole)
        self.db.acquitter_alarme(alarme_id)

        for col in range(t.columnCount()):
            item = t.item(row, col)
            if item:
                item.setBackground(QColor("#2A2A2A"))
        item_statut = t.item(row, 6)
        if item_statut:
            item_statut.setText("acquittee")

        print(f"Alarme ID={alarme_id} acquittée")

    def acquitter_tout(self):
        """Acquitte toutes les alarmes actives."""
        t = self.ui.table_alarmes_historique

        if t.rowCount() == 0:
            QMessageBox.information(self, "Acquittement", "Aucune alarme dans la liste.")
            return

        self.db.acquitter_toutes()

        for row in range(t.rowCount()):
            for col in range(t.columnCount()):
                item = t.item(row, col)
                if item:
                    item.setBackground(QColor("#2A2A2A"))
            item_statut = t.item(row, 6)
            if item_statut:
                item_statut.setText("acquittee")

        print("Toutes les alarmes acquittées")

    def exporter_alarmes(self):
        """Exporte le contenu de table_alarmes_historique en CSV."""
        t = self.ui.table_alarmes_historique
        nb_lignes = t.rowCount()

        if nb_lignes == 0:
            QMessageBox.warning(self, "Export", "Aucune alarme à exporter.")
            return

        nom_defaut = f"alarmes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        chemin, _ = QFileDialog.getSaveFileName(self, "Exporter les alarmes", nom_defaut, "CSV (*.csv)")
        if not chemin:
            return

        try:
            with open(chemin, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Date/Heure", "Capteur", "Type", "Message", "Sévérité", "Statut"])
                for row in range(nb_lignes):
                    ligne = [
                        t.item(row, col).text() if t.item(row, col) else ""
                        for col in range(1, 7)
                    ]
                    writer.writerow(ligne)
            QMessageBox.information(self, "Export réussi", f"{nb_lignes} alarmes exportées vers :\n{chemin}")
            print(f"Export alarmes : {chemin}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur export", f"Échec :\n{e}")
            print(f"Erreur export alarmes : {e}")

    # ─────────────────────────────────────────────────────────
    # HISTORIQUE — CHARGEMENT
    # ─────────────────────────────────────────────────────────

    def charger_historique(self):
        """Charge les mesures depuis SQLite et met à jour l'onglet Historique."""
        capteur_id = self.ui.combo_histo_capteur.currentData()
        debut_ts, fin_ts = self._periode_vers_timestamps()

        mesures = self.db.charger_mesures(
            capteur_id=capteur_id,
            debut=debut_ts,
            fin=fin_ts
        )

        if not mesures:
            self.ui.table_logs.setRowCount(0)
            self._reinitialiser_stats()
            self.graph_histo.reset()
            return

        self.ui.table_logs.setRowCount(len(mesures))
        for row, (date_heure, valeur, unite) in enumerate(mesures):
            self.ui.table_logs.setItem(row, 0, QTableWidgetItem(str(date_heure)))
            item_val = QTableWidgetItem(f"{valeur:.4f}" if valeur is not None else "--")
            item_val.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.ui.table_logs.setItem(row, 1, item_val)
            self.ui.table_logs.setItem(row, 2, QTableWidgetItem(str(unite) if unite else ""))
        self.ui.table_logs.resizeColumnsToContents()

        valeurs = [v for _, v, _ in mesures if v is not None]
        if valeurs:
            arr = np.array(valeurs)
            unite_affichee = mesures[0][2] or ""
            self.ui.label_stats_moyenne_val.setText(f"{arr.mean():.4f} {unite_affichee}")
            self.ui.label_stats_rms_val.setText(f"{float(np.sqrt(np.mean(arr**2))):.4f} {unite_affichee}")
            self.ui.label_stats_min_val.setText(f"{arr.min():.4f} {unite_affichee}")
            self.ui.label_stats_max_val.setText(f"{arr.max():.4f} {unite_affichee}")
        else:
            self._reinitialiser_stats()

        self.graph_histo.reset()
        for _, val, _ in mesures:
            if val is not None:
                self.graph_histo.maj_signal(val)

        print(f"Historique chargé : {len(mesures)} mesures")

    def _reinitialiser_stats(self):
        """Remet les labels de statistiques à --."""
        for label in [
            self.ui.label_stats_moyenne_val,
            self.ui.label_stats_rms_val,
            self.ui.label_stats_min_val,
            self.ui.label_stats_max_val,
        ]:
            label.setText("--")

    # ─────────────────────────────────────────────────────────
    # HISTORIQUE — EXPORT
    # ─────────────────────────────────────────────────────────

    def exporter_historique(self):
        """Exporte les données affichées dans table_logs selon le format choisi."""
        nb_lignes = self.ui.table_logs.rowCount()
        if nb_lignes == 0:
            QMessageBox.warning(self, "Export", "Aucune donnée à exporter. Chargez d'abord l'historique.")
            return

        format_choisi = self.ui.combo_export_format.currentText()
        extensions = {"CSV": "*.csv", "JSON": "*.json"}
        filtre = f"{format_choisi} ({extensions[format_choisi]})"
        nom_defaut = f"historique_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_choisi.lower()}"
        chemin, _ = QFileDialog.getSaveFileName(self, "Exporter les données", nom_defaut, filtre)

        if not chemin:
            return

        donnees = []
        for row in range(nb_lignes):
            donnees.append({
                "date_heure": self.ui.table_logs.item(row, 0).text(),
                "valeur": self.ui.table_logs.item(row, 1).text(),
                "unite": self.ui.table_logs.item(row, 2).text(),
            })

        try:
            if format_choisi == "CSV":
                self._exporter_csv(chemin, donnees)
            elif format_choisi == "JSON":
                self._exporter_json(chemin, donnees)
            QMessageBox.information(self, "Export réussi", f"{nb_lignes} lignes exportées vers :\n{chemin}")
            print(f"Export {format_choisi} : {chemin}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur export", f"Échec de l'export :\n{e}")
            print(f"Erreur export : {e}")

    def exporter_logs(self):
        """Exporte les logs bruts depuis la DB en CSV."""
        nom_defaut = f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        chemin, _ = QFileDialog.getSaveFileName(self, "Exporter logs", nom_defaut, "CSV (*.csv)")
        if not chemin:
            return
        try:
            mesures = self.db.charger_mesures()
            if not mesures:
                QMessageBox.warning(self, "Export", "Aucun log à exporter.")
                return
            with open(chemin, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Date/Heure", "Valeur", "Unité"])
                writer.writerows(mesures)
            QMessageBox.information(self, "Export réussi", f"{len(mesures)} lignes exportées vers :\n{chemin}")
            print(f"Export logs : {chemin}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur export", f"Échec :\n{e}")
            print(f"Erreur export logs : {e}")

    def _exporter_csv(self, chemin, donnees):
        with open(chemin, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["date_heure", "valeur", "unite"])
            writer.writeheader()
            writer.writerows(donnees)

    def _exporter_json(self, chemin, donnees):
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)

    # ─────────────────────────────────────────────────────────
    # COMMANDES
    # ─────────────────────────────────────────────────────────

    def scanner_reseau(self):
        """Envoie un broadcast SCAN et vide la liste en attente des réponses."""
        self.ui.list_cartes.clear()
        seq = self._next_seq()
        trame = f"CMD:SCAN;SEQ:{seq}"
        trame_complete = f"{trame};CHK:{self._checksum(trame)}"
        self.udp.envoyer_broadcast(trame_complete)
        self.ui.text_terminal_output.append(f"> {trame_complete}")
        print(f"Scan réseau lancé (SEQ:{seq})")

    def _get_ip_carte_selectionnee(self):
        """Retourne l'IP de la carte sélectionnée dans list_cartes, ou None."""
        item = self.ui.list_cartes.currentItem()
        if item is None:
            QMessageBox.warning(self, "Aucune carte", "Sélectionnez une carte dans la liste.")
            return None
        try:
            return item.text().replace("Carte — IP: ", "").strip()
        except IndexError:
            QMessageBox.warning(self, "Erreur", "Impossible de lire l'IP de la carte.")
            return None

    def demarrer_acquisition(self):
        """Envoie la commande START à la carte."""
        ip_carte = self._get_ip_carte_selectionnee()
        if ip_carte is None:
            return
        seq = self._next_seq()
        trame = f"CMD:START;SEQ:{seq}"
        trame_complete = f"{trame};CHK:{self._checksum(trame)}"
        self.udp.envoyer(trame_complete, ip_carte)
        self.ui.text_terminal_output.append(f"> {trame_complete}")
        self.db.sauvegarder_commande(
            commande=trame_complete,
            capteur_id=ip_carte,
            statut_ack="en_attente"
        )
        print(f"Commande START envoyée → {ip_carte}")

    def arreter_acquisition(self):
        """Envoie la commande STOP à la carte."""
        ip_carte = self._get_ip_carte_selectionnee()
        if ip_carte is None:
            return
        seq = self._next_seq()
        trame = f"CMD:STOP;SEQ:{seq}"
        trame_complete = f"{trame};CHK:{self._checksum(trame)}"
        self.udp.envoyer(trame_complete, ip_carte)
        self.ui.text_terminal_output.append(f"> {trame_complete}")
        self.db.sauvegarder_commande(
            commande=trame_complete,
            capteur_id=ip_carte,
            statut_ack="en_attente"
        )
        print(f"Commande STOP envoyée → {ip_carte}")

    def reveiller_capteur(self):
        """Envoie la commande WAKE à la carte."""
        ip_carte = self._get_ip_carte_selectionnee()
        if ip_carte is None:
            return
        seq = self._next_seq()
        trame = f"CMD:WAKE;SEQ:{seq}"
        trame_complete = f"{trame};CHK:{self._checksum(trame)}"
        self.udp.envoyer(trame_complete, ip_carte)
        self.ui.text_terminal_output.append(f"> {trame_complete}")
        self.db.sauvegarder_commande(
            commande=trame_complete,
            capteur_id=ip_carte,
            statut_ack="en_attente"
        )
        print(f"Commande WAKE envoyée → {ip_carte}")

    def _next_seq(self):
        """Retourne le prochain numéro de séquence sur 3 chiffres et l'incrémente."""
        self._seq = (self._seq + 1) % 1000
        return f"{self._seq:03d}"

    def _checksum(self, trame):
        """Calcule le checksum XOR."""
        resultat = 0
        for char in trame:
            resultat ^= ord(char)
        return format(resultat, '02X')

    def ouvrir_params_reseau(self):
        self.dialog = QDialog()
        self.dialog_ui = Ui_DialogParamsReseau()
        self.dialog_ui.setupUi(self.dialog)
        self.dialog_ui.spinbox_port_local.setMaximum(65535)
        self.dialog_ui.spinbox_port_dest.setMaximum(65535)

        # Pré-remplir avec les valeurs actuelles
        self.dialog_ui.spinbox_port_local.setValue(self.udp.port_local)
        self.dialog_ui.spinbox_port_dest.setValue(self.udp.port_dest)
        self.dialog_ui.lineEdit.setText(self.udp.broadcast)

        # Charger params_reseau.json si existant
        if os.path.exists("params_reseau.json"):
            try:
                with open("params_reseau.json", "r", encoding="utf-8") as f:
                    pr = json.load(f)
                self.dialog_ui.combo_timeout_ack.addItems(["500 ms", "1 s", "2 s", "5 s"])
                self.dialog_ui.combo_retries.addItems(["1", "2", "3", "5", "10"])
                self.dialog_ui.combo_timeout_liaison.addItems(["5 s", "10 s", "30 s", "60 s"])
                self.dialog_ui.combo_timeout_ack.setCurrentText(pr.get("timeout_ack", "500 ms"))
                self.dialog_ui.combo_retries.setCurrentText(pr.get("retries", "1"))
                self.dialog_ui.combo_timeout_liaison.setCurrentText(pr.get("timeout_liaison", "5 s"))
                self.dialog_ui.spinbox_rssi_min.setValue(pr.get("rssi_min", -80.0))
                self.dialog_ui.spinbox_per_max.setValue(pr.get("per_max", 5.0))
                self.dialog_ui.spinbox_latence_max.setValue(pr.get("latence_max", 100.0))
            except Exception as e:
                print(f"Erreur chargement params_reseau.json : {e}")
                self.dialog_ui.combo_timeout_ack.addItems(["500 ms", "1 s", "2 s", "5 s"])
                self.dialog_ui.combo_retries.addItems(["1", "2", "3", "5", "10"])
                self.dialog_ui.combo_timeout_liaison.addItems(["5 s", "10 s", "30 s", "60 s"])
                self.dialog_ui.spinbox_rssi_min.setValue(-80.0)
                self.dialog_ui.spinbox_per_max.setValue(5.0)
                self.dialog_ui.spinbox_latence_max.setValue(100.0)
        else:
            self.dialog_ui.combo_timeout_ack.addItems(["500 ms", "1 s", "2 s", "5 s"])
            self.dialog_ui.combo_retries.addItems(["1", "2", "3", "5", "10"])
            self.dialog_ui.combo_timeout_liaison.addItems(["5 s", "10 s", "30 s", "60 s"])
            self.dialog_ui.spinbox_rssi_min.setValue(-80.0)
            self.dialog_ui.spinbox_per_max.setValue(5.0)
            self.dialog_ui.spinbox_latence_max.setValue(100.0)

        # Brancher les boutons — une seule fois
        self.dialog_ui.btn_cancel.clicked.connect(self.dialog.reject)
        self.dialog_ui.btn_apply_reseau.clicked.connect(
            lambda: self._appliquer_params_reseau(self.dialog)
        )
        self.dialog_ui.btn_reset_reseau.clicked.connect(lambda: (
            self.dialog_ui.spinbox_port_local.setValue(5001),
            self.dialog_ui.spinbox_port_dest.setValue(5002),
            self.dialog_ui.lineEdit.setText("192.168.10.255"),
            self.dialog_ui.combo_timeout_ack.setCurrentIndex(0),
            self.dialog_ui.combo_retries.setCurrentIndex(0),
            self.dialog_ui.combo_timeout_liaison.setCurrentIndex(0),
            self.dialog_ui.spinbox_rssi_min.setValue(-80.0),
            self.dialog_ui.spinbox_per_max.setValue(5.0),
            self.dialog_ui.spinbox_latence_max.setValue(100.0),
        ))

        self.dialog.exec()

    def _appliquer_params_reseau(self, dialog):
        nouveau_port_local = self.dialog_ui.spinbox_port_local.value()
        nouveau_port_dest  = self.dialog_ui.spinbox_port_dest.value()
        broadcast          = self.dialog_ui.lineEdit.text()

        params_reseau = {
            "port_local":       nouveau_port_local,
            "port_dest":        nouveau_port_dest,
            "broadcast":        broadcast,
            "timeout_ack":      self.dialog_ui.combo_timeout_ack.currentText(),
            "retries":          self.dialog_ui.combo_retries.currentText(),
            "timeout_liaison":  self.dialog_ui.combo_timeout_liaison.currentText(),
            "rssi_min":         self.dialog_ui.spinbox_rssi_min.value(),
            "per_max":          self.dialog_ui.spinbox_per_max.value(),
            "latence_max":      self.dialog_ui.spinbox_latence_max.value(),
        }
        with open("params_reseau.json", "w", encoding="utf-8") as f:
            json.dump(params_reseau, f, ensure_ascii=False, indent=2)

        mode_actuel = self.udp.mode
        ip_actuelle = self.udp.ip_distante
        self.udp.arreter()
        if mode_actuel == "distant":
            self.udp = RemoteWorker(ip_serveur=ip_actuelle)
        else:
            self.udp = UDPWorker(
                port_local  = nouveau_port_local,
                port_dest   = nouveau_port_dest,
                broadcast   = broadcast,
                mode        = mode_actuel,
                ip_distante = ip_actuelle,
            )
        self.udp.trame_recue.connect(self.traiter_trame)
        self.udp.ack_recu.connect(self.traiter_ack)
        self.udp.demarrer()


        dialog.accept()
        QMessageBox.information(self, "Réseau",
            f"UDP mis à jour → local:{nouveau_port_local} dest:{nouveau_port_dest}")
        print(f"Paramètres réseau sauvegardés : {params_reseau}")

    def envoyer_commande(self):
        cmd = self.ui.input_cmd.text()
        if cmd:
            if self.ip_carte_selectionnee is None:
                self.ui.text_terminal_output.append("⚠ Aucune carte sélectionnée !")
                return
            self.ui.text_terminal_output.append(f"> {cmd}")
            self.udp.envoyer(cmd, self.ip_carte_selectionnee)
            self.db.sauvegarder_commande(
                commande=cmd,
                capteur_id=None,
                statut_ack="manuel"
            )
            self.ui.input_cmd.clear()
            self._ajouter_historique_commande(cmd)
            print(f"Commande envoyée : {cmd}")
    
    def envoyer_config(self):
        """Lit les paramètres UI et envoie CMD:CONFIG à la carte."""
        params = self._lire_params_ui()
        
        udp_map = {"1 Hz": 1000, "5 Hz": 200, "10 Hz": 100, "50 Hz": 20, "100 Hz": 10}
        rate_ms = udp_map.get(params["udp"], 100)
        bins = int(params["fft"])
        
        seq = self._next_seq()
        trame = f"CMD:CONFIG;RATE:{rate_ms};BINS:{bins};SEQ:{seq}"
        trame_complete = f"{trame};CHK:{self._checksum(trame)}"
        
        self.ui.text_terminal_output.append(f"> {trame_complete}")
        if self.ip_carte_selectionnee:
            self.udp.envoyer(trame_complete, self.ip_carte_selectionnee)
        self._ajouter_historique_commande(trame_complete)
        print(f"Config envoyée : RATE={rate_ms}ms BINS={bins}")

    def effacer_terminal(self):
        self.ui.text_terminal_output.clear()
        
    def _ajouter_historique_commande(self, cmd):
        horodatage = datetime.now().strftime("%H:%M:%S")
        self.ui.list_cmd_history.addItem(f"[{horodatage}] {cmd}")
        self.ui.list_cmd_history.scrollToBottom()

    def _maj_metriques(self):
        """Met à jour les métriques réseau toutes les secondes."""
        self.ui.label_debit_val.setText(f"{self._paquets_recus} pkt/s")
        if self._paquets_envoyes > 0:
            per = ((self._paquets_envoyes - self._paquets_recus) / self._paquets_envoyes) * 100
            per = max(0, per)
            self.ui.label_per_val.setText(f"{per:.1f} %")
            self.ui.label_prod_per.setText(f"PER : {per:.1f} %")
        self.ui.label_paquets_val.setText(f"{self._paquets_recus} / {self._paquets_envoyes}")
        self._paquets_recus = 0

    def _rafraichir_graphes(self):
        self.graph_prod.rafraichir()
        self.graph_histo.rafraichir()

    def commande_rapide(self, type_cmd):
        if type_cmd == "CONFIG":
            self.envoyer_config()
            return
        
        seq = self._next_seq()
        self._timestamps_envoi[seq] = datetime.now()
        trame = f"CMD:{type_cmd};SEQ:{seq}"
        trame_complete = f"{trame};CHK:{self._checksum(trame)}"
        self.ui.text_terminal_output.append(f"> {trame_complete}")
        if self.ip_carte_selectionnee:
            self.udp.envoyer(trame_complete, self.ip_carte_selectionnee)
        self._paquets_envoyes += 1
        self.db.sauvegarder_commande(
            commande=trame_complete,
            capteur_id=None,
            statut_ack="en_attente"
        )
        self._ajouter_historique_commande(trame_complete)
        print(f"Commande rapide : {trame_complete}")

    # ─────────────────────────────────────────────────────────
    # PARAMÈTRES
    # ─────────────────────────────────────────────────────────

    def appliquer_parametres(self):
        params = self._lire_params_ui()
        self._sauvegarder_params_fichier(params)
        QMessageBox.information(self, "Paramètres", "Paramètres enregistrés.")
        print(f"Paramètres appliqués : {params}")

    def _on_mode_changed(self, mode):
        if not self.ip_carte_selectionnee:
            return
        if mode == "Mode éco":
            self.commande_rapide("ECO")
        elif mode == "Continu":
            self.commande_rapide("WAKE")

    def reinitialiser_parametres(self):
        self._appliquer_params_ui(dict(PARAMS_DEFAUT))
        print("Paramètres réinitialisés aux valeurs par défaut")

    def reinitialiser_tout(self):
        self._appliquer_params_ui(dict(PARAMS_DEFAUT))
        self._sauvegarder_params_fichier(dict(PARAMS_DEFAUT))
        self.ui.table_alarmes_historique.setRowCount(0)
        self.ui.table_logs.setRowCount(0)
        self.ui.list_cartes.clear()
        self.ui.text_terminal_output.clear()
        QMessageBox.information(self, "Réinitialisation", "Tout a été réinitialisé.")
        print("Réinitialisation complète effectuée")

    # ─────────────────────────────────────────────────────────
    # FERMETURE
    # ─────────────────────────────────────────────────────────

    def closeEvent(self, event):
        self.udp.arreter()
        self.db.fermer()
        event.accept()
