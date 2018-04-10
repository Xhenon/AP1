from tkinter import *
from math import sqrt , ceil
import random
import algo_voisins_hexa
import copy
import cProfile
import multiprocessing as mp
import time
import png
import sys

class Tableau:
    
    def __init__(self , width , height , vaporDensity , kappa , alpha , beta , theta , mu, gamma , sigma):
        self.listeCristal = []
        self.frontiere = []
        self.vaporDensity = vaporDensity #densité de vapeur initiale
        self.amount = height*width
        self.kappa = kappa #quantité de vapeur qui se transforme en glace durant le gel
        self.alpha = alpha # seuil à dépasser par l'eau pour qu'une case avec 3 voisins cristaux se transforme en cristal
        self.beta = beta # pareil mais pour 1 ou 2 voisins cristaux seulement
        self.gamma = gamma # fonte de la glace
        self.mu = mu #fonte de l'eau
        self.theta = theta #attachement 3 cristaux (vapeur)
        self.sigma = sigma #bruit
        self.width = width
        self.height = height
        self.ids = []
        self.vaporMap = []
        self.waterMap = []
        self.iceMap = []
        self.currentIndex = 0 #index correspond à l'étape que l'on affiche à l'écran
        self.maxIndex = 0 #index maximumactuellement généré
        self.states = {}
        
        self.neighbors = {}
        for i in range(width):
            for j in range(height):
                self.neighbors[(i , j)]=algo_voisins_hexa.voisins_grille_hexa([[0 for i in range(width)] for j in range(height)] , (j , i))  
    
        
        for i in range(width):
            self.vaporMap.append([self.vaporDensity for i in range(height)])
            self.waterMap.append([0.0 for i in range(height)])
            self.iceMap.append([0.0 for i in range(height)])
            self.ids.append([-1 for i in range(height)])
        
        #On ajoute un bloc de glace au milieu de la grille
        xMid , yMid = int(width/2) , int(height/2-1)
        print("cristal initial :" , xMid, yMid)
        self.listeCristal.append((xMid, yMid))
        
        for k in self.neighbors[(xMid , yMid)]:
            self.frontiere.append(k)
        
        self.vaporMap[xMid][yMid] = 0.0
        self.iceMap[xMid][yMid] = 1.0
        self.waterMap[xMid][yMid] = 0.0
        
        self.states['0wat']=list(self.waterMap)
        self.states['0vap']=list(self.vaporMap)
        self.states['0ice']=list(self.iceMap)
    
    
    def createArray(self, radius , canvas):
        '''
        Créer un tableau hexagonal de dimension (x,y)
        :param radius: (int) rayon de l'hexagone (longueur centre - sommet)
        :param canvas: (tkinter.Canvas) canvas sur lequel on affiche les cases
    
        CU: x et y > 0
    
        '''
        xOffset = 0
        ab = radius/2
        ao = sqrt(radius*radius- ab*ab)
        espaceX = ao*2
        espaceY= radius+ab
        vapeur = 1.0
        for j in range(self.height):
            for i in range(self.width):
                if j%2==0: #si i est pair
                    self.ids[i][j]=canvas.create_polygon([i*espaceX-ao, j*espaceY+ab , i*espaceX , j*espaceY+radius , i*espaceX+ao , j*espaceY+ab , i*espaceX+ao , j*espaceY-ab , i*espaceX , j*espaceY-radius , i*espaceX-ao ,j*espaceY-ab] , outline='black' ,  fill='grey' , width = 2)
            
                else: # si i est impair
                    self.ids[i][j]=canvas.create_polygon([i*espaceX, j*espaceY+ab , i*espaceX+ao , j*espaceY+radius , i*espaceX+2*ao , j*espaceY+ab , i*espaceX+2*ao , j*espaceY-ab , i*espaceX+ao , j*espaceY-radius , i*espaceX ,j*espaceY-ab] , outline='black' ,  fill='grey' , width = 2)  

    def updateColors(self, canvas):
        changeIds = []
        changeColors = []
        for i in range(self.width):
            for j in range(self.height):
                v = self.vaporMap[i][j]
                ice = self.iceMap[i][j]
                w = self.waterMap[i][j]/3
                
                
                blue = '00'
                red = '00'
                green = '00'
                
                red= format(int(v*255) , 'x')
                if len(red)==1:
                    red= '0'+red
                        
                green= format(int(w*255) , 'x')
                if len(green)==1:
                    green= '0'+green  
                        
                blue= format(int(ice*255) , 'x')
                if len(blue)==1:
                    blue= '0'+blue
                        
                if canvas.itemcget(self.ids[i][j] , 'fill') != '#'+red+green+blue:
                    changeIds.append(self.ids[i][j])
                    changeColors.append('#'+red+green+blue)
        
        for i in range(len(changeIds)):
            canvas.itemconfig(changeIds[i], fill=changeColors[i])
            
    def diffusion(self):
        vap = [[0 for j in range(self.height)] for i in range(self.width)]
        #vap = [[-1]*self.height]*self.width
        #vap = copy.deepcopy(self.vaporMap)
        for i in range(self.width):
            for j in range(self.height):
                vap[i][j]=0
                if (i , j) not in self.listeCristal:
                    mean = self.vaporMap[i][j]
                    n = 1 # nombre d'éléments dans la moyenne
                   
                    for k in self.neighbors[(i , j)]:
                        if k not in self.listeCristal: 
                            n+=1
                            mean+=self.vaporMap[k[0]][k[1]]
                    vap[i][j]=mean/n
                else:
                    vap[i][j]=self.vaporMap[i][j]
        self.vaporMap = list(vap)


    def gel(self):
        vap =  copy.deepcopy(self.vaporMap)
        wat = copy.deepcopy(self.waterMap)
        ice = copy.deepcopy(self.iceMap)
        for k in self.frontiere:
            i = k[0]
            j = k[1]
            wat[i][j]+=(1-self.kappa)*vap[i][j]
            ice[i][j]+=(self.kappa)*vap[i][j]
            vap[i][j]= 0
            
            if wat[i][j]>1:
                wat[i][j]=1
            
            if ice[i][j]>1:
                ice[i][j]=1
                
            
        self.vaporMap= list(vap)
        self.iceMap= list(ice)
        self.waterMap= list(wat)
        
        
    def fonte(self):
        vap = copy.deepcopy(self.vaporMap)
        wat = copy.deepcopy(self.waterMap)
        ice = copy.deepcopy(self.iceMap)
        
        for k in self.frontiere:
            i = k[0]
            j = k[1]
            vap[i][j]+=self.mu*wat[i][j]+self.gamma*ice[i][j]
            wat[i][j]=(1-self.mu)*wat[i][j]
            ice[i][j]=(1-self.gamma)*ice[i][j]
            
            if vap[i][j]>1:
                vap[i][j]=1
            
        self.vaporMap= copy.deepcopy(vap)
        self.iceMap= copy.deepcopy(ice)
        self.waterMap= copy.deepcopy(wat)
        
    def attachement(self):
        vap = copy.deepcopy(self.vaporMap)
        wat = copy.deepcopy(self.waterMap)
        ice = copy.deepcopy(self.iceMap)
        crist = copy.deepcopy(self.listeCristal)
        front = copy.deepcopy(self.frontiere)
        toRemove = [] #liste des coordonnées des cases à supprimer de la liste 'frontiere à la fin de l'opération (le faire pendant cause des problemes)'
        
        for f in range(len(self.frontiere)):
            k = self.frontiere[f]
            i = k[0]
            j = k[1]
            voisins = self.neighbors[(i ,j)]
            voisinsCrist= []
            voisinsNonCrist = []
            sommeVap = 0
                    
            for v in voisins:
                if v in self.listeCristal:
                    voisinsCrist.append(v)
                else:
                    voisinsNonCrist.append(v)
                sommeVap+=self.vaporMap[i][j]
                                
                            
            if len(voisinsCrist) >=4:
                crist.append((i , j))
                toRemove.append((i ,j))
                for e in voisinsNonCrist:
                    if e not in front:
                        front.append(e)
                ice[i][j]+=wat[i][j]
                wat[i][j] = 0
                vap[i][j] = 0
                if ice[i][j]>1:
                    ice[i][j]=1
                            
                                                            
            elif len(voisinsCrist)==3 and (wat[i][j]>=1 or (sommeVap < self.theta and wat[i][j]>self.alpha)) :
                crist.append((i , j))
                toRemove.append((i ,j))
                for e in voisinsNonCrist:
                    if e not in front:
                        front.append(e)
                ice[i][j]+=wat[i][j]
                wat[i][j] = 0
                vap[i][j] = 0
                if ice[i][j]>1:
                    ice[i][j]=1
                            
            elif (len(voisinsCrist)==2 or len(voisinsCrist)==1) and wat[i][j]>self.beta:
                crist.append((i , j))
                toRemove.append((i ,j))
                for e in voisinsNonCrist:
                    if e not in front:
                        front.append(e)
                ice[i][j]+=wat[i][j]
                wat[i][j] = 0
                vap[i][j] = 0
                if ice[i][j]>1:
                    ice[i][j]=1
                            
        
        
        for e in toRemove:
            front.remove(e)
        
        self.vaporMap= list(vap) # on peut également remplacer cette instruction par une deep copy si des problèmes surviennent
        self.iceMap= list(ice)
        self.waterMap= list(wat)
        self.listeCristal = list(crist)
        self.frontiere = list(front)
    
    def next(self , amount=1):
        for i in range(amount):
            if self.currentIndex == self.maxIndex:
                self.currentIndex+=1
                self.maxIndex+=1
                self.generate(self.currentIndex)
                print('etape :',i,'/',amount)
                
            else:
                self.currentIndex+=1
        self.changeGridTo(self.currentIndex)
        print("étape", self.currentIndex)
            
        
    def changeGridTo(self , state):
        #affiche une autre grille à la place de celle actuelle
        self.waterMap = copy.deepcopy(self.states[str(state)+'wat'])
        self.vaporMap = copy.deepcopy(self.states[str(state)+'vap'])
        self.iceMap = copy.deepcopy(self.states[str(state)+'ice'])
        
        
    def generate(self, index):
        self.diffusion()
        self.gel()
        self.attachement()
        self.fonte()
        
        self.states[str(index)+'wat']=copy.deepcopy(self.waterMap)
        self.states[str(index)+'vap']=copy.deepcopy(self.vaporMap)
        self.states[str(index)+'ice']=copy.deepcopy(self.iceMap)
        
        #bruit()
        
    def getIds(self):
        return self.ids
    
    def getVaporMap(self):
        return self.vaporMap
    
    def getWaterMap(self):
        return self.waterMap
    
    def getIceMap(self):
        return self.iceMap
    
    def printConfig(self):
        print('alpha' , self.alpha)
        print('beta ' , self.beta)
        print('gamma' , self.gamma)
        print('kappa' , self.kappa)
        print('mu   ' , self.mu)
        print('sigma' , self.sigma)
        print('theta' , self.theta)

    def getIndex(self):
        return self.currentIndex

