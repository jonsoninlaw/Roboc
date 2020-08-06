# -*-coding:utf-8 -*

"""
Module contenant les fonctions nécessaires
à l'exécution du jeu Roboc
"""

def recup_lab(chemin_lab):

    """
    Fonction permettant de retourner une carte de labyrinthe
    dans une variable sous forme de chaîne de caractères
    -
    chemin_lab : chemin d'accès relatif au fichier
                 contenant la carte de labyrinthe
    """

    with open(chemin_lab, "r") as fichier:
        lab = fichier.read()
    return lab


def comparer_lab(chemin_lab, chemin_raz):

    """
    Fonction permettant de comparer le dernier labyrinthe
    enregistré avec celui d'origine
    Retourne True si les 2 labyrinthes sont identiques
    -
    chemin_lab : chemin d'accès relatif au fichier
                 labyrinthe en cours
    chemin_raz : chemin d'accès relatif au fichier
                 labyrinthe d'orogine
    """

    lab = recup_lab(chemin_lab)
    with open(chemin_raz, "r") as fichier:
        lab_raz = fichier.read()
    if lab == lab_raz:
        return True
    else:
        return False


def position_depart(lab):

    """
    Fonction qui vérifie la position de départ du robot
    et la renvoie sous forme de liste contenant les coordonnées
    -
    lab : chaîne de caractères contenant le labyrinthe
    """

    # On transforme chaque ligne du labyrinthe sous forme
    # d'élément de liste
    # puis on repère la position de départ du robot
    lab_lignes = lab.split("\n")
    compteur = 0
    for element in lab_lignes:
        if "X" in element:
            ligne_depart = compteur
        else:
            compteur += 1
    compteur = 0
    for element in lab_lignes[ligne_depart]:
        if "X" in element:
            colonne_depart = compteur
        else:
            compteur += 1

    return [ligne_depart, colonne_depart]


def position_arrivee(lab, position_dep, direction, distance):

    """
    Fonction qui retourne la position d'arrivée du robot
    -
    lab :  chaîne de caractères contenant le labyrinthe
    position_dep : coordonnées de départ du robot (tuple)
    direction : chaîne de caractère contenant la direction
                demandée par le joueur
    distance : entier correspondant au nombre de cases que
               doit parcourir le robot
    """

    # On détermine la position d'arrivée du robot
    # en fonction du choix du joueur
    # Verticalement :
    if direction.upper() == "N":
        ligne_arrivee = position_dep[0] - distance
    elif direction.upper() == "S":
        ligne_arrivee = position_dep[0] + distance
    else:
        ligne_arrivee = position_dep[0]
    # Horizontalement :
    if direction.upper() == "E":
        colonne_arrivee = position_dep[1] + distance
    elif direction.upper() == "O":
        colonne_arrivee = position_dep[1] - distance
    else : colonne_arrivee = position_dep[1]

    return [ligne_arrivee, colonne_arrivee]


def verif_deplacement(lab, position_arr, direction):

    """
    Fonction qui vérifie que le déplacement demandé est possible
    Peut également retourner une erreur ou bien une victoire
    -
    lab :  chaîne de caractères contenant le labyrinthe
    position_arr : coordonnées d'arrivée du robot (tuple)
    direction : chaîne de caractère contenant la direction
                demandée par le joueur
    """

    # Initialisation des variables
    lab_lignes = lab.split("\n")
    ligne_arr = position_arr[0]
    colonne_arr = position_arr[1]
    erreur = False
    victoire = False

    # Pour chaque direction possible :
    # Si on rencontre un mur (O), on indique une erreur
    # et on propose de recommencer
    # Si on rencontre la sortie (U), c'est gagné

    # Direction Nord (N)
    if direction.upper() == "N":
        try:
            if lab_lignes[ligne_arr][colonne_arr] == "O":
                print("\nVous ne pouvez pas aller plus loin !")
                erreur = True                
            elif lab_lignes[ligne_arr][colonne_arr] == "U":
                victoire = True
        except IndexError:
            pass
        
    # Direction Sud (S)
    elif direction.upper() == "S":
        try:
            if lab_lignes[ligne_arr][colonne_arr] == "O":
                print("\nVous ne pouvez pas aller plus loin !")
                erreur = True
            elif lab_lignes[ligne_arr][colonne_arr] == "U":
                victoire = True
        except IndexError:
            pass

    # Direction Est (E)
    elif direction.upper() == "E":
        try:
            if lab_lignes[ligne_arr][colonne_arr] == "O":
                print("\nVous ne pouvez pas aller plus loin !")
                erreur = True
            elif lab_lignes[ligne_arr][colonne_arr] == "U":
                victoire = True
        except IndexError:
            pass

    # Direction Ouest (O)
    elif direction.upper() == "O":
        try:
            if lab_lignes[ligne_arr][colonne_arr] == "O":
                print("\nVous ne pouvez pas aller plus loin !")
                erreur = True
            elif lab_lignes[ligne_arr][colonne_arr] == "U":
                victoire = True
        except IndexError:
            pass

    return erreur, victoire


