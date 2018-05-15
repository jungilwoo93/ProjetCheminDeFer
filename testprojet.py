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

#créer la fenêtre d'application
root = tk.Tk()
#récupérer la taille d'écran d'ordi
ecran_width = root.winfo_screenwidth()
ecran_height = root.winfo_screenheight()-50
#définir la taille d'écran d'or comme la fenêtre d'application
root.geometry(str(ecran_width)+'x'+str(ecran_height))


f1=tk.Frame(root,bg='gold', width=ecran_width+1000, height=ecran_height)
f1.config(width=ecran_width+1000, height=ecran_height)
f1.grid(column=0,columnspan=1000,sticky=tk.E)

vsb = tk.Scrollbar(root, orient=tk.VERTICAL)
vsb.grid(row=0, column=3, rowspan=4, sticky=tk.N+tk.S+tk.E)#
hsb = tk.Scrollbar(root, orient=tk.HORIZONTAL)
hsb.grid(row=3, column=0,columnspan=5, sticky=tk.E+tk.W+tk.S)#
c = tk.Canvas(root, yscrollcommand=vsb.set, xscrollcommand=hsb.set, width=1, bd=0,highlightthickness=0)
#c.yview_moveto(1)
#c.xview_moveto(1)
c.grid(row=0, column=0, sticky=tk.W+tk.N + tk.S)#,sticky="news"
vsb.config( command=c.yview)#c.yview
hsb.config(command=c.xview)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#variable global
var=tk.StringVar()
var.set("Paragraphe")
typeZone={"Titre","Paragraphe","Lettrine","Image"}

#les fonctions
#fonctions de buttonConfirm
def confirmer():
    listAction.insert(tk.END,var.get())

    
#mettre le title et background pour l'application
root.title("Projet")



#creer un nouveau frame pour la partie de fichier
#f1=tk.Frame(root)
labelFichier=tk.Label(f1,text='Les fichiers choisis : ')
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


listFrame.grid(row=1,pady=5,padx=20,sticky=tk.W)



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
labelZoneChoix=tk.Label(f1,text='La zone choisi est : ')
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





#f0 = tk.Frame(f1)
#f0.grid(fill=tk.BOTH)
#f0.pack(fill=tk.BOTH)
#c.grid(sticky=tk.E)
#c.create_window(0, 0,  window=f1)

 
#c.create_window(0, 0,  window=f0)
#f0.update_idletasks()
#c.config(scrollregion=c.bbox("all"))#a mettre a la fin

#afficher image dés qu'on selectionner un element
zoneImage=tk.Frame(f1,bg="black")
#zoneImage.grid(row=2,column=10,rowspan=2,columnspan=8,sticky=tk.E )

def onselect(evt):
    cadre=tk.Canvas(zoneImage,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=320,height=240,bg="black")#,bg="black"
    dicimg = {}
    #selection = listFiles.curselection()
    #print(selection[0])
    w=evt.widget
    if len(w.curselection())!=0 :
        index = int(w.curselection()[0])
        #value = w.get(index)
        img=Image.open(listPath[index])
        #img.resize((320,240))
        #img.zoom(320/img.width(), 240/img.height())
        photo = ImageTk.PhotoImage(img)
        dicimg['img1'] = photo
        cadre.image=photo
        
        cadre.create_image(400,320,image =photo) 
        #zoneImage.grid(row=2,column=5000,rowspan=2,columnspan=8,sticky=tk.E)#,padx=20,pady=20
        cadre.grid(row=2,column=500,rowspan=2,columnspan=30,sticky=tk.E)# padx=20,pady=20,
        zoneImage.grid(row=2,column=10,rowspan=2,columnspan=8,sticky=tk.E )
        cadre.config(scrollregion=cadre.bbox("all"))

listFiles.bind('<<ListboxSelect>>', onselect)  
 
#démarrer du réceptionnaire d'événements

c.create_window(0, 0,  window=f1)
f1.update_idletasks()
c.config(scrollregion=c.bbox("all"))#pour scrooll

root.mainloop()

