from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
import os  # Import nécessaire pour utiliser os.path

# Import de l'instance `db` et `app` depuis app.py
from password_management.app import db, app
# Blueprint pour le changement de mot de passe
password_bp = Blueprint(
    'password_bp',
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '.'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static')
)

# Modèle pour les utilisateurs
class User(db.Model):
    __tablename__ = 'user'  # Nom explicite de la table
    __table_args__ = {'extend_existing': True}  # Autorise la redéfinition si nécessaire

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    old_password = db.Column(db.String(120), nullable=False)
    new_password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

@password_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        email = request.form['email']
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        # Utiliser le contexte d'application pour effectuer des opérations sur la base de données
        with app.app_context():
            new_user = User(email=email, old_password=old_password, new_password=new_password)
            db.session.add(new_user)
            db.session.commit()

        flash('Mot de passe mis à jour avec succès !', 'success')
        return redirect(url_for('password_bp.success'))

    return render_template('change_password.html')

@password_bp.route('/success')
def success():
    return render_template('success.html')