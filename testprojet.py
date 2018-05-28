# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

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

#########################################################  fenetre principale ##################################################
#créer la fenêtre d'application
root = tk.Tk()
#récupérer la taille d'écran d'ordi
ecran_width = root.winfo_screenwidth()*0.9
ecran_height = root.winfo_screenheight()*0.85
#définir la taille d'écran d'or comme la fenêtre d'application
#root.geometry(str(ecran_width)+'x'+str(ecran_height))
root.geometry('%dx%d+%d+%d' % (ecran_width, ecran_height, 1, 1))
#mettre le title et background pour l'application
root.title("Trainning Chemin de Fer")
root.resizable(width=False,height=False)
colorDefault="#F5F5DC" #bd=-2 #supprime bordure
#F5F5DC #beige

####################################################### frame entier ########################################################3
f=tk.Frame(root,bg=colorDefault ,width=ecran_width,height=ecran_height)
#scrollbar pour la fenetre pricipqle
#vsb = tk.Scrollbar(f, orient=tk.VERTICAL)
#vsb.grid(row=0, column=3, rowspan=4, sticky=tk.N+tk.S+tk.E)#
#vsb.grid(row=0,column=2,rowspan=5,sticky=tk.E+tk.N+tk.S)
#hsb = tk.Scrollbar(f, orient=tk.HORIZONTAL)
#hsb.grid(row=1,column=0,sticky=tk.W)

#hsb.grid(row=1, column=0,columnspan=5, sticky=tk.E+tk.W)
#c = tk.Canvas(f, yscrollcommand=vsb.set, xscrollcommand=hsb.set, width=ecran_width, height=ecran_height,bd=0,highlightthickness=0)
c=tk.Canvas(f,width=ecran_width, height=ecran_height,bd=0,highlightthickness=0,bg=colorDefault)
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
typeZone={"Titre","Paragraphe","Lettrine","Image"}
listPath=[]
drawRect=None
listFileWithActionRect={}
listActionRect={}
selectedAction=None
nameProjet='new'
selectedFile=None
listActionOfFile=None
currentSelectedFile=None
lastSelectedFile=None
currentSelectedAction=None
lastSelectedAction=None
numPage=0
countRect=1
rectSelect=None
xmlProjet=None

#################################################### toutes les fonctions  ####################################################
# fonction de buttonConfirm
def confirmer():
    global countRect
    listAction.insert(tk.END,var.get()+'-'+str(countRect))
    listActionRect[var.get()+'-'+str(countRect)]=drawRect.getCoordonnes()
    #listRect.append(dict1[var.get()+'-'+str(nbConfirm)])
    #listRect.append(var.get()+'-'+str(nbConfirm))
    #listRect.append(listActionRect[var.get()+'-'+str(nbConfirm)])
    #print("list"+str(listRect))
    #selection=currentSelectedFile
    #print("selection"+selection)
    listFileWithActionRect[currentSelectedFile]=listActionRect
    print("listFileToRect"+str(listFileWithActionRect))
    countRect+=1
    #print(drawRect.getCoordonnes())
    
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
	nbSelected=len(choice)
	#recupere le nom apartir du chemin
	for i in range (0,nbSelected):
		ext = os.path.splitext(choice[i])[1]
		nomExt=basename(choice[i])
		#nom=choice[i]
		nom=os.path.splitext(nomExt)[0]
		if ext == '.pdf':
			global nameProjet
			nameProjet=nom
			listImg = pti.pdfToPng(choice[i],nameProjet,30)#30==resolution base 90 resol haut
			size=len(listImg)
			for k in range (0, size) :
				listFiles.insert(listFiles.size(),basename(listImg[k])) 
				listPath.append(listImg[k])
		else :
			if nom!="": #sinon quand on clic sur parcourir mais qu'on ne choisi rien ça rajoute un espace blanc
				listFiles.insert(listFiles.size(),nom) 
				#listFiles.
				listPath.append(choice[i])
				# listFiles.TopIndex = listFiles.ListCount
	listFiles.select_set(0)    
	listInitial={}
	for file in listFiles.get(0,tk.END):
		listFileWithActionRect[file]=listInitial
	#print(str(listFileWithActionRect))
	resizeImg(0)
	recharge()
	#pour trier par ordre alpha et enlever les boutons            
