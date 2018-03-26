from tkinter import *
from math import sqrt , ceil
import random

''' ----Création de la fenetre---- '''

fen = Tk()
#fen.protocol("WM_DELETE_WINDOW", onClosing)
w = 1200 ; h = 800
can = Canvas(fen, width=1200, height=800, bg='ivory')

img = PhotoImage(width=w,height=h)
can.create_image((w//2, h//2), image=img, state="normal")
can.pack(side=TOP)


class Tableau:
    
    
    
    def __init__(self, width , height):
        self.width = width
        self.height = height
        self.cases = []
        for i in range(width):
            colone = []
            for j in range(height):
                colone.append(Case(0 , 0 , 0, 0))
            self.cases.append(colone)
        self.neighbors = 
        
        
    def getNeighbors(self, case):
        
        
        
    def updateColors(self, canvas):
        for i in self.cases:
            for j in i:
                w = j.getWaterProportion()
                v = j.getVaporProportion()
                
                blue = '00'
                red = '00'
                
                if(w!=0 or v!=0):
                    blue= format(int(w*255) , 'x')
                    if len(blue)==1:
                        blue= '0'+blue
                
                    red= format(int(v*255) , 'x')
                    if len(red)==1:
                        red= '0'+red
                    
                    canvas.itemconfig(j.getId(), fill='#'+red+'00'+blue)
                else:
                     canvas.itemconfig(j.getId(), fill='#82f0ff')
                
               
    
    def setCaseAt(self, x , y , case):
        self.cases[x][y] = case
        
    def getCaseAt(self, x , y):
        return self.cases[x][y]
    
    def getCases(self):
        return self.cases
    
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
        for j in range(self.height):
            for i in range(self.width):
                x = random.uniform(0 , 1)
                y= random.uniform(0 , 1)
                if j%2==0: #si i est pair
                    self.cases[i][j]=Case(x , 0.0 ,y , canvas.create_polygon([i*espaceX-ao, j*espaceY+ab , i*espaceX , j*espaceY+radius , i*espaceX+ao , j*espaceY+ab , i*espaceX+ao , j*espaceY-ab , i*espaceX , j*espaceY-radius , i*espaceX-ao ,j*espaceY-ab] , outline='red' ,  fill='grey' , width = 1))
            
                else: # si i est impair
                    self.cases[i][j]=Case(x , 0.0 , y , canvas.create_polygon([i*espaceX-2*ao, j*espaceY+ab , i*espaceX-ao , j*espaceY+radius , i*espaceX , j*espaceY+ab , i*espaceX , j*espaceY-ab , i*espaceX-ao , j*espaceY-radius , i*espaceX-2*ao ,j*espaceY-ab] , outline='red' ,  fill='grey' , width = 1))
         
        
        
class Case:
    def __init__(self , water , solid , vapor , id):
        self.water = water
        self.solid = solid
        self.vapor = vapor
        self.id = id
        
    def getId(self):
        return self.id
    
    def getWaterProportion(self):
        return self.water
    
    def getSolidProportion(self):
        return self.solid
    
    def getVaporProportion(self):
        return self.vapor
    
    def setWaterProportion(self, water):
        self.water = water
    
    def setSolidProportion(self, solid):
        self.solid = solid
    
    def setVaporProportion(self, vapor):
        self.vapor = vapor
    
   
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


table = Tableau(dim[0] , dim[1])
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
        
        
    '''ligne = random.randint(0, h)
    # data: tuple avec {} -> motif pour une première ligne (on met autant d'éléments qu'on veut entre les accolades, ca fait un motif), {} -> motif d'une deuxième ligne
    #data = ('{#000000 #000000 #000000 #FFFFFF} {#000000 #FFFFFF #000000 #FFFFFF} {#FFFFFF #010000 #FFFFFF #FFFFFF}')
    data = (ult(int(w/40) , int(h/40)))
   # x = random.randint(0 ,h)
    #img.put("{red green} {blue yellow}", to=(0 , 0 , 400,600))
    img.put(data , to=(0,0,w , h))'''



