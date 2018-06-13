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
#créer la fenêtre d'application
root = tk.Tk()
#récupérer la taille d'écran d'ordi
screen_width = root.winfo_screenwidth()*0.9
screen_height = root.winfo_screenheight()*0.85
#définir la taille d'écran d'or comme la fenêtre d'application
#root.geometry(str(screen_width)+'x'+str(screen_height))
root.geometry('%dx%d+%d+%d' % (screen_width, screen_height, 1, 1))
#mettre le title et background pour l'application
root.title("Trainning Chemin de Fer")
#fixer la taille de fenêtre, on peut pas agrandir et réduire la fênetre
root.resizable(width=False,height=False)
#colorDefault="#F5F5DC" #F5F5DC #beige #bd=-2 #supprime bordure
func=co.FunctionCommun()
func.setSizeScreen(screen_width,screen_height)

####################################################### frame entier ########################################################3
f=tk.Frame(root,bg=func.colorDefault ,width=screen_width,height=screen_height)
#scrollbar pour la fenetre pricipqle
#vsb = tk.Scrollbar(f, orient=tk.VERTICAL)
#vsb.grid(row=0, column=3, rowspan=4, sticky=tk.N+tk.S+tk.E)#
#vsb.grid(row=0,column=2,rowspan=5,sticky=tk.E+tk.N+tk.S)
#hsb = tk.Scrollbar(f, orient=tk.HORIZONTAL)
#hsb.grid(row=1,column=0,sticky=tk.W)

#hsb.grid(row=1, column=0,columnspan=5, sticky=tk.E+tk.W)
#c = tk.Canvas(f, yscrollcommand=vsb.set, xscrollcommand=hsb.set, width=screen_width, height=screen_height,bd=0,highlightthickness=0)
c=tk.Canvas(f,width=screen_width, height=screen_height,bd=0,highlightthickness=0,bg=func.colorDefault)
#c.yview_moveto(1)
#c.xview_moveto(1)
c.grid(row=0, column=0, sticky=tk.W+tk.N + tk.S)#,sticky="news"
#vsb.config(command=c.yview)#c.yview
#hsb.config(command=c.xview)
#root.grid_rowconfigure(0, weight=1)
#root.grid_columnconfigure(0, weight=1)

######################################################## variable global #######################################################
var=tk.StringVar()
var.set("Paragraphe")
#################################################### toutes les fonctions  ####################################################

	
menubar=tk.Menu(root)
root.config(menu = menubar)
menufichier = tk.Menu(menubar,tearoff=0)
cheminDeFer = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label="Fichier", menu=menufichier)
menubar.add_cascade(label="Chemin de fer", menu=cheminDeFer)


def continueProj():
	func.continueProjet()
	if func.projetIsChoose():
		cheminDeFer.entryconfig(0, state =tk.ACTIVE)
		menufichier.entryconfig(3, state =tk.ACTIVE)
		buttonLast.entryconfig(state =tk.ACTIVE)
		buttonSave.entryconfig(state =tk.ACTIVE)
		
def newProj():
	func.newProjet()
	if func.projetIsChoose():
		cheminDeFer.entryconfig(0, state =tk.ACTIVE)
		menufichier.entryconfig(3, state =tk.ACTIVE)
		buttonLast.entryconfig(0, state =tk.ACTIVE)
		buttonSave.entryconfig(0, state =tk.ACTIVE)

 
#menufichier.add_command(label="Enregistrer", command=save)
#menufichier.add_separator()
#menufichier.add_command(label="Quitter", command=root.destroy) 


cheminDeFer.add_command(label="Crée", command=func.deepLearnig, state =tk.DISABLED)

############################################################ frame à gauche ####################################################
#f1=tk.Frame(root,bg='gold', width=screen_width+1000, height=screen_height)
#f1.config(width=screen_width+1000, height=screen_height)
#f1.grid(column=0,columnspan=1000,sticky=tk.E)
f1=tk.Frame(c,bg=func.colorDefault,height=screen_height,width=screen_width*0.4)
f1.grid(row=0,column=0,sticky=tk.S+tk.W+tk.N)