#    listFiles.Sorted = True
#    listPath.sort()
#    j=0
#    while j < (listFiles.size() - 1) :
#        if (listFiles.get(j + 1,j+1) == listFiles.get(j,j)) :
#            listFiles.delete(j,j)
#            listPath.remove(listPath[j])
#            j = 0
#        else :
#            j += 1
    #listPath.reverse()??????????????????????????
    
            
 
# supprimer de la liste tout les fichiers
def delecteAll():
    listFiles.delete(0,tk.END) 
    listPath.clear()
    
def nextPage():  #a mettre dans enregister #voir si onSelect se fait tout seul
	global numPage
	if gs.projetExist(nameProjet):
		gs.update(nameProjet,str(int(numPage)+1))
	else :
		gs.writeInText(nameProjet,numPage+1)
	save()
	if int(numPage)<listFiles.size() :
		numPage=int(numPage)
		numPage += 1
		listFiles.selection_clear(0, tk.END)
		#if int(numPage)<listFiles.size() :
		listFiles.selection_set(int(numPage))
		#else:
		#	numPage=listFiles.size()-1
		#	listFiles.selection_set(int(numPage))
		resizeImg(int(numPage))
		recharge()
    
    
    
def lastPage():
	save()
	global numPage
	if gs.projetExist(nameProjet):
		gs.update(nameProjet,int(numPage)-1)
	else :
		gs.writeInText(nameProjet,int(numPage)-1)
	if int(numPage)>0 :
		numPage=int(numPage)
		numPage -= 1
		#print(numPage)
		listFiles.selection_clear(0, tk.END)
		listFiles.selection_set(int(numPage))
		resizeImg(int(numPage))
		recharge()


############################# Barre menu 
def newProjet():
	global numPage
	numPage=0
	chooseFile()
	global xmlProjet
	xmlProjet=xl.newProjet(nameProjet)
	page=xl.addPage('imageFromPdf/' + nameProjet+ '/'+ nameProjet + 'page-0.png',numPage, xmlProjet)
	xmlProjet=xl.endProjet(nameProjet,xmlProjet)
	gs.writeInText(nameProjet,numPage)


	'''
def projetToContinu(listProjet):   
    global nameProjet
    print('coucou')
    print(listProjet.curselection())
    nameProjet =listProjet.get(listProjet.curselection())
    global numPage
    numPage=gs.getAvancementProjet(nameProjet)
    listFiles.selection_set(numPage)
    #peut etre 
    '''

    
def continueProjet():
	rootpop = tk.Tk()
	rootpop.title("choisit le projet")
	listFrame=tk.Frame(rootpop)
	
	yDefilB = tk.Scrollbar(listFrame, orient='vertical')
	yDefilB.grid(row=0, column=1, sticky='ns')
	xDefilB = tk.Scrollbar(listFrame, orient='horizontal')
	xDefilB.grid(row=1, column=0, sticky='ew')
	
	listProjet = tk.Listbox(listFrame,
		xscrollcommand=xDefilB.set,
		yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE)    
	listProjet.grid(row=0)#'nsew'
	#listFiles.pack(side="left",fill="y")  
	xDefilB['command'] = listProjet.xview
	yDefilB['command'] = listProjet.yview    
	#global xl.xmlProjets
	#xl.duplicationProjet()
	#print(len(xl.listProjets))
	Projetlist=gs.getListProjet()
	for i in range (0 ,len(Projetlist)):
		listProjet.insert(1,Projetlist[i])
	listFrame.grid(row=0,pady=0,padx=15,sticky=tk.W+tk.N +tk.E)
	listProjet.grid(row=0,pady=0,padx=15,sticky=tk.W+tk.N +tk.E)


	def projetToContinu(evt):   
		global nameProjet
		#nameProjet=listProjet.curselection()
		#rootpop.destroy
		if len(listProjet.curselection())!=0:
			nameProjet =listProjet.get(listProjet.curselection()[0])
			global numPage
			numPage=gs.getAvancementProjet(nameProjet)
			print('le num de la page')
			print(numPage)
			listFiles.selection_set(int(numPage))
			reloadImg()
			resizeImg(int(numPage))
			global xmlProjet
			xmlProjet=xl.continuePoject(nameProjet)
			listInitial={}
			for file in listFiles.get(0,tk.END):
				listFileWithActionRect[file]=listInitial
			rootpop.destroy()
			rootpop.quit()
	
	listProjet.bind('<<ListboxSelect>>', projetToContinu)
	
	rootpop.mainloop()


