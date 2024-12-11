from flask import Flask, send_from_directory
import os
from password_management.change_password import password_bp

app = Flask(__name__)
app.secret_key = 'secret_key'  # Nécessaire pour les messages flash

# Route pour servir le fichier styles.css
@app.route('/styles.css')
def serve_css():
    return send_from_directory(os.path.dirname(__file__), 'styles.css')

# Enregistrer le blueprint pour le changement de mot de passe
app.register_blueprint(password_bp)

if __name__ == '__main__':
    app.run(debug=True)