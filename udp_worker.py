import socket
import threading
from PySide6.QtCore import QObject, Signal


class UDPWorker(QObject):
    # Signaux émis vers l'IHM
    trame_recue = Signal(object, str)   # trame brute reçue
    ack_recu    = Signal(str, str)      # ACK reçu
    liaison_perdue = Signal(str)        # timeout liaison

    def __init__(
        self,
        port_local=5001,
        port_dest=5002,
        broadcast="192.168.10.255",
        port_ecoute_carte=5002,
        mode="local",           # "local" ou "distant"
        ip_distante="",         # IP publique de la box si mode distant
    ):
        super().__init__()
        self.port_local        = port_local
        self.port_dest         = port_dest
        self.broadcast         = broadcast
        self.port_ecoute_carte = port_ecoute_carte
        self.mode              = mode        # "local" ou "distant"
        self.ip_distante       = ip_distante # IP/hostname box distante

        self.socket = None
        self.actif  = False
        self.thread = None

    # ─────────────────────────────────────────────────────────
    # Démarrage / arrêt
    # ─────────────────────────────────────────────────────────

    def demarrer(self):
        """Démarre l'écoute UDP dans un thread séparé."""
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
            self.socket = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(("", self.port_local))
        self.socket.settimeout(0.5)

        self.actif  = True
        self.thread = threading.Thread(target=self._ecouter, daemon=True)
        self.thread.start()

        # Handshake initial selon le mode
        if self.mode == "distant":
            # Envoi direct vers l'IP publique de la box (port forwarding)
            self.envoyer("Envoi requete adresse IP", self.ip_distante)
            print(f"[UDP] Mode distant → handshake vers {self.ip_distante}:{self.port_dest}")
        else:
            # Broadcast LAN classique
            self.envoyer_broadcast("Envoi requete adresse IP", port=self.port_ecoute_carte)
            print(f"[UDP] Mode local → broadcast sur {self.broadcast}:{self.port_ecoute_carte}")

        print(f"[UDP] Écoute sur port {self.port_local}")

    def arreter(self):
        self.actif = False
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
            self.socket = None
        print("[UDP] Arrêté")

    # ─────────────────────────────────────────────────────────
    # Boucle d'écoute
    # ─────────────────────────────────────────────────────────

    def _ecouter(self):
        """Boucle d'écoute dans le thread dédié."""
        while self.actif:
            try:
                data, addr = self.socket.recvfrom(4096)

                # En mode distant, l'adresse source est celle de la box (NAT)
                # On utilise ip_distante comme référence d'affichage
                ip_source = addr[0]
                if self.mode == "distant" and self.ip_distante:
                    ip_source = self.ip_distante

                # Paquet binaire MIC ?
                if len(data) > 10 and data[0] == 0x4D:
                    self.trame_recue.emit(data, ip_source)
                    continue

                trame = data.decode("utf-8").strip()

                if trame.startswith("CARTE_DISPO"):
                    print(f"[UDP] CARTE_DISPO reçu — envoi handshake")
                    if self.mode == "distant":
                        self.envoyer("Envoi requete adresse IP", self.ip_distante)
                    else:
                        self.envoyer_broadcast(
                            "Envoi requete adresse IP", port=self.port_dest
                        )
                    continue

                if trame.startswith("ACK"):
                    self.ack_recu.emit(trame, ip_source)
                else:
                    self.trame_recue.emit(trame, ip_source)

            except socket.timeout:
                continue
            except Exception as e:
                if self.actif:
                    print(f"[UDP] Erreur écoute : {e}")
                break

    # ─────────────────────────────────────────────────────────
    # Envoi
    # ─────────────────────────────────────────────────────────

    def envoyer(self, trame, ip_dest):
        """
        Envoie une trame UDP vers une IP précise.
        Fonctionne en mode local ET distant.
        """
        try:
            if self.socket and ip_dest:
                if isinstance(trame, str):
                    trame = trame.encode("utf-8")
                self.socket.sendto(trame, (ip_dest, self.port_dest))
                print(f"[UDP] → {ip_dest}:{self.port_dest}  {trame[:60]}")
        except Exception as e:
            print(f"[UDP] Erreur envoi : {e}")

    def envoyer_broadcast(self, trame, port=None):
        """
        Envoie en broadcast (mode local uniquement).
        En mode distant, redirige vers envoyer() avec ip_distante.
        """
        if self.mode == "distant":
            # Pas de broadcast hors LAN — on envoie directement
            self.envoyer(trame, self.ip_distante)
            return
        try:
            port = port or self.port_dest
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            if isinstance(trame, str):
                trame = trame.encode("utf-8")
            sock.sendto(trame, (self.broadcast, port))
            sock.close()
            print(f"[UDP] Broadcast → {self.broadcast}:{port}")
        except Exception as e:
            print(f"[UDP] Erreur broadcast : {e}")

    # ─────────────────────────────────────────────────────────
    # Utilitaires
    # ─────────────────────────────────────────────────────────

    def est_distant(self) -> bool:
        return self.mode == "distant"

    def ip_cible(self) -> str:
        """Retourne l'IP à cibler pour les envois directs."""
        if self.mode == "distant":
            return self.ip_distante
        return ""