def deepLearnig():
	from DrawOnImage import Segmentation as sg
	from DrawOnImage import Classification
	from DrawOnImage import drawOnImage
	from UseCheminDeFer import mainSeeResult
	#global sg.namePropjet
	sg.nameProjet=nameProjet
	save()
	root.destroy()
	rootpop.quit()

	
menubar=tk.Menu(root)
root.config(menu = menubar)
menufichier = tk.Menu(menubar,tearoff=0)
cheminDeFer = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label="Fichier", menu=menufichier)
menubar.add_cascade(label="Chemin de fer", menu=cheminDeFer)

menufichier.add_command(label="Nouveau Projet", command=newProjet)
menufichier.add_command(label="Continuer Projet", command = continueProjet) 
menufichier.add_separator() 
#menufichier.add_command(label="Enregistrer", command=save)
#menufichier.add_separator()
#menufichier.add_command(label="Quitter", command=root.destroy) 

cheminDeFer.add_command(label="Crée", command=deepLearnig)
############################################################ frame à gauche ####################################################
#f1=tk.Frame(root,bg='gold', width=ecran_width+1000, height=ecran_height)
#f1.config(width=ecran_width+1000, height=ecran_height)
#f1.grid(column=0,columnspan=1000,sticky=tk.E)
f1=tk.Frame(c,bg=colorDefault,height=ecran_height,width=ecran_width*0.4)
f1.grid(row=0,column=0,sticky=tk.S+tk.W+tk.N)

####################### label fichiers choisis
labelFichier=tk.Label(f1,text='Les fichiers choisis : ', bg=colorDefault)
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


def reloadImg() :
	listImgFromPdf = os.listdir('imgFromPdf/' + nameProjet)
	chrono = lambda v: os.path.getmtime(os.path.join('imgFromPdf/' + nameProjet, v))
	listImgFromPdf.sort(key = chrono)
	#print(listImgFromPdf)
	#print(len(listImgFromPdf))
	for k in range (0,len(listImgFromPdf)) :
		nomExt=basename(listImgFromPdf[k])
		nom=os.path.splitext(nomExt)[0]
		listFiles.insert(listFiles.size(), nom)
		listPath.append('imgFromPdf/' + nameProjet + '/' + listImgFromPdf[k])
	listFiles.select_set(0) 
  
      
################### frame pour les buttons parcourir, supprimer, vider
#zoneButton=tk.Frame(f1)
"""boutonParcourir=tk.Button(zoneButton,text="Parcourir",command=chooseFile).grid(row=1, column=0,sticky=tk.S,padx=40)
boutonSupprimer=tk.Button(zoneButton,text="Supprimer",command=delecteSelection).grid(row=1, column=1,sticky=tk.S,padx=40)
boutonSupprimer=tk.Button(zoneButton,text="Vider",command=delecteAll).grid(row=1, column=2,sticky=tk.S,ipadx=10,padx=40)"""
#zoneButton.grid(row=2,pady=5)

################## label pour la zone choisie
labelZoneChoix=tk.Label(f1,text='La zone choisie est : ', bg=colorDefault)#,  gold
labelZoneChoix.config(font=('Forte',18))
labelZoneChoix.grid(row=2, sticky=tk.W)

########################3 frame pour afficher les radiobuttons des choix
zoneRadioButton=tk.Frame(f1, bg=colorDefault)
a=0
for i,v in enumerate(typeZone):
    tk.Radiobutton(zoneRadioButton, text=v, variable=var, value = v, bg=colorDefault).grid(row=0, column=a,sticky=tk.W,padx=20)
    a+=1
