# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:37:31 2018

@author: Rachel NOIREAU & Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf
from PIL import Image, ImageFont, ImageDraw, ImageTk


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
rectFull=False


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
nitem.set(1)
dim.add_radiobutton(label="item1",  variable=nitem, value=1)
dim.add_radiobutton(label="item2", variable=nitem, value=2)#command=item,
dim.add_radiobutton(label="item3",  variable=nitem, value=3)
#dim.add_radiobutton()



root.mainloop()