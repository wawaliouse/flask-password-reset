import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD

def send_alert_email(recipient_email, user_name, device, location):
    """
    Envoie un email d'alerte en utilisant le template HTML.
    """
    # Charger le contenu du template HTML depuis le fichier
    with open("alert_email.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    # Remplacer les variables dynamiques dans le template
    html_content = html_content.replace("{{ user_name }}", user_name)
    html_content = html_content.replace("{{ device }}", device)
    html_content = html_content.replace("{{ location }}", location)

    # Créer le message email
    msg = MIMEMultipart("alternative")
    msg['Subject'] = f"Action requise : tentative de connexion depuis {location}"
    msg['From'] = f"Qonto.com <{EMAIL_ADDRESS}>"
    msg['To'] = recipient_email

    # Attacher le contenu HTML
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
            print(f"Email d'alerte envoyé avec succès à {recipient_email} !")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")