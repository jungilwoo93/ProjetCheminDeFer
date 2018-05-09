# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf
import os
from os.path import basename
#from tkFileDialog import *
from tkinter import *
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




listFiles=tk.Listbox()




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
boutonParcourir=tk.Button(fenetre,text="parcourir",command=chooseFile).pack()
boutonSupprimer=tk.Button(fenetre,text="supprimer",command=delecteSelection).pack()
boutonSupprimer=tk.Button(fenetre,text="vider",command=delecteAll).pack()



fenetre.mainloop()

