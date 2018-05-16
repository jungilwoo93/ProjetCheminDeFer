# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf
from PIL import Image, ImageFont, ImageDraw, ImageTk
from os.path import basename
import DrawRect as rect
import xml as xl
#########################################################  fenetre principale ##################################################
#créer la fenêtre d'application
root = tk.Tk()
#récupérer la taille d'écran d'ordi
ecran_width = root.winfo_screenwidth()
ecran_height = root.winfo_screenheight()-75
#définir la taille d'écran d'or comme la fenêtre d'application
#root.geometry(str(ecran_width)+'x'+str(ecran_height))
root.geometry('%dx%d+%d+%d' % (ecran_width, ecran_height, 1, 1))
#mettre le title et background pour l'application
root.title("Projet")
####################################################### frame entier ########################################################3
f=tk.Frame(root,bg="green",width=ecran_width,height=ecran_height)
#scrollbar pour la fenetre pricipqle
vsb = tk.Scrollbar(f, orient=tk.VERTICAL)
#vsb.grid(row=0, column=3, rowspan=4, sticky=tk.N+tk.S+tk.E)#
vsb.grid(row=0,column=2,rowspan=5,sticky=tk.E+tk.N+tk.S)
hsb = tk.Scrollbar(f, orient=tk.HORIZONTAL)
#hsb.grid(row=1,column=0,sticky=tk.W)

hsb.grid(row=1, column=0,columnspan=5, sticky=tk.E+tk.W)
c = tk.Canvas(f, yscrollcommand=vsb.set, xscrollcommand=hsb.set, width=ecran_width-25, height=ecran_height-25,bd=0,highlightthickness=0)
#c.yview_moveto(1)
#c.xview_moveto(1)
c.grid(row=0, column=0, sticky=tk.W+tk.N + tk.S)#,sticky="news"
vsb.config(command=c.yview)#c.yview
hsb.config(command=c.xview)
#root.grid_rowconfigure(0, weight=1)
#root.grid_columnconfigure(0, weight=1)

######################################################## variable global #######################################################
var=tk.StringVar()
var.set("Paragraphe")
typeZone={"Titre","Paragraphe","Lettrine","Image"}
listPath=[]

#################################################### toutes les fonctions  ####################################################
# fonction de buttonConfirm
def confirmer():
    listAction.insert(tk.END,var.get())
    
# parcours choit du fichier
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
    #pour trier par ordre alpha et enlever les boutons            
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
            
# supprimer de la liste les fichiers selectionnés
def delecteSelection():
    selection = listFiles.curselection()
    listFiles.delete(selection[0])
    listPath.remove(selection[0])
 
# supprimer de la liste tout les fichiers
def delecteAll():
    #cs=listFiles.curselection()
    #listFiles.delete(0,cs[0] -1)
    listFiles.delete(0,tk.END) 
    listPath.clear()

############################################################ frame à gauche ####################################################
#f1=tk.Frame(root,bg='gold', width=ecran_width+1000, height=ecran_height)
#f1.config(width=ecran_width+1000, height=ecran_height)
#f1.grid(column=0,columnspan=1000,sticky=tk.E)
f1=tk.Frame(c,bg='gold')

####################### label fichiers choisis
labelFichier=tk.Label(f1,text='Les fichiers choisis : ')
labelFichier.config(font=('Forte',18))
labelFichier.grid(row=0,sticky=tk.W,pady=5)

################################ frame pour listeBox et leur scrollbar
listFrame=tk.Frame(f1)

###################### scrollbar vertical et horizontal
yDefilB = tk.Scrollbar(listFrame, orient='vertical')
yDefilB.grid(row=0, column=1, sticky='ns')
xDefilB = tk.Scrollbar(listFrame, orient='horizontal')
xDefilB.grid(row=1, column=0, sticky='ew')

##################### listBox pour afficher les fichiers choisis
listFiles = tk.Listbox(listFrame,
     xscrollcommand=xDefilB.set,
     yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE)
listFiles.grid(row=0)#'nsew'
#listFiles.pack(side="left",fill="y")  
xDefilB['command'] = listFiles.xview
yDefilB['command'] = listFiles.yview
listFrame.grid(row=1,pady=5,padx=20,sticky=tk.W)

################### frame pour les buttons parcourir, supprimer, vider
zoneButton=tk.Frame(f1)
boutonParcourir=tk.Button(zoneButton,text="Parcourir",command=chooseFile).grid(row=1, column=0,sticky=tk.S,padx=40)
boutonSupprimer=tk.Button(zoneButton,text="Supprimer",command=delecteSelection).grid(row=1, column=1,sticky=tk.S,padx=40)
boutonSupprimer=tk.Button(zoneButton,text="Vider",command=delecteAll).grid(row=1, column=2,sticky=tk.S,ipadx=10,padx=40)
zoneButton.grid(row=2,pady=5)

