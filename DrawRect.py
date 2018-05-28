import tkinter as tk
trace = 0 
class CanvasEventsDemo:

	startX=0
	startY=0
	rightstartX=0
	rightstartY=0
	isDraw=False
	isMove=False
	finalX=0
	finalY=0
	rightfinalX=0
	rightfinalY=0
	objectId=None
	color="Black"
	listRectDrawn={}
	listRect=[]
	idAction=0
	listBoxAction=None
	listActionRect=None
	listFileWithActionRect=None
	currentFile=None
	listRectAppear=[]
	#fileChanged=False
	
	def __init__(self, parent,listbox,actionRectList,fileWithActionRectList,currentFileSelected,fileChange,col=None):
		self.canvas = parent
		self.isDraw=False
		self.isMove=False
		self.listBoxAction=listbox
		self.listActionRect=actionRectList
		self.listFileWithActionRect=fileWithActionRectList
		self.currentFile=currentFileSelected
		self.fileChanged=fileChange
		#print("true or false?????????????"+str(fileChange))
		#print("!!!!!!!!!!!!!listRect!!!!!!!!!!!!!"+str(self.listRect))
		if fileChange is True:
			if len(self.listRect) >1:
				self.canvas.delete(self.listRect[len(self.listRect)-1])
			for i in range(0,len(self.listRectAppear)):
				self.canvas.delete(listRectAppear[i])
			self.listRectAppear=[]
			#fileChange=False
		#print("!!!!!!!!!!!!!listRect!!!!!!!!!!!!!"+str(self.listRect))
		#print("listbox")
		#print("listActionRect"+str(actionRectList))
		#print("listFileWithActionRect"+str(fileWithActionRectList))
		#print("currentFileSelected"+str(currentFileSelected))
		if col is not None:
			print("isBlack")
			self.color="Black"
		else:
			print("another color")
			self.color=col
		self.drawn  = None
		
	def leftOnStart(self, event):
		global objectId
		self.start = event
		canvas = self.start.widget
		if self.isDraw is True :
			canvas.delete(objectId)
		#print("true or false?????????????"+str(fileChange))
		#if self.fileChanged is True:
		#	print("is true")
		self.drawn = None
		self.startX=self.start.x
		self.startY=self.start.y
		self.isDraw=False
		print("is True? " +str(self.fileChanged))
		print("is draw? " +str(self.isDraw)) 

        
	def rightOnStart(self,event):
		global objectId,isDraw,isMove
		self.rightstart = event
		canvas = self.start.widget
		if self.isDraw is True:
			canvas.delete(objectId)
		self.drawn = None
		self.rightstartX=self.rightstart.x
		self.rightstartY=self.rightstart.y
		self.isMove=False

	def leftOnGrow(self, event): 
		global objectId,isDraw                      
		canvas = event.widget
		if self.isDraw is False:
			#print("is draw")
			if self.drawn: 
				canvas.delete(self.drawn)
			objectId = canvas.create_rectangle(self.start.x, self.start.y, event.x, event.y)
			if trace: 
				print("trace")
				print(objectId)
			self.drawn = objectId
			#print("objectID: " +str(objectId))
			#print("drawn" + str(self.drawn))
        

	def leftOnClear(self, event):
		global objectId
		canvas = event.widget
		canvas.delete(objectId)
		self.drawn=None

	def rightOnMove(self, event):
		canvas = event.widget
		if self.drawn: 
			canvas.delete(self.drawn)
		diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
		objectId = canvas.create_rectangle(self.start.x+diffX, self.start.y+diffY, self.finalX+diffX, self.finalY+diffY)
		if trace: 
			print("trace")
			print(objectId)
		self.drawn = objectId
		self.isMove=False
            
	def leftOnFinal(self,event):
		global isDraw,listBoxAction,idAction,listActionRect,listFileWithActionRect,currentFile
		self.final=event
		self.finalX=event.x
		self.finalY=event.y
		self.isDraw=True
		self.idAction=self.listBoxAction.size()+1
		self.listBoxAction.insert(self.listBoxAction.size(),'Paragraphe-'+str(self.idAction))
		self.listActionRect['Paragraphe-'+str(self.idAction)]=self.getCoordonnes()
		self.listFileWithActionRect[self.currentFile]=self.listActionRect
		self.listRect.append(objectId)
		self.listBoxAction.select_set(0,tk.END)
		for i in range(0,self.listBoxAction.size()) : 
			selection=self.listBoxAction.get(i)
			list1=[]
			list1=self.listActionRect[selection]
			selectedAction=self.canvas.create_rectangle(list1[0],list1[1],list1[0]+list1[2],list1[1]+list1[3],width=3)
			self.listRectAppear.append(selectedAction)
	
	def rightOnFinal(self,event):
		global isMove
		self.isMove=True
		self.rightfinal=event
		self.rightfinalX=event.x
		self.rightfinalY=event.y
		self.isDraw=True
        
	def getCoordonnes(self):
		listCoord=[]
		if self.isMove is True :
			listCoord.append(self.rightstartX)
			listCoord.append(self.rightstartY)
		else:
			listCoord.append(self.startX)
			listCoord.append(self.startY)
		width=abs(self.finalX-self.startX)
		height=abs(self.finalY-self.startY)
		listCoord.append(width)
		listCoord.append(height)
		listCoord.append(objectId)
		return listCoord
    
	def deleteRect(self,idRect):
		print("delete rect")
		self.listRect.remove(idRect)
		self.canvas.delete(idRect)
