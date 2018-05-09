# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
#from tkinter import *
#créer la fenêtre d'application
fenetre = tk.Tk()
#variable
var = tk.IntVar()
var.set(1)
typeZone={"Titre","Paragraphe","Lettrine","Image"}

#fonctions
def confirmer():
    print(var)
    
#mettre le title et background pour l'application
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

#frame pour le zone avec les radiobuttons
f2=tk.Frame(fenetre)
#label pour le zone choisit
labelZoneChoix=tk.Label(f2,text='La zone choisit est : ')
labelZoneChoix.config(font=('Forte',18))
labelZoneChoix.grid(row=0, sticky=W)
#les radiobuttons pour les choix
a=1
for i,v in enumerate(typeZone):
    print(i)
    tk.Radiobutton(f2, text=v, variable=var, value = a).grid(row=a, column=1,sticky=W)
    a+=1

#button pour comfirmer le choix avec la zone choisit sur image
buttonConfirm=tk.Button(f2,text="Confirmer",command=confirmer).grid(row=len(typeZone)+1,column=1,sticky=W)

f2.pack()
f2.grid(row=1,column=2)



#démarrer du réceptionnaire d'événements
fenetre.mainloop()

