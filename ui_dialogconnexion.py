# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DialogConnexion.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (QDialog, QFrame, QLabel, QLineEdit,
                                QPushButton, QRadioButton)


class Ui_DialogConnexion(object):
    def setupUi(self, DialogConnexion):
        if not DialogConnexion.objectName():
            DialogConnexion.setObjectName(u"DialogConnexion")
        DialogConnexion.resize(500, 320)

        # Titre
        self.label_titre = QLabel(DialogConnexion)
        self.label_titre.setObjectName(u"label_titre")
        self.label_titre.setGeometry(QRect(10, 10, 480, 20))

        # Frame mode
        self.frame_mode = QFrame(DialogConnexion)
        self.frame_mode.setObjectName(u"frame_mode")
        self.frame_mode.setGeometry(QRect(10, 40, 480, 101))
        self.frame_mode.setFrameShape(QFrame.StyledPanel)
        self.frame_mode.setFrameShadow(QFrame.Raised)

        self.label_mode_title = QLabel(self.frame_mode)
        self.label_mode_title.setObjectName(u"label_mode_title")
        self.label_mode_title.setGeometry(QRect(10, 0, 200, 16))

        self.radio_local = QRadioButton(self.frame_mode)
        self.radio_local.setObjectName(u"radio_local")
        self.radio_local.setGeometry(QRect(10, 25, 460, 31))
        self.radio_local.setChecked(True)

        self.radio_distant = QRadioButton(self.frame_mode)
        self.radio_distant.setObjectName(u"radio_distant")
        self.radio_distant.setGeometry(QRect(10, 62, 460, 31))

        # Frame IP distante
        self.frame_distant = QFrame(DialogConnexion)
        self.frame_distant.setObjectName(u"frame_distant")
        self.frame_distant.setGeometry(QRect(10, 155, 480, 101))
        self.frame_distant.setFrameShape(QFrame.StyledPanel)
        self.frame_distant.setFrameShadow(QFrame.Raised)
        self.frame_distant.setEnabled(False)

        self.label_ip_title = QLabel(self.frame_distant)
        self.label_ip_title.setObjectName(u"label_ip_title")
        self.label_ip_title.setGeometry(QRect(10, 0, 460, 16))

        self.input_ip = QLineEdit(self.frame_distant)
        self.input_ip.setObjectName(u"input_ip")
        self.input_ip.setGeometry(QRect(10, 25, 460, 41))

        self.label_ip_info = QLabel(self.frame_distant)
        self.label_ip_info.setObjectName(u"label_ip_info")
        self.label_ip_info.setGeometry(QRect(10, 72, 460, 16))

        # Boutons
        self.btn_quitter = QPushButton(DialogConnexion)
        self.btn_quitter.setObjectName(u"btn_quitter")
        self.btn_quitter.setGeometry(QRect(10, 275, 101, 31))

        self.btn_connecter = QPushButton(DialogConnexion)
        self.btn_connecter.setObjectName(u"btn_connecter")
        self.btn_connecter.setGeometry(QRect(380, 275, 111, 31))

        self.retranslateUi(DialogConnexion)
        QMetaObject.connectSlotsByName(DialogConnexion)

    def retranslateUi(self, DialogConnexion):
        DialogConnexion.setWindowTitle(QCoreApplication.translate("DialogConnexion", u"Connexion \u2014 IHM Wi-Fi", None))
        self.label_titre.setText(QCoreApplication.translate("DialogConnexion", u"Mode de connexion", None))
        self.label_mode_title.setText(QCoreApplication.translate("DialogConnexion", u"S\u00e9lectionner le mode", None))
        self.radio_local.setText(QCoreApplication.translate("DialogConnexion", u"Mode Local ", None))
        self.radio_distant.setText(QCoreApplication.translate("DialogConnexion", u"Mode Distant ", None))
        self.label_ip_title.setText(QCoreApplication.translate("DialogConnexion", u"Adresse IP publique ou nom de domaine de la box :", None))
        self.input_ip.setPlaceholderText(QCoreApplication.translate("DialogConnexion", u"ex : 82.45.123.67  ou  mondomaine.fr", None))
        self.btn_quitter.setText(QCoreApplication.translate("DialogConnexion", u"Quitter", None))
        self.btn_connecter.setText(QCoreApplication.translate("DialogConnexion", u"Se connecter", None))
