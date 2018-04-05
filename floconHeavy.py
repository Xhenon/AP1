from tkinter import *
from math import sqrt , ceil
import random
import algo_voisins_hexa
import copy
import cProfile
#cProfile.run('foo()')
import multiprocessing
import time

class Tableau:
    
    def __init__(self, width , height , vaporDensity , kappa , alpha , beta , theta , mu, gamma , sigma):
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
    
    def multiUpdateColors(self, canvas):
        start_time = time.time()
        p = mp.Pool(processes=mp.cpu_count())
        t = p.map(stuff, [None for i in range(10)])
        p.close()
        print("--- %s seconds ---" % (time.time() - start_time))
    
    def updateColors(self, canvas):
       
        
        changeIds = []
        changeColors = []
        for i in range(self.width):
            for j in range(self.height):
                w = self.waterMap[i][j]
                v = self.vaporMap[i][j]
                ice = self.iceMap[i][j]
                
                
                blue = '00'
                red = '00'
                green = '00'
                               
                blue= format(int(w*255) , 'x')
                if len(blue)==1:
                    blue= '0'+blue
                
                red= format(int(v*255) , 'x')
                if len(red)==1:
                    red= '0'+red
                        
                green= format(int(ice*255) , 'x')
                if len(green)==1:
                    green= '0'+green
                        
                if canvas.itemcget(self.ids[i][j] , 'fill') != '#'+red+green+blue:
                    changeIds.append(self.ids[i][j])
                    changeColors.append('#'+red+green+blue)
        
        for i in range(len(changeIds)):
            canvas.itemconfig(changeIds[i], fill=changeColors[i])
        
        
    def forceUpdate(self , canvas):
        for i in range(self.width):
            for j in range(self.height):
                w = self.waterMap[i][j]
                v = self.vaporMap[i][j]
                ice = self.iceMap[i][j]
                
                blue = '00'
                red = '00'
                green = '00'
                               
                blue= format(int(w*255) , 'x')
                if len(blue)==1:
                    blue= '0'+blue
                
                red= format(int(v*255) , 'x')
                if len(red)==1:
                    red= '0'+red
                        
                green= format(int(ice*255) , 'x')
                if len(green)==1:
                    green= '0'+green
                        
                canvas.itemconfig(self.ids[i][j], fill='#'+red+green+blue)
        print("rafraichissement terminé")
            
    def diffusion(self):
        vap = copy.deepcopy(self.vaporMap)
        for i in range(self.width):
            for j in range(self.height):
                if (i , j) not in self.listeCristal:
                    mean = self.vaporMap[i][j]
                    n = 1 # nombre d'éléments dans la moyenne
                    for k in self.neighbors[(i , j)]:
                        if k not in self.listeCristal: 
                            n+=1
                            mean+=self.vaporMap[k[0]][k[1]]
                    vap[i][j]=mean/n
                
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
        #print(len(self.frontiere))
    
    def next(self , canvas , amount=1):
        for i in range(amount):
            if self.currentIndex == self.maxIndex:
                self.currentIndex+=1
                self.maxIndex+=1
                self.generate(self.currentIndex)
                
            else:
                self.currentIndex+=1
        self.changeGridTo(self.currentIndex, canvas)
        print("étape", self.currentIndex)

    def previous(self , canvas , amount=1):
        for i in range(amount):
            if self.currentIndex !=0:
                self.currentIndex-=1
        self.changeGridTo(self.currentIndex, canvas)
        print("étape",self.currentIndex)
            
        
    def changeGridTo(self , state , canvas):
        #affiche une autre grille à la place de celle actuelle
        self.waterMap = copy.deepcopy(self.states[str(state)+'wat'])
        self.vaporMap = copy.deepcopy(self.states[str(state)+'vap'])
        self.iceMap = copy.deepcopy(self.states[str(state)+'ice'])
        
        self.updateColors(canvas)
        
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
    


''' ----Création de la fenetre---- '''

if __name__=='__main__':
    
    fen = Tk()
    w = 1600 ; h = 1100
    can = Canvas(fen, width=w, height=h, bg='ivory') #1200 , 800
    can.pack(side=TOP)


    radius = 12 #30
    dim = getHexagonesFromRadius(w, h , radius)
    print("Tableau de dimension : ", dim[0] , dim[1])
                                        #vap en eau, seuil 2 3 vois,  
                                    #vapDens   seuil 3 vois,seuil 3 vois
    #table = Tableau(dim[0] , dim[1] , 0.8 , 0.6 , 0.4 , 0.6 , 0.3 , 0 , 0 , 0.0) #width , height , vaporDensity , kappa , alpha , beta : seuil à dépasser par l'eau pour que le glac , theta , mu, gamma , sigma
    table = Tableau(dim[0] , dim[1] , 0.8 , 0.5 , 0.9 , 0.9 , 0.2 , 0 , 0 , 0) #width , height , vaporDensity , vaporToWaterProportion , alpha , beta : seuil à dépasser par l'eau pour que le glac , theta , mu, gamma , sigma


    suivant = Button(text = "Suivant" , command = lambda: table.next(can), anchor = W)
    suivant.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
    nextWindow = can.create_window(0, 0, anchor=NW, window=suivant)

    precedent = Button(text = "Precedent" , command = lambda: table.previous(can) , anchor = W)
    precedent.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
    prevWindow = can.create_window(0, 30, anchor=NW, window=precedent)

    suivant2 = Button(text = "Suivant ++" , command = lambda: table.next(can , amount=20), anchor = W)
    suivant2.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
    nextWindow = can.create_window(90, 0, anchor=NW, window=suivant2)

    precedent2 = Button(text = "Precedent ++" , command = lambda: table.previous(can , amount=20) , anchor = W)
    precedent2.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
    prevWindow = can.create_window(90, 30, anchor=NW, window=precedent2)


    refresh = Button(text = "Rafraichir" , command = lambda: table.forceUpdate(can) , anchor = W)
    refresh.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
    prevWindow = can.create_window(0, 60, anchor=NW, window=refresh)


    table.createArray(radius , can)
    table.updateColors(can)
    run = True
    while run:
        try:
            fen.update()
        except:
            run = False
            
            try:
                fen.destroy()
            except:
                pass
            
    table.printConfig()