####################### label fichiers choisis
labelFichier=tk.Label(f1,text='Les fichiers choisis : ', bg=func.colorDefault)
labelFichier.config(font=('Arial',18))
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
     yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE,exportselection=0)
listFiles.grid(row=0)#'nsew'
func.setListBoxFiles(listFiles)
#listFiles.pack(side="left",fill="y")  
xDefilB['command'] = listFiles.xview
yDefilB['command'] = listFiles.yview
listFrame.grid(row=1,pady=5,padx=20,sticky=tk.W)


################## label pour la zone choisie
labelZoneChoix=tk.Label(f1,text='La zone choisie est : ', bg=func.colorDefault)#,  gold
labelZoneChoix.config(font=('Arial',18))
labelZoneChoix.grid(row=2, sticky=tk.W)

def setVar():
	func.setVar(var.get())
########################3 frame pour afficher les radiobuttons des choix
zoneRadioButton=tk.Frame(f1, bg=func.colorDefault)
a=0
for i,v in enumerate(func.typeZone):
    tk.Radiobutton(zoneRadioButton, text=v, variable=var, value = v, bg=func.colorDefault,command=setVar).grid(row=0, column=a,sticky=tk.W,padx=20)
    a+=1
zoneRadioButton.grid(row=3,sticky=tk.W,pady=5)

################ button pour comfirmer le choix avec la zone choisit sur image
buttonConfirm=tk.Button(f1,text="Confirmer",command=func.confirmer).grid(row=4,column=0,pady=5,sticky=tk.S)

################ listebox pour les Actions

# listFiles = tk.Listbox(listFrame,
     # xscrollcommand=xDefilB.set,
     # yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE,exportselection=0)
# listFiles.grid(row=0)#'nsew'
# func.setListBoxFiles(listFiles)
##listFiles.pack(side="left",fill="y")  
# xDefilB['command'] = listFiles.xview
# yDefilB['command'] = listFiles.yview
# listFrame.grid(row=1,pady=5,padx=20,sticky=tk.W)  
labelAction=tk.Label(f1,text="Les actions : ", bg=func.colorDefault)
labelAction.config(font=('Arial',18))
labelAction.grid(row=5,column=0,pady=5,sticky=tk.W)



listFrame2=tk.Frame(f1)
###################### scrollbar vertical et horizontal
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

listAction.bind('<<ListboxSelect>>', func.onSelectAction)  
for i in range(0,listAction.size()):
	listAction.selection_set(i)
func.setListBoxAction(listAction)






