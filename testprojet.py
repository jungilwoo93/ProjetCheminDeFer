# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf
from PIL import Image, ImageFont, ImageDraw, ImageTk
#import os
from os.path import basename
#from tkinter import *
#créer la fenêtre d'application
fenetre = tk.Tk()

#variable global
var=tk.StringVar()
var.set(0)
typeZone={"Titre","Paragraphe","Lettrine","Image"}

#les fonctions
#fonctions de buttonConfirm
def confirmer():
    listAction.insert(tk.END,var.get())

    
#mettre le title et background pour l'application
fenetre.title("Projet")

#récupérer la taille d'écran d'ordi
ecran_width = fenetre.winfo_screenwidth()
ecran_height = fenetre.winfo_screenheight()
#définir la taille d'écran d'or comme la fenêtre d'application
fenetre.geometry(str(ecran_width)+'x'+str(ecran_height))

#creer un nouveau frame pour la partie de fichier
f1=tk.Frame(fenetre)
labelFichier=tk.Label(f1,text='Les fichier choisit : ')
labelFichier.config(font=('Forte',18))
labelFichier.grid(row=0,sticky=tk.W,pady=5)

listFrame=tk.Frame(f1)
yDefilB = tk.Scrollbar(f1, orient='vertical')
yDefilB.grid(row=0, column=1, sticky='ns')

xDefilB = tk.Scrollbar(f1, orient='horizontal')
xDefilB.grid(row=1, column=0, sticky='ew')

listFiles = tk.Listbox(listFrame,
     xscrollcommand=xDefilB.set,
     yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE)
listFiles.pack(pady=10,padx=20)#'nsew'
xDefilB['command'] = listFiles.xview
yDefilB['command'] = listFiles.yview
#scrollbar.config(command=listbox.yview)
#defilX = tk.Scrollbar(self, orient='horizontal',command=listFiles.xview)
#defilX.grid(row=1, column=0, sticky='ew')
#listFiles['xscrollcommand']=defilX.set
j=1;#i=1
#listFiles=tk.Listbox(listFrame,width=70,height=15,selectmode=tk.SINGLE).pack(pady=10,padx=20)
listFrame.grid(row=1,sticky=tk.W)

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
    listFiles.Sorted = True
    while i < (listFiles.size() - 1) :
        if (listFiles.get(i + 1,i+1) == listFiles.get(i,i)) :
            listFiles.delete(i,i)
            i = 0
        else :
            i += 1
            
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
zoneButton=tk.Frame(f1)
boutonParcourir=tk.Button(zoneButton,text="parcourir",command=chooseFile).grid(row=1, column=0,sticky=tk.S,padx=40)
boutonSupprimer=tk.Button(zoneButton,text="supprimer",command=delecteSelection).grid(row=1, column=1,sticky=tk.S,padx=40)
boutonSupprimer=tk.Button(zoneButton,text="vider",command=delecteAll).grid(row=1, column=2,sticky=tk.S,ipadx=10,padx=40)
zoneButton.grid(row=2,pady=10)
f1.grid(row=1,column=1)

#nouveau frame pour le zone avec les radiobuttons
f2=tk.Frame(fenetre)
#label pour le zone choisit
labelZoneChoix=tk.Label(f2,text='La zone choisit est : ')
labelZoneChoix.config(font=('Forte',18))
labelZoneChoix.grid(row=0, sticky=tk.W)

#les radiobuttons pour les choix
a=1
for i,v in enumerate(typeZone):
    tk.Radiobutton(f2, text=v, variable=var, value = v).grid(row=a, column=0,sticky=tk.W)
    a+=1

#button pour comfirmer le choix avec la zone choisit sur image
buttonConfirm=tk.Button(f2,text="Confirmer",command=confirmer).grid(row=len(typeZone)+1,column=0,sticky=tk.S)
#liste Action
labelAction=tk.Label(f2,text="Les actions : ")
labelAction.config(font=('Forte',18))
labelAction.grid(row=len(typeZone)+2,column=0,sticky=tk.W)
listAction = tk.Listbox(f2,width=70,height=10)
listAction.grid(row=len(typeZone)+3,column=0)
f2.grid(row=2,column=1)

#afficher image dés qu'on selectionner un element
def onselect(evt):
    print("element selectionner")
    cadre=tk.Canvas(fenetre,width=440,height=380)#,bg="black"
    dicimg = {}
    #selection = listFiles.curselection()
    #print(selection[0])
    w=evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    img=Image.open(value)
    photo = ImageTk.PhotoImage(img)
    dicimg['img1'] = photo
    cadre.image=photo
    item = cadre.create_image(320,240,image =photo) 
    cadre.grid(row=1,column=2)

listFiles.bind('<<ListboxSelect>>', onselect)   
#démarrer du réceptionnaire d'événements
fenetre.mainloop()

