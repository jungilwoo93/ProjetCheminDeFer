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

listFiles=tk.Listbox()
i=1;
#parcours choit du fichier
def chooseFile():
    choice = tf.askopenfilename()
    nom=basename(choice)
    print(nom)
    if nom!="":
            listFiles.insert(1,nom) #ça se met par ordre alphabetique
    
    #i+=1
    #print(i)

def delecteSelection():
    selection = listFiles.curselection()
    listFiles.delete(selection[0])    
    
def delecteAll():
    cs=listFiles.curselection()
    #listFiles.delete(0,cs[0] -1)
    listFiles.delete(0,tk.END)
    
    
listFiles.pack()    
boutonParcourir=tk.Button(fenetre,text="parcourir",command=chooseFile).pack()
boutonSupprimer=tk.Button(fenetre,text="supprimer",command=delecteSelection).pack()
boutonSupprimer=tk.Button(fenetre,text="vider",command=delecteAll).pack()



fenetre.mainloop()