################ button pour confirmer le choix des element de la page ##############
fButtons=tk.Frame(f1, bg=func.colorDefault)
buttonDeselect=tk.Button(fButtons,text="Deselect/Select all",command=func.de_select, state =tk.DISABLED)
buttonDelete=tk.Button(fButtons,text="Supprimer",command=func.deleteSelection).grid(row=0,column=1,padx=20,sticky=tk.S)
buttonLast=tk.Button(fButtons,text="Précédent",command=func.lastPage, state =tk.DISABLED)
buttonSave=tk.Button(fButtons,text="Enregistrer et Suivant",command=func.nextPage, state =tk.DISABLED)
buttonLast.grid(row=0,column=2,padx=20,sticky=tk.S)
#buttonSave=tk.Button(fButtons,text="Suivant",command=suivant).grid(row=0,column=1,padx=50,sticky=tk.S)
buttonDeselect.grid(row=0,column=0,padx=20,sticky=tk.S)
buttonSave.grid(row=0,column=3,padx=20,sticky=tk.S)
fButtons.grid(row=7,column=0,pady=20)


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
fImg=tk.Frame(c,width=screen_width*0.6,height=screen_height, bg=func.colorDefault)
fImg.grid(row=0,column=1,sticky=tk.N+tk.S)
cadre=tk.Canvas(c, bg=func.colorDefault, bd=-2)
cadre.grid(row=0,column=1)
func.setCadre(cadre)

 
""" 
def resizeImg(index):
    global drawRect,newImg,currentSelectedFile,lastSelectedFile,listActionRect
    dicimg={}
    img=Image.open(listPath[int(index)])
    #img.resize((320,240))
    #img.zoom(320/img.width(), 240/img.height())
    wd,hg=img.size
    mwd=screen_width
    mhg=screen_height
    if wd>mwd :
        scale= 1.0*wd/mwd
        newImg=img.resize((int(wd/scale),int(hg/scale)),Image.ANTIALIAS)
        cadre.config(width=wd/scale,height=hg/scale)
        photo = ImageTk.PhotoImage(newImg)
        dicimg['img1'] = photo
        cadre.image=photo
        cadre.create_image(0,0,image=photo,anchor="nw") 
    elif hg > mhg:
        scale = 1.0*hg/mhg
        newImg = img.resize((int(wd/scale),int(hg/scale)), Image.ANTIALIAS)
        cadre.config(width=wd/scale,height=hg/scale)
        photo = ImageTk.PhotoImage(newImg)
        dicimg['img1'] = photo
        cadre.image=photo
        cadre.create_image(0,0,image=photo,anchor="nw") 
    else:
        cadre.config(width=wd,height=hg)
        photo = ImageTk.PhotoImage(img)
        dicimg['img1'] = photo
        cadre.image=photo
        cadre.create_image(0,0,image=photo,anchor="nw") 
    #newImg.save(listPath[index])  
    #newImg.close() 
    if currentSelectedFile is None:   
        currentSelectedFile=listFiles.get(listFiles.curselection())
        fileChange=False
    else:
        if lastSelectedFile!=currentSelectedFile:
            fileChange=True
        else:
            fileChange=False    
    drawRect=rect.CanvasEventsDemo(cadre,listAction,listActionRect,listFileWithActionRect,currentSelectedFile,fileChange)
    cadre.bind('<ButtonPress-1>', drawRect.leftOnStart)  
    cadre.bind('<B1-Motion>',     drawRect.leftOnGrow)   
    cadre.bind('<Double-1>',      drawRect.leftOnClear)
    cadre.bind('<ButtonRelease-1>', drawRect.leftOnFinal)
    cadre.bind('<ButtonPress-3>', drawRect.rightOnStart)
    cadre.bind('<B3-Motion>',     drawRect.rightOnMove)
    cadre.bind('<ButtonRelease-3>',drawRect.rightOnFinal)
    gs.update(nameProjet,numPage)"""
 


"""def onselect(evt):
	global drawRect,newImg,currentSelectedFile,lastSelectedFile,listActionRect
	#cadre=tk.Canvas(c,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=screen_width-600,height=screen_height-25,bg="black")#,bg="black"
	#cadre=tk.Label(f,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=320,height=240,bg="green")
	#cadre=tk.Canvas(root,width=screen_width-500,height=screen_height,bg="black")
	#dicimg = {}
	#selection = listFiles.curselection()
	#print(selection[0])
	w=evt.widget
	if len(w.curselection())!=0 :
		index = int(w.curselection()[0])
		global numPage
		numPage=index
		#value = w.get(index)
		#print(index)
		recharge()
		resizeImg(index)
		selectAll()
		
		if currentSelectedFile != listFiles.get(listFiles.curselection()):
			listAction.delete(0,tk.END)
			listAction.insert(tk.END,var.get()+'-'+str(nbConfirm))
			print("different")
		list=[]
		list=dict[selection]
		selectedAction=cadre.create_rectangle(list[0],list[1],list[0]+list[2],list[1]+list[3],width=5)"""
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
#def printList(event):  
#    print(listFiles.get(listFiles.curselection()))  
listFiles.bind('<<ListboxSelect>>', func.onselect)  #green
#listFiles.bind('<Double-Button-1>',func.openModif)  #####a virer

#buttonLast.bind('<Button-1>', onselect)
#buttonSave.bind('<Button-1>', onselect)
#démarrer du réceptionnaire d'événements

#c.create_window(0, 0,  window=f)

#f.update_idletasks()
#f1.update_idletasks()
c.config(scrollregion=c.bbox("all"))#pour scrooll
f.grid(row=0,column=0,sticky=tk.W+tk.N)
root.mainloop()

