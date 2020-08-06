# -*-coding:utf-8 -*

import socket
hote = ""
port = 12800

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
connexion_avec_client, infos_connexion = connexion_principale.accept()

msg_recu = b""


import os
import time
from objets.cls_robot import *
from objets.cls_labyrinthe import *

continuer = True
directions = ("n", "N", "s", "S", "e", "E", "o", "O")

# Début de la boucle principale
# ---------------------------------------------------------------------------------------------------

while continuer:
    
    choix_labyrinthe = 0    # Le numéro de labyrinthe choisi par le joueur
    numero_carte = 0        # Variable comptant le nombre de cartes disponibles
    index_cartes = []       # Liste contenant les numéros des cartes disponibles

    # On récupère les noms des fichiers de cartes
    # et on les affiche sous forme de liste numérotée
    cartes = list(os.listdir("cartes"))
    connexion_avec_client.send(b"\nLabyrinthes existants:")
    for element in cartes:
        numero_carte += 1
        envoi = "\n  {0} - {1}".format(numero_carte, element[:-4]).encode()
        connexion_avec_client.send(envoi)
        index_cartes.append(numero_carte)

    # On demande au joueur sur quel labyrinthe il souhaite jouer
    while choix_labyrinthe not in index_cartes:
        try:
            connexion_avec_client.send(b"\n\nEntrez un numero de labyrinthe pour commencer a jouer: ")
            time.sleep(0.5)
            connexion_avec_client.send(b"pret")
            choix_labyrinthe = int(connexion_avec_client.recv(1024).decode())
        except ValueError:
            envoi = "\nVous devez entrer un nombre compris entre 1 et {}".format(numero_carte).encode()
            connexion_avec_client.send(envoi)
            continue
        if choix_labyrinthe not in index_cartes:
            envoi = "\nVous devez entrer un nombre compris entre 1 et {}".format(numero_carte).encode()
            connexion_avec_client.send(envoi)

    # On définit le chemin d'accès au fichier de labyrinthe choisi dans 2 variables:
    # chemin_lab (labyrinthe en cours), chemin_raz (le même labyrinthe mais non modifié)
    chemin_lab = "cartes/{}".format(cartes[choix_labyrinthe - 1])
    chemin_temp = "cartes_temp/{}".format(cartes[choix_labyrinthe - 1])
    chemin_raz = "cartes_raz/{}".format(cartes[choix_labyrinthe - 1])

    # On crée un objet contenant le labyrinthe choisi
    labyrinthe = Labyrinthe(chemin_lab, chemin_raz)
    

    # Début du jeu
    # --------------------------------------------------------------------------------------------------

    victoire = False	# Variable indiquant si le joueur a trouvé la sortie
    porte = False		# Variable indiquant si une porte était présente sur la position du robot
    suivant = True		# Variable vérifiant si le robot doit continuer d'avancer

    # La variable etape_fin permet d'afficher le labyrinthe à chaque pas que fait le robot
    # lorsqu'on indique une distance supérieure à 1. Cette variable devient True lorsque
    # le robot arrive au bout de son déplacement.
    etape_fin = False

    # On explique les règles et les commandes au joueur
    regles = "\
\n- Le X represente votre robot, vous devez l'amener jusqu'a\
\n  la sortie representee par le U.\
\n- Les . sont des portes que vous pouvez traverser et les O\
\n  sont des murs que vous ne pouvez pas traverser.\
\n- Vous devez entrer une direction dans laquelle vous deplacer :\
\n  N pour Nord, S pour Sud, E pour Est, O pour Ouest.\
\n  Vous pouvez avancer plus vite en indiquant un nombre (exemple: N3).\
\n- Vous pouvez percer un mur en tapant P suivi d'une direction.\
\n- Vous pouvez murer une porte en tapant M suivi d'une direction.\
\n- Tapez Q pour quitter".encode()

    connexion_avec_client.send(regles)

    while not victoire:

        if not etape_fin:

        	# Tant que le robot ne s'est pas arrêté,
            # on ouvre le labyrinthe en cours et on l'affiche
            labyrinthe.carte = labyrinthe._recup_lab(chemin_lab)
            robot = Robot(labyrinthe.carte)
            lab_a_envoyer = "\n{}\n".format(labyrinthe.carte).encode()
            connexion_avec_client.send(lab_a_envoyer)

        if suivant:

        	# Tant que le robot ne s'est pas arrêté,
            # on demande au joueur dans quelle direction il souhaite aller
            # en anticipant d'éventuelles erreurs d'entrée
            connexion_avec_client.send(b"\nA vous de jouer (Tapez R pour afficher les regles): ")
            time.sleep(0.3)
            connexion_avec_client.send(b"pret")
            choix = connexion_avec_client.recv(1024).decode()
            
            if choix == "":
                connexion_avec_client.send(b"\nVous devez entrer quelque chose...")
                continue
            
            elif choix.upper() == "Q":
                connexion_avec_client.send(b"\nDeconnexion...")
                connexion_avec_client.close()
                connexion_principale.close()
                exit()
            
            elif choix.upper() == "R":
                connexion_avec_client.send(regles)
                continue
            
            elif choix[0].upper() == "P":
                if len(choix) != 2 or choix[1] not in directions:
                    connexion_avec_client.send(b"\nVous devez entrer P suivi d'une direction (N, S, E ou O).")
                else:
                    direction = choix[1]
                    percer = labyrinthe.percer_mur(chemin_temp, labyrinthe.carte, robot.x, robot.y, direction)
                    labyrinthe.carte = percer[0]
                    labyrinthe.enregistrer_lab(labyrinthe.carte, chemin_lab)
                    connexion_avec_client.send(percer[1])
                continue

            elif choix[0].upper() == "M":
                if len(choix) != 2 or choix[1] not in directions:
                    connexion_avec_client.send(b"\nVous devez entrer M suivi d'une direction (N, S, E ou O).")
                else:
                    direction = choix[1]
                    murer = labyrinthe.murer_porte(chemin_temp, labyrinthe.carte, robot.x, robot.y, direction)
                    labyrinthe.carte = murer[0]
                    labyrinthe.enregistrer_lab(labyrinthe.carte, chemin_lab)
                    connexion_avec_client.send(murer[1])
                continue

            direction = str(choix[0])
            if direction in directions:
                try:
                    if len(choix) > 1:
                        distance = int(choix[1:])
                    else:
                        distance = 1
                except ValueError:
                    connexion_avec_client.send(b"\nCette commande n'est pas reconnue.")
                    continue
            else:
                connexion_avec_client.send(b"\nCette commande n'est pas reconnue.")
                continue
            if distance == 0:
                connexion_avec_client.send(b"\nLe nombre de deplacement ne peut pas etre egal a 0")
                continue

            # On récupère les coordonnées de départ et d'arrivée du robot
            position_dep = [robot.y, robot.x]
            position_arr = robot.position_arrivee(robot.x, robot.y, direction, distance)

            # On initialise un cycle qui va déplacer le robot case par case
            # et afficher le labyrinthe après chaque déplacement
            etape = 0
            etape_fin = False
        
        if abs(distance) > 1 and etape != distance:
            if direction.upper() == "N":
                if suivant == False:
                    position_dep[0] -= 1
                position_arr[0] = position_dep[0] - 1
            elif direction.upper() == "S":
                if suivant == False:
                    position_dep[0] += 1
                position_arr[0] = position_dep[0] + 1
            elif direction.upper() == "E":
                if suivant == False:
                    position_dep[1] += 1
                position_arr[1] = position_dep[1] + 1
            elif direction.upper() == "O":
                if suivant == False:
                    position_dep[1] -= 1
                position_arr[1] = position_dep[1] - 1
            etape += 1
            suivant = False
        elif etape == distance:
            suivant = True
            etape_fin = True

        #import pdb; pdb.set_trace()

        # A chaque déplacement d'une case on vérifie que le robot
        # n'entre pas dans un mur
        position_ver = robot.verif_deplacement(labyrinthe.carte, position_arr, direction)
        if position_ver[0]:
            etape_fin = False
            suivant = True
            message = position_ver[2].encode()
            connexion_avec_client.send(message)
            continue
        elif position_ver[1]:
            victoire = True

        # On modifie la variable lab pour marquer la nouvelle position
        # du robot et remettre éventuellement une porte à l'ancienne position
        porte = robot.verif_porte(chemin_temp, robot.x, robot.y)
        labyrinthe.carte = labyrinthe.modif_lab(labyrinthe.carte, robot.x, robot.y, position_arr, porte)
        
        # On enregistre le labyrinthe dans le fichier en cours
        labyrinthe.enregistrer_lab(labyrinthe.carte, chemin_lab)

    # On affiche un smiley si le joueur a gagné
    with open("win.txt") as fichier:
        win = fichier.read()
    connexion_avec_client.send(win.encode())
    connexion_avec_client.send(b"\nFelicitations ! Vous avez gagne !")

connexion_avec_client.send(b"Deconnexion...")
connexion_avec_client.close()
connexion_principale.close()