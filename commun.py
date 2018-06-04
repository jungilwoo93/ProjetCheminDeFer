import tkinter as tk
from PIL import Image, ImageFont, ImageDraw, ImageTk
import DrawRect as rect
import creatXml as xl
import gestionSave as gs
import pdfToImg as pti

class FunctionCommun:
	#### variable ####
	#root = tk.Tk()
	var=tk.StringVar()
	var.set("Paragraphe")
	typeZone={"Titre","Paragraphe","Lettrine","Image"}
	colorDefault="#F5F5DC"
	screen_width=None
	screen_height=None
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
	numberPage=0
	listAction=None
	listFiles=None
	listModif=None
	def __init__(self,listbox=None):
		self.listAction=listbox
		
	def setListBoxAction(self,listbox):
		self.listAction=listbox
		
	def setSizeScreen(self,width,height):
		self.screen_width=width
		self.screen_height=height
	
	def setListBoxFiles(self,listbox):
		self.listFiles=listbox
		
	def changeColRect(self):
		value = str(self.var.get())
		if value == 'Titre' :
			self.createRectBySelectionListbox(2,'blue')
		elif value == 'Lettrine' :
			self.createRectBySelectionListbox(2,'green')
		elif value == 'Image' : 
			self.createRectBySelectionListbox(2,'red')
		else:
			self.createRectBySelectionListbox(2,'black')

	def createRectBySelectionListbox(self,wd=None,outline=None,fill=None):
		currentSelect=self.listAction.curselection()
		for i in range(0,len(currentSelect)):
			selection=self.listAction.get(currentSelect[i])
			list1=[]
			list1=listActionRect[selection]
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

	def confirmer(self):
		#print("listActionRect orginal " +str(listActionRect))
		listActionOrigin=listAction.get(0,tk.END)
		listTextSelection=[]
		listTextChange=[]
		drawRect.deleteAllRectAppear()
		changeColRect()
		currentSelect=listAction.curselection()
		for i in range(0,len(currentSelect)):
			selection=listAction.get(currentSelect[i])
			listTextSelection.append(selection)
		for k in range(0,len(listTextSelection)):
			(typeAction,idAction) = listTextSelection[k].split("-")
			listTextChange.append(var.get()+'-'+idAction)
		for j in range(0,len(currentSelect)):
			listAction.insert(int(currentSelect[j]),str(listTextChange[j]))
			listAction.delete(int(currentSelect[j])+1)
			#print("selection "+selection)
		newListActionRect={}
		listActionChange=listAction.get(0,tk.END)
		for h in range(0,listAction.size()):
			newListActionRect[listActionChange[h]]=listActionRect[listActionOrigin[h]]
		listActionRect.clear()
		for key in newListActionRect :
			listActionRect[key]=newListActionRect[key]
		listFileWithActionRect[currentSelectedFile]=listActionRect

	def resizeImg(self,path,cadre):
		global drawRect,newImg,currentSelectedFile,lastSelectedFile,listActionRect
		dicimg={}
		#if index is not None:
		#	img=Image.open(listPath[int(index)])
		#if path is not None :
		img=Image.open(path)
		#img.resize((320,240))
		#img.zoom(320/img.width(), 240/img.height())
		wd,hg=img.size
		mwd=self.screen_width
		mhg=self.screen_height
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
		if self.currentSelectedFile is None:   
			#self.currentSelectedFile=listFiles.get(listFiles.curselection())
			self.fileChange=False
		else:
			if self.lastSelectedFile!=self.currentSelectedFile:
				self.fileChange=True
			else:
				self.fileChange=False    
		self.drawRect=rect.CanvasEventsDemo(cadre,self.listAction,self.listActionRect,self.listFileWithActionRect,self.currentSelectedFile,self.fileChange)
		cadre.bind('<ButtonPress-1>', self.drawRect.leftOnStart)  
		cadre.bind('<B1-Motion>',     self.drawRect.leftOnGrow)   
		cadre.bind('<Double-1>',      self.drawRect.leftOnClear)
		cadre.bind('<ButtonRelease-1>', self.drawRect.leftOnFinal)
		cadre.bind('<ButtonPress-3>', self.drawRect.rightOnStart)
		cadre.bind('<B3-Motion>',     self.drawRect.rightOnMove)
		cadre.bind('<ButtonRelease-3>',self.drawRect.rightOnFinal)
		gs.update(self.nameProjet,self.numPage)
		
	def de_select(self):
		#global countClick
		listSelectionAction=listAction.curselection()
		#listSelectionAction=listAction.curselection()
		if len(listSelectionAction) < listAction.size() :
			selectAll()
		else:
			deselectAll()

	def deselectAll(self):
		listAction.selection_clear(0,tk.END)
		list1=drawRect.deselectRect()
		#print("list1 " + str(list1))
		sizeList=len(list1)
		for i in range(0,sizeList):
			#print("out here?")
			drawRect.deselectAll(list1[i])
		drawRect.clearListRectAppear()
		
	def selectAll(self):
		self.listAction.select_set(0,tk.END)
		currentSelect=self.listAction.curselection()
		for i in range(0,len(currentSelect)):
			selection=self.listAction.get(currentSelect[i])
			list1=[]
			list1=self.listModif[selection]
			#list1=listActionRect[selection]
			#print("listActionRect " +str(listActionRect))
			#print("selection " + str(selection))
			#print("list1 " + str(list1))
			self.drawRect.creatRect(selection,list1,3)
			
	def onSelectAction(self,evt):
		global drawRect
		currentSelect=listAction.curselection()
		drawRect.deleteAllRectAppear()
		for i in range(0,len(currentSelect)):
			selection=listAction.get(currentSelect[i])
			#print("selection " +str(selection))
			list1=[]
			list1=listActionRect[selection]
			#print("listActionRect "+str(list1))
			drawRect.creatRect(selection,list1,3)
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
		
	def deleteSelection(self):#pour liste des actions
		global drawRect
		currentselection = listAction.curselection()
		#print("current selection " +str(currentselection))
		#print("size " + str(len(currentselection)))
		listSelection=[]
		for i in range(0,len(currentselection)):
			#print("current selection " +str(currentselection[i]))
			selection=listAction.get(currentselection[i])
			#print("selection " +str(selection))
			list1=listActionRect[selection]
			idRect=list1[4]
			drawRect.deleteRect(selection,idRect)
		a = range(0,len(currentselection))
		for x in reversed(a):
			#print(str(x))
			listAction.delete(currentselection[x])
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
		
	def delecteAll(self):
		listFiles.delete(0,tk.END) 
		listPath.clear()
		
	def nextPage(self):  #a mettre dans enregister #voir si onSelect se fait tout seul
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
			self.resizeImg(int(numPage))
			self.recharge()
		
		
		
	def lastPage(self):
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
			self.recharge()


	############################# Barre menu 
	def newProjet(self):
		global numPage
		numPage=0
		chooseFile()
		global xmlProjet
		xmlProjet=xl.newProjet(nameProjet)
		page=xl.addPage('imgFromPdf/' + nameProjet+ '/'+ nameProjet + 'page-0.png',numPage, xmlProjet)
		xmlProjet=xl.endProjet(nameProjet,xmlProjet)
		gs.writeInText(nameProjet,numPage)
		
	def saveModif(self):
		print('coucou')
		
	def getCoordsFromXml(self,pathImg,projet):
		xmlProjet=xl.getExistingXml(projet)
		listInitial={}
		list1=xl.getRectForModification(projet,pathImg,xmlProjet)
		print("list1 " +str(list1))
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
				list3.append('blue')
			elif list2[1] =='Lettrine' :
				list3.append('green')
			elif list2[1]=='Image':
				list3.append('red')
			else:
				list3.append('black')
			list3.append(None)
			listInitial[str(list2[1])+'-'+str(list2[2])]=list3
		(path1,path2,nameFile)=pathImg.split('/')
		self.listFileWithActionRect[nameFile]=listInitial
		#print(str(listInitial))
		for key in self.listModif:
			self.listAction.insert(tk.END,key)		
		self.selectAll()
		
	def save(self):
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