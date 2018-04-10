from multiprocessing.pool import ThreadPool
import sys
import os
import subprocess

def startCommand(command):
    subprocess.call(command , cwd =os.getcwd() , shell=True)



if __name__ == '__main__':

    f = open(sys.argv[1] , 'r')
    #f = open('test.txt' , 'r')
    ligne = f.readline()
    commands = []
    commande = []
    while ligne != '':
        commande = ['python' , 'floconCommand.py']
        commande += ligne.split(' ')
        commands.append(commande)
        ligne = f.readline()
    f.close()
    res = ThreadPool().map(startCommand, commands)
    #startCommand(commands[0])