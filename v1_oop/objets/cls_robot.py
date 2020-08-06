# -*-coding:utf-8 -*

from objets.cls_obstacle import *

class Robot:

    def __init__(self, carte):

        position_dep = self._position_depart(carte)
        
        self.x = position_dep[1]
        self.y = position_dep[0]


    def _position_depart(self, carte):

        """
        Fonction qui vérifie la position de départ du robot
        et la renvoie sous forme de liste contenant les coordonnées
        -
        carte : chaîne de caractères contenant le labyrinthe
        """

        # On transforme chaque ligne du labyrinthe sous forme
        # d'élément de liste
        # puis on repère la position de départ du robot
        lab_lignes = carte.split("\n")
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


    def position_arrivee(self, position_x, position_y, direction, distance):

        """
        Fonction qui retourne la position d'arrivée du robot
        -
        position_x,
        position_y : coordonnées de départ du robot (tuple)
        direction  : chaîne de caractère contenant la direction
                     demandée par le joueur
        distance   : entier correspondant au nombre de cases que
                     doit parcourir le robot
        """

        # On détermine la position d'arrivée du robot
        # en fonction du choix du joueur
        # Verticalement :
        if direction.upper() == "N":
            ligne_arrivee = position_y - distance
        elif direction.upper() == "S":
            ligne_arrivee = position_y + distance
        else:
            ligne_arrivee = position_y
        # Horizontalement :
        if direction.upper() == "E":
            colonne_arrivee = position_x + distance
        elif direction.upper() == "O":
            colonne_arrivee = position_x - distance
        else : colonne_arrivee = position_x

        return [ligne_arrivee, colonne_arrivee]


    def verif_deplacement(self, carte, position_arr, direction):

        """
        Fonction qui vérifie que le déplacement demandé est possible
        Peut également retourner une erreur ou bien une victoire
        -
        carte :  chaîne de caractères contenant le labyrinthe
        position_arr : coordonnées d'arrivée du robot (tuple)
        direction : chaîne de caractère contenant la direction
                    demandée par le joueur
        """

        # Initialisation des variables
        lab_lignes = carte.split("\n")
        ligne_arr = position_arr[0]
        colonne_arr = position_arr[1]
        erreur = False
        victoire = False

        # Pour chaque direction possible :
        # Si on rencontre un mur (O), on indique une erreur
        # et on propose de recommencer
        # Si on rencontre la sortie (U), c'est gagné

        if direction.upper() in "NSEO":
            try:
                obstacle = Obstacle(lab_lignes[ligne_arr][colonne_arr])
                if obstacle.passage == False:
                    print("\nVous ne pouvez pas aller plus loin !")
                    erreur = True                
                elif obstacle.victoire == True:
                    victoire = True
            except IndexError:
                pass

        return erreur, victoire


    def verif_porte(self, chemin_raz, position_x, position_y):

        """
        Fonction appelée lors de la reprise d'une
        partie déjà commencée qui vérifie si une
        porte était présente sur la position du robot
        dans le labyrinthe d'origine
        -
        chemin_raz : chemin relatif du labyrinthe choisi
                     d'origine
        position_x,
        position_y : les coordonnées de position initiale
                       du robot (tuple)
        """

        with open(chemin_raz, "r") as fichier:
            lab = fichier.read()
        lab_lignes = lab.split("\n")
        if lab_lignes[position_y][position_x] == ".":
            return True
        else:
            return False