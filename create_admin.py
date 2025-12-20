import json
from werkzeug.security import generate_password_hash

username = input("Nom d'utilisateur admin : ")
password = input("Mot de passe : ")

with open("admin.json", "r") as f:
    users = json.load(f)

users[username] = {
    "password": generate_password_hash(password)
}

with open("admin.json", "w") as f:
    json.dump(users, f, indent=4)

print("✅ Compte admin créé avec succès")
