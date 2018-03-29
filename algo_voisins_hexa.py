def voisins_grille_hexa(grille,coord):
    """
        Renvoie la liste ordonnée des voisins de la cellule de coordonées coord dans une grille hexagonale.
        :param grille: (list)
        :param coord: (tuple)
        :return: (list)
        
        CU :
        - les valeurs de coord doivent être positives ou nulles
        - la celulle doit se trouver dans la grille
        
        Exemples :
        >>> voisins_grille_hexa(generation_grille(4,5,0),(1,1))
        [(0, 1), (0, 2), (1, 0), (1, 2), (2, 1), (2, 2)]
        >>> voisins_grille_hexa(generation_grille(4,5,0),(0,0))
        [(0, 1), (1, 0)]
        >>> voisins_grille_hexa(generation_grille(3,5,0),(2,0))
        [(1, 0), (2, 1)]
    """
    voisins = []
    if coord[0] < 0 :
        ligne = len(grille) + coord[0]
    else :
        ligne = coord[0]
    if coord[1] < 0 :
        colonne = len(grille[0]) + coord[1]
    else :
        colonne = coord[1]
    ligne_max, colonne_max = len(grille)-1, len(grille[0])-1
    if ligne > ligne_max or colonne > colonne_max :
        print("La cellule est en dehors de la grille.")
        return []
    condition = {"non_haut" : ligne > 0, "non_bas" : ligne < ligne_max, "non_droit" : colonne < colonne_max,"non_gauche" : colonne > 0, "pair" : ligne % 2 == 1, "impair" : ligne % 2 == 0, "grille_pair" : ligne_max % 2 == 1, "grille_impair" : ligne_max % 2 == 0}
    if condition["non_droit"] :
        voisins += [(ligne,colonne+1)]
    if condition["non_gauche"] :
        voisins += [(ligne,colonne-1)]
    if condition["non_bas"] :
        voisins += [(ligne+1,colonne)]
    if condition["non_haut"] :
        voisins += [(ligne-1,colonne)]
    if condition["grille_pair"] :
        if condition["pair"] :
            if condition["non_droit"] :
                if condition["non_haut"] :
                    voisins += [(ligne-1, colonne+1)]
                if condition["non_bas"] :
                    voisins += [(ligne+1, colonne+1)]
        else :
            if condition["non_gauche"] :
                if condition["non_haut"] :
                    voisins += [(ligne-1, colonne-1)]
                if condition["non_bas"] :
                    voisins += [(ligne+1, colonne-1)]
    else :
        if condition["pair"] :
            if condition["non_droit"] :
                voisins += [(ligne-1, colonne+1),(ligne+1, colonne+1)]
        else :
            if condition["non_gauche"] :
                if condition["non_haut"] :
                    voisins += [(ligne-1, colonne-1)]
                if condition["non_bas"] :
                    voisins += [(ligne+1, colonne-1)]
    for i in range(len(voisins)):
        voisins[i]= (voisins[i][1] , voisins[i][0]) 
        
    return sorted(voisins)

def etat_cellule(grille,coord):
    """
        Renvoie le contenu de la cellule dont les coordonées sont passées en paramètre.
        :param grille: (list)
        :param coord: (tuple)
        :return: (any)
        
        CU : les coordonéees doivent correspondre à une cellule de la grille
        
        Exemple :
        >>> etat_cellule(generation_grille(4,5,0),(1,1))
        0
        >>> etat_cellule([[0,0],[0,5],[0,0]],(1,1))
        5
        >>> etat_cellule(generation_grille(4,5,0),(5,1))
        Cellule invalide.
    """
    try :
        return grille[coord[0]][coord[1]]
    except IndexError:
        print("Cellule invalide.")
        

if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,verbose=True)