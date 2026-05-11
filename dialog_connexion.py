# -*- coding: utf-8 -*-
"""
Dialog de connexion au démarrage.
Utilise Ui_DialogConnexion depuis ui_dialogconnexion.py
"""

import json
import os
import re
from PySide6.QtWidgets import QDialog, QMessageBox
from ui_dialogconnexion import Ui_DialogConnexion

PARAMS_CONNEXION_FILE = "params_connexion.json"


def _valider_ip(ip: str) -> bool:
    """Valide une IPv4 ou un hostname."""
    ip = ip.strip()
    if not ip:
        return False
    patron_ipv4 = r"^(\d{1,3}\.){3}\d{1,3}$"
    if re.match(patron_ipv4, ip):
        return all(0 <= int(p) <= 255 for p in ip.split("."))
    return bool(re.match(r"^[a-zA-Z0-9.\-]+$", ip))


class DialogConnexion(QDialog):
    """
    Dialog affichée au lancement.
    Expose .mode ("local" ou "distant") et .ip_distante après accept().
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DialogConnexion()
        self.ui.setupUi(self)

        # Résultats exposés
        self.mode        = "local"
        self.ip_distante = ""

        # Connexion des signaux
        self.ui.radio_local.toggled.connect(self._on_mode_change)
        self.ui.radio_distant.toggled.connect(self._on_mode_change)
        self.ui.btn_quitter.clicked.connect(self.reject)
        self.ui.btn_connecter.clicked.connect(self._valider)

        # Pré-remplir avec le dernier choix
        self._charger_derniere_config()

    # ─────────────────────────────────────────────────────────
    # Slots
    # ─────────────────────────────────────────────────────────

    def _on_mode_change(self):
        distant = self.ui.radio_distant.isChecked()
        self.ui.frame_distant.setEnabled(distant)
        if distant:
            self.ui.input_ip.setFocus()

    def _valider(self):
        if self.ui.radio_distant.isChecked():
            ip = self.ui.input_ip.text().strip()
            if not _valider_ip(ip):
                QMessageBox.warning(
                    self,
                    "Adresse invalide",
                    "Veuillez entrer une adresse IP valide (ex : 82.45.123.67)\n"
                    "ou un nom de domaine (ex : mondomaine.fr)."
                )
                self.ui.input_ip.setFocus()
                return
            self.mode        = "distant"
            self.ip_distante = ip
        else:
            self.mode        = "local"
            self.ip_distante = ""

        self._sauvegarder_config()
        self.accept()

    # ─────────────────────────────────────────────────────────
    # Persistance
    # ─────────────────────────────────────────────────────────

    def _sauvegarder_config(self):
        try:
            with open(PARAMS_CONNEXION_FILE, "w", encoding="utf-8") as f:
                json.dump({"mode": self.mode, "ip_distante": self.ip_distante}, f, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde config connexion : {e}")

    def _charger_derniere_config(self):
        if not os.path.exists(PARAMS_CONNEXION_FILE):
            return
        try:
            with open(PARAMS_CONNEXION_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
            if config.get("mode") == "distant":
                self.ui.radio_distant.setChecked(True)
                self.ui.input_ip.setText(config.get("ip_distante", ""))
            else:
                self.ui.radio_local.setChecked(True)
        except Exception as e:
            print(f"Erreur chargement config connexion : {e}")