zoneRadioButton.grid(row=3,sticky=tk.W,pady=5)

################ button pour comfirmer le choix avec la zone choisit sur image
buttonConfirm=tk.Button(f1,text="Confirmer",command=confirmer).grid(row=4,column=0,pady=5,sticky=tk.S)

################ listebox pour les Actions
def onSelectAction(evt):
    global selectedAction
    if selectedAction is not None:
        cadre.delete(selectedAction)
    selection=listAction.get(listAction.curselection())
    list1=[]
    list1=listActionRect[selection]
    selectedAction=cadre.create_rectangle(list1[0],list1[1],list1[0]+list1[2],list1[1]+list1[3],width=5)
    
labelAction=tk.Label(f1,text="Les actions : ", bg=colorDefault)
labelAction.config(font=('Forte',18))
labelAction.grid(row=5,column=0,pady=5,sticky=tk.W)
listAction = tk.Listbox(f1,width=70,height=8,selectmode=tk.MULTIPLE)
listAction.grid(row=6,column=0,pady=5)
listAction.bind('<<ListboxSelect>>', onSelectAction)  
for i in range(0,listAction.size()):
	listAction.selection_set(i)

# supprimer de la liste les fichiers selectionnés
def deleteSelection():#pour liste des actions
    global drawRect
    currentselection = listAction.curselection()
    selection=listAction.get(listAction.curselection())
    list1=[]
    list1=listActionRect[selection]
    idRect=list1[4]
    drawRect.deleteRect(idRect)
    listAction.delete(currentselection[0])
    #listPath.remove(selection[0])

#################fonctio de generation du xml
def save():
	global xmlProjet
	if not(xl.pageExist(nameProjet, str(numPage),xmlProjet)) :
		page = xl.addPage(str(listPath[int(numPage)]),numPage,xmlProjet)
		
		xmlProjet=xl.endProjet(nameProjet,xmlProjet)
	else :
		page = xl.foundPage(nameProjet, numPage,xmlProjet)
	sizelist=listAction.size()
	#w=evt.widget
	listItems=listAction.get(0,tk.END)
	"""for i in range(0,sizelist) :
		(typeAction,idAction) = list1[i].split("-")
		print("type"+typeAction)
		print("id"+idAction)"""
	#listActionRect[selection]
	for k in range (0,sizelist) :
		(typeAction,idAction) = listItems[k].split("-")
		#listAction.selection_set(k)
		#selection = listAction.curselection()
		#typeEl = selection[0]
		#index = int(listAction.curselection()[0])#.w
		#recuprerton rectangle d'index k
		listCoord=listActionRect[listItems[k]]
		typeEl=typeAction
		numElem=idAction #id
		posiX=listCoord[0]
		posiY=listCoord[1]
		widthEl=listCoord[2]
		heightEl=listCoord[3]
		
		if not(xl.reSave(nameProjet, numPage, numElem,xmlProjet)) :
			xl.addElement(typeEl, numElem, posiX, posiY, widthEl, heightEl,nameProjet, numPage, xmlProjet)
			xmlProjet=xl.endProjet(nameProjet,xmlProjet)
		else :
			if not(xl.sameType(nameProjet, numPage, numElem, typeEl,xmlProjet)):
				xmlProjet=xl.replace(nameProjet, numPage, numElem, typeEl,xmlProjet)
				xmlProjet=xl.endProjet(nameProjet,xmlProjet)
	#nextPage()



###fin barre menu qui a besoin de save
menufichier.add_command(label="Enregistrer", command=save)
menufichier.add_separator()
menufichier.add_command(label="Quitter", command=root.destroy) 


