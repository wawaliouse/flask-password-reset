from flask import Flask, send_from_directory, redirect, url_for
import os
import importlib.util
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'  # Nécessaire pour les messages flash

# Chemin du répertoire courant de l'application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Configuration de la base de données SQLite avec un chemin relatif
DB_PATH = os.path.join(BASE_DIR, 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données avec l'application Flask
db = SQLAlchemy()
db.init_app(app)

# Charger le module `change_password.py` depuis un chemin relatif
change_password_path = os.path.join(BASE_DIR, 'change_password.py')
spec = importlib.util.spec_from_file_location("change_password", change_password_path)
change_password = importlib.util.module_from_spec(spec)
spec.loader.exec_module(change_password)

# Importer le blueprint depuis le module chargé
password_bp = change_password.password_bp
app.register_blueprint(password_bp)

# Charger le module `track_email.py` depuis un chemin relatif
track_email_path = os.path.join(BASE_DIR, 'track_email.py')
track_spec = importlib.util.spec_from_file_location("track_email", track_email_path)
track_email = importlib.util.module_from_spec(track_spec)
track_spec.loader.exec_module(track_email)

# Importer le blueprint depuis le module chargé
track_email_bp = track_email.track_email_bp
app.register_blueprint(track_email_bp)

# Route pour servir le fichier styles.css avec un chemin relatif
@app.route('/styles.css')
def serve_css():
    return send_from_directory(os.path.join(BASE_DIR, 'password_management'), 'styles.css')

# Route de base pour rediriger vers la page de changement de mot de passe
@app.route('/')
def home():
    return redirect(url_for('password_bp.change_password'))

# Créer les tables si elles n'existent pas déjà
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)