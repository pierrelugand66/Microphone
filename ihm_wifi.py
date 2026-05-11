from PySide6.QtWidgets import (
    QWidget, QGridLayout, QTabWidget, QFrame, QLabel, QPushButton,
    QListWidget, QTableWidget, QTableWidgetItem, QTextEdit, QLineEdit,
    QComboBox, QDoubleSpinBox, QDateTimeEdit, QAbstractItemView, QStatusBar,
    QMainWindow
)
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)

class Ui_MainWindow:

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 799)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # ── Onglet Accueil (tab_3) ────────────────────────────────────────
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")

        self.frame_wake_banner = QFrame(self.tab_3)
        self.frame_wake_banner.setObjectName("frame_wake_banner")
        self.frame_wake_banner.setGeometry(QRect(0, 0, 1260, 80))
        self.frame_wake_banner.setStyleSheet(
            "QFrame#frame_wake_banner {"
            "  background-color: #FAEEDA;"
            "  border: 1px solid #BA7517;"
            "  border-radius: 4px;"
            "}"
        )
        self.frame_wake_banner.setFrameShape(QFrame.NoFrame)

        self.label_wake_message = QLabel(self.frame_wake_banner)
        self.label_wake_message.setAlignment(Qt.AlignCenter)
        self.label_wake_message.setObjectName("label_wake_message")
        self.label_wake_message.setGeometry(QRect(220, 30, 840, 21))
        self.label_wake_message.setStyleSheet("color: #000000; font-weight: bold;")

        self.label_wake_id = QLabel(self.frame_wake_banner)
        self.label_wake_id.setObjectName("label_wake_id")
        self.label_wake_id.setGeometry(QRect(120, 30, 101, 16))
        self.label_wake_id.setStyleSheet("color: #000000; font-weight: bold;")

        self.btn_wake = QPushButton(self.frame_wake_banner)
        self.btn_wake.setObjectName("btn_wake")
        self.btn_wake.setGeometry(QRect(1090, 19, 151, 41))
        self.btn_wake.setStyleSheet(
            "QPushButton {"
            "  background-color: transparent;"
            "  color: #BA7517;"
            "  font-weight: bold;"
            "  border-radius: 4px;"
            "  border: 2px solid #BA7517;"
            "}"
            "QPushButton:hover { background-color: rgba(186, 117, 23, 30); }"
            "QPushButton:pressed { background-color: rgba(186, 117, 23, 60); }"
        )

        self.frame_main = QFrame(self.tab_3)
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setGeometry(QRect(-10, 80, 1260, 250))
        self.frame_main.setFrameShape(QFrame.NoFrame)

        self.frame_system_status = QFrame(self.frame_main)
        self.frame_system_status.setObjectName("frame_system_status")
        self.frame_system_status.setGeometry(QRect(0, 0, 620, 250))
        self.frame_system_status.setFrameShape(QFrame.NoFrame)

        self.label_system_title = QLabel(self.frame_system_status)
        self.label_system_title.setObjectName("label_system_title")
        self.label_system_title.setGeometry(QRect(50, 20, 91, 16))

        self.list_cartes = QListWidget(self.frame_system_status)
        self.list_cartes.setObjectName("list_cartes")
        self.list_cartes.setGeometry(QRect(30, 40, 461, 191))

        self.btn_scan = QPushButton(self.frame_system_status)
        self.btn_scan.setObjectName("btn_scan")
        self.btn_scan.setGeometry(QRect(500, 90, 111, 81))

        self.frame_network_summary = QFrame(self.frame_main)
        self.frame_network_summary.setObjectName("frame_network_summary")
        self.frame_network_summary.setGeometry(QRect(630, 0, 620, 250))
        self.frame_network_summary.setFrameShape(QFrame.NoFrame)

        self.label_network_title = QLabel(self.frame_network_summary)
        self.label_network_title.setObjectName("label_network_title")
        self.label_network_title.setGeometry(QRect(10, 20, 81, 16))

        self.label_latence_title = QLabel(self.frame_network_summary)
        self.label_latence_title.setObjectName("label_latence_title")
        self.label_latence_title.setGeometry(QRect(10, 60, 81, 16))

        self.label_latence_val = QLabel(self.frame_network_summary)
        self.label_latence_val.setObjectName("label_latence_val")
        self.label_latence_val.setGeometry(QRect(20, 80, 49, 16))

        self.label_rssi_title = QLabel(self.frame_network_summary)
        self.label_rssi_title.setObjectName("label_rssi_title")
        self.label_rssi_title.setGeometry(QRect(380, 60, 49, 16))

        self.label_rssi_val = QLabel(self.frame_network_summary)
        self.label_rssi_val.setObjectName("label_rssi_val")
        self.label_rssi_val.setGeometry(QRect(380, 80, 49, 16))

        self.label_per_title = QLabel(self.frame_network_summary)
        self.label_per_title.setObjectName("label_per_title")
        self.label_per_title.setGeometry(QRect(10, 120, 49, 16))

        self.label_per_val = QLabel(self.frame_network_summary)
        self.label_per_val.setObjectName("label_per_val")
        self.label_per_val.setGeometry(QRect(10, 140, 49, 16))

        self.label_debit_title = QLabel(self.frame_network_summary)
        self.label_debit_title.setObjectName("label_debit_title")
        self.label_debit_title.setGeometry(QRect(370, 120, 49, 16))

        self.label_debit_val = QLabel(self.frame_network_summary)
        self.label_debit_val.setObjectName("label_debit_val")
        self.label_debit_val.setGeometry(QRect(370, 140, 49, 16))

        self.label_canal_title = QLabel(self.frame_network_summary)
        self.label_canal_title.setObjectName("label_canal_title")
        self.label_canal_title.setGeometry(QRect(10, 180, 71, 16))

        self.label_canal_val = QLabel(self.frame_network_summary)
        self.label_canal_val.setObjectName("label_canal_val")
        self.label_canal_val.setGeometry(QRect(10, 200, 49, 16))

        self.label_paquets_title = QLabel(self.frame_network_summary)
        self.label_paquets_title.setObjectName("label_paquets_title")
        self.label_paquets_title.setGeometry(QRect(370, 180, 131, 16))

        self.label_paquets_val = QLabel(self.frame_network_summary)
        self.label_paquets_val.setObjectName("label_paquets_val")
        self.label_paquets_val.setGeometry(QRect(370, 200, 49, 16))

        self.frame_capteurs = QFrame(self.tab_3)
        self.frame_capteurs.setObjectName("frame_capteurs")
        self.frame_capteurs.setGeometry(QRect(0, 420, 1260, 200))
        self.frame_capteurs.setFrameShape(QFrame.NoFrame)

        self.label_capteurs_title = QLabel(self.frame_capteurs)
        self.label_capteurs_title.setObjectName("label_capteurs_title")
        self.label_capteurs_title.setGeometry(QRect(10, 0, 111, 16))

        self.table_capteurs = QTableWidget(self.frame_capteurs)
        self.table_capteurs.setObjectName("table_capteurs")
        self.table_capteurs.setGeometry(QRect(10, 20, 1231, 161))
        self.table_capteurs.setColumnCount(5)
        for i in range(5):
            self.table_capteurs.setHorizontalHeaderItem(i, QTableWidgetItem())
        self.table_capteurs.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_capteurs.setAlternatingRowColors(True)
        self.table_capteurs.setSelectionBehavior(QAbstractItemView.SelectItems)

        self.frame_actions = QFrame(self.tab_3)
        self.frame_actions.setObjectName("frame_actions")
        self.frame_actions.setGeometry(QRect(0, 630, 1260, 60))
        self.frame_actions.setFrameShape(QFrame.NoFrame)

        self.btn_start = QPushButton(self.frame_actions)
        self.btn_start.setObjectName("btn_start")
        self.btn_start.setGeometry(QRect(20, 14, 150, 32))

        self.btn_stop = QPushButton(self.frame_actions)
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setGeometry(QRect(320, 14, 75, 32))

        self.btn_export = QPushButton(self.frame_actions)
        self.btn_export.setObjectName("btn_export")
        self.btn_export.setGeometry(QRect(700, 14, 130, 32))

        self.btn_network_settings = QPushButton(self.frame_actions)
        self.btn_network_settings.setObjectName("btn_network_settings")
        self.btn_network_settings.setGeometry(QRect(1100, 14, 130, 32))

        self.tabWidget.addTab(self.tab_3, "")

        # ── Onglet Production (tab_4) ─────────────────────────────────────
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")

        self.frame_production_graphes = QFrame(self.tab_4)
        self.frame_production_graphes.setObjectName("frame_production_graphes")
        self.frame_production_graphes.setGeometry(QRect(0, 0, 920, 741))
        self.frame_production_graphes.setFrameShape(QFrame.StyledPanel)
        self.frame_production_graphes.setFrameShadow(QFrame.Raised)

        self.label_prod_signal_title = QLabel(self.frame_production_graphes)
        self.label_prod_signal_title.setObjectName("label_prod_signal_title")
        self.label_prod_signal_title.setGeometry(QRect(20, 20, 200, 20))

        self.widget_prod_signal = QWidget(self.frame_production_graphes)
        self.widget_prod_signal.setObjectName("widget_prod_signal")
        self.widget_prod_signal.setGeometry(QRect(10, 50, 900, 300))

        self.label_prod_fft_title = QLabel(self.frame_production_graphes)
        self.label_prod_fft_title.setObjectName("label_prod_fft_title")
        self.label_prod_fft_title.setGeometry(QRect(20, 365, 200, 20))

        self.widget_prod_fft = QWidget(self.frame_production_graphes)
        self.widget_prod_fft.setObjectName("widget_prod_fft")
        self.widget_prod_fft.setGeometry(QRect(10, 395, 900, 320))

        self.frame_production_side = QFrame(self.tab_4)
        self.frame_production_side.setObjectName("frame_production_side")
        self.frame_production_side.setGeometry(QRect(930, 0, 340, 741))
        self.frame_production_side.setFrameShape(QFrame.StyledPanel)
        self.frame_production_side.setFrameShadow(QFrame.Raised)

        self.label_prod_vals_title = QLabel(self.frame_production_side)
        self.label_prod_vals_title.setObjectName("label_prod_vals_title")
        self.label_prod_vals_title.setGeometry(QRect(10, 10, 310, 20))

        self.label_prod_val_title = QLabel(self.frame_production_side)
        self.label_prod_val_title.setObjectName("label_prod_val_title")
        self.label_prod_val_title.setGeometry(QRect(10, 45, 150, 18))

        self.label_prod_val = QLabel(self.frame_production_side)
        self.label_prod_val.setObjectName("label_prod_val")
        self.label_prod_val.setGeometry(QRect(10, 65, 155, 22))

        self.label_prod_rms_title = QLabel(self.frame_production_side)
        self.label_prod_rms_title.setObjectName("label_prod_rms_title")
        self.label_prod_rms_title.setGeometry(QRect(175, 45, 150, 18))

        self.label_prod_rms = QLabel(self.frame_production_side)
        self.label_prod_rms.setObjectName("label_prod_rms")
        self.label_prod_rms.setGeometry(QRect(175, 65, 155, 22))

        self.label_prod_min_title = QLabel(self.frame_production_side)
        self.label_prod_min_title.setObjectName("label_prod_min_title")
        self.label_prod_min_title.setGeometry(QRect(10, 105, 150, 18))

        self.label_prod_min = QLabel(self.frame_production_side)
        self.label_prod_min.setObjectName("label_prod_min")
        self.label_prod_min.setGeometry(QRect(10, 125, 155, 22))

        self.label_prod_max_title = QLabel(self.frame_production_side)
        self.label_prod_max_title.setObjectName("label_prod_max_title")
        self.label_prod_max_title.setGeometry(QRect(175, 105, 150, 18))

        self.label_prod_max = QLabel(self.frame_production_side)
        self.label_prod_max.setObjectName("label_prod_max")
        self.label_prod_max.setGeometry(QRect(175, 125, 155, 22))

        self.label_prod_conv_title = QLabel(self.frame_production_side)
        self.label_prod_conv_title.setObjectName("label_prod_conv_title")
        self.label_prod_conv_title.setGeometry(QRect(10, 168, 310, 20))

        self.label_prod_raw = QLabel(self.frame_production_side)
        self.label_prod_raw.setObjectName("label_prod_raw")
        self.label_prod_raw.setGeometry(QRect(10, 198, 155, 22))

        self.label_prod_db = QLabel(self.frame_production_side)
        self.label_prod_db.setObjectName("label_prod_db")
        self.label_prod_db.setGeometry(QRect(175, 198, 155, 22))

        self.label_prod_liaison_title = QLabel(self.frame_production_side)
        self.label_prod_liaison_title.setObjectName("label_prod_liaison_title")
        self.label_prod_liaison_title.setGeometry(QRect(10, 245, 310, 20))

        self.label_prod_rssi = QLabel(self.frame_production_side)
        self.label_prod_rssi.setObjectName("label_prod_rssi")
        self.label_prod_rssi.setGeometry(QRect(10, 275, 310, 22))

        self.label_prod_latence = QLabel(self.frame_production_side)
        self.label_prod_latence.setObjectName("label_prod_latence")
        self.label_prod_latence.setGeometry(QRect(10, 307, 310, 22))

        self.label_prod_per = QLabel(self.frame_production_side)
        self.label_prod_per.setObjectName("label_prod_per")
        self.label_prod_per.setGeometry(QRect(10, 339, 310, 22))

        self.tabWidget.addTab(self.tab_4, "")

        # ── Onglet Maintenance (tab_5) ────────────────────────────────────
        self.tab_5 = QWidget()
        self.tab_5.setObjectName("tab_5")

        self.frame_terminal = QFrame(self.tab_5)
        self.frame_terminal.setObjectName("frame_terminal")
        self.frame_terminal.setGeometry(QRect(0, 0, 750, 741))
        self.frame_terminal.setFrameShape(QFrame.StyledPanel)
        self.frame_terminal.setFrameShadow(QFrame.Raised)

        self.label_terminal_title = QLabel(self.frame_terminal)
        self.label_terminal_title.setObjectName("label_terminal_title")
        self.label_terminal_title.setGeometry(QRect(20, 10, 160, 16))

        self.text_terminal_output = QTextEdit(self.frame_terminal)
        self.text_terminal_output.setObjectName("text_terminal_output")
        self.text_terminal_output.setGeometry(QRect(20, 40, 711, 511))
        self.text_terminal_output.setReadOnly(True)

        self.input_cmd = QLineEdit(self.frame_terminal)
        self.input_cmd.setObjectName("input_cmd")
        self.input_cmd.setGeometry(QRect(20, 560, 461, 81))

        self.btn_send_cmd = QPushButton(self.frame_terminal)
        self.btn_send_cmd.setObjectName("btn_send_cmd")
        self.btn_send_cmd.setGeometry(QRect(490, 580, 101, 41))

        self.btn_clear_terminal = QPushButton(self.frame_terminal)
        self.btn_clear_terminal.setObjectName("btn_clear_terminal")
        self.btn_clear_terminal.setGeometry(QRect(620, 580, 101, 41))

        self.label_ack_title = QLabel(self.frame_terminal)
        self.label_ack_title.setObjectName("label_ack_title")
        self.label_ack_title.setGeometry(QRect(20, 660, 160, 16))

        self.label_ack_status = QLabel(self.frame_terminal)
        self.label_ack_status.setObjectName("label_ack_status")
        self.label_ack_status.setGeometry(QRect(80, 700, 101, 16))

        self.label_ack_latence = QLabel(self.frame_terminal)
        self.label_ack_latence.setObjectName("label_ack_latence")
        self.label_ack_latence.setGeometry(QRect(300, 700, 101, 16))

        self.label_ack_seq = QLabel(self.frame_terminal)
        self.label_ack_seq.setObjectName("label_ack_seq")
        self.label_ack_seq.setGeometry(QRect(520, 700, 61, 16))

        self.frame_commands = QFrame(self.tab_5)
        self.frame_commands.setObjectName("frame_commands")
        self.frame_commands.setGeometry(QRect(760, 0, 480, 741))
        self.frame_commands.setFrameShape(QFrame.StyledPanel)
        self.frame_commands.setFrameShadow(QFrame.Raised)

        self.label_carte_cible_val = QLabel(self.frame_commands)
        self.label_carte_cible_val.setObjectName("label_carte_cible_val")
        self.label_carte_cible_val.setGeometry(QRect(20, 10, 441, 51))

        self.label_capteur_cible_val = QLabel(self.frame_commands)
        self.label_capteur_cible_val.setObjectName("label_capteur_cible_val")
        self.label_capteur_cible_val.setGeometry(QRect(20, 70, 441, 51))

        self.label_cmd_rapides_title = QLabel(self.frame_commands)
        self.label_cmd_rapides_title.setObjectName("label_cmd_rapides_title")
        self.label_cmd_rapides_title.setGeometry(QRect(20, 180, 111, 16))

        self.btn_cmd_wake = QPushButton(self.frame_commands)
        self.btn_cmd_wake.setObjectName("btn_cmd_wake")
        self.btn_cmd_wake.setGeometry(QRect(30, 210, 95, 31))

        self.btn_cmd_start = QPushButton(self.frame_commands)
        self.btn_cmd_start.setObjectName("btn_cmd_start")
        self.btn_cmd_start.setGeometry(QRect(180, 210, 95, 31))

        self.btn_cmd_stop = QPushButton(self.frame_commands)
        self.btn_cmd_stop.setObjectName("btn_cmd_stop")
        self.btn_cmd_stop.setGeometry(QRect(340, 210, 95, 31))

        self.btn_cmd_status = QPushButton(self.frame_commands)
        self.btn_cmd_status.setObjectName("btn_cmd_status")
        self.btn_cmd_status.setGeometry(QRect(30, 260, 95, 31))

        self.btn_cmd_reset = QPushButton(self.frame_commands)
        self.btn_cmd_reset.setObjectName("btn_cmd_reset")
        self.btn_cmd_reset.setGeometry(QRect(180, 260, 95, 31))

        self.btn_cmd_config = QPushButton(self.frame_commands)
        self.btn_cmd_config.setObjectName("btn_cmd_config")
        self.btn_cmd_config.setGeometry(QRect(340, 260, 95, 31))

        self.label_lock_title = QLabel(self.frame_commands)
        self.label_lock_title.setObjectName("label_lock_title")
        self.label_lock_title.setGeometry(QRect(30, 330, 81, 16))

        self.input_password = QLineEdit(self.frame_commands)
        self.input_password.setObjectName("input_password")
        self.input_password.setGeometry(QRect(30, 360, 441, 51))
        self.input_password.setEchoMode(QLineEdit.Password)

        self.btn_unlock = QPushButton(self.frame_commands)
        self.btn_unlock.setObjectName("btn_unlock")
        self.btn_unlock.setGeometry(QRect(355, 370, 110, 31))

        self.label_historique_cmd_title = QLabel(self.frame_commands)
        self.label_historique_cmd_title.setObjectName("label_historique_cmd_title")
        self.label_historique_cmd_title.setGeometry(QRect(20, 450, 155, 16))

        self.list_cmd_history = QListWidget(self.frame_commands)
        self.list_cmd_history.setObjectName("list_cmd_history")
        self.list_cmd_history.setGeometry(QRect(10, 471, 471, 251))

        self.tabWidget.addTab(self.tab_5, "")

        # ── Onglet Alarmes (tab_6) ────────────────────────────────────────
        self.tab_6 = QWidget()
        self.tab_6.setObjectName("tab_6")

        self.frame_alarmes_actives = QFrame(self.tab_6)
        self.frame_alarmes_actives.setObjectName("frame_alarmes_actives")
        self.frame_alarmes_actives.setGeometry(QRect(0, 0, 1260, 300))
        self.frame_alarmes_actives.setFrameShape(QFrame.StyledPanel)
        self.frame_alarmes_actives.setFrameShadow(QFrame.Raised)

        self.label_alarmes_title = QLabel(self.frame_alarmes_actives)
        self.label_alarmes_title.setObjectName("label_alarmes_title")
        self.label_alarmes_title.setGeometry(QRect(20, 10, 91, 16))

        self.label_alarmes_actives_title = QTableWidget(self.frame_alarmes_actives)
        self.label_alarmes_actives_title.setObjectName("label_alarmes_actives_title")
        self.label_alarmes_actives_title.setGeometry(QRect(10, 40, 1241, 192))
        self.label_alarmes_actives_title.setColumnCount(6)
        for i in range(6):
            self.label_alarmes_actives_title.setHorizontalHeaderItem(i, QTableWidgetItem())

        self.btn_acquit = QPushButton(self.frame_alarmes_actives)
        self.btn_acquit.setObjectName("btn_acquit")
        self.btn_acquit.setGeometry(QRect(30, 250, 171, 41))

        self.btn_acquit_all = QPushButton(self.frame_alarmes_actives)
        self.btn_acquit_all.setObjectName("btn_acquit_all")
        self.btn_acquit_all.setGeometry(QRect(260, 250, 161, 41))

        self.label_alarmes_count = QLabel(self.frame_alarmes_actives)
        self.label_alarmes_count.setObjectName("label_alarmes_count")
        self.label_alarmes_count.setGeometry(QRect(120, 10, 47, 16))

        self.frame_historique_alarmes = QFrame(self.tab_6)
        self.frame_historique_alarmes.setObjectName("frame_historique_alarmes")
        self.frame_historique_alarmes.setGeometry(QRect(0, 310, 1260, 421))
        self.frame_historique_alarmes.setFrameShape(QFrame.StyledPanel)
        self.frame_historique_alarmes.setFrameShadow(QFrame.Raised)

        self.label_historique_alarmes_title = QLabel(self.frame_historique_alarmes)
        self.label_historique_alarmes_title.setObjectName("label_historique_alarmes_title")
        self.label_historique_alarmes_title.setGeometry(QRect(10, 10, 121, 16))

        self.table_alarmes_historique = QTableWidget(self.frame_historique_alarmes)
        self.table_alarmes_historique.setObjectName("table_alarmes_historique")
        self.table_alarmes_historique.setGeometry(QRect(10, 90, 1241, 321))
        self.table_alarmes_historique.setColumnCount(6)
        for i in range(6):
            self.table_alarmes_historique.setHorizontalHeaderItem(i, QTableWidgetItem())

        self.btn_export_alarmes = QPushButton(self.frame_historique_alarmes)
        self.btn_export_alarmes.setObjectName("btn_export_alarmes")
        self.btn_export_alarmes.setGeometry(QRect(1104, 10, 121, 71))

        self.combo_filtre_severite = QComboBox(self.frame_historique_alarmes)
        self.combo_filtre_severite.setObjectName("combo_filtre_severite")
        self.combo_filtre_severite.setGeometry(QRect(160, 20, 431, 51))

        self.combo_filtre_capteur = QComboBox(self.frame_historique_alarmes)
        self.combo_filtre_capteur.setObjectName("combo_filtre_capteur")
        self.combo_filtre_capteur.setGeometry(QRect(620, 20, 431, 51))

        self.tabWidget.addTab(self.tab_6, "")

        # ── Onglet Historique (tab_7) ─────────────────────────────────────
        self.tab_7 = QWidget()
        self.tab_7.setObjectName("tab_7")

        self.frame_historique_graphes = QFrame(self.tab_7)
        self.frame_historique_graphes.setObjectName("frame_historique_graphes")
        self.frame_historique_graphes.setGeometry(QRect(0, 0, 900, 741))
        self.frame_historique_graphes.setFrameShape(QFrame.StyledPanel)
        self.frame_historique_graphes.setFrameShadow(QFrame.Raised)

        self.combo_histo_capteur = QComboBox(self.frame_historique_graphes)
        self.combo_histo_capteur.setObjectName("combo_histo_capteur")
        self.combo_histo_capteur.setGeometry(QRect(20, 10, 841, 51))

        self.combo_histo_periode = QComboBox(self.frame_historique_graphes)
        self.combo_histo_periode.setObjectName("combo_histo_periode")
        self.combo_histo_periode.setGeometry(QRect(20, 70, 841, 51))

        self.datetime_histo_debut = QDateTimeEdit(self.frame_historique_graphes)
        self.datetime_histo_debut.setObjectName("datetime_histo_debut")
        self.datetime_histo_debut.setGeometry(QRect(20, 130, 841, 41))

        self.datetime_histo_fin = QDateTimeEdit(self.frame_historique_graphes)
        self.datetime_histo_fin.setObjectName("datetime_histo_fin")
        self.datetime_histo_fin.setGeometry(QRect(20, 180, 841, 41))

        self.btn_histo_load = QPushButton(self.frame_historique_graphes)
        self.btn_histo_load.setObjectName("btn_histo_load")
        self.btn_histo_load.setGeometry(QRect(20, 230, 141, 41))

        self.label_histo_courbe_title = QLabel(self.frame_historique_graphes)
        self.label_histo_courbe_title.setObjectName("label_histo_courbe_title")
        self.label_histo_courbe_title.setGeometry(QRect(20, 290, 101, 16))

        self.widget_courbe = QWidget(self.frame_historique_graphes)
        self.widget_courbe.setObjectName("widget_courbe")
        self.widget_courbe.setGeometry(QRect(10, 310, 871, 200))

        self.label_histo_fft_title = QLabel(self.frame_historique_graphes)
        self.label_histo_fft_title.setObjectName("label_histo_fft_title")
        self.label_histo_fft_title.setGeometry(QRect(20, 530, 71, 16))

        self.widget_fft = QWidget(self.frame_historique_graphes)
        self.widget_fft.setObjectName("widget_fft")
        self.widget_fft.setGeometry(QRect(10, 560, 871, 160))

        self.frame_historique_side = QFrame(self.tab_7)
        self.frame_historique_side.setObjectName("frame_historique_side")
        self.frame_historique_side.setGeometry(QRect(910, 0, 330, 741))
        self.frame_historique_side.setFrameShape(QFrame.StyledPanel)
        self.frame_historique_side.setFrameShadow(QFrame.Raised)

        self.label_stats_title = QLabel(self.frame_historique_side)
        self.label_stats_title.setObjectName("label_stats_title")
        self.label_stats_title.setGeometry(QRect(10, 10, 81, 16))

        self.label_stats_moyenne_title = QLabel(self.frame_historique_side)
        self.label_stats_moyenne_title.setObjectName("label_stats_moyenne_title")
        self.label_stats_moyenne_title.setGeometry(QRect(20, 40, 80, 20))

        self.label_stats_moyenne_val = QLabel(self.frame_historique_side)
        self.label_stats_moyenne_val.setObjectName("label_stats_moyenne_val")
        self.label_stats_moyenne_val.setGeometry(QRect(20, 60, 47, 13))

        self.label_stats_rms_title = QLabel(self.frame_historique_side)
        self.label_stats_rms_title.setObjectName("label_stats_rms_title")
        self.label_stats_rms_title.setGeometry(QRect(190, 40, 47, 13))

        self.label_stats_rms_val = QLabel(self.frame_historique_side)
        self.label_stats_rms_val.setObjectName("label_stats_rms_val")
        self.label_stats_rms_val.setGeometry(QRect(190, 60, 47, 13))

        self.label_stats_min_title = QLabel(self.frame_historique_side)
        self.label_stats_min_title.setObjectName("label_stats_min_title")
        self.label_stats_min_title.setGeometry(QRect(20, 110, 47, 13))

        self.label_stats_min_val = QLabel(self.frame_historique_side)
        self.label_stats_min_val.setObjectName("label_stats_min_val")
        self.label_stats_min_val.setGeometry(QRect(20, 130, 47, 13))

        self.label_stats_max_title = QLabel(self.frame_historique_side)
        self.label_stats_max_title.setObjectName("label_stats_max_title")
        self.label_stats_max_title.setGeometry(QRect(190, 110, 47, 13))

        self.label_stats_max_val = QLabel(self.frame_historique_side)
        self.label_stats_max_val.setObjectName("label_stats_max_val")
        self.label_stats_max_val.setGeometry(QRect(190, 130, 47, 13))

        self.label_logs_title = QLabel(self.frame_historique_side)
        self.label_logs_title.setObjectName("label_logs_title")
        self.label_logs_title.setGeometry(QRect(20, 230, 80, 16))

        self.table_logs = QTableWidget(self.frame_historique_side)
        self.table_logs.setObjectName("table_logs")
        self.table_logs.setGeometry(QRect(10, 260, 301, 231))
        self.table_logs.setColumnCount(3)
        for i in range(3):
            self.table_logs.setHorizontalHeaderItem(i, QTableWidgetItem())

        self.combo_export_format = QComboBox(self.frame_historique_side)
        self.combo_export_format.setObjectName("combo_export_format")
        self.combo_export_format.setGeometry(QRect(10, 560, 301, 51))

        self.btn_export_histo = QPushButton(self.frame_historique_side)
        self.btn_export_histo.setObjectName("btn_export_histo")
        self.btn_export_histo.setGeometry(QRect(10, 620, 301, 41))

        self.label_export_title = QLabel(self.frame_historique_side)
        self.label_export_title.setObjectName("label_export_title")
        self.label_export_title.setGeometry(QRect(20, 530, 47, 13))

        self.tabWidget.addTab(self.tab_7, "")

        # ── Onglet Paramètres (tab_8) ─────────────────────────────────────
        self.tab_8 = QWidget()
        self.tab_8.setObjectName("tab_8")

        self.frame_params_gauche = QFrame(self.tab_8)
        self.frame_params_gauche.setObjectName("frame_params_gauche")
        self.frame_params_gauche.setGeometry(QRect(0, 0, 610, 741))
        self.frame_params_gauche.setFrameShape(QFrame.StyledPanel)
        self.frame_params_gauche.setFrameShadow(QFrame.Raised)

        self.label_params_capteur_title = QLabel(self.frame_params_gauche)
        self.label_params_capteur_title.setObjectName("label_params_capteur_title")
        self.label_params_capteur_title.setGeometry(QRect(10, 10, 150, 16))

        self.label_params_capteur_val = QLabel(self.frame_params_gauche)
        self.label_params_capteur_val.setObjectName("label_params_capteur_val")
        self.label_params_capteur_val.setGeometry(QRect(10, 30, 591, 51))

        self.label_params_acq_title = QLabel(self.frame_params_gauche)
        self.label_params_acq_title.setObjectName("label_params_acq_title")
        self.label_params_acq_title.setGeometry(QRect(10, 120, 71, 16))

        self.label_frequence_echantillonage = QLabel(self.frame_params_gauche)
        self.label_frequence_echantillonage.setObjectName("label_frequence_echantillonage")
        self.label_frequence_echantillonage.setGeometry(QRect(10, 160, 155, 16))

        self.combo_params_sps = QComboBox(self.frame_params_gauche)
        self.combo_params_sps.setObjectName("combo_params_sps")
        self.combo_params_sps.setGeometry(QRect(170, 150, 421, 41))

        self.label_taille_buffer_fft = QLabel(self.frame_params_gauche)
        self.label_taille_buffer_fft.setObjectName("label_taille_buffer_fft")
        self.label_taille_buffer_fft.setGeometry(QRect(10, 230, 131, 16))

        self.combo_params_fft = QComboBox(self.frame_params_gauche)
        self.combo_params_fft.setObjectName("combo_params_fft")
        self.combo_params_fft.setGeometry(QRect(170, 210, 421, 41))

        self.label_frequence_envoie_udp = QLabel(self.frame_params_gauche)
        self.label_frequence_envoie_udp.setObjectName("label_frequence_envoie_udp")
        self.label_frequence_envoie_udp.setGeometry(QRect(10, 290, 155, 16))

        self.combo_params_udp = QComboBox(self.frame_params_gauche)
        self.combo_params_udp.setObjectName("combo_params_udp")
        self.combo_params_udp.setGeometry(QRect(170, 270, 421, 41))

        self.combo_params_resolution = QComboBox(self.frame_params_gauche)
        self.combo_params_resolution.setObjectName("combo_params_resolution")
        self.combo_params_resolution.setGeometry(QRect(170, 330, 421, 41))

        self.label_resolution_adc = QLabel(self.frame_params_gauche)
        self.label_resolution_adc.setObjectName("label_resolution_adc")
        self.label_resolution_adc.setGeometry(QRect(10, 340, 121, 16))

        self.label_params_mode_title = QLabel(self.frame_params_gauche)
        self.label_params_mode_title.setObjectName("label_params_mode_title")
        self.label_params_mode_title.setGeometry(QRect(10, 450, 81, 16))

        self.label_mode_fonctionnement = QLabel(self.frame_params_gauche)
        self.label_mode_fonctionnement.setObjectName("label_mode_fonctionnement")
        self.label_mode_fonctionnement.setGeometry(QRect(10, 490, 141, 16))

        self.combo_params_mode = QComboBox(self.frame_params_gauche)
        self.combo_params_mode.setObjectName("combo_params_mode")
        self.combo_params_mode.setGeometry(QRect(170, 480, 421, 41))

        self.label_mode_fonctionnement_2 = QLabel(self.frame_params_gauche)
        self.label_mode_fonctionnement_2.setObjectName("label_mode_fonctionnement_2")
        self.label_mode_fonctionnement_2.setGeometry(QRect(10, 570, 101, 16))

        self.combo_params_timeout = QComboBox(self.frame_params_gauche)
        self.combo_params_timeout.setObjectName("combo_params_timeout")
        self.combo_params_timeout.setGeometry(QRect(170, 550, 421, 41))

        self.frame_params_droite = QFrame(self.tab_8)
        self.frame_params_droite.setObjectName("frame_params_droite")
        self.frame_params_droite.setGeometry(QRect(620, 0, 610, 741))
        self.frame_params_droite.setFrameShape(QFrame.StyledPanel)
        self.frame_params_droite.setFrameShadow(QFrame.Raised)

        self.label_params_seuils_title = QLabel(self.frame_params_droite)
        self.label_params_seuils_title.setObjectName("label_params_seuils_title")
        self.label_params_seuils_title.setGeometry(QRect(10, 10, 81, 16))

        self.label_valeur_max = QLabel(self.frame_params_droite)
        self.label_valeur_max.setObjectName("label_valeur_max")
        self.label_valeur_max.setGeometry(QRect(10, 60, 91, 16))

        self.spinbox_val_max = QDoubleSpinBox(self.frame_params_droite)
        self.spinbox_val_max.setObjectName("spinbox_val_max")
        self.spinbox_val_max.setGeometry(QRect(160, 50, 431, 41))

        self.label_valeur_min = QLabel(self.frame_params_droite)
        self.label_valeur_min.setObjectName("label_valeur_min")
        self.label_valeur_min.setGeometry(QRect(10, 130, 91, 16))

        self.spinbox_val_min = QDoubleSpinBox(self.frame_params_droite)
        self.spinbox_val_min.setObjectName("spinbox_val_min")
        self.spinbox_val_min.setGeometry(QRect(160, 120, 431, 41))

        self.label_seuil_rms_max = QLabel(self.frame_params_droite)
        self.label_seuil_rms_max.setObjectName("label_seuil_rms_max")
        self.label_seuil_rms_max.setGeometry(QRect(10, 200, 130, 16))

        self.spinbox_rms_max = QDoubleSpinBox(self.frame_params_droite)
        self.spinbox_rms_max.setObjectName("spinbox_rms_max")
        self.spinbox_rms_max.setGeometry(QRect(160, 190, 431, 41))

        self.label_seuil_db_si_max = QLabel(self.frame_params_droite)
        self.label_seuil_db_si_max.setObjectName("label_seuil_db_si_max")
        self.label_seuil_db_si_max.setGeometry(QRect(10, 270, 140, 16))

        self.spinbox_db_max = QDoubleSpinBox(self.frame_params_droite)
        self.spinbox_db_max.setObjectName("spinbox_db_max")
        self.spinbox_db_max.setGeometry(QRect(160, 260, 431, 41))

        self.label_params_id_title = QLabel(self.frame_params_droite)
        self.label_params_id_title.setObjectName("label_params_id_title")
        self.label_params_id_title.setGeometry(QRect(10, 370, 155, 16))

        self.label_id_capteur = QLabel(self.frame_params_droite)
        self.label_id_capteur.setObjectName("label_id_capteur")
        self.label_id_capteur.setGeometry(QRect(20, 410, 81, 16))

        self.input_capteur_id = QLineEdit(self.frame_params_droite)
        self.input_capteur_id.setObjectName("input_capteur_id")
        self.input_capteur_id.setGeometry(QRect(130, 400, 451, 41))

        self.label_nom_affiche = QLabel(self.frame_params_droite)
        self.label_nom_affiche.setObjectName("label_nom_affiche")
        self.label_nom_affiche.setGeometry(QRect(20, 480, 81, 16))

        self.input_capteur_nom = QLineEdit(self.frame_params_droite)
        self.input_capteur_nom.setObjectName("input_capteur_nom")
        self.input_capteur_nom.setGeometry(QRect(130, 470, 451, 41))

        self.label_carte_associe = QLabel(self.frame_params_droite)
        self.label_carte_associe.setObjectName("label_carte_associe")
        self.label_carte_associe.setGeometry(QRect(10, 550, 81, 16))

        self.combo_capteur_carte = QLineEdit(self.frame_params_droite)
        self.combo_capteur_carte.setObjectName("combo_capteur_carte")
        self.combo_capteur_carte.setGeometry(QRect(130, 540, 451, 41))

        self.btn_params_appliquer = QPushButton(self.frame_params_droite)
        self.btn_params_appliquer.setObjectName("btn_params_appliquer")
        self.btn_params_appliquer.setGeometry(QRect(20, 620, 131, 41))

        self.btn_params_reset = QPushButton(self.frame_params_droite)
        self.btn_params_reset.setObjectName("btn_params_reset")
        self.btn_params_reset.setGeometry(QRect(220, 620, 145, 41))

        self.btn_params_reset_all = QPushButton(self.frame_params_droite)
        self.btn_params_reset_all.setObjectName("btn_params_reset_all")
        self.btn_params_reset_all.setGeometry(QRect(430, 620, 160, 41))

        self.tabWidget.addTab(self.tab_8, "")

        # ── Layout principal ──────────────────────────────────────────────
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)

    def retranslateUi(self, MainWindow):
        _tr = QCoreApplication.translate
        MainWindow.setWindowTitle(_tr("MainWindow", "IHM Wi-Fi — Microcontrôleur"))

        # Accueil
        self.label_wake_message.setText(_tr("MainWindow", " en mode éco, réveillez-le pour accéder à Production"))
        self.label_wake_id.setText(_tr("MainWindow", "Capteur ID:--"))
        self.btn_wake.setText(_tr("MainWindow", "Réveiller le capteur"))
        self.label_system_title.setText(_tr("MainWindow", "État du système"))
        self.btn_scan.setText(_tr("MainWindow", "Scanner le réseau"))
        self.label_network_title.setText(_tr("MainWindow", "Résumé réseau"))
        self.label_latence_title.setText(_tr("MainWindow", "Latence moy."))
        self.label_latence_val.setText(_tr("MainWindow", "-- ms"))
        self.label_rssi_title.setText(_tr("MainWindow", "RSSI"))
        self.label_rssi_val.setText(_tr("MainWindow", "-- dBm"))
        self.label_per_title.setText(_tr("MainWindow", "PER"))
        self.label_per_val.setText(_tr("MainWindow", "-- %"))
        self.label_debit_title.setText(_tr("MainWindow", "Débit"))
        self.label_debit_val.setText(_tr("MainWindow", "-- pkt/s"))
        self.label_canal_title.setText(_tr("MainWindow", "Canal Wi-Fi"))
        self.label_canal_val.setText(_tr("MainWindow", "--"))
        self.label_paquets_title.setText(_tr("MainWindow", "Paquets reçus/envoyés"))
        self.label_paquets_val.setText(_tr("MainWindow", "-- / --"))
        self.label_capteurs_title.setText(_tr("MainWindow", "Capteurs connectés"))
        self.table_capteurs.horizontalHeaderItem(0).setText(_tr("MainWindow", "ID"))
        self.table_capteurs.horizontalHeaderItem(1).setText(_tr("MainWindow", "Type"))
        self.table_capteurs.horizontalHeaderItem(2).setText(_tr("MainWindow", "Carte"))
        self.table_capteurs.horizontalHeaderItem(3).setText(_tr("MainWindow", "État"))
        self.table_capteurs.horizontalHeaderItem(4).setText(_tr("MainWindow", "Action"))
        self.btn_start.setText(_tr("MainWindow", "Démarrer acquisition"))
        self.btn_stop.setText(_tr("MainWindow", "Arrêter"))
        self.btn_export.setText(_tr("MainWindow", "Exporter logs"))
        self.btn_network_settings.setText(_tr("MainWindow", "Paramètres réseau"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _tr("MainWindow", "Accueil"))

        # Production
        self.label_prod_signal_title.setText(_tr("MainWindow", "Signal temporel"))
        self.label_prod_fft_title.setText(_tr("MainWindow", "Spectre FFT"))
        self.label_prod_vals_title.setText(_tr("MainWindow", "Valeurs temps réel"))
        self.label_prod_val_title.setText(_tr("MainWindow", "Valeur"))
        self.label_prod_val.setText(_tr("MainWindow", "--"))
        self.label_prod_rms_title.setText(_tr("MainWindow", "RMS"))
        self.label_prod_rms.setText(_tr("MainWindow", "--"))
        self.label_prod_min_title.setText(_tr("MainWindow", "Min"))
        self.label_prod_min.setText(_tr("MainWindow", "--"))
        self.label_prod_max_title.setText(_tr("MainWindow", "Max"))
        self.label_prod_max.setText(_tr("MainWindow", "--"))
        self.label_prod_conv_title.setText(_tr("MainWindow", "Conversion ADC → dB SPL"))
        self.label_prod_raw.setText(_tr("MainWindow", "-- raw"))
        self.label_prod_db.setText(_tr("MainWindow", "-- dB SPL"))
        self.label_prod_liaison_title.setText(_tr("MainWindow", "État liaison"))
        self.label_prod_rssi.setText(_tr("MainWindow", "RSSI : -- dBm"))
        self.label_prod_latence.setText(_tr("MainWindow", "Latence : -- ms"))
        self.label_prod_per.setText(_tr("MainWindow", "PER : -- %"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _tr("MainWindow", "Production"))

        # Maintenance
        self.label_terminal_title.setText(_tr("MainWindow", "Terminal de commandes"))
        self.input_cmd.setPlaceholderText(_tr("MainWindow", "CMD:...;ID:...;SEQ:...;CHK:..."))
        self.btn_send_cmd.setText(_tr("MainWindow", "Envoyer"))
        self.btn_clear_terminal.setText(_tr("MainWindow", "Effacer"))
        self.label_ack_title.setText(_tr("MainWindow", "Dernière réponse ACK"))
        self.label_ack_status.setText(_tr("MainWindow", "Statut : --"))
        self.label_ack_latence.setText(_tr("MainWindow", "Latence : -- ms"))
        self.label_ack_seq.setText(_tr("MainWindow", "SEQ : --"))
        self.label_carte_cible_val.setText(_tr("MainWindow", "Aucune carte sélectionnée"))
        self.label_capteur_cible_val.setText(_tr("MainWindow", "Aucun capteur sélectionné"))
        self.label_cmd_rapides_title.setText(_tr("MainWindow", "Commandes rapides"))
        self.btn_cmd_wake.setText(_tr("MainWindow", "Réveiller"))
        self.btn_cmd_start.setText(_tr("MainWindow", "Démarrer"))
        self.btn_cmd_stop.setText(_tr("MainWindow", "Arrêter"))
        self.btn_cmd_status.setText(_tr("MainWindow", "Statut"))
        self.btn_cmd_reset.setText(_tr("MainWindow", "Reset"))
        self.btn_cmd_config.setText(_tr("MainWindow", "Config"))
        self.label_lock_title.setText(_tr("MainWindow", "Accès restreint"))
        self.btn_unlock.setText(_tr("MainWindow", "Déverrouiller"))
        self.label_historique_cmd_title.setText(_tr("MainWindow", "Historique commandes"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _tr("MainWindow", "Maintenance"))

        # Alarmes
        self.label_alarmes_title.setText(_tr("MainWindow", "Alarmes actives"))
        self.label_alarmes_actives_title.horizontalHeaderItem(0).setText(_tr("MainWindow", "Heure"))
        self.label_alarmes_actives_title.horizontalHeaderItem(1).setText(_tr("MainWindow", "ID"))
        self.label_alarmes_actives_title.horizontalHeaderItem(2).setText(_tr("MainWindow", "Type"))
        self.label_alarmes_actives_title.horizontalHeaderItem(3).setText(_tr("MainWindow", "Message"))
        self.label_alarmes_actives_title.horizontalHeaderItem(4).setText(_tr("MainWindow", "Sévérité"))
        self.label_alarmes_actives_title.horizontalHeaderItem(5).setText(_tr("MainWindow", "Actions"))
        self.btn_acquit.setText(_tr("MainWindow", "Acquitter sélection"))
        self.btn_acquit_all.setText(_tr("MainWindow", "Acquitter tout"))
        self.label_alarmes_count.setText(_tr("MainWindow", "0"))
        self.label_historique_alarmes_title.setText(_tr("MainWindow", "Historique des alarmes"))
        self.table_alarmes_historique.horizontalHeaderItem(0).setText(_tr("MainWindow", "Heure"))
        self.table_alarmes_historique.horizontalHeaderItem(1).setText(_tr("MainWindow", "ID"))
        self.table_alarmes_historique.horizontalHeaderItem(2).setText(_tr("MainWindow", "Type"))
        self.table_alarmes_historique.horizontalHeaderItem(3).setText(_tr("MainWindow", "Message"))
        self.table_alarmes_historique.horizontalHeaderItem(4).setText(_tr("MainWindow", "Sévérité"))
        self.table_alarmes_historique.horizontalHeaderItem(5).setText(_tr("MainWindow", "Statut"))
        self.btn_export_alarmes.setText(_tr("MainWindow", "Exporter"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _tr("MainWindow", "Alarmes"))

        # Historique
        self.btn_histo_load.setText(_tr("MainWindow", "Charger"))
        self.label_histo_courbe_title.setText(_tr("MainWindow", "Courbe temporelle"))
        self.label_histo_fft_title.setText(_tr("MainWindow", "Spectre FFT"))
        self.label_stats_title.setText(_tr("MainWindow", "Statistiques"))
        self.label_stats_moyenne_title.setText(_tr("MainWindow", "Moyenne"))
        self.label_stats_moyenne_val.setText(_tr("MainWindow", "--"))
        self.label_stats_rms_title.setText(_tr("MainWindow", "RMS"))
        self.label_stats_rms_val.setText(_tr("MainWindow", "--"))
        self.label_stats_min_title.setText(_tr("MainWindow", "Min"))
        self.label_stats_min_val.setText(_tr("MainWindow", "--"))
        self.label_stats_max_title.setText(_tr("MainWindow", "Max"))
        self.label_stats_max_val.setText(_tr("MainWindow", "--"))
        self.label_logs_title.setText(_tr("MainWindow", "Logs bruts"))
        self.table_logs.horizontalHeaderItem(0).setText(_tr("MainWindow", "Heure"))
        self.table_logs.horizontalHeaderItem(1).setText(_tr("MainWindow", "Valeur"))
        self.table_logs.horizontalHeaderItem(2).setText(_tr("MainWindow", "Unité"))
        self.btn_export_histo.setText(_tr("MainWindow", "Exporter les données"))
        self.label_export_title.setText(_tr("MainWindow", "EXPORT"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _tr("MainWindow", "Historique"))

        # Paramètres
        self.label_params_capteur_title.setText(_tr("MainWindow", "Capteur sélectionné"))
        self.label_params_capteur_val.setText(_tr("MainWindow", "Aucun capteur sélectionné"))
        self.label_params_acq_title.setText(_tr("MainWindow", "Acquisition"))
        self.label_frequence_echantillonage.setText(_tr("MainWindow", "Fréquence d'échantillonnage"))
        self.label_taille_buffer_fft.setText(_tr("MainWindow", "Taille buffer FFT"))
        self.label_frequence_envoie_udp.setText(_tr("MainWindow", "Fréquence d'envoi UDP"))
        self.label_resolution_adc.setText(_tr("MainWindow", "Résolution ADC"))
        self.label_params_mode_title.setText(_tr("MainWindow", "Mode capteur"))
        self.label_mode_fonctionnement.setText(_tr("MainWindow", "Mode de fonctionnement"))
        self.label_mode_fonctionnement_2.setText(_tr("MainWindow", "Timeout mode éco"))
        self.label_params_seuils_title.setText(_tr("MainWindow", "Seuils d'alarme"))
        self.label_valeur_max.setText(_tr("MainWindow", "Valeur max (V)"))
        self.label_valeur_min.setText(_tr("MainWindow", "Valeur min (V)"))
        self.label_seuil_rms_max.setText(_tr("MainWindow", "Seuil RMS max (V)"))
        self.label_seuil_db_si_max.setText(_tr("MainWindow", "Seuil dB SPL max (dB)"))
        self.label_params_id_title.setText(_tr("MainWindow", "Identification capteur"))
        self.label_id_capteur.setText(_tr("MainWindow", "ID capteur"))
        self.label_nom_affiche.setText(_tr("MainWindow", "Nom affiché"))
        self.label_carte_associe.setText(_tr("MainWindow", "Carte associée"))
        self.btn_params_appliquer.setText(_tr("MainWindow", "Appliquer"))
        self.btn_params_reset.setText(_tr("MainWindow", "Réinitialiser"))
        self.btn_params_reset_all.setText(_tr("MainWindow", "Réinitialiser tout"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), _tr("MainWindow", "Paramètres"))
