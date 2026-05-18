# -*- coding: utf-8 -*-
"""
RemoteWorker — remplace UDPWorker en mode distant.
- Commandes  : HTTP via FastAPI (requests)
- Données    : ZeroMQ SUB (streaming temps réel)
- Signaux    : identiques à UDPWorker pour que controller.py ne voit pas la différence
"""

import threading
import requests
import zmq
from PySide6.QtCore import QObject, Signal


class RemoteWorker(QObject):
    # ── Mêmes signaux que UDPWorker ──
    trame_recue    = Signal(object, str)
    ack_recu       = Signal(str, str)
    liaison_perdue = Signal(str)

    def __init__(self, ip_serveur: str, port_api: int = 8000, port_zmq: int = 5555):
        super().__init__()
        self.ip_serveur  = ip_serveur   # IP du PC serveur Smartacc
        self.port_api    = port_api     # Port FastAPI (commandes)
        self.port_zmq    = port_zmq     # Port ZeroMQ  (données)
        self.base_url    = f"http://{ip_serveur}:{port_api}"

        self._actif      = False
        self._thread_zmq = None

        # Attributs de compatibilité avec UDPWorker
        self.port_local  = port_api
        self.port_dest   = port_zmq
        self.broadcast   = ""
        self.mode        = "distant"
        self.ip_distante = ip_serveur

    # ─────────────────────────────────────────────────────────
    # Démarrage / arrêt
    # ─────────────────────────────────────────────────────────

    def demarrer(self):
        """Démarre l'écoute ZeroMQ dans un thread séparé."""
        self._actif      = True
        self._thread_zmq = threading.Thread(target=self._ecouter_zmq, daemon=True)
        self._thread_zmq.start()
        print(f"[REMOTE] Connecté au serveur {self.ip_serveur} — API:{self.port_api} ZMQ:{self.port_zmq}")

    def arreter(self):
        """Arrête l'écoute ZeroMQ."""
        self._actif = False
        print("[REMOTE] Arrêté")

    # ─────────────────────────────────────────────────────────
    # Écoute ZeroMQ (données temps réel)
    # ─────────────────────────────────────────────────────────

    def _ecouter_zmq(self):
        """Thread d'écoute ZeroMQ — reçoit les données audio en streaming."""
        ctx    = zmq.Context()
        socket = ctx.socket(zmq.SUB)
        socket.connect(f"tcp://{self.ip_serveur}:{self.port_zmq}")
        socket.setsockopt(zmq.SUBSCRIBE, b"")  # s'abonner à tous les topics
        socket.setsockopt(zmq.RCVTIMEO, 500)   # timeout 500ms pour pouvoir arrêter

        print(f"[ZMQ] Abonné à tcp://{self.ip_serveur}:{self.port_zmq}")

        while self._actif:
            try:
                data = socket.recv()
                # Paquet binaire MIC ?
                if len(data) > 10 and data[0] == 0x4D:
                    self.trame_recue.emit(data, self.ip_serveur)
                else:
                    trame = data.decode("utf-8").strip()
                    if trame.startswith("ACK"):
                        self.ack_recu.emit(trame, self.ip_serveur)
                    else:
                        self.trame_recue.emit(trame, self.ip_serveur)
            except zmq.Again:
                # Timeout — on continue la boucle
                continue
            except Exception as e:
                if self._actif:
                    print(f"[ZMQ] Erreur : {e}")
                break

        socket.close()
        ctx.term()
        print("[ZMQ] Thread arrêté")

    # ─────────────────────────────────────────────────────────
    # Envoi commandes via FastAPI (HTTP)
    # ─────────────────────────────────────────────────────────

    def envoyer(self, trame: str, ip_dest: str = ""):
        """
        Envoie une commande au serveur via HTTP POST.
        Compatible avec udp_worker.envoyer() — même signature.
        """
        threading.Thread(
            target=self._post_commande,
            args=(trame,),
            daemon=True
        ).start()

    def envoyer_broadcast(self, trame: str, port=None):
        """
        En mode distant le broadcast n'existe pas.
        On envoie directement au serveur via HTTP.
        """
        self.envoyer(trame)

    def _post_commande(self, trame: str):
        """Envoie la commande au serveur FastAPI en arrière-plan."""
        try:
            resp = requests.post(
                f"{self.base_url}/commande",
                json={"trame": trame},
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                ack  = data.get("ack", "")
                if ack:
                    self.ack_recu.emit(ack, self.ip_serveur)
                print(f"[HTTP] → {trame} | ← {ack}")
            else:
                print(f"[HTTP] Erreur {resp.status_code} pour : {trame}")
        except requests.exceptions.ConnectionError:
            print(f"[HTTP] Serveur inaccessible : {self.base_url}")
            self.liaison_perdue.emit(self.ip_serveur)
        except requests.exceptions.Timeout:
            print(f"[HTTP] Timeout pour : {trame}")
        except Exception as e:
            print(f"[HTTP] Erreur : {e}")

    # ─────────────────────────────────────────────────────────
    # Utilitaires (compatibilité UDPWorker)
    # ─────────────────────────────────────────────────────────

    def est_distant(self) -> bool:
        return True

    def ip_cible(self) -> str:
        return self.ip_serveur
