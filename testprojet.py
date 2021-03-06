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
var.set("Paragraphe")
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
labelFichier=tk.Label(f1,text='Les fichier choisis : ')
labelFichier.config(font=('Forte',18))
labelFichier.grid(row=0,sticky=tk.W,pady=5)

listFrame=tk.Frame(f1)
yDefilB = tk.Scrollbar(listFrame, orient='vertical')
yDefilB.grid(row=0, column=1, sticky='ns')

xDefilB = tk.Scrollbar(listFrame, orient='horizontal')
xDefilB.grid(row=1, column=0, sticky='ew')

listFiles = tk.Listbox(listFrame,
     xscrollcommand=xDefilB.set,
     yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE)
listFiles.grid(row=0)#'nsew'
xDefilB['command'] = listFiles.xview
yDefilB['command'] = listFiles.yview
#scrollbar.config(command=listbox.yview)
#defilX = tk.Scrollbar(self, orient='horizontal',command=listFiles.xview)
#defilX.grid(row=1, column=0, sticky='ew')
#listFiles['xscrollcommand']=defilX.set
j=1;#i=1
#listFiles=tk.Listbox(listFrame,width=70,height=15,selectmode=tk.SINGLE).pack(pady=10,padx=20)
listFrame.grid(row=1,pady=5,padx=20,sticky=tk.W)

#listbox = tk.Listbox(fenetre, yscrollcommand=scrollbar.set)
#scrollbar = tk.Scrollbar(listbox)
#scrollbar.pack(side='right', fill='y')
#listbox.pack()

#scrollbar.config(command=listbox.yview)
#defilX = tk.Scrollbar(self, orient='horizontal',command=listFiles.xview)
#defilX.grid(row=1, column=0, sticky='ew')
#listFiles['xscrollcommand']=defilX.set

listPath=[]

#parcours choit du fichier
def chooseFile():
    #choice=fenetre.FileDialog(tf.msoFileDialogOpen)
    choice = tf.askopenfilenames() #fichier uniquement
    #choice = tf.askdirectory()  #repertoire uniquement
    #defaultextension='.png'
    #filetypes=[('BMP FILES','*.bmp')]#pas sure
    #filetypes=[('PNG FILES','*.png')]
    #("JPEG",'*.jpg')
    #print(choice)
    #choiceBoth=tf.
    #os.listdir #pour recupereelement d'un dosier
    i=1;
    j=1
    nbSelected=len(choice)
    #recupere le nom apartir du chemin
    for i in range (0,nbSelected):
        nom=basename(choice[i])
        #nom=choice[i]
        if nom!="": #sinon quand on clic sur parcourir mais qu'on ne choisi rien ça rajoute un espace blanc
                listFiles.insert(1,nom) #ça se met par ordre aleatoire
                listPath.append(choice[i])
                #i+=1
                #print(i)
    listFiles.Sorted = True
    listPath.sort()
    while j < (listFiles.size() - 1) :
        if (listFiles.get(j + 1,j+1) == listFiles.get(j,j)) :
            listFiles.delete(j,j)
            listPath.remove(listPath[j])
            j = 0
        else :
            j += 1
    listPath.reverse()
            
#supprimer de la liste les fichiers selectionnés
def delecteSelection():
    selection = listFiles.curselection()
    listFiles.delete(selection[0])
    listPath.remove(selection[0])####################################
 
#supprimer de la liste tout les fichiers
def delecteAll():
    #cs=listFiles.curselection()
    #listFiles.delete(0,cs[0] -1)
    listFiles.delete(0,tk.END) 
    listPath.clear()
    
#listFiles.pack(side="left",fill="y")   
zoneButton=tk.Frame(f1)
boutonParcourir=tk.Button(zoneButton,text="Parcourir",command=chooseFile).grid(row=1, column=0,sticky=tk.S,padx=40)
boutonSupprimer=tk.Button(zoneButton,text="Supprimer",command=delecteSelection).grid(row=1, column=1,sticky=tk.S,padx=40)
boutonSupprimer=tk.Button(zoneButton,text="Vider",command=delecteAll).grid(row=1, column=2,sticky=tk.S,ipadx=10,padx=40)
zoneButton.grid(row=2,pady=5)
#f1.grid(row=1,column=1)

#nouveau frame pour le zone avec les radiobuttons
#f2=tk.Frame(fenetre)
#label pour le zone choisit
labelZoneChoix=tk.Label(f1,text='La zone choisie est : ')
labelZoneChoix.config(font=('Forte',18))
labelZoneChoix.grid(row=3, sticky=tk.W)

#les radiobuttons pour les choix
zoneRadioButton=tk.Frame(f1)
a=0
for i,v in enumerate(typeZone):
    tk.Radiobutton(zoneRadioButton, text=v, variable=var, value = v).grid(row=a, column=0,sticky=tk.W)
    a+=1
zoneRadioButton.grid(row=4,sticky=tk.W,pady=5)
#button pour comfirmer le choix avec la zone choisit sur image
buttonConfirm=tk.Button(f1,text="Confirmer",command=confirmer).grid(row=5,column=0,pady=5,sticky=tk.S)
#liste Action
labelAction=tk.Label(f1,text="Les actions : ")
labelAction.config(font=('Forte',18))
labelAction.grid(row=6,column=0,pady=5,sticky=tk.W)
listAction = tk.Listbox(f1,width=70,height=8)
listAction.grid(row=7,column=0,pady=5)
f1.grid(row=0,column=1)

#afficher image dés qu'on selectionner un element
def onselect(evt):

    cadre=tk.Canvas(fenetre,width=600,height=750)#,bg="black"

    dicimg = {}
    #selection = listFiles.curselection()
    #print(selection[0])
    w=evt.widget
    if len(w.curselection())!=0 :
        index = int(w.curselection()[0])
        value = w.get(index)
        img=Image.open(listPath[index])
        img.resize((320,240))
        #img.zoom(320/img.width(), 240/img.height())
        print(value)
        photo = ImageTk.PhotoImage(img)
        dicimg['img1'] = photo
        cadre.image=photo
<<<<<<< HEAD
        item = cadre.create_image(600,800,image =photo) 
        cadre.grid(row=0,column=2,padx=20,pady=20)

=======
        item = cadre.create_image(0,0,image =photo) 
        cadre.grid(row=1,column=2)
        #.resize((x,y)) puis .save('nouvnom')
        
>>>>>>> fc5f3def5f94a27be45396edfde27055257a29c8
listFiles.bind('<<ListboxSelect>>', onselect)   
#démarrer du réceptionnaire d'événements
fenetre.mainloop()