def getHexagonesFromRadius(x , y , radius):
    '''
    Renvoie le nombre d'hexagones affichables pour une fenetre de dimension (x , y) pour des hexagones de rayon 'radius'
    :param x: (int) longueur de la fenetre
    :param y: (int) largeur de la fenetre
    :param radius: (int) rayon des hexagones
    :return: (tuple) nombre d'hexagones en longueur et en largeur (on arrondit au supérieur)
    
    CU: radius>0
    '''
    ab = radius/2
    ao = sqrt(radius*radius - ab*ab)
    x-=ao
    y-=radius
    xCount = 2+ceil(x/(2*ao))
    yCount = 2+ceil(y/(radius+ab))
    
    return(xCount, yCount)


def export(w , h , table , fileName):
    wr = png.Writer(w, h)
    l=[]
    
    for j in range(h):
        t = ()
        for i in range(w):
            v = int(table.getVaporMap()[i][j]*255)
            if v>255:
                v=255
            
            ice = int(table.getIceMap()[i][j]*255/2)
            if ice>255:
                ice=255
                
            wa = int(table.getWaterMap()[i][j]*255)
            if wa>255:
                wa=255
                
            t+=(v , wa , ice)
        l.append(t)
    file = open(fileName , 'wb')
    wr.write(file , l)
    file.close()
    print("done")
            