################ button pour confirmer le choix des element de la page ##############
fButtons=tk.Frame(f1, bg=colorDefault)
buttonDelete=tk.Button(fButtons,text="Supprimer",command=deleteSelection).grid(row=0,column=0,padx=40,sticky=tk.S)
buttonLast=tk.Button(fButtons,text="Précédent",command=lastPage).grid(row=0,column=1,padx=40,sticky=tk.S)
buttonSave=tk.Button(fButtons,text="Enregistrer et Suivant",command=nextPage).grid(row=0,column=2,padx=40,sticky=tk.S)
#buttonSave=tk.Button(fButtons,text="Suivant",command=suivant).grid(row=0,column=1,padx=50,sticky=tk.S)
fButtons.grid(row=7,column=0,pady=20)

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
fImg=tk.Frame(c,width=ecran_width*0.6,height=ecran_height, bg=colorDefault)
fImg.grid(row=0,column=1,sticky=tk.N+tk.S)
cadre=tk.Canvas(c, bg=colorDefault, bd=-2)
cadre.grid(row=0,column=1)

"""def selectByButton():
    global numPage
    resizeImg(numPage)
    dicimg = {}
    #pk supprimer des choses?
    img=Image.open(listPath[numPage])
    wd,hg=img.size
    mwd=ecran_width
    mhg=ecran_height
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
    drawRect=rect.CanvasEventsDemo(cadre)
    cadre.bind('<ButtonPress-1>', drawRect.onStart)  
    cadre.bind('<B1-Motion>',     drawRect.onGrow)   
    cadre.bind('<Double-1>',      drawRect.onClear)  
    cadre.bind('<ButtonPress-3>', drawRect.onMove)   
    cadre.bind('<ButtonRelease-1>', drawRect.onFinal)
    gs.update(nameProjet,numPage)"""
    
def resizeImg(index):
    global drawRect,newImg,currentSelectedFile,lastSelectedFile,listActionRect
    dicimg={}
    img=Image.open(listPath[int(index)])
    #img.resize((320,240))
    #img.zoom(320/img.width(), 240/img.height())
    wd,hg=img.size
    mwd=ecran_width
    mhg=ecran_height
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
    gs.update(nameProjet,numPage)
 
def recharge():
	global currentSelectedFile,lastSelectedFile,listActionRect
	#global selectedAction
	if currentSelectedFile is not None:
		lastSelectedFile=currentSelectedFile
		currentSelectedFile=listFiles.get(listFiles.curselection())
		if lastSelectedFile!=currentSelectedFile:
			listAction.delete(0,tk.END)
			newListActionRect={}
			listActionRect=newListActionRect
			#print(str(listActionRect))
			#mapAction=getMapActionRect(currentSelectedFile)
			mapActionRect=listFileWithActionRect[currentSelectedFile]
			if mapActionRect is not None :
				print("mapActionRect isn't none")
				for key in mapActionRect :
					listAction.insert(tk.END,key)
                    #print(mapActionRect[key])
					listActionRect[key]=mapActionRect[key]
                    #print(str(listActionRect[key]))
			#else:
			#    print("is none")
	else:
		currentSelectedFile=listFiles.get(listFiles.curselection())

def onselect(evt):
	global drawRect,newImg,currentSelectedFile,lastSelectedFile,listActionRect
	#cadre=tk.Canvas(c,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=ecran_width-600,height=ecran_height-25,bg="black")#,bg="black"
	#cadre=tk.Label(f,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=320,height=240,bg="green")
	#cadre=tk.Canvas(root,width=ecran_width-500,height=ecran_height,bg="black")
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
		resizeImg(index)
		recharge()
		"""if currentSelectedFile != listFiles.get(listFiles.curselection()):
				listAction.delete(0,tk.END)
				listAction.insert(tk.END,var.get()+'-'+str(nbConfirm))
				print("different")"""
		"""list=[]
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

listFiles.bind('<<ListboxSelect>>', onselect)  #green
#buttonLast.bind('<Button-1>', onselect)
#buttonSave.bind('<Button-1>', onselect)
#démarrer du réceptionnaire d'événements

#c.create_window(0, 0,  window=f)

#f.update_idletasks()
#f1.update_idletasks()
c.config(scrollregion=c.bbox("all"))#pour scrooll
f.grid(row=0,column=0,sticky=tk.W+tk.N)
root.mainloop()

