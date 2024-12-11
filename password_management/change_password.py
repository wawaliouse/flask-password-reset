from flask import Blueprint, render_template, request, redirect, url_for, flash
import json
import os

# Blueprint pour le changement de mot de passe
password_bp = Blueprint(
    'password_bp',
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '.'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static')
)

# Chemin vers le fichier JSON pour stocker les utilisateurs
USER_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'users.json')

# Charger les utilisateurs depuis le fichier JSON
def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return []
    with open(USER_DATA_FILE, 'r') as file:
        return json.load(file)

# Sauvegarder les utilisateurs dans le fichier JSON
def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

@password_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        email = request.form['email']
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        # Charger les utilisateurs existants
        users = load_users()

        # Ajouter les nouvelles informations
        users.append({
            "email": email,
            "old_password": old_password,
            "new_password": new_password
        })

        # Sauvegarder dans le fichier JSON
        save_users(users)

        flash('Mot de passe mis à jour avec succès !', 'success')
        return redirect(url_for('password_bp.success'))

    return render_template('change_password.html')

@password_bp.route('/success')
def success():
    return render_template('success.html')