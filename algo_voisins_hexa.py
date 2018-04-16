#!/usr/bin/env python
# -*- coding: utf-8 -*-

def voisins_grille_hexa(grille,coord):
    """
        Renvoie la liste ordonnée des voisins de la cellule de coordonées coord dans une grille hexagonale.
        :param grille: (list)
        :param coord: (tuple)
        :return: (list)
        
        CU :
        - les valeurs de coord doivent être positives ou nulles
        - la cellule doit se trouver dans la grille
        
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