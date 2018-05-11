# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf
import os
from os.path import basename
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
f1=tk.Frame(fenetre)
listFiles=tk.Listbox(f1).grid(row=0, sticky=tk.W)
#listbox = tk.Listbox(fenetre, yscrollcommand=scrollbar.set)
#scrollbar = tk.Scrollbar(listbox)
#scrollbar.pack(side='right', fill='y')
#listbox.pack()

#scrollbar.config(command=listbox.yview)
#defilX = tk.Scrollbar(self, orient='horizontal',command=listFiles.xview)
#defilX.grid(row=1, column=0, sticky='ew')
#listFiles['xscrollcommand']=defilX.set
i=1;
#parcours choit du fichier
def chooseFile():
    #choice=fenetre.FileDialog(tf.msoFileDialogOpen)
    choice = tf.askopenfilenames() #fichier uniquement
    #choice = tf.askdirectory()  #repertoire uniquement
    #defaultextension='.png'
    #print(choice)
    #choiceBoth=tf.
    #os.listdir #pour recupereelement d'un dosier
    
    nbSelected=len(choice)
    #recupere le nom apartir du chemin
    for i in range (0,nbSelected):
        nom=basename(choice[i])
        if nom!="": #sinon quand on clic sur parcourir mais qu'on ne choisi rien ça rajoute un espace blanc
                listFiles.insert(1,nom) #ça se met par ordre aleatoire
                #i+=1
                #print(i)

#supprimer de la liste les fichiers selectionnés
def delecteSelection():
    selection = listFiles.curselection()
    listFiles.delete(selection[0])    
 
#supprimer de la liste tout les fichiers
def delecteAll():
    #cs=listFiles.curselection()
    #listFiles.delete(0,cs[0] -1)
    listFiles.delete(0,tk.END)   
    
#listFiles.pack(side="left",fill="y")    
boutonParcourir=tk.Button(f1,text="parcourir",command=chooseFile).grid(row=1, column=1,sticky=tk.W)
boutonSupprimer=tk.Button(f1,text="supprimer",command=delecteSelection).grid(row=2, column=1,sticky=tk.W)
boutonSupprimer=tk.Button(f1,text="vider",command=delecteAll).grid(row=3, column=1,sticky=tk.W)

f1.pack()
f1.grid(row=1,column=1)

#frame pour le zone avec les radiobuttons
f2=tk.Frame(fenetre)
#label pour le zone choisit
labelZoneChoix=tk.Label(f2,text='La zone choisit est : ')
labelZoneChoix.config(font=('Forte',18))
labelZoneChoix.grid(row=0, sticky=tk.W)

#les radiobuttons pour les choix
a=1
for i,v in enumerate(typeZone):
    print(i)
    tk.Radiobutton(f2, text=v, variable=var, value = a).grid(row=a, column=1,sticky=tk.W)
    a+=1

#button pour comfirmer le choix avec la zone choisit sur image
buttonConfirm=tk.Button(f2,text="Confirmer",command=confirmer).grid(row=len(typeZone)+1,column=1,sticky=tk.W)

f2.pack()
f2.grid(row=2,column=1)

#démarrer du réceptionnaire d'événements
fenetre.mainloop()

