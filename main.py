from send_email import send_alert_email

if __name__ == '__main__':
    recipient = input("Entrez l'adresse email du destinataire : ")
    user_name = input("Entrez le nom de l'utilisateur : ")
    device = "iPhone 15 (iOS)"
    location = "Maroc"

    send_alert_email(recipient, user_name, device, location)