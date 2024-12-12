import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD

# Fonction pour obtenir la date et l'heure actuelles
def get_current_date_time():
    """Retourne la date et l'heure actuelle sous forme de chaîne formatée."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_alert_email(recipient_email, user_name, device, location):
    template_path = os.path.join(os.path.dirname(__file__), "alert_login.html")
    send_email(recipient_email, template_path, {
        "{{ user_name }}": user_name,
        "{{ device }}": device,
        "{{ location }}": location,
        "{{ date_time }}": get_current_date_time()
    }, "Action requise : tentative de connexion à haut risque")

def send_unusual_login_email(recipient_email, user_name, device, location):
    template_path = os.path.join(os.path.dirname(__file__), "alert_unusual_login.html")
    send_email(recipient_email, template_path, {
        "{{ user_name }}": user_name,
        "{{ device }}": device,
        "{{ location }}": location,
        "{{ date_time }}": get_current_date_time()
    }, "Connexion inhabituelle détectée")

def send_password_change_code_email(recipient_email, user_name):
    template_path = os.path.join(os.path.dirname(__file__), "password_change_code.html")
    send_email(recipient_email, template_path, {
        "{{ user_name }}": user_name
    }, "Code de confirmation pour le changement de mot de passe")

def send_email(recipient_email, template_file, replacements, subject):
    with open(template_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    for key, value in replacements.items():
        html_content = html_content.replace(key, value)

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = f"Qonto.com <{EMAIL_ADDRESS}>"
    msg['To'] = recipient_email

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
            print(f"Email envoyé avec succès à {recipient_email} !")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")