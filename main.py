import sys
from PySide6.QtWidgets import QApplication
from controller import MainController
from dialog_connexion import DialogConnexion


def main():
    app = QApplication(sys.argv)

    # ── Dialog de connexion au démarrage ──
    dialog = DialogConnexion()
    if dialog.exec() != DialogConnexion.DialogCode.Accepted:
        # L'utilisateur a cliqué Quitter
        sys.exit(0)

    # Récupérer le choix
    mode      = dialog.mode         # "local" ou "distant"
    ip_dist   = dialog.ip_distante  # "" si local, sinon l'IP/hostname saisi

    # ── Lancer l'IHM principale avec le mode choisi ──
    window = MainController(mode=mode, ip_distante=ip_dist)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()