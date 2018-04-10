import sys
import random

if __name__=='__main__':
    width = '100'
    height= '100'
    loop='4'
    ecart='100'
    amount = '5'
    name = 'default.txt'
    arg = sys.argv
    continu =True
    if len(arg)>1:
        if arg[1]=='help':
            print("parametres:")
            print('\tw: longueur')
            print('\th: largeur')
            print('\trep: repetitions du copier-coller')
            print("\tloop: nombre de fois que l'on va exporter l'image en png")
            print("\tecart: ecart (en nombre d'etapes) entre chaque exportation")
            print('\tname: nom du fichier à exporter')
            continu=False
            
        else:
            for i in arg:
                if i.startswith('w'):
                    try:
                        width=i.split('=')[1]
                    except:
                        print("Valeur d'un parametre non précisé (w)")
                    
                if i.startswith('h'):
                    try:
                        height=i.split('=')[1]
                    except:
                        print("Valeur d'un parametre non précisé (h)")
                    
                if i.startswith('rep'):
                    try:
                        amount=i.split('=')[1]
                    except:
                        print("Valeur d'un parametre non précisé (rep)")
                        
                if i.startswith('loop'):
                    try:
                        loop=i.split('=')[1]
                    except:
                        print("Valeur d'un parametre non précisé (loop)")
                        
                if i.startswith('ecart'):
                    try:
                        ecart=i.split('=')[1]
                    except:
                        print("Valeur d'un parametre non précisé (ecart)")
                    
                if i.startswith('name'):
                    try:
                         name=i.split('=')[1]
                    except:
                        print("Valeur d'un parametre non précisé (name)")
               
        
    if continu:
        f = open(name+'.txt' , 'w')
        for i in range(int(amount)):
            f.write('w='+width + ' h='+height + ' alpha='+ str(random.uniform(0 , 1)) + ' beta='+str(random.uniform(0 , 1)) + ' gamma='+ str(random.uniform(0 , 1)) + ' kappa='+ str(random.uniform(0 , 1)) + \
                    ' mu='+ str(random.uniform(0 , 1)) + ' sigma='+ str(random.uniform(0 , 1)) + ' theta='+ str(random.uniform(0 , 1)) + ' repet='+loop + ' file='+name+str(i)+ ' ecart='+ecart+'\n')
        f.close
                
    
        
    
            