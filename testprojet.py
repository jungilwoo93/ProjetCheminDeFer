# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""
#### libraries à importer
import tkinter as tk
import tkinter.filedialog as tf
from PIL import Image, ImageFont, ImageDraw, ImageTk
import os
from os.path import basename

#### nos autre fichier
import DrawRect as rect
import creatXml as xl
import gestionSave as gs
import pdfToImg as pti
import commun as co

#########################################################  fenetre principale ##################################################
root = tk.Tk() #créer la fenêtre d'application
#récupérer la taille d'écran d'ordi
screen_width = root.winfo_screenwidth()*0.9
screen_height = root.winfo_screenheight()*0.85
root.geometry('%dx%d+%d+%d' % (screen_width, screen_height, 1, 1)) #définir la taille d'écran d'or comme la fenêtre d'application
root.title("Trainning Chemin de Fer") #mettre le title et background pour l'application
root.resizable(width=False,height=False) #fixer la taille de fenêtre, on peut pas agrandir et réduire la fênetre
func=co.FunctionCommun() #initialiser commun.py pour utiliser les fonctions
func.setSizeScreen(screen_width,screen_height)

####################################################### frame entier ########################################################3
f=tk.Frame(root,bg=func.colorDefault ,width=screen_width,height=screen_height)
c=tk.Canvas(f,width=screen_width, height=screen_height,bd=0,highlightthickness=0,bg=func.colorDefault)
c.grid(row=0, column=0, sticky=tk.W+tk.N + tk.S)

######################################################## variable global #######################################################
var=tk.StringVar() #valeur pour les radiobuttons
var.set("Paragraphe") #valeur radiobutton par default 

######################menu bar###################
menubar=tk.Menu(root)
root.config(menu = menubar)
menufichier = tk.Menu(menubar,tearoff=0)
cheminDeFer = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label="Fichier", menu=menufichier)
menubar.add_cascade(label="Chemin de fer", menu=cheminDeFer)




##########barre de menu
#menufichier.add_command(label="Nouveau Projet", command=newProj)
#menufichier.add_command(label="Continuer Projet", command = continueProj) 
#menufichier.add_separator()
#menufichier.add_command(label="Enregistrer", command=func.save, state =tk.DISABLED)
#menufichier.add_separator()
#menufichier.add_command(label="Quitter", command=root.destroy) 
cheminDeFer.add_command(label="Crée", command=func.deepLearnig, state =tk.DISABLED)

############################################################ frame à gauche ####################################################
f1=tk.Frame(c,bg=func.colorDefault,height=screen_height,width=screen_width*0.4)
f1.grid(row=0,column=0,sticky=tk.S+tk.W+tk.N)

####################### label fichiers choisis
labelFichier=tk.Label(f1,text='Les fichiers choisis : ', bg=func.colorDefault)
labelFichier.config(font=('Arial',18))
labelFichier.grid(row=0,sticky=tk.W,pady=5)

################################ frame pour listeBox et leur scrollbar
listFrame=tk.Frame(f1)

###################### scrollbar vertical et horizontal pour listbox listbox Files
yDefilB = tk.Scrollbar(listFrame, orient='vertical')
yDefilB.grid(row=0, column=1, sticky='ns')
xDefilB = tk.Scrollbar(listFrame, orient='horizontal')
xDefilB.grid(row=1, column=0, sticky='ew')

##################### listBox pour afficher les fichiers choisis
listFiles = tk.Listbox(listFrame,
     xscrollcommand=xDefilB.set,
     yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE,exportselection=0)
listFiles.grid(row=0)
func.setListBoxFiles(listFiles) #mettre listbox Files dans commun.py pour qu'on puisse l'utiliser
listFiles.bind('<<ListboxSelect>>', func.onselect) #evenement de listFiles #quand on selectionne un ficher
xDefilB['command'] = listFiles.xview
yDefilB['command'] = listFiles.yview
listFrame.grid(row=1,pady=5,padx=20,sticky=tk.W)


################## label pour la zone choisie
labelZoneChoix=tk.Label(f1,text='La zone choisie est : ', bg=func.colorDefault)#,  gold
labelZoneChoix.config(font=('Arial',18))
labelZoneChoix.grid(row=2, sticky=tk.W)

# fonction de radiobutton pour mettre la variable dans commun.py et l'utiliser
def setVar():
	func.setVar(var.get())
######################## frame pour afficher les radiobuttons des choix
zoneRadioButton=tk.Frame(f1, bg=func.colorDefault)
a=0
for i,v in enumerate(func.typeZone):
    tk.Radiobutton(zoneRadioButton, text=v, variable=var, value = v, bg=func.colorDefault,command=setVar).grid(row=0, column=a,sticky=tk.W,padx=20)
    a+=1
zoneRadioButton.grid(row=3,sticky=tk.W,pady=5)

