from send_email import send_alert_email, send_unusual_login_email, send_password_change_code_email
from datetime import datetime

if __name__ == '__main__':
    recipient = input("Entrez l'adresse email du destinataire : ")
    user_name = input("Entrez le nom de l'utilisateur : ")

    print("\nChoisissez le type de mail à envoyer :")
    print("1. Tentative de connexion à haut risque")
    print("2. Connexion détectée depuis un appareil ou pays inhabituel")
    print("3. Code de confirmation pour le changement de mot de passe")

    choice = input("\nEntrez le numéro du mail à envoyer (1/2/3) : ")

    if choice == "1":
        device = input("Entrez le nom de l'appareil : ")
        location = input("Entrez la localisation : ")
        send_alert_email(recipient, user_name, device, location)

    elif choice == "2":
        device = input("Entrez le nom de l'appareil : ")
        location = input("Entrez la localisation : ")
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_unusual_login_email(recipient, user_name, device, location)

    elif choice == "3":
        send_password_change_code_email(recipient, user_name)

    else:
        print("Choix invalide. Veuillez relancer le programme.")