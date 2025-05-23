import json
import os
from cryptography.fernet import Fernet

# Schlüssel generieren und speichern, wenn nicht vorhanden
def generate_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

# Schlüssel laden
def load_key():
    return open("key.key", "rb").read()

# Passwort speichern
def save_password(service, username, password):
    key = load_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())

    data = {}
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)

    data[service] = {"username": username, "password": encrypted.decode()}

    with open("passwords.json", "w") as file:
        json.dump(data, file)

# Passwort abrufen
def get_password(service):
    key = load_key()
    fernet = Fernet(key)

    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
            if service in data:
                username = data[service]["username"]
                encrypted = data[service]["password"]
                password = fernet.decrypt(encrypted.encode()).decode()
                print(f"Service: {service}\nUsername: {username}\nPassword: {password}")
                return
    print("Service nicht gefunden.")

# Hauptmenü
def main():
    generate_key()
    while True:
        print("\n1. Passwort speichern\n2. Passwort anzeigen\n3. Beenden")
        choice = input("Wähle eine Option: ")

        if choice == "1":
            service = input("Dienstname: ")
            username = input("Benutzername: ")
            password = input("Passwort: ")
            save_password(service, username, password)
        elif choice == "2":
            service = input("Dienstname zum Suchen: ")
            get_password(service)
        elif choice == "3":
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()
