# -*-coding:utf-8 -*

import os
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
    print("\nLabyrinthes existants:")
    for element in cartes:
        numero_carte += 1
        print("  {0} - {1}".format(numero_carte, element[:-4]))
        index_cartes.append(numero_carte)

    # On demande au joueur sur quel labyrinthe il souhaite jouer
    while choix_labyrinthe not in index_cartes:
        try:
            choix_labyrinthe = int(input("\nEntrez un numéro de labyrinthe pour commencer à jouer: "))
        except ValueError:
            print("\nVous devez entrer un nombre compris entre 1 et {}".format(numero_carte))
            continue
        if choix_labyrinthe not in index_cartes:
            print("\nVous devez entrer un nombre compris entre 1 et {}".format(numero_carte))

    # On définit le chemin d'accès au fichier de labyrinthe choisi dans 2 variables:
    # chemin_lab (labyrinthe en cours), chemin_raz (le même labyrinthe mais non modifié)
    chemin_lab = "cartes/{}".format(cartes[choix_labyrinthe - 1])
    chemin_raz = "cartes_raz/{}".format(cartes[choix_labyrinthe - 1])
    
    # On crée un objet contenant le labyrinthe choisi
    labyrinthe = Labyrinthe(chemin_lab, chemin_raz)

    # On vérifie si une partie est en cours et on propose au joueur de la continuer
    # S'il ne souhaite pas la continuer le labyrinthe est Remis A Zéro
    if not labyrinthe.sauvegarde:
        raz = ""
        while raz not in ("o", "O", "n", "N"):
            raz = input("\nUne partie est en cours sur ce labyrinthe.\nSouhaitez-vous la continuer ? (O/N) : ")
        if raz.upper() == "N":
            labyrinthe.raz_lab(chemin_lab, chemin_raz)
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
    print("\n- Le X représente votre robot, vous devez l'amener jusqu'à")
    print("la sortie représentée par le U.")
    print("- Les . sont des portes que vous pouvez traverser et les O")
    print("sont des murs que vous ne pouvez pas traverser.")
    print("- Vous devez entrer une direction dans laquelle vous déplacer :")
    print("N pour Nord, S pour Sud, E pour Est, O pour Ouest.")
    print("Vous pouvez avancer plus vite en indiquant un nombre (exemple: N3).")
    print("- Si vous quittez, la partie sera automatiquement sauvegardée.")

    while not victoire:

        if not etape_fin:

        	# Tant que le robot ne s'est pas arrêté,
            # on ouvre le labyrinthe en cours et on l'affiche
            labyrinthe.carte = labyrinthe._recup_lab(chemin_lab)
            robot = Robot(labyrinthe.carte)
            print("\n" + labyrinthe.carte)

        if suivant:

        	# Tant que le robot ne s'est pas arrêté,
            # on demande au joueur dans quelle direction il souhaite aller
            # en anticipant d'éventuelles erreurs d'entrée
            choix = input("\nChoisissez une direction (ou Q pour quitter): ")
            if choix == "":
                print("\nVous devez entrer un point cardinal et éventuellement un nombre de déplacements\
                        \nPar exemple: N3")
                continue
            elif choix.upper() == "Q":
                exit()
            direction = choix[0]
            if direction in directions:
                try:
                    if len(choix) > 1:
                        distance = int(choix[1:])
                    else:
                        distance = 1
                except ValueError:
                    print("\nVous devez entrer un point cardinal et éventuellement un nombre de déplacements\
                        \nPar exemple: N3")
                    continue
            else:
                print("\nVous devez entrer un point cardinal et éventuellement un nombre de déplacements\
                    \nPar exemple: N3")
                continue
            if distance == 0:
                print("\nLe nombre de déplacement ne peut pas être égal à 0")
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
            continue
        elif position_ver[1]:
            victoire = True

        # On modifie la variable lab pour marquer la nouvelle position
        # du robot et remettre éventuellement une porte à l'ancienne position
        porte = robot.verif_porte(chemin_raz, robot.x, robot.y)
        labyrinthe.carte = labyrinthe.modif_lab(labyrinthe.carte, robot.x, robot.y, position_arr, porte)
        
        # On enregistre le labyrinthe dans le fichier en cours
        labyrinthe.enregistrer_lab(labyrinthe.carte, chemin_lab)

    # On affiche un smiley si le joueur a gagné
    with open("win.txt") as fichier:
        win = fichier.read()
    print("\n\n" + win)
    print("\nFélicitations ! Vous avez gagné !")
    labyrinthe.raz_lab(chemin_lab, chemin_raz)