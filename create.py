#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess

'''
sert à générer plusieurs processus  'floconCommand.py' en même temps pour générer plus de floconss
(s'exécute uniquement en terminal de commande)
'''

if __name__ == '__main__':

    f = open(sys.argv[1] , 'r')
    ligne = f.readline()
    commands = []
    commande = []
    while ligne != '':
        commande = ['python' , 'floconCommand.py']
        commande += ligne.split(' ')
        commands.append(commande)
        ligne = f.readline()
    f.close()
    
    for command in commands:
        subprocess.Popen(command) 
    