def verif_porte(chemin_raz, position_dep):

    """
    Fonction appelée lors de la reprise d'une
    partie déjà commencée qui vérifie si une
    porte était présente sur la position du robot
    dans le labyrinthe d'origine
    -
    chemin_raz : chemin relatif du labyrinthe choisi
                 d'origine
    position_dep : les coordonnées de position initiale
                   du robot (tuple)
    """

    with open(chemin_raz, "r") as fichier:
        lab = fichier.read()
    lab_lignes = lab.split("\n")
    if lab_lignes[position_dep[0]][position_dep[1]] == ".":
        return True
    else:
        return False


def modif_lab(lab, position_dep, position_arr, porte):

    """
    Fonction qui modifie le labyrinthe en interchangeant
    la position de départ et d'arrivée du robot et replace
    une porte à la position de départ s'il y en avait une
    -
    lab :  chaîne de caractères contenant le labyrinthe
    position_dep : les coordonnées de position initiale
                   du robot (tuple)
    position_ver : les coordonnées de position d'arrivée
                   du robot vérifiée par la fonction
                   verif_deplacement() (tuple)
    porte : booléen indiquand si une porte était présente
            sur la position de départ
    """

    # On convertit les lignes de départ et d'arrivée
    # du labyrinthe en listes indexables
    lab_lignes = lab.split("\n")
    ligne_dep = list(lab_lignes[position_dep[0]])
    ligne_arr = list(lab_lignes[position_arr[0]])

    # On cherche à savoir si la ligne de départ est
    # différente de la ligne d'arrivée pour savoir si
    # le robot se déplace verticalement ou horizontalement
    if ligne_arr != ligne_dep:
        ligne_arr[position_arr[1]] = "X"
        if porte == True:
            ligne_dep[position_dep[1]] = "."
        else:
            ligne_dep[position_dep[1]] = " "    
        lab_lignes[position_arr[0]] = "".join(ligne_arr)
        lab_lignes[position_dep[0]] = "".join(ligne_dep)
    else:
        ligne_arr[position_arr[1]] = "X"
        if porte == True:
            ligne_arr[position_dep[1]] = "."
        else:
            ligne_arr[position_dep[1]] = " "
        lab_lignes[position_arr[0]] = "".join(ligne_arr)
    
    # On regroupe les lignes modifiées sous forme de
    # chaîne de caractères
    lab = "\n".join(lab_lignes)

    return lab


def enregistrer_lab(lab, chemin_lab):

    """
    Fonction destinée à enregistrer le labyrinthe en cours
    dans le fichier correspondant
    -
    lab :  chaîne de caractères contenant le labyrinthe
    chemin_lab : chemin d'accès relatif au fichier
                 labyrinthe en cours
    """

    with open(chemin_lab, "w") as fichier:
        fichier.write(lab)


def raz_lab(chemin_lab, chemin_raz):

    """
    Fonction qui réinitialise le labyrinthe dans sa
    configuration d'origine
    -
    chemin_lab : chemin d'accès relatif au fichier
                 labyrinthe en cours
    chemin_raz : chemin relatif du labyrinthe choisi
                 d'origine
    """

    with open(chemin_raz, "r") as fichier:
        lab = fichier.read()
    with open(chemin_lab, "w") as fichier:
        fichier.write(lab)