################## label pour la zone choisie
labelZoneChoix=tk.Label(f1,text='La zone choisi est : ')
labelZoneChoix.config(font=('Forte',18))
labelZoneChoix.grid(row=3, sticky=tk.W)

########################3 frame pour afficher les radiobuttons des choix
zoneRadioButton=tk.Frame(f1)
a=0
for i,v in enumerate(typeZone):
    tk.Radiobutton(zoneRadioButton, text=v, variable=var, value = v).grid(row=a, column=0,sticky=tk.W)
    a+=1
zoneRadioButton.grid(row=4,sticky=tk.W,pady=5)

################ button pour comfirmer le choix avec la zone choisit sur image
buttonConfirm=tk.Button(f1,text="Confirmer",command=confirmer).grid(row=5,column=0,pady=5,sticky=tk.S)

################ listebox pour les Actions
labelAction=tk.Label(f1,text="Les actions : ")
labelAction.config(font=('Forte',18))
labelAction.grid(row=6,column=0,pady=5,sticky=tk.W)
listAction = tk.Listbox(f1,width=70,height=8)
listAction.grid(row=7,column=0,pady=5)
f1.grid(row=0,column=0)


#################fonctio de generation du xml
def save():
    page = xl.newPage('nom Page')
    sizelist=listAction.size()
    #k=0
    #w=evt.widget
    for k in range (0,sizelist) :
        #if len(w.curselection())!=0 :
        selection = listAction.curselection()
        typeEl = selection[0]
        index = int(listAction.curselection()[0])#.w
        posiX=1
        posiY=1
        widthEl=1
        heightEl=1
        xl.addElement(typeEl, posiX, posiY, widthEl, heightEl,page)
        
    
################ button pour confirmer le choix des element de la page
buttonSave=tk.Button(f1,text="Enregistrer",command=save).grid(row=7,column=0,pady=5,sticky=tk.S)



############################################### frame à droite pour afficher l'image ##########################################
#f0 = tk.Frame(f1)
#f0.grid(fill=tk.BOTH)
#f0.pack(fill=tk.BOTH)
#c.grid(sticky=tk.E)
#c.create_window(0, 0,  window=f1)

 
#c.create_window(0, 0,  window=f0)
#f0.update_idletasks()
#c.config(scrollregion=c.bbox("all"))#a mettre a la fin

#afficher image dés qu'on selectionne un element
#zoneImage=tk.Frame(root,bg="black")
#zoneImage.grid(row=2,column=10,rowspan=2,columnspan=8,sticky=tk.E )
cadre=tk.Canvas(c,width=ecran_width-600,height=ecran_height-25)
cadre.grid(row=0,column=1,sticky=tk.S+tk.N)

def onselect(evt):
    #cadre=tk.Canvas(c,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=ecran_width-600,height=ecran_height-25,bg="black")#,bg="black"
    #cadre=tk.Label(f,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=320,height=240,bg="green")
    #cadre=tk.Canvas(root,width=ecran_width-500,height=ecran_height,bg="black")
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
        a=rect.CanvasEventsDemo(cadre)
        cadre.bind('<ButtonPress-1>', a.onStart)  
        cadre.bind('<B1-Motion>',     a.onGrow)   
        cadre.bind('<Double-1>',      a.onClear)  
        cadre.bind('<ButtonPress-3>', a.onMove)   
        #zoneImage.grid(row=2,column=5000,rowspan=2,columnspan=8,sticky=tk.E)#,padx=20,pady=20
        #cadre.grid(row=2,column=500,rowspan=2,columnspan=30,sticky=tk.E)# padx=20,pady=20,
        #cadre.grid(row=0,column=1,sticky=tk.S)
        #cadre.create_window(0, 0,  window=f)
        #cadre.create_window(0,0,window=f1)
        #c.create_window(1,0,window=cadre)
        #f.update_idletasks()
        #f1.grid(row=0,column=0,sticky=tk.W+tk.S)
        
        #cadre.update_idletasks()
        #zoneImage.grid(row=0,column=1,rowspan=2,columnspan=8,sticky=tk.E )
        #cadre.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        #cadre.config(scrollregion=cadre.bbox("all"))

listFiles.bind('<<ListboxSelect>>', onselect)  
 
#démarrer du réceptionnaire d'événements

#c.create_window(0, 0,  window=f)

#f.update_idletasks()
#f1.update_idletasks()
c.config(scrollregion=c.bbox("all"))#pour scrooll
f.grid(row=0,column=0,sticky=tk.W+tk.N)
root.mainloop()