''' ----Création de la fenetre---- '''

if __name__=='__main__':
    repet , ecart , w , h = 1 , 50 , 100 , 100
    fileName = "flocon"
    vapeurInitiale = 0.9
    alpha , beta, gamma , kappa, mu , sigma , theta = -1 , -1 , -1 , -1 , -1 , -1 , -1
    
    if len(sys.argv)==2 and sys.argv[1]=='help':
        print('Liste des parametres:')
        print("\tecart: nombre d'étapes que l'on calcule d'un coup avant d'exporter le résultat sous forme d'image")
        print("\trepet: nombre de répétitions d'étapes")
        print("\tw: longueur de la grille")
        print("\th: largeur de la grille")
        print("\tfile: nom du fichier (sans l'extension) ou l'on exportera l'image")
        print("\tvapeur: quantité initiale de vapeur")
        print("\talpha: parametre")
        print("\tbeta: parametre")
        print("\tgamma: parametre")
        print("\tkappa: parametre")
        print("\tmu: parametre")
        print("\tsigma: parametre")
        print("\ttheta: parametre")
        
    
    else:
        for arg in sys.argv:
            if arg.startswith('ecart'):
                try:
                    ecart=int(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (ecart)")
            
            elif arg.startswith('repet'):
                try:
                    repet=int(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (repet)")
            
            elif arg.startswith('w'):
                try:
                    w=int(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (w)")
                    
            elif arg.startswith('h'):
                try:
                    h=int(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (h)")
            
            elif arg.startswith('vapeur'):
                try:
                    vapeurInitiale=float(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (vapeur)")
            
            elif arg.startswith('alpha'):
                try:
                    alpha=float(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (alpha)")
                    
            
            elif arg.startswith('beta'):
                try:
                    beta=float(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (beta)")
            
            elif arg.startswith('gamma'):
                try:
                    gamma=float(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (gamma)")
                    
            
            elif arg.startswith('kappa'):
                try:
                    kappa=float(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (kappa)")
            
            elif arg.startswith('mu'):
                try:
                    mu=float(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (mu)")
                    
            
            elif arg.startswith('sigma'):
                try:
                    sigma=float(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (sigma)")
            
            elif arg.startswith('theta'):
                try:
                    theta=float(arg.split('=')[1])
                except:
                    print("Valeur d'un parametre non précisé (theta)")
            
            elif arg.startswith('file'):
                try:
                    fileName=arg.split('=')[1]
                except:
                    print("Valeur d'un parametre non précisé (file)")
                    
        if alpha ==-1:
            alpha=random.uniform(0 , 1)
        
        if beta ==-1:
            beta=random.uniform(0 , 1)
            
        if gamma ==-1:
            gamma=random.uniform(0 , 1)

        if kappa ==-1:
            kappa=random.uniform(0 , 1)

        if mu ==-1:
            mu=random.uniform(0 , 1)

        if sigma ==-1:
            sigma=random.uniform(0 , 1)

        if theta ==-1:
            theta=random.uniform(0 , 1)


        print("Tableau de dimension :", w, h)
        
                                            #vap en eau, seuil 2 3 vois,  
                                        #vapDens   seuil 3 vois,seuil 3 vois
        #table = Tableau(dim[0] , dim[1] , 0.8 , 0.6 , 0.4 , 0.6 , 0.3 , 0 , 0 , 0.0) #width , height , vaporDensity , kappa , alpha , beta : seuil à dépasser par l'eau pour que le glace , theta , mu, gamma , sigma
        table = Tableau(w , h , vapeurInitiale , kappa , alpha , beta , theta , mu , gamma , sigma) #width , height , vaporDensity , kappa , alpha , beta : seuil à dépasser par l'eau pour que le glace , theta , mu, gamma , sigma

        x=1
        for i in range(repet):
            print('boucle numéro',x) 
            table.next(amount=ecart)
            export(w , h , table , fileName+str(i+1)+'.png')
            x+=1
            


