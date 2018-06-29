"""
Created on Tue May 22 09:37:31 2018

@author: Liuyan PAN
"""
#la classe pour designer les rectangles
#des fonctions à améliorer, tester qu'on a choisit un rect ou pas, après on peut le supprimer ou bouger, maintenant la fonction pour bouger les rectangles ne fonctionne pas bien.
#important : si on utiliser le canvas pour créer des choses, par exemple create_rectangle, create_windows, create_image,etc, il nous faut penser et supprimer bien tous ce qu'on crée
import tkinter as tk
import commun as co
trace = 0 
class CanvasEventsRect:
	startX=0 #noter la position de start quand on appuie le button gauche de souri
	startY=0
	rightstartX=0 #noter la position de final quand on appuie le button droit de souri
	rightstartY=0
	isDrawn=False #le rect est dessiné ou pas
	isMove=False #pour la fonction de movement du rect, ça fonctionne pas bien, il faut l'améliorer
	finalX=0 #noter la position de start quand on appuie le button droite de souri
	finalY=0
	rightfinalX=0 #noter la position de final quand on appuie le button droite de souri
	rightfinalY=0
	objectId=None #stocke id de rect quand nous créons le rect
	listBoxAction=None
	listFileWithActionRect=None 
	currentFile=None
	listRectAppear=[] #stroker les ids de rect qui sont créés et affichés
	#isWinModif=None #pour savoir que c'est la fenêtre Main.py ou WinModification.py, inutile pour l'instant
	func=co.FunctionCommun()
	buttonConfirme=None
	buttonDelete=None
	def __init__(self, parent,listbox,fileWithActionRectList,currentFileSelected,buttonConf,buttonDel,fileChange=None):
		self.canvas = parent
		self.isDrawn=False
		self.isMove=False
		self.listBoxAction=listbox
		self.listFileWithActionRect=fileWithActionRectList
		self.currentFile=currentFileSelected
		self.func.setListBoxAction(listbox)
		self.buttonConfirme=buttonConf
		self.buttonDelete=buttonDel
		self.func.setButton(self.buttonConfirme,self.buttonDelete)

		if fileChange is not None: #si le current fichier est changé, il faut supprimer les rectangles sont créés et affichés
			if fileChange is True:
				for i in range(0,len(self.listRectAppear)):
					self.canvas.delete(self.listRectAppear[i])
				self.listRectAppear=[]
				if self.listBoxAction.size() >0 :
					self.listBoxAction.select_set(0,tk.END)
		self.drawn  = None #=objectId
		
	def leftOnStart(self, event): #le button gauche appuyé
		global objectId
		self.start = event
		canvas = self.start.widget
		if self.isDrawn is True : #si le rect précédant est créé, on le supprime pour designer un nouveau rect, le rect précédant est stocké dans listRectAppear dans la foncttion leftOnFinal
			canvas.delete(objectId)
		self.drawn = None 
		self.startX=self.start.x
		self.startY=self.start.y
		self.isDrawn=False

        
	def rightOnStart(self,event): #le button droite appuyé
		global objectId,isDrawn,isMove
		self.rightstart = event
		canvas = self.start.widget
		if self.isDrawn is True:
			canvas.delete(objectId)
		self.drawn = None
		self.rightstartX=self.rightstart.x
		self.rightstartY=self.rightstart.y
		self.isMove=False

	def leftOnGrow(self, event): # le button gauche est appuyé et bougé
		global objectId,isDrawn                      
		canvas = event.widget
		if self.isDrawn is False:
			if self.drawn: 
				canvas.delete(self.drawn)
			objectId = canvas.create_rectangle(self.start.x, self.start.y, event.x, event.y,outline="gray")
			if trace: #tracer le rect
				print("trace")
				print(objectId)
			self.drawn = objectId
        

	def leftOnClear(self, event): # double click pour supprimer 
		#cette fonction peut être améliorer
		global objectId
		canvas = event.widget
		canvas.delete(objectId)
		self.drawn=None

	def rightOnMove(self, event): #le button droite appuyé et bougé, pour bouger les rectangles
		#fonction à améliorer
		canvas = event.widget
		if self.drawn: 
			canvas.delete(self.drawn)
		diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
		objectId = canvas.create_rectangle(self.start.x+diffX, self.start.y+diffY, self.finalX+diffX, self.finalY+diffY,outline="gray")
		if trace: 
			print("trace")
			print(objectId)
		self.drawn = objectId
		self.isMove=False
            
	def leftOnFinal(self,event):
		global isDraw,listBoxAction,listFileWithActionRect,currentFile,buttonConfirme,buttonDelete
		listActionRect=self.listFileWithActionRect[self.currentFile]
		self.final=event
		self.finalX=event.x
		self.finalY=event.y
		self.isDrawn=True
		idAction=self.listBoxAction.size()+1 #id de action essayer de recuperer par le nom de listbox,if size de listbox>0,sinon par 1,2,3...... #c'est possible que id est répété, essayer de trouver une idée pour évider ça
		self.listBoxAction.insert(self.listBoxAction.size(),'Paragraphe-'+str(idAction))
		listActionRect['Paragraphe-'+str(idAction)]=self.getCoordonnes()
		self.listFileWithActionRect[self.currentFile]=listActionRect
		self.listBoxAction.select_set(0,tk.END)
		for i in range(0,self.listBoxAction.size()) : 
			selection=self.listBoxAction.get(i)
			list1=[]
			list1=listActionRect[selection]
			selectedAction=self.canvas.create_rectangle(list1[0],list1[1],list1[0]+list1[2],list1[1]+list1[3],width=2,outline=list1[6]) #couleur de rect est gris par default
			list1[4]=selectedAction
			self.listRectAppear.append(selectedAction)#stocker les rects crée
		self.canvas.delete(objectId)
		self.buttonDelete.config(state =tk.ACTIVE)
		self.buttonConfirme.config(state =tk.ACTIVE)
	
	def rightOnFinal(self,event):
		#fonction à améliorer
		global isMove
		self.isMove=True
		self.rightfinal=event
		self.rightfinalX=event.x
		self.rightfinalY=event.y
		self.isDrawn=True
        
	def getCoordonnes(self):
		listCoord=[]
		if self.isMove is True : #renvoyer la position de rect bougé
			listCoord.append(self.rightstartX)
			listCoord.append(self.rightstartY)
		else: #sinon renvoyer la position de rect créé sans bouger
			if self.startX > self.finalX:
				listCoord.append(self.finalX)
				listCoord.append(self.finalY)
			else:
				listCoord.append(self.startX)
				listCoord.append(self.startY)
		width=abs(self.finalX-self.startX)
		height=abs(self.finalY-self.startY)
		listCoord.append(width)
		listCoord.append(height)
		listCoord.append(self.objectId) #id de rect
		listCoord.append(2) #épaiseur de border
		listCoord.append('gray') #couleur de border de rect
		listCoord.append(None) #couleur plein de rect
		return listCoord
    
	def deselectAll(self,idRect): #supprimer le rect indiqué
		self.canvas.delete(idRect)
	
	def deleteAllRectAppear(self): #supprimer tous les rects affichés
		for i in range(0,len(self.listRectAppear)):
			self.canvas.delete(self.listRectAppear[i])
		
	def deleteRect(self,selection,idRect): #supprimer le rect choisit
		listActionRect=self.listFileWithActionRect[self.currentFile]
		list1=[]
		list1=listActionRect[selection]
		del listActionRect[selection]
		self.canvas.delete(idRect)
	
	def getListRectAppear(self): #retourner la liste listRectAppear
		list1=[]
		list1=self.listRectAppear
		return list1
		
	def clearListRectAppear(self): 
		#self.listRectAppear=[]
		self.listRectAppear.clear()
		
	def creatRect(self,actionRect,coordRect,wd=None, colOutline=None, colFill=None): #créer les rectangles avec l'option
		list2=self.listFileWithActionRect[self.currentFile]
		list1=list2[actionRect]
		if wd is not None:
			list1[5]=wd
			if colOutline is not None:
				list1[6]=colOutline
				if colFill is not None:
					list1[7]=str(colFill)
					selectedAction=self.canvas.create_rectangle(coordRect[0],coordRect[1],coordRect[0]+coordRect[2],coordRect[1]+coordRect[3],width=wd, outline=colOutline, fill=colFill)
				else:
					selectedAction=self.canvas.create_rectangle(coordRect[0],coordRect[1],coordRect[0]+coordRect[2],coordRect[1]+coordRect[3],width=wd, outline=colOutline)
			else:
				if colFill is not None:
					list1[7]=str(colFill)
					selectedAction=self.canvas.create_rectangle(coordRect[0],coordRect[1],coordRect[0]+coordRect[2],coordRect[1]+coordRect[3],width=wd,fill=colFill)
				else:
					selectedAction=self.canvas.create_rectangle(coordRect[0],coordRect[1],coordRect[0]+coordRect[2],coordRect[1]+coordRect[3],width=wd,outline=coordRect[6])
		else:
			if colOutline is not None:
				list1[6]=colOutline
				if colFill is not None:
					list1[7]=str(colFill)
					selectedAction=self.canvas.create_rectangle(coordRect[0],coordRect[1],coordRect[0]+coordRect[2],coordRect[1]+coordRect[3],outline=colOutline, fill=colFill)
				else:
					selectedAction=self.canvas.create_rectangle(coordRect[0],coordRect[1],coordRect[0]+coordRect[2],coordRect[1]+coordRect[3],outline=colOutline)
			else:
				if colFill is not None:
					list1[7]=str(colFill)
					selectedAction=self.canvas.create_rectangle(coordRect[0],coordRect[1],coordRect[0]+coordRect[2],coordRect[1]+coordRect[3],fill=colFill)
				else:
					selectedAction=self.canvas.create_rectangle(coordRect[0],coordRect[1],coordRect[0]+coordRect[2],coordRect[1]+coordRect[3])
		list1[4]=selectedAction
		if selectedAction not in self.listRectAppear : #Quand on crée le rectangle et on l'affiche, il faut le mettre dans cette liste
			self.listRectAppear.append(selectedAction)
		return self.listRectAppear
	
