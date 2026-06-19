import sqlite3
import os
from datetime import datetime

class DataManager:
    def __init__(self, db_path="ihm_data.db"):
        self.db_path = db_path
        self.connexion = None
        self.initialiser_db()

    def initialiser_db(self):
        """Crée la base de données et les tables si elles n'existent pas"""
        self.connexion = sqlite3.connect(self.db_path, check_same_thread=False)
        curseur = self.connexion.cursor()

        # Table mesures
        curseur.execute('''
            CREATE TABLE IF NOT EXISTS mesures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capteur_id TEXT NOT NULL,
                type TEXT NOT NULL,
                valeur REAL,
                unite TEXT,
                timestamp INTEGER,
                date_heure TEXT
            )
        ''')

        # Table alarmes
        curseur.execute('''
            CREATE TABLE IF NOT EXISTS alarmes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capteur_id TEXT NOT NULL,
                type TEXT NOT NULL,
                message TEXT,
                severite TEXT,
                statut TEXT DEFAULT 'active',
                timestamp INTEGER,
                date_heure TEXT
            )
        ''')

        # Table commandes
        curseur.execute('''
            CREATE TABLE IF NOT EXISTS commandes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                commande TEXT NOT NULL,
                capteur_id TEXT,
                statut_ack TEXT,
                timestamp INTEGER,
                date_heure TEXT
            )
        ''')

        try:
            curseur.execute("ALTER TABLE mesures ADD COLUMN samples TEXT")
        except Exception:
            pass  # colonne déjà existante

        self.connexion.commit()
        print(f"Base de données initialisée : {self.db_path}")

    def sauvegarder_mesure(self, capteur_id, type_trame, valeur, unite, timestamp, samples=None):
        try:
            import json
            date_heure = datetime.fromtimestamp(timestamp / 1000 if timestamp > 1e10 else timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            samples_json = json.dumps(samples) if samples is not None else None
            curseur = self.connexion.cursor()
            curseur.execute('''
                INSERT INTO mesures (capteur_id, type, valeur, unite, timestamp, date_heure, samples)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (capteur_id, type_trame, valeur, unite, timestamp, date_heure, samples_json))
            self.connexion.commit()
        except Exception as e:
            print(f"Erreur sauvegarde mesure : {e}")

    def sauvegarder_alarme(self, capteur_id, type_alarme, message, severite):
        """Sauvegarde une alarme dans la base"""
        try:
            timestamp = int(datetime.now().timestamp())
            date_heure = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            curseur = self.connexion.cursor()
            curseur.execute('''
                INSERT INTO alarmes (capteur_id, type, message, severite, statut, timestamp, date_heure)
                VALUES (?, ?, ?, ?, 'active', ?, ?)
            ''', (capteur_id, type_alarme, message, severite, timestamp, date_heure))
            self.connexion.commit()
        except Exception as e:
            print(f"Erreur sauvegarde alarme : {e}")

    def sauvegarder_commande(self, commande, capteur_id, statut_ack):
        """Sauvegarde une commande envoyée"""
        try:
            timestamp = int(datetime.now().timestamp())
            date_heure = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            curseur = self.connexion.cursor()
            curseur.execute('''
                INSERT INTO commandes (commande, capteur_id, statut_ack, timestamp, date_heure)
                VALUES (?, ?, ?, ?, ?)
            ''', (commande, capteur_id, statut_ack, timestamp, date_heure))
            self.connexion.commit()
        except Exception as e:
            print(f"Erreur sauvegarde commande : {e}")

    def charger_mesures(self, capteur_id=None, debut=None, fin=None):
        """Charge les mesures depuis la base avec filtres optionnels"""
        try:
            curseur = self.connexion.cursor()
            requete = "SELECT date_heure, valeur, unite, samples FROM mesures WHERE 1=1"
            params = []
            if capteur_id:
                requete += " AND capteur_id = ?"
                params.append(capteur_id)
            if debut:
                requete += " AND timestamp >= ?"
                params.append(debut)
            if fin:
                requete += " AND timestamp <= ?"
                params.append(fin)
            requete += " ORDER BY timestamp ASC"
            curseur.execute(requete, params)
            return curseur.fetchall()
        except Exception as e:
            print(f"Erreur chargement mesures : {e}")
            return []

    def charger_alarmes(self, severite=None, capteur_id=None):
        """Charge les alarmes depuis la base.
        Retourne des tuples : (id, date_heure, capteur_id, type, message, severite, statut)
        """
        try:
            curseur = self.connexion.cursor()
            requete = (
                "SELECT id, date_heure, capteur_id, type, message, severite, statut "
                "FROM alarmes WHERE 1=1"
            )
            params = []
            if severite:
                requete += " AND severite = ?"
                params.append(severite)
            if capteur_id:
                requete += " AND capteur_id = ?"
                params.append(capteur_id)
            requete += " ORDER BY timestamp DESC"
            curseur.execute(requete, params)
            return curseur.fetchall()
        except Exception as e:
            print(f"Erreur chargement alarmes : {e}")
            return []

    def acquitter_alarme(self, alarme_id):
        """Acquitte une alarme par son id DB"""
        try:
            curseur = self.connexion.cursor()
            curseur.execute(
                "UPDATE alarmes SET statut = 'acquittee' WHERE id = ?",
                (alarme_id,)
            )
            self.connexion.commit()
        except Exception as e:
            print(f"Erreur acquittement alarme : {e}")
        
    def purger_alarmes_acquittees(self):
        """Supprime de la base toutes les alarmes déjà acquittées."""
        try:
            curseur = self.connexion.cursor()
            curseur.execute("DELETE FROM alarmes WHERE statut = 'acquittee'")
            self.connexion.commit()
            print(f"Alarmes acquittées purgées : {curseur.rowcount} ligne(s) supprimée(s)")
        except Exception as e:
            print(f"Erreur purge alarmes : {e}")

    def acquitter_toutes(self):
        """Acquitte toutes les alarmes actives"""
        try:
            curseur = self.connexion.cursor()
            curseur.execute(
                "UPDATE alarmes SET statut = 'acquittee' WHERE statut = 'active'"
            )
            self.connexion.commit()
        except Exception as e:
            print(f"Erreur acquittement toutes alarmes : {e}")

    def fermer(self):
        """Ferme la connexion à la base"""
        if self.connexion:
            self.connexion.close()
            print("Base de données fermée")