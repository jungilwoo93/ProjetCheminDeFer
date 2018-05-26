# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:37:31 2018

@author: Rachel NOIREAU & Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf
from PIL import Image, ImageFont, ImageDraw, ImageTk

#fichier lier
import buttonFunction as bf



####fenetre
root = tk.Tk()
ecran_width = root.winfo_screenwidth()*0.9
ecran_height = root.winfo_screenheight()*0.85
root.geometry('%dx%d+%d+%d' % (ecran_width, ecran_height, 1, 1))
root.title("Chemin de Fer")
root.resizable(width=False,height=False)
colorDefault="#F5F5DC"

####variable
dimention=[4,8]
rectFull=False
defaultColor="#F5F5DC"

####menu barrre
menubar=tk.Menu(root)
root.config(menu = menubar)
menufichier = tk.Menu(menubar,tearoff=0)
view = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label="Fichier", menu=menufichier)
menubar.add_cascade(label="Affichage", menu=view)

menufichier.add_command(label="Exporter en pdf", command=bf.exportToPdf)
menufichier.add_separator() 
menufichier.add_command(label="Quitter", command=root.destroy) 

rect= tk.Menu(view,tearoff=0)
dim= tk.Menu(view,tearoff=0)
view.add_cascade(label="rectangle", menu=rect)
view.add_cascade(label="dimention", menu=dim)
rect.add_checkbutton(label="Plein", command=bf.fullRect(rectFull))
#rect.add_command(label="Vide", command=bf.fullRect)
#rect.add_command(label="Plein", command=bf.emptyRect)

nitem=tk.IntVar()
nitem.set(3)# bouton seletionner par defaut doit etre le meme que celui selectionner en haut

#########nombre de page par feuille
dim.add_radiobutton(label="2*2",  variable=nitem, value=1,  command=bf.setDimention(2,2))
dim.add_radiobutton(label="3*4", variable=nitem, value=2,  command=bf.setDimention(3,4))#command=item,
dim.add_radiobutton(label="4*8",  variable=nitem, value=3,  command=bf.setDimention(4,8))
dim.add_radiobutton(label="5*10",  variable=nitem, value=4,  command=bf.setDimention(5,10))
dim.add_radiobutton(label="6*16",  variable=nitem, value=5,  command=bf.setDimention(6,16))



###########l'aperçu

dicimg={}

canva=tk.Canvas(root, width =760, height = 760, bg =defaultColor)
canva.grid()


#img.resize((320,240))
#img.zoom(320/img.width(), 240/img.height())
#wd,hg=img.size
mwd=ecran_width
mhg=ecran_height
listImg=bf.getListImg('test')
posX=0
posY=0
widthImg=dimention[0]
for image in listImg:
	print(image)
	img=Image.open('DrawOnImage/finalResult/'+ 'test'+ '/' + image)
	wd,hg=img.size
	scale= 1.0*wd/mwd
	newImg=img.resize((int(wd/widthImg),int(hg/widthImg)),Image.ANTIALIAS)
	canva.config(width=wd/scale,height=hg/scale)
	photo = ImageTk.PhotoImage(newImg)
	canva.image=photo
	canva.create_image(posX,posY,image=photo,anchor="nw")
	dicimg[photo] = photo
	posX+=wd/widthImg+2
	#posY+=widthImg
# mise en page à l'aide de la méthode 'grid':
canva.grid(sticky=tk.NE, rowspan = 10, padx =10, pady =5)
#row = lig, column = col,









root.mainloop()