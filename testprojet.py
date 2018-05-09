# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog
#from tkFileDialog import *
#from tkinter import *
#créer la fenêtre d'application
fenetre = tk.Tk()
#mettre le title pour l'application
fenetre.title("Projet")
#récupérer la taille d'écran d'ordi
ecran_width = fenetre.winfo_screenwidth()
ecran_height = fenetre.winfo_screenheight()
#définir la taille d'écran d'or comme la fenêtre d'application
fenetre.geometry(str(ecran_width)+'x'+str(ecran_height))
#rachel a fait
#fenetre.attributes("-fullscreen", 1)
#w=fenetre.winfo_screenwidth()
#h=fenetre.winfo_screenheight() 
#fenetre.configure(width=w-2,height=h-50)
#tk.Button(fenetre, text="Quit", command=fenetre.destroy).pack()
#démarrer du réceptionnaire d'événements
def chooseFile():
    choice = tkinter.filedialog.askopenfilename()
    print(choice)
    
boutonParcourir=tk.Button(fenetre,text="parcourir",command=chooseFile).pack()
#boutonParcourir.pack



fenetre.mainloop()

