from tkinter import *
from math import sqrt , ceil
import random
import algo_voisins_hexa

''' ----Création de la fenetre---- '''

fen = Tk()
#fen.protocol("WM_DELETE_WINDOW", onClosing)
w = 1200 ; h = 800
can = Canvas(fen, width=1200, height=800, bg='ivory')

img = PhotoImage(width=w,height=h)
can.create_image((w//2, h//2), image=img, state="normal")
can.pack(side=TOP)


class Tableau:
    
    def __init__(self, width , height , vaporDensity , vaporToIceProportion , alpha , beta , theta , mu, gamma , sigma):
        self.vaporDensity = vaporDensity #densité de vapeur initiale
        self.amount = height*width
        self.vaporToIceProportion = vaporToIceProportion #quantité de vapeur qui se transforme en glace durant le gel
        self.alpha = alpha # attachement 3 cristaux (eau)
        self.beta = beta # attachement 2 cristaux
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
        for i in range(width):
            self.vaporMap.append([self.vaporDensity for i in range(height)])
            self.waterMap.append([0.0 for i in range(height)])
            self.iceMap.append([0.0 for i in range(height)])
            self.ids.append([-1 for i in range(height)])
        
        #On ajoute un bloc de glace au milieu de la grille
        xMid , yMid = int(width/2) , int(height/2-1)
        print(xMid, yMid)
        self.vaporMap[xMid][yMid] = 0.0
        self.iceMap[xMid][yMid] = 1.0
        self.waterMap[xMid][yMid] = 0.0
        
        self.neighbors = {}
        for i in range(width): #self.cases
            for j in range(height): #self.cases[i]
                self.neighbors[(i , j)]=algo_voisins_hexa.voisins_grille_hexa([[0 for i in range(width)] for j in range(height)] , (j , i))  
    
    
    
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
        for i in range(self.width):
            for j in range(self.height):
                w = self.waterMap[i][j]
                v = self.vaporMap[i][j]
                
                blue = '00'
                red = '00'
                
                if(w!=0 or v!=0):
                    blue= format(int(w*255) , 'x')
                    if len(blue)==1:
                        blue= '0'+blue
                
                    red= format(int(v*255) , 'x')
                    if len(red)==1:
                        red= '0'+red
                    
                    canvas.itemconfig(self.ids[i][j], fill='#'+red+'00'+blue)
                else:
                     canvas.itemconfig(self.ids[i][j], fill='#82f0ff')
                
            
    def diffusion(self):
        l = [[-1.0 for i in range(self.height)] for j in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                #print(i ,j)
                if i == 12 and j == 9:
                    print(self.neighbors[(i , j)])
                mean = self.vaporMap[i][j]
                n = 1 # nombre d'éléments dans la moyenne
                for k in self.neighbors[(i , j)]:
                    n+=1
                    mean+=self.vaporMap[k[0]][k[1]]
                l[i][j]=mean/n
        self.vaporMap = list(l)
           
    def getIds(self):
        return self.ids
    
    def getVaporMap(self):
        return self.vaporMap
    
    def getWaterMap(self):
        return self.waterMap
    
    def getIceMap(self):
        return self.iceMap



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
    
radius = 30
dim = getHexagonesFromRadius(w, h , radius)
print("Tableau de dimension : ", dim[0] , dim[1])

table = Tableau(dim[0] , dim[1] , 0.8 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0)
table.createArray(radius , can)
table.diffusion()
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
        
        
    '''ligne = random.randint(0, h)
    # data: tuple avec {} -> motif pour une première ligne (on met autant d'éléments qu'on veut entre les accolades, ca fait un motif), {} -> motif d'une deuxième ligne
    #data = ('{#000000 #000000 #000000 #FFFFFF} {#000000 #FFFFFF #000000 #FFFFFF} {#FFFFFF #010000 #FFFFFF #FFFFFF}')
    data = (ult(int(w/40) , int(h/40)))
   # x = random.randint(0 ,h)
    #img.put("{red green} {blue yellow}", to=(0 , 0 , 400,600))
    img.put(data , to=(0,0,w , h))'''



