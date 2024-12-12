from flask import Blueprint, redirect, request
from datetime import datetime
import sqlite3
import os

# Créer un blueprint pour le suivi des e-mails
track_email_bp = Blueprint('track_email_bp', __name__)

# Chemin relatif vers la base de données SQLite
DB_PATH = os.path.join(os.getcwd(), "users.db")

# Route pour le pixel de suivi avec un identifiant d'e-mail
@track_email_bp.route('/track-email/<email>')
def track_email(email):
    try:
        # Se connecter à la base de données SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Créer la table si elle n'existe pas déjà
        cursor.execute('''CREATE TABLE IF NOT EXISTS email_opens (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT NOT NULL,
                            opened_at DATETIME NOT NULL,
                            ip_address TEXT NOT NULL
                          )''')

        # Insérer les informations de suivi dans la base de données
        cursor.execute('INSERT INTO email_opens (email, opened_at, ip_address) VALUES (?, ?, ?)',
                       (email, datetime.utcnow(), request.remote_addr))

        # Valider les changements et fermer la connexion
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du suivi : {e}")
    finally:
        conn.close()

    # Rediriger vers l'image transparente hébergée en ligne
    return redirect("https://i.postimg.cc/JhrJF9X6/pixel-transparent.png")