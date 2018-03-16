from tkinter import *
import random

fen = Tk()
#fen.protocol("WM_DELETE_WINDOW", onClosing)
w = 1200 ; h = 800
can = Canvas(fen, width=1200, height=800, bg='ivory')

img = PhotoImage(width=w,height=h)
can.create_image((w//2, h//2), image=img, state="normal")
can.pack(side=TOP)

def randnum():
    fin = ""
    x=''
    
    for i in range(3):
        x = format(random.randint(0 , 255) , 'x')
        if len(x)==1:
            x= '0'+x
        fin +=x
    return fin

def plusrand(x):
    res = ''
    for i in range(x):
        res+=('#'+randnum()+ ' ')
    return res

def ult(x , y):
    res = ""
    for i in range(y):
        res += " {" + plusrand(x)+"}"
    return res
    
##def update():
##    img.put("#"+randnum()+randnum()+randnum() , (random.randint(0 , w-1) , random.randint(0 , h-1)))
##    fen.after(0 , update)
##
##fen.after(0 , update)
##fen.mainloop()


#img.put("#"+randnum() , (random.randint(0 , w-1) , random.randint(0 , h-1)))

while True:
    fen.update()
    ligne = random.randint(0, h)
    # data: tuple avec {} -> motif pour une première ligne (on met autant d'éléments qu'on veut entre les accolades, ca fait un motif), {} -> motif d'une deuxième ligne
    #data = ('{#000000 #000000 #000000 #FFFFFF} {#000000 #FFFFFF #000000 #FFFFFF} {#FFFFFF #010000 #FFFFFF #FFFFFF}')
    data = (ult(int(w/40) , int(h/40)))
   # x = random.randint(0 ,h)
    #img.put("{red green} {blue yellow}", to=(0 , 0 , 400,600))
    img.put(data , to=(0,0,w , h))


