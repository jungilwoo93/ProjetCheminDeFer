import tkinter as tk
from PIL import Image, ImageFont, ImageDraw, ImageTk
import os
from os.path import basename
import tkinter.filedialog as tf
from lxml import etree

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
	screen_width=None #transferer la taille d'ecran de main.py et WinModification.py pour qu'on peut utiliser dans commun.py
	screen_height=None
	listPath=[] #stocker tous les chemins de d'images du projet
	drawRect=None #creer la classe DrawRect pour le canvas d'image de main.py
	drawRectModif=None #creer la classe DrawRect pour le canvas d'image de WinModification.py
	listFileWithActionRect={} #dictionnaire, tous les fichiers et tous les actions et tous les rectangles qui sont dans ce dictionnaire
	listActionRect={} #peut etre on peut le supprimer 
	nameProjet='new'
	currentSelectedFile= None #pour noter le fichier current
	lastSelectedFile=None #pour noter le dernier fichier
	numPage=0 #pour noter numero de page
	xmlProjet=None  
	numberPage=0
	listAction=None #stocker listbox Action
	listFiles=None #stocker listbox Files
	cadre=None #stocker canvas d'image
	isWinModif=False 
	
	#### fonctions ####
	def __init__(self,listbox=None): #construteur
		self.listAction=listbox
	
	def projetIsChoose(self):
		print(self.nameProjet!='new')
		return self.nameProjet!='new'
	
	def setVar(self,var): #main.py et WinModification.py transmet la variable de radiobutton a commun.py
		self.var=var
		
	def setListBoxAction(self,listbox):
		self.listAction=listbox
		
	def setSizeScreen(self,width,height):
		self.screen_width=width
		self.screen_height=height
	
	def setListBoxFiles(self,listbox):
		self.listFiles=listbox
		
	def setCadre(self,cadre):
		self.cadre=cadre
		
	def changeColRect(self,drawRect): 
		value = str(self.var)
		if value == 'Titre' :
			self.createRectBySelectionListbox(drawRect,2,'red')
		elif value == 'Lettrine' :
			self.createRectBySelectionListbox(drawRect,2,'blue')
		elif value == 'Image' : 
			self.createRectBySelectionListbox(drawRect,2,'green')
		else:
			self.createRectBySelectionListbox(drawRect,2,'gray')

	def createRectBySelectionListbox(self,drawRect,wd=None,outline=None,fill=None):
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
		#print("listActionRect orginal " +str(listActionRect))
		listActionOrigin=self.listAction.get(0,tk.END)
		listTextSelection=[]
		listTextChange=[]
		if self.isWinModif is True:
			self.drawRectModif.deleteAllRectAppear()
			self.changeColRect(self.drawRectModif)
		else:
			self.drawRect.deleteAllRectAppear()
			self.changeColRect(self.drawRect)
		currentSelect=self.listAction.curselection()
		for i in range(0,len(currentSelect)):
			selection=self.listAction.get(currentSelect[i])
			listTextSelection.append(selection)
		for k in range(0,len(listTextSelection)):
			(typeAction,idAction) = listTextSelection[k].split("-")
			listTextChange.append(str(self.var)+'-'+idAction)
		for j in range(0,len(currentSelect)):
			self.listAction.insert(int(currentSelect[j]),str(listTextChange[j]))
			self.listAction.delete(int(currentSelect[j])+1)
			#print("selection "+selection)
		newListActionRect={}
		listActionChange=self.listAction.get(0,tk.END)
		for h in range(0,self.listAction.size()):
			newListActionRect[listActionChange[h]]=self.listActionRect[listActionOrigin[h]]
		self.listActionRect.clear()
		for key in newListActionRect :
			self.listActionRect[key]=newListActionRect[key]
		self.listFileWithActionRect[self.currentSelectedFile]=self.listActionRect

	def resizeImg(self,index,cadre):
		self.cadre=cadre #mettre le canvas
		dicimg={}
		img=Image.open(self.listPath[int(index)]) #ovrir l'image
		#img.resize((320,240))
		#img.zoom(320/img.width(), 240/img.height())
		wd,hg=img.size
		mwd=self.screen_width
		mhg=self.screen_height
		#resize image
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
		#newImg.save(listPath[index])  
		#newImg.close()
		
		if self.currentSelectedFile is None:   
			self.currentSelectedFile=self.listFiles.get(self.listFiles.curselection())
			self.fileChange=False
		else:
			if self.lastSelectedFile!=self.currentSelectedFile:
				self.fileChange=True
			else:
				self.fileChange=False   
		#print("currentList " +str(self.currentSelectedFile))
		#print(" self.listFileWithActionRect " +str(self.listFileWithActionRect))
		self.isWinModif=False
		self.drawRect=rect.CanvasEventsDemo(self.cadre,self.listAction,self.listActionRect,self.listFileWithActionRect,self.currentSelectedFile,self.isWinModif,self.fileChange) #il y a des arguments inutils, nous pouvons essayer de les enlever
		#les events de souris
		self.cadre.bind('<ButtonPress-1>', self.drawRect.leftOnStart)  
		self.cadre.bind('<B1-Motion>',     self.drawRect.leftOnGrow)   
		self.cadre.bind('<Double-1>',      self.drawRect.leftOnClear)
		self.cadre.bind('<ButtonRelease-1>', self.drawRect.leftOnFinal)
		self.cadre.bind('<ButtonPress-3>', self.drawRect.rightOnStart)
		self.cadre.bind('<B3-Motion>',     self.drawRect.rightOnMove)
		self.cadre.bind('<ButtonRelease-3>',self.drawRect.rightOnFinal)
		gs.update(self.nameProjet,self.numPage)
		
	
	def setImageForModif(self,path,cadre): #repeter un peu la fonction de resizeImg, nous pourrons essayer de fusionner les 2 fonctions
		self.cadre=cadre
		#global drawRect,newImg,currentSelectedFile,lastSelectedFile,listActionRect
		dicimg={}
		img=Image.open(path)
		#img.resize((320,240))
		#img.zoom(320/img.width(), 240/img.height())
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
		#print("listAction " +str(self.listAction))
		#print("listActionRect " + str(self.listActionRect))
		#print("listFileWithActionRect " +str(self.listFileWithActionRect))
		self.drawRectModif=rect.CanvasEventsDemo(self.cadre,self.listAction,self.listActionRect,self.listFileWithActionRect,nameFile,self.isWinModif)
		self.cadre.bind('<ButtonPress-1>', self.drawRectModif.leftOnStart)  
		self.cadre.bind('<B1-Motion>',     self.drawRectModif.leftOnGrow)   
		self.cadre.bind('<Double-1>',      self.drawRectModif.leftOnClear)
		self.cadre.bind('<ButtonRelease-1>', self.drawRectModif.leftOnFinal)
		self.cadre.bind('<ButtonPress-3>', self.drawRectModif.rightOnStart)
		self.cadre.bind('<B3-Motion>',     self.drawRectModif.rightOnMove)
		self.cadre.bind('<ButtonRelease-3>',self.drawRectModif.rightOnFinal)
		gs.update(self.nameProjet,self.numPage)
		return scale
		
	def de_select(self):
		#global countClick
		listSelectionAction=self.listAction.curselection()
		#listSelectionAction=listAction.curselection()
		if len(listSelectionAction) < self.listAction.size() :
			if self.isWinModif is True:
				self.selectAll(self.currentSelectedFile)
			else:
				self.selectAll()
		else:
			self.deselectAll()

	def deselectAll(self):
		self.listAction.selection_clear(0,tk.END)
		if self.isWinModif is True:
			list1=self.drawRectModif.deselectRect()
			#if drawRectModif is not None, deselectRect()
			#print("list1 " + str(list1))
			sizeList=len(list1)
			for i in range(0,sizeList):
				#print("out here?")
				self.drawRectModif.deselectAll(list1[i])
			self.drawRectModif.clearListRectAppear()
		else:
			list1=self.drawRect.deselectRect()
			#if drawRectModif is not None, deselectRect()
			#print("list1 " + str(list1))
			sizeList=len(list1)
			for i in range(0,sizeList):
				#print("out here?")
				self.drawRect.deselectAll(list1[i])
			self.drawRect.clearListRectAppear()
		
	def selectAll(self,nameFile=None):
		self.listAction.select_set(0,tk.END)
		currentSelect=self.listAction.curselection()
		for i in range(0,len(currentSelect)):
			selection=self.listAction.get(currentSelect[i])
			#print("current !!!!!!!!!! " +str(self.currentSelectedFile))
			if self.isWinModif is True:
				#print("listfilewithactionrect   !!!" +str(self.listFileWithActionRect))
				self.listActionRect=self.listFileWithActionRect[nameFile]
				list1=[]
				list1=self.listActionRect[selection]
				self.drawRectModif.creatRect(selection,list1,3)
			else:
				self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
				list1=[]
				#list1=self.listModif[selection]
				list1=self.listActionRect[selection]
				#print("listActionRect " +str(self.listActionRect))
				#print("selection " + str(selection))
				#print("list1 " + str(list1))
				
				self.drawRect.creatRect(selection,list1,3)
			
	def onSelectAction(self,evt):
		#global drawRect
		currentSelect=self.listAction.curselection()
		print("currentSelect " +str(currentSelect))
		if self.isWinModif is True:
			self.drawRectModif.deleteAllRectAppear()
			for i in range(0,len(currentSelect)):
				self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
				selection=self.listAction.get(currentSelect[i])
				#print("selection " +str(selection))
				#self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
				list1=[]
				list1=self.listActionRect[selection]
				#print("listActionRect "+str(list1))
				self.drawRectModif.creatRect(selection,list1,3)
		else:
			self.drawRect.deleteAllRectAppear()
			for i in range(0,len(currentSelect)):
				self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
				selection=self.listAction.get(currentSelect[i])
				#print("selection " +str(selection))
				#self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
				list1=[]
				list1=self.listActionRect[selection]
				#print("listActionRect "+str(list1))
				self.drawRect.creatRect(selection,list1,3)
		"""currentSelect=listAction.curselection()
		if len(currentSelect) >1:
			print("when all selected "+str(listAction.curselection()))
			tmp=0
			for i in range(0,len(currentSelect)):
				if int(currentSelect[i])==tmp:
					tmp+=1
			listAction.selection_clear(0,tk.END)
			listAction.select_set(tmp)
			tmp=0
			print("after select " +str(listAction.curselection()))
		else:
			
			print("if length of currentSelect =1 or =0")"""
		"""global selectedAction
		if selectedAction is not None:
			cadre.delete(selectedAction)
		selection=listAction.get(listAction.curselection())
		list1=[]
		list1=listActionRect[selection]
		selectedAction=cadre.create_rectangle(list1[0],list1[1],list1[0]+list1[2],list1[1]+list1[3],width=5)"""
		
	def deleteSelection(self):#fonction de button "Supprimer" pour supprimer les items que nous avons selectionner dans listbox des actions
		self.listActionRect=self.listFileWithActionRect[self.currentSelectedFile]
		#print("listActionRect " +str(listActionRect))
		currentselection = self.listAction.curselection()
		#print("current selection " +str(currentselection))
		#print("size " + str(len(currentselection)))
		listSelection=[]
		for i in range(0,len(currentselection)):
			#print("current selection " +str(currentselection[i]))
			selection=self.listAction.get(currentselection[i])
			#print("selection " +str(selection))
			list1=self.listActionRect[selection]
			idRect=list1[4]
			if self.isWinModif is True:
				self.drawRectModif.deleteRect(selection,idRect)
			else:
				self.drawRect.deleteRect(selection,idRect)
		a = range(0,len(currentselection))
		for x in reversed(a):
			#print(str(x))
			self.listAction.delete(currentselection[x])
		#print("listFile with Action rECT : " + str(listFileWithActionRect))
		#for k in range(0,len(currentselection)-1).reverse():
		#	print(str(k))
			#
		"""for i in range(0,len(currentselection)):
			print("current selection " +str(currentselection[i]))
			
			list1=[]
			list1=listActionRect[selection]
			idRect=list1[4]
			drawRect.deleteRect(selection,idRect)
			listAction.delete(currentselection[i])"""
		"""else:
			selection=listAction.get(currentselection[0])
			list1=[]
			
			listAction.delete(currentselection[0])"""
		#pas encore supprimer dans la liste!!!!!!!!!!!!!!!!
		#listPath.remove(selection[0])
		
	def deleteAll(self):
		self.listFiles.delete(0,tk.END) 
		self.listPath.clear()
		
	def nextPage(self):  #a mettre dans enregister #voir si onSelect se fait tout seul
		#global numPage
		if gs.projetExist(self.nameProjet):
			gs.update(self.nameProjet,str(int(self.numPage)+1))
		else :
			gs.writeInText(self.nameProjet,self.numPage+1)
		self.save()
		if int(self.numPage)<self.listFiles.size() :
			self.numPage=int(self.numPage)
			self.numPage += 1
			self.listFiles.selection_clear(0, tk.END)
			#if int(numPage)<listFiles.size() :
			self.listFiles.selection_set(int(self.numPage))
			#else:
			#	numPage=listFiles.size()-1
			#	listFiles.selection_set(int(numPage))
			self.recharge()
			self.resizeImg(int(self.numPage),self.cadre)
			self.selectAll()
		
		
		
	def lastPage(self):
		self.save()
		#global numPage
		if gs.projetExist(self.nameProjet):
			gs.update(self.nameProjet,int(self.numPage)-1)
		else :
			gs.writeInText(self.nameProjet,int(self.numPage)-1)
		if int(self.numPage)>0 :
			self.numPage=int(self.numPage)
			self.numPage -= 1
			#print(numPage)
			self.listFiles.selection_clear(0, tk.END)
			self.listFiles.selection_set(int(self.numPage))
			self.recharge()
			self.resizeImg(int(self.numPage),self.cadre)
			self.selectAll()
			


	############################# Barre menu 
	def newProjet(self):
		#global numPage
		self.numPage=0
		self.chooseFile()
		#global xmlProjet
		self.xmlProjet=xl.newProjet(self.nameProjet)
		page=xl.addPage('imgFromPdf/' + self.nameProjet+ '/'+ self.nameProjet + 'page-0.png',self.numPage,self.xmlProjet)
		self.xmlProjet=xl.endProjet(self.nameProjet,self.xmlProjet)
		gs.writeInText(self.nameProjet,self.numPage)
	
	def continueProjet(self):
		#fenêtre pour choisir le projet
		rootpop = tk.Tk()
		rootpop.title("choisit le projet")
		listFrame=tk.Frame(rootpop)
		
		yDefilB = tk.Scrollbar(listFrame, orient='vertical')
		yDefilB.grid(row=0, column=1, sticky='ns')
		xDefilB = tk.Scrollbar(listFrame, orient='horizontal')
		xDefilB.grid(row=1, column=0, sticky='ew')
		
		listProjet = tk.Listbox(listFrame,
			xscrollcommand=xDefilB.set,
			yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE,exportselection=0)    
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
			#global nameProjet,numPage,xmlProjet,currentSelectedFile
			#nameProjet=listProjet.curselection()
			#rootpop.destroy
			if len(listProjet.curselection())!=0 :
				self.nameProjet =listProjet.get(listProjet.curselection()[0])  #recuperer le nom de projet que nous avons choisit
				self.numPage=gs.getAvancementProjet(self.nameProjet) 
				self.listFiles.selection_set(int(self.numPage))
				self.reloadImg()
				self.resizeImg(int(self.numPage),self.cadre)#re
				self.xmlProjet=xl.continuePoject(self.nameProjet)
				self.currentSelectedFile=self.nameProjet
				listFileInListbox = self.listFiles.get(0,tk.END) #recuperer tous les noms de fichier dans listbox 
				for i in range(0,len(listFileInListbox)):
					list1=xl.getRect(self.nameProjet,i,self.xmlProjet)
					#print("list1 " +str(list1))
					listInitial={}
					for k in range(0,len(list1)):
						list2=list1[k]	
						#print("list2 "+str(list2))
						#print(str(int(list2[0]))+'=?'+str(i))
						if int(list2[0]) == i :
							#print("coucou")
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
							#print("list3 "+str(list3))
							listInitial[str(list2[1])+'-'+str(list2[2])]=list3
							#print("listInitial  "+str(listInitial))
						else:
							listInitial={}
					self.listFileWithActionRect[listFileInListbox[i]]=listInitial
				#print("listFilewithaCTIONrECT " +str(self.listFileWithActionRect))
				#for file in listFiles.get(0,tk.END):
				#	listFileWithActionRect[file]=listInitial
				#print('listFileWithActionRect ' +str(listFileWithActionRect)) 
				self.recharge()
				#deselectAll()
				self.selectAll()
				rootpop.destroy()
				rootpop.quit()
	
		listProjet.bind('<<ListboxSelect>>', projetToContinu)
	
		rootpop.mainloop()
	
	def saveModif(self,nameProjet,numPage,scale):
		pathXml ="DrawOnImage/workshop_test/"+ nameProjet +"/"
		self.xmlEdit=etree.Element(nameProjet)
		page = xl.addPage(str(self.listPath[int(self.numPage)]),self.numPage,self.xmlEdit)
		#page = xl.foundPage(self.nameProjet, self.numPage,self.xmlEdit)
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
		pathIMG='imgFromPdf/' + nameProjet+ '/'+ nameProjet+'page-'+ str(numPage) +'.png'
		ei.drawIm(pathIMG,nameProjet,scale)
		
	def getCoordsFromXml(self,pathImg,nameprojet,numPage,scale):
		#global xmlProjet
		#xmlProjet=xl.getExistingXml(nameprojet)
		self.xmlProjet=xl.getXmlToModif(nameprojet,numPage)
		#self.getxmlProjet=xl.getXmlToModif(nameprojet,numPage)#xl.getExistingXml(nameprojet)
		listInitial={}
		list1=xl.getRectForModification(nameprojet,pathImg,self.xmlProjet,scale)
		#print("list1 " +str(list1))
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
		#print("current file " +str(self.currentSelectedFile))
		self.listFileWithActionRect[nameFile]=listInitial
		listModif=self.listFileWithActionRect[nameFile]
		#print(str(listInitial))
		for key in listModif:
			self.listAction.insert(tk.END,key)
		self.selectAll(nameFile)
		
		'''
		def getCoordsFromXml(self,pathImg,projet):
		global xmlProjet
		xmlProjet=xl.getExistingXml(projet)
		self.getxmlProjet=xl.getExistingXml(projet)
		listInitial={}
		list1=xl.getRectForModification(projet,pathImg,self.getxmlProjet)
		#print("list1 " +str(list1))
		for i in range(0,len(list1)):
			list2=list1[i]
			list3=[]
			list3.append(int(list2[3]))
			list3.append(int(list2[4]))
			list3.append(int(list2[5]))
			list3.append(int(list2[6]))
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
		#print("current file " +str(self.currentSelectedFile))
		self.listFileWithActionRect[nameFile]=listInitial
		listModif=self.listFileWithActionRect[nameFile]
		#print(str(listInitial))
		for key in listModif:
			self.listAction.insert(tk.END,key)
		self.selectAll(nameFile)'''
		
	def save(self):
		#global xmlProjet
		if not(xl.pageExist(self.nameProjet, str(self.numPage),self.xmlProjet)) :
			page = xl.addPage(str(self.listPath[int(self.numPage)]),self.numPage,self.xmlProjet)
			
			self.xmlProjet=xl.endProjet(self.nameProjet,self.xmlProjet)
		else :
			page = xl.foundPage(self.nameProjet, self.numPage,self.xmlProjet)
		sizelist=self.listAction.size()
		#w=evt.widget
		listItems=self.listAction.get(0,tk.END)
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
				self.xmlProjet=xl.endProjet(self.nameProjet,self.xmlProjet)
			else :
				#print(str(self.nameProjet)+' ... '+ str(self.numPage)+' ... '+ str(numElem)+' ... '+ str(typeEl)+' ... '+str(self.xmlProjet))
				if not(xl.sameType(self.nameProjet, self.numPage, numElem, typeEl,self.xmlProjet)):
					self.xmlProjet=xl.replace(self.nameProjet, self.numPage, numElem, typeEl,self.xmlProjet)
					self.xmlProjet=xl.endProjet(self.nameProjet,self.xmlProjet)
		#nextPage()
	def openModif(self,nameProjet,numPage):
		import WinModification as modif
		root=tk.Toplevel()
		#global self.nameProjet
		self.nameProjet=nameProjet
		self.numPage=numPage
		#var=tk.StringVar()
		#var.set("Paragraphe")
		#numPage=0	
		#pathImg='imgFromPdf/TD3/TD3page-0.png'
		#selection=self.listFiles.curselection()############### ca marche
		#print(str(selection))
		#print("all path " +str(self.listPath))
		#print("path " +str(self.listPath[selection[0]]))
		#print("nameprojet " +str(self.nameProjet))
		#nameProjet='TD3'
		#modif.creatWin(root,self.listPath[selection[0]],self.nameProjet)
		#self.isWinModif=True
		modif.creatWin(root,self.nameProjet,numPage)#,self.listPath[selection[0]]
		
	
	# parcours choit du fichier
	def chooseFile(self):
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
				#global nameProjet
				self.nameProjet=nom
				listImg = pti.pdfToPng(choice[i],self.nameProjet,60)#30==resolution base 90 resol haut
				self.numberPage = pti.getCountPage()
				size=len(listImg)
				for k in range (0, size) :
					self.listFiles.insert(self.listFiles.size(),basename(listImg[k])) 
					self.listPath.append(listImg[k])
			else :
				if nom!="": #sinon quand on clic sur parcourir mais qu'on ne choisi rien ça rajoute un espace blanc
					self.listFiles.insert(self.listFiles.size(),nom) 
					#listFiles.
					self.listPath.append(choice[i])
					# listFiles.TopIndex = listFiles.ListCount
		self.listFiles.select_set(0)    
		listInitial={}
		for file in self.listFiles.get(0,tk.END):
			self.listFileWithActionRect[file]=listInitial
		#print(str(listFileWithActionRect))
		self.resizeImg(0,self.cadre)
		self.recharge()
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
		
	def deepLearnig(self):
		if not(gs.cheminIsDone(self.nameProjet)):
			print('creeation de cdf')
			from DrawOnImage import Segmentation as sg
			sg.Segm(self.nameProjet, self.numberPage)#nombre de page il et calculer dans pdfToimage
			from DrawOnImage import Classification as cl
			cl.classif(self.nameProjet)
			from DrawOnImage import drawOnImage as doi #a remettre c'est juste lourd
			doi.drawIm(self.nameProjet)
			gs.doChemin(self.nameProjet,self.numPage)
		from UseCheminDeFer import mainSeeResult as msr# a changer pour le nom aussi
		msr.creatChemin(self.nameProjet)
		
		#global sg.namePropjet
		#sg.nameProjet=nameProjet
		#cl.nameProjet=nameProjet
		#doi.nameProjet=nameProjet
		#save()
		#root.destroy()
		#root.quit()
	
	def reloadImg(self) :
		listImgFromPdf = os.listdir('imgFromPdf/' + self.nameProjet)
		chrono = lambda v: os.path.getmtime(os.path.join('imgFromPdf/' + self.nameProjet, v))
		listImgFromPdf.sort(key = chrono)
		for k in range (0,len(listImgFromPdf)) :
			nomExt=basename(listImgFromPdf[k])
			nom=os.path.splitext(nomExt)[0]
			self.listFiles.insert(self.listFiles.size(), nom)
			self.listPath.append('imgFromPdf/' + self.nameProjet + '/' + listImgFromPdf[k])
		#global numberPage
		self.numberPage=len(listImgFromPdf)
		self.listFiles.select_set(self.numPage)#pour que ça aille a la page ou on en etait
		
		# supprimer de la liste les fichiers selectionnés
		
	def recharge(self):
		#global currentSelectedFile,lastSelectedFile,listActionRect
		#global selectedAction
		if self.currentSelectedFile is not None:
			if len(self.listFiles.curselection())!=0 :
				self.lastSelectedFile=self.currentSelectedFile
				self.currentSelectedFile=self.listFiles.get(self.listFiles.curselection())
				if self.lastSelectedFile!=self.currentSelectedFile:
					self.listAction.delete(0,tk.END)
					newListActionRect={}
					self.listActionRect=newListActionRect
					#mapAction=getMapActionRect(currentSelectedFile)
					mapActionRect=self.listFileWithActionRect[self.currentSelectedFile]
					if mapActionRect is not None :
						#print("mapActionRect isn't none")
						for key in mapActionRect :
							self.listAction.insert(tk.END,key)
							#print(mapActionRect[key])
							self.listActionRect[key]=mapActionRect[key]
							#print(str(listActionRect[key]))
				#else:
				#    print("is none")
		else:
			self.currentSelectedFile=self.listFiles.get(self.listFiles.curselection())
		#print("current file    ?!"+str(self.currentSelectedFile))
			
	def onselect(self,evt):
		#global drawRect,newImg,currentSelectedFile,lastSelectedFile,listActionRect
		#cadre=tk.Canvas(c,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=screen_width-600,height=screen_height-25,bg="black")#,bg="black"
		#cadre=tk.Label(f,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=320,height=240,bg="green")
		#cadre=tk.Canvas(root,width=screen_width-500,height=screen_height,bg="black")
		#dicimg = {}
		#selection = listFiles.curselection()
		#print(selection[0])
		w=evt.widget
		if len(w.curselection())!=0 :
			index = int(w.curselection()[0])
			#global numPage
			self.numPage=index
			#value = w.get(index)
			#print(index)
			self.recharge()
			self.resizeImg(index,self.cadre)
			self.selectAll()
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