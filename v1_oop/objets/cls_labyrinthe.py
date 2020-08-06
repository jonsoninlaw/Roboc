# -*-coding:utf-8 -*

class Labyrinthe:

    def __init__(self, chemin_lab, chemin_raz):

        self.carte = self._recup_lab(chemin_lab)
        self.sauvegarde = self._comparer_lab(chemin_lab, chemin_raz)


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


    def _comparer_lab(self, chemin_lab, chemin_raz):

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

        with open(chemin_lab, "r") as fichier:
            lab = fichier.read()
        with open(chemin_raz, "r") as fichier:
            lab_raz = fichier.read()
        if lab == lab_raz:
            return True
        else:
            return False


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