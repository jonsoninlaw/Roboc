import socket

hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

msg_a_envoyer = ""
while msg_a_envoyer != b"fin":

    msg_recu = connexion_avec_serveur.recv(1024)
    msg_recu = msg_recu.decode()
    if msg_recu == "pret":
        msg_a_envoyer = input("> ")
    else:
        print(msg_recu)
        continue
    # Peut planter si vous tapez des caractères spéciaux
    if msg_a_envoyer == "":
        continue
    msg_a_envoyer = msg_a_envoyer.encode()
    # On envoie le message
    connexion_avec_serveur.send(msg_a_envoyer)

print("Fermeture de la connexion")
connexion_avec_serveur.close()