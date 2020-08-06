# -*-coding:utf-8 -*

import random

class Labyrinthe:

    def __init__(self, chemin_lab, chemin_raz):

        self.raz_lab(chemin_lab, chemin_raz)
        self.carte = self._recup_lab(chemin_lab)
        self.carte = self._creer_robot(self.carte)
        self.enregistrer_lab(self.carte, chemin_lab)
        self.carte = self._recup_lab(chemin_lab)


    def _recup_lab(self, chemin_lab):
    
        """
        Méthode interne permettant de retourner une carte de labyrinthe
        dans une variable sous forme de chaîne de caractères
        -
        chemin_lab : chemin d'accès relatif au fichier
                     contenant la carte de labyrinthe
        """

        with open(chemin_lab, "r") as fichier:
            lab = fichier.read()
        return lab


    def _creer_robot(self, carte):

        lab_lignes = carte.split("\n")
        test = False
        ligne = len(lab_lignes) - 1
        colonne = len(lab_lignes[0]) - 1
        while not test:
            ligne_robot = random.randint(1, ligne - 1)
            colonne_robot = random.randint(1, colonne - 1)
            if lab_lignes[ligne_robot][colonne_robot] == " ":
                test = True
                
        ligne_creation = list(lab_lignes[ligne_robot])
        ligne_creation[colonne_robot] = "X"
        lab_lignes[ligne_robot] = "".join(ligne_creation)
        lab = "\n".join(lab_lignes)
        return lab


    def modif_lab(self, lab, position_x, position_y, position_arr, porte):

        """
        Fonction qui modifie le labyrinthe en interchangeant
        la position de départ et d'arrivée du robot et replace
        une porte à la position de départ s'il y en avait une
        -
        lab :  chaîne de caractères contenant le labyrinthe
        position_x,
        position_y   : les coordonnées de position initiale
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
        ligne_dep = list(lab_lignes[position_y])
        ligne_arr = list(lab_lignes[position_arr[0]])

        # On cherche à savoir si la ligne de départ est
        # différente de la ligne d'arrivée pour savoir si
        # le robot se déplace verticalement ou horizontalement
        if ligne_arr != ligne_dep:
            ligne_arr[position_arr[1]] = "X"
            if porte == True:
                ligne_dep[position_x] = "."
            else:
                ligne_dep[position_x] = " "    
            lab_lignes[position_arr[0]] = "".join(ligne_arr)
            lab_lignes[position_y] = "".join(ligne_dep)
        else:
            ligne_arr[position_arr[1]] = "X"
            if porte == True:
                ligne_arr[position_x] = "."
            else:
                ligne_arr[position_x] = " "
            lab_lignes[position_arr[0]] = "".join(ligne_arr)
        
        # On regroupe les lignes modifiées sous forme de
        # chaîne de caractères
        lab = "\n".join(lab_lignes)

        return lab


    def enregistrer_lab(self, lab, chemin_lab):

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


    def raz_lab(self, chemin_lab, chemin_raz):

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


    def percer_mur(self, chemin_temp, lab, position_x, position_y, direction):

        ligne_porte = []
        lab_lignes = lab.split("\n")

        lab_temp = self._recup_lab(chemin_temp)
        lab_temp_lignes = lab_temp.split("\n")

        if direction.lower() == "n" and lab_lignes[position_y - 1][position_x] == "O":
            if position_y - 1 == 0:
                message = "\nIl est interdit de percer ce mur !"
            else:
                ligne_porte = list(lab_lignes[position_y - 1])
                ligne_porte[position_x] = "."
                lab_lignes[position_y - 1] = "".join(ligne_porte)
                message = "\nBravo, la voie est libre !"
                
                ligne_temp = list(lab_temp_lignes[position_y - 1])
                ligne_temp[position_x] = "."
                lab_temp_lignes[position_y - 1] = "".join(ligne_temp)

        elif direction.lower() == "s" and lab_lignes[position_y + 1][position_x] == "O":
            if position_y + 1 == len(lab_lignes) - 1:
                message = "\nIl est interdit de percer ce mur !"
            else:
                ligne_porte = list(lab_lignes[position_y + 1])
                ligne_porte[position_x] = "."
                lab_lignes[position_y + 1] = "".join(ligne_porte)
                message = "\nBravo, la voie est libre !"

                ligne_temp = list(lab_temp_lignes[position_y + 1])
                ligne_temp[position_x] = "."
                lab_temp_lignes[position_y + 1] = "".join(ligne_temp)

        elif direction.lower() == "e" and lab_lignes[position_y][position_x + 1] == "O":
            if position_x + 1 == len(lab_lignes[0]) - 1:
                message = "\nIl est interdit de percer ce mur !"
            else:
                ligne_porte = list(lab_lignes[position_y])
                ligne_porte[position_x + 1] = "."
                lab_lignes[position_y] = "".join(ligne_porte)
                message = "\nBravo, la voie est libre !"

                ligne_temp = list(lab_temp_lignes[position_y])
                ligne_temp[position_x + 1] = "."
                lab_temp_lignes[position_y] = "".join(ligne_temp)

        elif direction.lower() == "o" and lab_lignes[position_y][position_x - 1] == "O":
            if position_x - 1 == 0:
                message = "\nIl est interdit de percer ce mur !"
            else:
                ligne_porte = list(lab_lignes[position_y])
                ligne_porte[position_x - 1] = "."
                lab_lignes[position_y] = "".join(ligne_porte)
                message = "\nBravo, la voie est libre !"

                ligne_temp = list(lab_temp_lignes[position_y])
                ligne_temp[position_x - 1] = "."
                lab_temp_lignes[position_y] = "".join(ligne_temp)

        else :
            message = "\nIl n'y a aucun mur à percer !"

        message = message.encode()
        lab = "\n".join(lab_lignes)
        lab_temp = "\n".join(lab_temp_lignes)
        self.enregistrer_lab(lab_temp, chemin_temp)

        return lab, message


    def murer_porte(self, chemin_temp, lab, position_x, position_y, direction):

        ligne_porte = []
        lab_lignes = lab.split("\n")

        lab_temp = self._recup_lab(chemin_temp)
        lab_temp_lignes = lab_temp.split("\n")

        if direction.lower() == "n" and lab_lignes[position_y - 1][position_x] == ".":
            ligne_porte = list(lab_lignes[position_y - 1])
            ligne_porte[position_x] = "O"
            lab_lignes[position_y - 1] = "".join(ligne_porte)
            message = "\nVoilà, la porte est murée !"
            
            ligne_temp = list(lab_temp_lignes[position_y - 1])
            ligne_temp[position_x] = "O"
            lab_temp_lignes[position_y - 1] = "".join(ligne_temp)

        elif direction.lower() == "s" and lab_lignes[position_y + 1][position_x] == ".":
            ligne_porte = list(lab_lignes[position_y + 1])
            ligne_porte[position_x] = "O"
            lab_lignes[position_y + 1] = "".join(ligne_porte)
            message = "\nVoilà, la porte est murée !"
            
            ligne_temp = list(lab_temp_lignes[position_y + 1])
            ligne_temp[position_x] = "O"
            lab_temp_lignes[position_y + 1] = "".join(ligne_temp)

        elif direction.lower() == "e" and lab_lignes[position_y][position_x + 1] == ".":
            ligne_porte = list(lab_lignes[position_y])
            ligne_porte[position_x + 1] = "O"
            lab_lignes[position_y] = "".join(ligne_porte)
            message = "\nVoilà, la porte est murée !"

            ligne_temp = list(lab_temp_lignes[position_y])
            ligne_temp[position_x + 1] = "O"
            lab_temp_lignes[position_y] = "".join(ligne_temp)

        elif direction.lower() == "o" and lab_lignes[position_y][position_x - 1] == ".":
            ligne_porte = list(lab_lignes[position_y])
            ligne_porte[position_x - 1] = "O"
            lab_lignes[position_y] = "".join(ligne_porte)
            message = "\nVoilà, la porte est murée !"

            ligne_temp = list(lab_temp_lignes[position_y])
            ligne_temp[position_x - 1] = "O"
            lab_temp_lignes[position_y] = "".join(ligne_temp)

        else :
            message = "\nIl n'y a aucune porte à murer !"

        message = message.encode()
        lab = "\n".join(lab_lignes)
        lab_temp = "\n".join(lab_temp_lignes)
        self.enregistrer_lab(lab_temp, chemin_temp)

        return lab, message