################ button pour comfirmer le choix avec la zone choisit sur image
buttonConfirm=tk.Button(f1,text="Confirmer",command=func.confirmer).grid(row=4,column=0,pady=5,sticky=tk.S)

################ listebox pour les Actions
labelAction=tk.Label(f1,text="Les actions : ", bg=func.colorDefault)
labelAction.config(font=('Arial',18))
labelAction.grid(row=5,column=0,pady=5,sticky=tk.W)

listFrame2=tk.Frame(f1)
###################### scrollbar vertical et horizontal pour listbox Action
yDefilB = tk.Scrollbar(listFrame2, orient='vertical')
yDefilB.grid(row=0, column=1, sticky='ns')
xDefilB = tk.Scrollbar(listFrame2, orient='horizontal')
xDefilB.grid(row=1, column=0, sticky='ew')

listAction = tk.Listbox(listFrame2,
     xscrollcommand=xDefilB.set,
     yscrollcommand=yDefilB.set,width=70,height=7,selectmode=tk.MULTIPLE)
listAction.grid(row=0)
xDefilB['command'] = listAction.xview
yDefilB['command'] = listAction.yview
listFrame2.grid(row=6,column=0,pady=4, padx=20, sticky=tk.W)

#listAction.grid(row=6,column=0,pady=5)


fButtons=tk.Frame(f1, bg=func.colorDefault)
buttonDelete=tk.Button(fButtons,text="Supprimer",command=func.deleteSelection, state =tk.DISABLED)

def deSelect():
	func.de_select()
	print(len(listAction.curselection()))
	if len(listAction.curselection())!=0:
		buttonDelete.config(state =tk.ACTIVE)
	else:
		buttonDelete.config(state =tk.DISABLED)

################ button pour confirmer le choix des element de la page ##############

buttonDeselect=tk.Button(fButtons,text="Deselect/Select all",command=func.de_select, state =tk.DISABLED)
buttonLast=tk.Button(fButtons,text="Précédent",command=func.lastPage, state =tk.DISABLED)
buttonSave=tk.Button(fButtons,text="Enregistrer et Suivant",command=func.nextPage, state =tk.DISABLED)

buttonLast.grid(row=0,column=2,padx=20,sticky=tk.S)
buttonDeselect.grid(row=0,column=0,padx=20,sticky=tk.S)
buttonDelete.grid(row=0,column=1,padx=20,sticky=tk.S)
buttonSave.grid(row=0,column=3,padx=20,sticky=tk.S)
fButtons.grid(row=7,column=0,pady=20)



def onSelectAction(event):
	func.onSelectAction(event)
	if len(listAction.curselection())!=0:
		buttonDelete.config(state =tk.ACTIVE)
	else:
		buttonDelete.config(state =tk.DISABLED)

listAction.bind('<<ListboxSelect>>', onSelectAction) #evenement de listAction #quand on selectionne une/des action(s)
for i in range(0,listAction.size()):
	listAction.selection_set(i)
func.setListBoxAction(listAction)#mettre listbox Action dans commun.py pour qu'on puisse l'utiliser


def continueProj():
	func.continueProjet()
	if func.projetIsChoose():
		cheminDeFer.entryconfig(0, state =tk.ACTIVE)
		menufichier.entryconfig(3, state =tk.ACTIVE)
		global buttonLast, buttonSave, buttonDeselect
		buttonLast.config(state =tk.ACTIVE)
		buttonSave.config(state =tk.ACTIVE)
		buttonDeselect.config(state =tk.ACTIVE)
		
def newProj():
	func.newProjet()
	if func.projetIsChoose():
		cheminDeFer.entryconfig(0, state =tk.ACTIVE)
		menufichier.entryconfig(3, state =tk.ACTIVE)
		global buttonLast, buttonSave,buttonDeselect
		buttonLast.config(state =tk.ACTIVE)
		buttonSave.config(state =tk.ACTIVE)
		buttonDeselect.config(state =tk.ACTIVE)


##########barre de menu
menufichier.add_command(label="Nouveau Projet", command=newProj)
menufichier.add_command(label="Continuer Projet", command = continueProj) 
menufichier.add_separator()
menufichier.add_command(label="Enregistrer", command=func.save, state =tk.DISABLED)
menufichier.add_separator()
menufichier.add_command(label="Quitter", command=root.destroy) 



############################################### frame à droite pour afficher l'image ##########################################
fImg=tk.Frame(c,width=screen_width*0.6,height=screen_height, bg=func.colorDefault)
fImg.grid(row=0,column=1,sticky=tk.N+tk.S)
cadre=tk.Canvas(c, bg=func.colorDefault, bd=-2)
cadre.grid(row=0,column=1)

func.setCadre(cadre)


listFiles.bind('<<ListboxSelect>>', func.onselect)  #green



c.config(scrollregion=c.bbox("all"))#pour scrooll
f.grid(row=0,column=0,sticky=tk.W+tk.N)
root.mainloop()

