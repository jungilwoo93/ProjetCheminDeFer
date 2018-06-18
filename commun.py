# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""
#ce fichier contient les fonctions communes pour la fenêtre de WinTraining.py et WinModification.py
#la conversion de pdf en image png et le traitement d'image sont trop lents, peut être on peut ajouter une barre de progression
#ajouter un button pour afficher tous les rectangles ou les cacher, au lieu de selectionner tous pour afficher
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageFont, ImageDraw, ImageTk
import os
from os.path import basename
import tkinter.filedialog as tf
from lxml import etree

#nos autre fichiers
import DrawRect as rect
import creatXml as xl
import gestionSave as gs
import pdfToImg as pti
import editImag as ei


class FunctionCommun:
	#### variable ####
	var=None #stocker la variable de radiobutton
	typeZone={"Titre","Paragraphe","Lettrine","Image"} 
	colorDefault="#F5F5DC" #couleur beige par défault
	screen_width=None #transferer la taille d'ecran de WinTraining.py et WinModification.py pour qu'on peut utiliser dans commun.py
	screen_height=None
	listPath=[] #stocker tous les chemins de d'images du projet
	drawRect=None #creer la classe DrawRect pour le canvas d'image de WinTraining.py
	drawRectModif=None #creer la classe DrawRect pour le canvas d'image de WinModification.py
	listFileWithActionRect={} #dictionnaire, tous les fichiers et tous les actions et tous les rectangles qui sont dans ce dictionnaire
	listActionRect={} #peut etre on peut le supprimer 
	nameProjet='new'
	currentSelectedFile= None #pour noter le fichier current
	currentIndex=None
	lastIndex=None
	lastSelectedFile=None #pour noter le dernier fichier
	numPage=0 #pour noter numero de page
	xmlProjet=None  
	numberPage=0
	listAction=None #stocker listbox Action
	listFiles=None #stocker listbox Files
	cadre=None #stocker canvas d'image
	isWinModif=False 
	buttonConfirme=None
	buttonDelete=None
	
	#### fonctions ####
	def __init__(self,listbox=None): #construteur
		self.listAction=listbox
	
	def projetIsChoose(self):
		return self.nameProjet!='new'
	
	def setVar(self,var): #WinTraining.py et WinModification.py transmet la variable de radiobutton a commun.py
		self.var=var
	
	def setButton(self,buttonConf,buttonDel):#WinTraining.py et WinModification.py transmet le buttons a commun.py
		self.buttonConfirme=buttonConf
		self.boutonDelete=buttonDel
	
	def setListBoxAction(self,listbox):#WinTraining.py et WinModification.py transmet le listbox d'Action a commun.py
		self.listAction=listbox
		
	def setSizeScreen(self,width,height):#WinTraining.py et WinModification.py transmet la size d'écran a commun.py
		self.screen_width=width
		self.screen_height=height
	
	def setListBoxFiles(self,listbox):#WinTraining.py et WinModification.py transmet le listbox de Fichier a commun.py
		self.listFiles=listbox
		
	def setCadre(self,cadre):#WinTraining.py et WinModification.py transmet le Canvas a commun.py
		self.cadre=cadre
		
	def changeColRect(self,drawRect): #quand on appuie le button comfirmer, le couleur des rectangles choisis seront changés
		value = str(self.var)
		if value == 'Titre' :
			self.createRectBySelectionListbox(drawRect,2,'red')
		elif value == 'Lettrine' :
			self.createRectBySelectionListbox(drawRect,2,'blue')
		elif value == 'Image' : 
			self.createRectBySelectionListbox(drawRect,2,'green')
		else:
			self.createRectBySelectionListbox(drawRect,2,'gray')

	def createRectBySelectionListbox(self,drawRect,wd=None,outline=None,fill=None): #créer des nouveaux rectangles quand on change le type d'Action
		currentSelect=self.listAction.curselection() 
		for i in range(0,len(currentSelect)):
			selection=self.listAction.get(currentSelect[i])
			self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
			list1=[]
			list1=self.listActionRect[selection]
			if wd is not None:
				if outline is not None:
					if fill is not None :
						drawRect.creatRect(selection,list1,wd,outline,fill)
					else:
						drawRect.creatRect(selection,list1,wd,outline)
				else:	
					if fill is not None :
						drawRect.creatRect(selection,list1,wd,None,fill)
					else:
						drawRect.creatRect(selection,list1,wd)
			else:
				if outline is not None:
					if fill is not None :
						drawRect.creatRect(selection,list1,None,outline,fill)
					else:
						drawRect.creatRect(selection,list1,None,outline)
				else:
					if fill is not None :
						drawRect.creatRect(selection,list1,None,None,fill)
					else:
						drawRect.creatRect(selection,list1)

	def confirmer(self): #fonction de button "confirmer"
		listActionOrigin=self.listAction.get(0,tk.END) #
		listTextSelection=[]
		listTextChange=[]
		if self.isWinModif is True:
			self.drawRectModif.deleteAllRectAppear() #supprimer les rects affichés
			self.changeColRect(self.drawRectModif) #changer le couleur de rect choisi et le recréer avec la nouvelle couleur
		else:
			self.drawRect.deleteAllRectAppear()
			self.changeColRect(self.drawRect)
		currentSelect=self.listAction.curselection()
		#changer le text d'action
		for i in range(0,len(currentSelect)):
			selection=self.listAction.get(currentSelect[i])
			listTextSelection.append(selection)
		for k in range(0,len(listTextSelection)):
			(typeAction,idAction) = listTextSelection[k].split("-")
			listTextChange.append(str(self.var)+'-'+idAction)
		for j in range(0,len(currentSelect)):
			self.listAction.insert(int(currentSelect[j]),str(listTextChange[j]))
			self.listAction.delete(int(currentSelect[j])+1)
		#changer le contenu de la liste listFileWithActionRect pour adapter les nouveaux rectangles
		newListActionRect={}
		listActionChange=self.listAction.get(0,tk.END)
		for h in range(0,self.listAction.size()):
			newListActionRect[listActionChange[h]]=self.listActionRect[listActionOrigin[h]]
		self.listActionRect.clear()
		for key in newListActionRect :
			self.listActionRect[key]=newListActionRect[key]
		self.listFileWithActionRect[self.currentSelectedFile]=self.listActionRect

		
	def resizeImg(self,index,cadre): #redimensionner la taille d'image pour afficher, si l'image est trop grande que le canvas
		self.cadre=cadre #mettre le canvas
		dicimg={}
		img=Image.open(self.listPath[int(index)]) #ovrir l'image
		wd,hg=img.size
		mwd=self.screen_width #s'il y a un pb de redimmentsionner l'image, peut être il faut mettre *0.6
		mhg=self.screen_height
		#resize image
		if wd>mwd : #si largeur de photo est plus grand que le largeur de Canvas
			scale= 1.0*wd/mwd
			newImg=img.resize((int(wd/scale),int(hg/scale)),Image.ANTIALIAS)
			self.cadre.config(width=wd/scale,height=hg/scale)
			photo = ImageTk.PhotoImage(newImg)
			dicimg['img1'] = photo
			self.cadre.image=photo
			self.cadre.create_image(0,0,image=photo,anchor="nw") 
		elif hg > mhg: #si le hauteur de phto est plus grand que le hauteur de Canvas
			scale = 1.0*hg/mhg
			newImg = img.resize((int(wd/scale),int(hg/scale)), Image.ANTIALIAS)
			self.cadre.config(width=wd/scale,height=hg/scale)
			photo = ImageTk.PhotoImage(newImg)
			dicimg['img1'] = photo
			self.cadre.image=photo
			self.cadre.create_image(0,0,image=photo,anchor="nw") 
		else:
			self.cadre.config(width=wd,height=hg)
			photo = ImageTk.PhotoImage(img)
			dicimg['img1'] = photo
			self.cadre.image=photo
			self.cadre.create_image(0,0,image=photo,anchor="nw") 
			
		#le fichier est changé ou pas, si le fichier current est changé, on supprimera les rectangles qui étaitent affichés et créés
		if self.currentSelectedFile is None:   
			self.currentSelectedFile=self.listFiles.get(self.listFiles.curselection())
			self.fileChange=False
		else:
			if self.lastSelectedFile!=self.currentSelectedFile:
				self.fileChange=True
			else:
				self.fileChange=False   

		self.isWinModif=False
		self.drawRect=rect.CanvasEventsRect(self.cadre,self.listAction,self.listFileWithActionRect,self.currentSelectedFile,self.buttonConfirme,self.buttonDelete,self.fileChange) 
		#les events de souris
		self.cadre.bind('<ButtonPress-1>', self.drawRect.leftOnStart)  
		self.cadre.bind('<B1-Motion>',     self.drawRect.leftOnGrow)   
		self.cadre.bind('<Double-1>',      self.drawRect.leftOnClear)
		self.cadre.bind('<ButtonRelease-1>', self.drawRect.leftOnFinal)
		#self.cadre.bind('<ButtonPress-3>', self.drawRect.rightOnStart)
		#self.cadre.bind('<B3-Motion>',     self.drawRect.rightOnMove)
		#self.cadre.bind('<ButtonRelease-3>',self.drawRect.rightOnFinal)
		gs.update(self.nameProjet,self.numPage)
		
	
	def setImageForModif(self,path,cadre): #repeter un peu la fonction de resizeImg, nous pourrons essayer de fusionner les 2 fonctions
		self.cadre=cadre
		dicimg={}
		img=Image.open(path)
		wd,hg=img.size
		mwd=self.screen_width
		mhg=self.screen_height
		if wd>mwd :
			scale= 1.0*wd/mwd
			newImg=img.resize((int(wd/scale),int(hg/scale)),Image.ANTIALIAS)
			self.cadre.config(width=wd/scale,height=hg/scale)
			photo = ImageTk.PhotoImage(newImg)
			dicimg['img1'] = photo
			self.cadre.image=photo
			self.cadre.create_image(0,0,image=photo,anchor="nw") 
		elif hg > mhg:
			scale = 1.0*hg/mhg
			newImg = img.resize((int(wd/scale),int(hg/scale)), Image.ANTIALIAS)
			self.cadre.config(width=wd/scale,height=hg/scale)
			photo = ImageTk.PhotoImage(newImg)
			dicimg['img1'] = photo
			self.cadre.image=photo
			self.cadre.create_image(0,0,image=photo,anchor="nw") 
		else:
			self.cadre.config(width=wd,height=hg)
			photo = ImageTk.PhotoImage(img)
			dicimg['img1'] = photo
			self.cadre.image=photo
			self.cadre.create_image(0,0,image=photo,anchor="nw") 
		self.isWinModif=True
		(path1,path2,nameFile)=path.split('/')
		self.drawRectModif=rect.CanvasEventsRect(self.cadre,self.listAction,self.listFileWithActionRect,nameFile,self.buttonConfirme,self.buttonDelete)
		self.cadre.bind('<ButtonPress-1>', self.drawRectModif.leftOnStart)  
		self.cadre.bind('<B1-Motion>',     self.drawRectModif.leftOnGrow)   
		self.cadre.bind('<Double-1>',      self.drawRectModif.leftOnClear)
		self.cadre.bind('<ButtonRelease-1>', self.drawRectModif.leftOnFinal)
		#self.cadre.bind('<ButtonPress-3>', self.drawRectModif.rightOnStart)
		#self.cadre.bind('<B3-Motion>',     self.drawRectModif.rightOnMove)
		#self.cadre.bind('<ButtonRelease-3>',self.drawRectModif.rightOnFinal)
		gs.update(self.nameProjet,self.numPage)
		#retourne scale pour 
		return scale
		
	def de_select(self): #pour le button Deselect/Select All
		listSelectionAction=self.listAction.curselection()
		if len(listSelectionAction) < self.listAction.size() :
			if self.isWinModif is True:
				self.selectAll(self.currentSelectedFile)
			else:
				self.selectAll()
		else:
			self.deselectAll()

	def deselectAll(self): #deselectionner tous les items de listbox action
		self.listAction.selection_clear(0,tk.END)
		if self.isWinModif is True:
			list1=self.drawRectModif.getListRectAppear() #recupérer les rectangles affichés pour les supprimer
			sizeList=len(list1)
			for i in range(0,sizeList):
				self.drawRectModif.deselectAll(list1[i]) #supprimer tous les rectangles quand on deselectionne tous les items de listbox
			self.drawRectModif.clearListRectAppear()
		else:
			list1=self.drawRect.getListRectAppear()
			sizeList=len(list1)
			for i in range(0,sizeList):
				self.drawRect.deselectAll(list1[i])
			self.drawRect.clearListRectAppear()
		
	def selectAll(self,nameFile=None): #sélectionner tous les items de listbox action et créer les rectangles correspondants
		self.listAction.select_set(0,tk.END)
		currentSelect=self.listAction.curselection()
		for i in range(0,len(currentSelect)):
			selection=self.listAction.get(currentSelect[i])
			if self.isWinModif is True:
				self.listActionRect=self.listFileWithActionRect[nameFile]
				list1=[]
				list1=self.listActionRect[selection]
				self.drawRectModif.creatRect(selection,list1,3)
			else:
				self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
				list1=[]
				list1=self.listActionRect[selection]
				self.drawRect.creatRect(selection,list1,3)
			
	def onSelectAction(self,evt): #quand on click dans le listbox Action
		currentSelect=self.listAction.curselection()
		if self.isWinModif is True:
			self.drawRectModif.deleteAllRectAppear()
			for i in range(0,len(currentSelect)):
				self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
				selection=self.listAction.get(currentSelect[i])
				list1=[]
				list1=self.listActionRect[selection]
				self.drawRectModif.creatRect(selection,list1,3)
		else:
			self.drawRect.deleteAllRectAppear()
			for i in range(0,len(currentSelect)):
				self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
				selection=self.listAction.get(currentSelect[i])
				list1=[]
				list1=self.listActionRect[selection]
				self.drawRect.creatRect(selection,list1,3)
		
	def deleteSelection(self):#fonction de button "Supprimer" pour supprimer les items que nous avons selectionner dans listbox des actions
		self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
		currentselection = self.listAction.curselection()
		listSelection=[]
		for i in range(0,len(currentselection)):
			selection=self.listAction.get(currentselection[i])
			list1=self.listActionRect[selection]
			idRect=list1[4]
			if self.isWinModif is True:
				self.drawRectModif.deleteRect(selection,idRect)
			else:
				self.drawRect.deleteRect(selection,idRect)
		a = range(0,len(currentselection))
		for x in reversed(a): #l'inverse de l'ordre de currentSelection, sinon il y aura un problème d'index
			self.listAction.delete(currentselection[x])
		
	def nextPage(self): #button Enregister et Suivant  #a mettre dans enregister #voir si onSelect se fait tout seul
		if gs.projetExist(self.nameProjet):
			gs.update(self.nameProjet,str(int(self.numPage)+1))
		else :
			gs.writeInText(self.nameProjet,self.numPage+1)
		self.save()
		if int(self.numPage)<self.listFiles.size() :
			self.numPage=int(self.numPage)
			self.numPage += 1
			self.listFiles.selection_clear(0, tk.END)
			self.listFiles.selection_set(int(self.numPage))
			self.recharge()
			self.resizeImg(int(self.numPage),self.cadre)
			self.selectAll()
		
		
		
	def lastPage(self): #button Précédent 
		self.save()
		if gs.projetExist(self.nameProjet):
			gs.update(self.nameProjet,int(self.numPage)-1)
		else :
			gs.writeInText(self.nameProjet,int(self.numPage)-1)
		if int(self.numPage)>0 :
			self.numPage=int(self.numPage)
			self.numPage -= 1
			self.listFiles.selection_clear(0, tk.END)
			self.listFiles.selection_set(int(self.numPage))
			self.recharge()
			self.resizeImg(int(self.numPage),self.cadre)
			self.selectAll()
			


	############################# Barre menu ############
	def newProjet(self): #fonctions de NewProjet sur le barre de menu
		self.numPage=0
		choice = self.chooseFile()
		if choice > 0: #si on a choisi un fichier
			self.xmlProjet,start=xl.newProjet(self.nameProjet)
			if not start: #ecrire la tête de la queue dans xml et le nom de projet et numero de page dans elemSave.txt
				page=xl.addPage('imgFromPdf/' + self.nameProjet+ '/'+ self.nameProjet + 'page-0.png',self.numPage,self.xmlProjet)
				self.xmlProjet=xl.endProjet(self.nameProjet,self.xmlProjet)
				gs.writeInText(self.nameProjet,self.numPage)
			self.continueProjet()
			
			
			
	def continueProjet(self):
		#fenêtre pour choisir le projet
		rootpop = tk.Tk()
		rootpop.title("Choisit le projet")
		listFrame=tk.Frame(rootpop)
		
		yDefilB = tk.Scrollbar(listFrame, orient='vertical')
		yDefilB.grid(row=0, column=1, sticky='ns')
		xDefilB = tk.Scrollbar(listFrame, orient='horizontal')
		xDefilB.grid(row=1, column=0, sticky='ew')
		
		listProjet = tk.Listbox(listFrame,
			xscrollcommand=xDefilB.set,
			yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE,exportselection=0)    
		listProjet.grid(row=0) 
		xDefilB['command'] = listProjet.xview
		yDefilB['command'] = listProjet.yview    
		Projetlist=gs.getListProjet()
		for i in range (0 ,len(Projetlist)):
			listProjet.insert(1,Projetlist[i])
		listFrame.grid(row=0,pady=0,padx=15,sticky=tk.W+tk.N +tk.E)
		listProjet.grid(row=0,pady=0,padx=15,sticky=tk.W+tk.N +tk.E)


		def projetToContinu(evt):   
			if len(listProjet.curselection())!=0 :
				self.nameProjet =listProjet.get(listProjet.curselection()[0])  #recuperer le nom de projet que nous avons choisit
				self.numPage=gs.getAvancementProjet(self.nameProjet) 
				self.currentIndex=self.numPage
				self.listFiles.selection_set(int(self.numPage))
				self.reloadImg()
				self.resizeImg(int(self.numPage),self.cadre)#re
				self.xmlProjet,temp=xl.continuePoject(self.nameProjet)
				self.currentSelectedFile=self.nameProjet
				listFileInListbox = self.listFiles.get(0,tk.END) #recuperer tous les noms de fichier dans listbox 
				for i in range(0,len(listFileInListbox)):
					list1=xl.getRect(self.nameProjet,i,self.xmlProjet)
					listInitial={}
					for k in range(0,len(list1)):
						list2=list1[k]
						if int(list2[0]) == i :
							list3=[]
							list3.append(int(list2[3])) #x
							list3.append(int(list2[4])) #y
							list3.append(int(list2[5])) #width
							list3.append(int(list2[6])) #height
							list3.append(None) #idRect
							list3.append(2) #epaiseur de border
							#couleur de border
							if list2[1] =='Titre':
								list3.append('red')
							elif list2[1] =='Lettrine' :
								list3.append('blue')
							elif list2[1]=='Image':
								list3.append('green')
							else:
								list3.append('gray')
							list3.append(None) #couleur de fill
							listInitial[str(list2[1])+'-'+str(list2[2])]=list3
						else:
							listInitial={}
					self.listFileWithActionRect[listFileInListbox[i]]=listInitial #stocker tous les fichiers, les actions de ces ficheirs,et les coordonnees de rectangles d'action 
				self.recharge()
				self.selectAll()
				rootpop.destroy()
				rootpop.quit()
	
		listProjet.bind('<<ListboxSelect>>', projetToContinu)
	
		rootpop.mainloop()
	
	def saveModif(self,nameProjet,numPage,scale): #pour la fenêtre WinModification.py, quand on modifie les erreurs, on utilise cette fonction pour enregistrer au lieu de save()
		pathXml ="DrawOnImage/workshop_test/"+ nameProjet +"/"
		self.xmlEdit=etree.Element(nameProjet)
		self.numPage=numPage
		page = xl.addPage('page-'+str(self.numPage)+'.png',self.numPage,self.xmlEdit)
		sizelist=self.listAction.size()
		listItems=self.listAction.get(0,tk.END)
		for k in range (0,sizelist) :
			(typeAction,idAction) = listItems[k].split("-")
			self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
			listCoord=self.listActionRect[listItems[k]]
			typeEl=typeAction
			numElem=idAction #id
			posiX=int(listCoord[0]*scale)
			posiY=int(listCoord[1]*scale)
			widthEl=int(listCoord[2]*scale)
			heightEl=int(listCoord[3]*scale)
			xl.addElement(typeEl, numElem, posiX, posiY, widthEl, heightEl,self.nameProjet, self.numPage, self.xmlEdit)
			with open(pathXml + '/' + 'page-'+ str(numPage) +'.png-Unlabelled.xml','w') as fichier:
				fichier.write(etree.tostring(self.xmlEdit,pretty_print=True).decode('utf-8'))#xmlProjet
				fichier.close()
		pathIMG='page-'+ str(numPage) +'.png'
		ei.drawIm(pathIMG,nameProjet,scale)
		
	def getCoordsFromXml(self,pathImg,nameprojet,numPage,scale):
		self.xmlProjet=xl.getXmlToModif(nameprojet,numPage)
		listInitial={}
		list1=xl.getRectForModification(nameprojet,pathImg,self.xmlProjet,scale) #recuperer les rects depuis les fichiers XML
		for i in range(0,len(list1)):
			list2=list1[i]
			list3=[]
			list3.append(int(int(list2[3])/scale))
			list3.append(int(int(list2[4])/scale))
			list3.append(int(int(list2[5])/scale))
			list3.append(int(int(list2[6])/scale))
			list3.append(None)
			list3.append(2)
			if list2[1] =='Titre':
				list3.append('red')
			elif list2[1] =='Lettrine' :
				list3.append('blue')
			elif list2[1]=='Image':
				list3.append('green')
			else:
				list3.append('gray')
			list3.append(None)
			listInitial[str(list2[1])+'-'+str(list2[2])]=list3
		(path1,path2,nameFile)=pathImg.split('/')
		self.currentSelectedFile=nameFile
		self.listFileWithActionRect[nameFile]=listInitial
		listModif=self.listFileWithActionRect[nameFile]#stocker les données qu'on a récupéré par xml dans la liste pour qu'on puisse utiliser après
		for key in listModif:
			self.listAction.insert(tk.END,key)
		self.selectAll(nameFile)
		
	def save(self): 
		if not(xl.pageExist(self.nameProjet, str(self.numPage),self.xmlProjet)) :
			page = xl.addPage(str(self.listPath[int(self.numPage)]),self.numPage,self.xmlProjet)
			
			self.xmlProjet=xl.endProjet(self.nameProjet,self.xmlProjet)
		else :
			page = xl.foundPage(self.nameProjet, self.numPage,self.xmlProjet)
		sizelist=self.listAction.size()
		listItems=self.listAction.get(0,tk.END)
		
		xl.delectPage(self.nameProjet,self.numPage,self.xmlProjet)
		page = xl.addPage(str(self.listPath[int(self.numPage)]),self.numPage,self.xmlProjet)
		self.xmlProjet=xl.endProjet(self.nameProjet,self.xmlProjet)
		
		for k in range (0,sizelist) :
			(typeAction,idAction) = listItems[k].split("-")
			self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
			listCoord=self.listActionRect[listItems[k]]
			typeEl=typeAction
			numElem=idAction #id
			posiX=listCoord[0]
			posiY=listCoord[1]
			widthEl=listCoord[2]
			heightEl=listCoord[3]
			
			if not(xl.reSave(self.nameProjet, self.numPage, numElem,self.xmlProjet)) :
				xl.addElement(typeEl, numElem, posiX, posiY, widthEl, heightEl,self.nameProjet, self.numPage, self.xmlProjet)
			else :
				if not(xl.sameType(self.nameProjet, self.numPage, numElem, typeEl,self.xmlProjet)):
					self.xmlProjet=xl.replace(self.nameProjet, self.numPage, numElem, typeEl,self.xmlProjet)
			self.xmlProjet=xl.endProjet(self.nameProjet,self.xmlProjet)
		
	def openModif(self,nameProjet,numPage,dimention): #ovrir la fenêtre de WinModification
		import WinModification as modif
		root=tk.Toplevel()
		self.nameProjet=nameProjet
		self.numPage=numPage
		def callback():
			question=messagebox.askyesno('Question','Ouvrir la fenêtre de Chemin de Fer')
			if question:
				from UseCheminDeFer import mainSeeResult as msr# a changer pour le nom aussi
				root.destroy()
				msr.creatChemin(self.nameProjet,dimention,True)
			else:
				root.destroy()
			
		root.protocol("WM_DELETE_WINDOW",callback) #s'il detecte la fenêtre qui est fermé, il va détruire la fenêtre de WinModification, ouvrir la fenêtre MainSeeResult(chemin de fer)
		modif.creatWin(root,self.nameProjet,numPage,dimention)
		
	
	# parcours choit du fichier
	def chooseFile(self):
		choice = tf.askopenfilenames(filetypes=[("pdf files","*.pdf")],multiple=0) #fichier pdf uniquement #il faut l'améliorer, on ne veut pas sélectionner multiple fichiers
		nbSelected=len(choice)
		listImg=0
		#recupere le nom apartir du chemin
		for i in range (0,nbSelected):
			ext = os.path.splitext(choice[i])[1]
			nomExt=basename(choice[i])
			nom=os.path.splitext(nomExt)[0]
			if ext == '.pdf':
				self.nameProjet=nom
				listImg = pti.pdfToPng(choice[i],self.nameProjet,60)#30==resolution base 90 resol haut
			else: #si c'est pas un fichier pdf, il affiche un messagebox, et relancer la fonction newProjet pour choisir un bon fichier de projet 
				messagebox.showinfo(title="Erreur",message="Type de fichier doit être Pdf")
				self.newProjet()
				
		return nbSelected
				
	def deepLearnig(self):
		if not(gs.cheminIsDone(self.nameProjet)):
			from DrawOnImage import Segmentation as sg
			sg.Segm(self.nameProjet, self.numberPage)#nombre de page il et calculer dans pdfToimage
			from DrawOnImage import Classification as cl
			cl.classif(self.nameProjet)
			from DrawOnImage import drawOnImage as doi #a remettre c'est juste lourd
			doi.drawIm(self.nameProjet)
			gs.doChemin(self.nameProjet,self.numPage)
		from UseCheminDeFer import mainSeeResult as msr# a changer pour le nom aussi
		msr.creatChemin(self.nameProjet)

	
	def reloadImg(self) :
		#listImgFromPdf = os.listdir('imgFromPdf/' + self.nameProjet)
		#chrono = lambda v: os.path.getmtime(os.path.join('imgFromPdf/' + self.nameProjet, v))
		#listImgFromPdf.sort(key = chrono)
		listImg = os.listdir('imgFromPdf/' + self.nameProjet)
		size = len(listImg)
		listImgOrder=[]
		for i in range (0,size):
			listImgOrder.append(self.nameProjet + 'page-' + str(i) + '.png')
		for k in range (0,len(listImgOrder)) :
			nomExt=basename(listImgOrder[k])
			nom=os.path.splitext(nomExt)[0]
			self.listFiles.insert(self.listFiles.size(), nom)
			self.listPath.append('imgFromPdf/' + self.nameProjet + '/' + listImgOrder[k])
		self.numberPage=len(listImgOrder)
		self.listFiles.select_set(self.numPage)#pour que ça aille a la page ou on en etait
		

		
	def recharge(self): #si les contenus de listFileWithActionRect sont changés, recharger les nouvelles contenues dans la liste
		if self.currentSelectedFile is not None:
			if len(self.listFiles.curselection())!=0 :
				self.lastSelectedFile=self.currentSelectedFile
				self.currentSelectedFile=self.listFiles.get(self.listFiles.curselection())
				if self.lastSelectedFile!=self.currentSelectedFile:
					self.listAction.delete(0,tk.END)
					newListActionRect={}
					self.listActionRect=newListActionRect
					mapActionRect=self.listFileWithActionRect[self.currentSelectedFile]
					if mapActionRect is not None :
						for key in mapActionRect :
							self.listAction.insert(tk.END,key)
							self.listActionRect[key]=mapActionRect[key]
		else:
			self.currentSelectedFile=self.listFiles.get(self.listFiles.curselection())
			
	def onselect(self,evt): #quand on click dans listbox Files
		w=evt.widget
		if len(w.curselection())!=0 :
			if gs.projetExist(self.nameProjet):
				gs.update(self.nameProjet,str(int(self.currentIndex)+1))
			else :
				gs.writeInText(self.nameProjet,self.currentIndex+1)
			self.save()
			self.lastIndex=self.currentIndex
			self.currentIndex = int(w.curselection()[0])
			self.numPage=self.currentIndex
			self.recharge()
			self.resizeImg(self.currentIndex,self.cadre)
			self.selectAll()