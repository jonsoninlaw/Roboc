# -*-coding:utf-8 -*

from fonctions import *
import os

continuer = True        # Variable autorisant à continuer la partie

# Liste des directions autorisées
dir_possible = ("n", "N", "s", "S", "e", "E", "o", "O")


# Début de la boucle principale
# ------------------------------------------------------------

while continuer:
    
    choix_lab = 0           # Le numéro de labyrinthe choisi par le joueur
    num_carte = 0           # Variable comptant le nombre de cartes disponibles
    index_cartes = []       # Liste contenant les numéros des cartes disponibles

    # On récupère les noms des fichiers de cartes
    # et on les affiche sous forme de liste numérotée
    cartes = list(os.listdir("cartes"))
    print("\nLabyrinthes existants:")
    for element in cartes:
        num_carte += 1
        print("  {0} - {1}".format(num_carte, element[:-4]))
        index_cartes.append(num_carte)

    # On demande au joueur sur quel labyrinthe il souhaite jouer
    while choix_lab not in index_cartes:
        try:
            choix_lab = int(input("\nEntrez un numéro de labyrinthe pour commencer à jouer: "))
        except ValueError:
            print("\nVous devez entrer un nombre compris entre 1 et {}".format(num_carte))
            continue
        if choix_lab not in index_cartes:
            print("\nVous devez entrer un nombre compris entre 1 et {}".format(num_carte))

    # On définit le chemin d'accès au fichier de labyrinthe choisi dans 2 variables:
    # chemin_lab (labyrinthe en cours), chemin_raz (le même labyrinthe mais non modifié)
    chemin_lab = "cartes/{}".format(cartes[choix_lab - 1])
    chemin_raz = "cartes_raz/{}".format(cartes[choix_lab - 1])

    # On vérifie si une partie est en cours et on propose au joueur de la continuer
    # S'il ne souhaite pas la continuer le labyrinthe est Remis A Zéro
    if not comparer_lab(chemin_lab, chemin_raz):
        raz = ""
        while raz not in ("o", "O", "n", "N"):
            raz = input("\nUne partie est en cours sur ce labyrinthe.\nSouhaitez-vous la continuer ? (O/N) : ")
        if raz.upper() == "N":
            raz_lab(chemin_lab, chemin_raz)
    

    # Début du jeu
    # ------------------------------------------------------------

    victoire = False
    porte = False

    # On explique les règles et les commandes au joueur
    print("\n- Le X représente votre robot, vous devez l'amener jusqu'à\n\
la sortie représentée par le U.\n\n\
- Les . sont des portes que vous pouvez traverser et les O\n\
sont des murs que vous ne pouvez pas traverser.\n\n\
- Vous devez entrer une direction dans laquelle vous déplacer :\n\
N pour Nord, S pour Sud, E pour Est, O pour Ouest.\n\
Vous pouvez avancer plus vite en indiquant un nombre (exemple: N3).\n\n\
- Si vous quittez, la partie sera automatiquement sauvegardée.")

    while not victoire:

        # On ouvre le labyrinthe en cours et on l'affiche
        lab = recup_lab(chemin_lab)
        print("\n" + lab)

        # On demande au joueur dans quelle direction il souhaite aller
        # en anticipant d'éventuelles erreurs d'entrée
        choix = input("\nChoisissez une direction (ou Q pour quitter): ")
        if choix == "":
            print("\nVous devez entrer un point cardinal et éventuellement un nombre de déplacements\
                    \nPar exemple: N3")
            continue
        elif choix.upper() == "Q":
            exit()
        direction = choix[0]
        if direction in dir_possible:
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

        # On vérifie que le déplacement choisi par le joueur est possible
        position_dep = position_depart(lab)
        position_arr = position_arrivee(lab, position_dep, direction, distance)
        position_ver = verif_deplacement(lab, position_dep, position_arr, direction)
        if position_ver[2]:
            continue
        elif position_ver[3]:
            victoire = True

        # On modifie la variable lab pour marquer la nouvelle position
        # du robot et remettre éventuellement une porte à l'ancienne position
        porte = verif_porte(chemin_raz, position_dep)
        lab = modif_lab(lab, position_dep, position_ver, porte)
        
        # On enregistre le labyrinthe dans le fichier en cours
        enregistrer_lab(lab, chemin_lab)

    # On affiche un smiley si le joueur a gagné
    with open("win.txt") as fichier:
        win = fichier.read()
    print("\n\n" + win)
    print("\nFélicitations ! Vous avez gagné !")
    raz_lab(chemin_lab, chemin_raz)