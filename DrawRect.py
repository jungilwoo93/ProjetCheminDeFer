"""
Created on Tue May 22 09:37:31 2018

@author: Liuyan PAN
"""
#la classe pour designer les rectangles
import tkinter as tk
import commun as co
trace = 0 
class CanvasEventsDemo:
	startX=0 #noter la position de start
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
	listRectDrawn={}
	#listRect=[]
	idAction=0
	listBoxAction=None
	listActionRect=None
	listFileWithActionRect=None
	currentFile=None
	listRectAppear=[]
	isWinModif=None
	func=co.FunctionCommun()
	#fileChanged=False
	def __init__(self, parent,listbox,actionRectList,fileWithActionRectList,currentFileSelected,isWinModif,fileChange=None):
		self.canvas = parent
		self.isDraw=False
		self.isMove=False
		self.isWinModif=isWinModif
		self.listBoxAction=listbox
		self.listActionRect=actionRectList
		self.listFileWithActionRect=fileWithActionRectList
		self.currentFile=currentFileSelected
		#self.fileChanged=fileChange
		self.func.setListBoxAction(listbox)
		#print("true or false?????????????"+str(fileChange))
		#print("!!!!!!!!!!!!!listRect!!!!!!!!!!!!!"+str(self.listRect))
		if fileChange is not None:
			if fileChange is True:
				#if len(self.listRect) >1:
				#	self.canvas.delete(self.listRect[len(self.listRect)-1])
				for i in range(0,len(self.listRectAppear)):
					self.canvas.delete(self.listRectAppear[i])
				self.listRectAppear=[]
				if self.listBoxAction.size() >0 :
					self.listBoxAction.select_set(0,tk.END)
				else:
					print("size <0")
				#fileChange=False
		#print("!!!!!!!!!!!!!listRect!!!!!!!!!!!!!"+str(self.listRect))
		#print("listbox")
		#print("listActionRect"+str(actionRectList))
		#print("listFileWithActionRect"+str(fileWithActionRectList))
		#print("currentFileSelected"+str(currentFileSelected))
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
		#print("is True? " +str(self.fileChanged))
		#print("is draw? " +str(self.isDraw)) 

        
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
			objectId = canvas.create_rectangle(self.start.x, self.start.y, event.x, event.y,outline="gray")
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
		objectId = canvas.create_rectangle(self.start.x+diffX, self.start.y+diffY, self.finalX+diffX, self.finalY+diffY,outline="gray")
		if trace: 
			print("trace")
			print(objectId)
		self.drawn = objectId
		self.isMove=False
            
	def leftOnFinal(self,event):
		print('listFileWithActionRect !!!!' + str(self.listFileWithActionRect))
		#global isDraw,listBoxAction,idAction,listActionRect,listFileWithActionRect,currentFile
		listActionRect=self.listFileWithActionRect[self.currentFile]
		print("listFileWithActionRect " +str(self.listFileWithActionRect))
		print("currentFile " +str(self.currentFile))
		
		self.final=event
		self.finalX=event.x
		self.finalY=event.y
		self.isDraw=True
		self.idAction=self.listBoxAction.size()+1##############id de action essayer de recuperer par le nom de listbox,if size de listbox>0,sinon par 1,2,3......
		self.listBoxAction.insert(self.listBoxAction.size(),'Paragraphe-'+str(self.idAction))
		listActionRect['Paragraphe-'+str(self.idAction)]=self.getCoordonnes()
		print("listActionRect " +str(listActionRect))
		self.listFileWithActionRect[self.currentFile]=listActionRect
		print("current " +str(self.currentFile))
		print("!!!!!!!!!!!!! "+str(self.listFileWithActionRect[self.currentFile]))
		#self.func.deselectAll()
		print('listFileWithActionRect ' + str(self.listFileWithActionRect))
		#self.listRect.append(objectId)#####################
		self.listBoxAction.select_set(0,tk.END)
		#print("size of listBoxAction " + self.listBoxAction.size())
		for i in range(0,self.listBoxAction.size()) : 
			selection=self.listBoxAction.get(i)
			list1=[]
			list1=listActionRect[selection]
			#print("listActionRect1111"+str(self.listActionRect[selection]))
			#print("list1"+str(list1))
			selectedAction=self.canvas.create_rectangle(list1[0],list1[1],list1[0]+list1[2],list1[1]+list1[3],width=2,outline=list1[6])
			list1[4]=selectedAction
			#print("selection     "+str(selectedAction))
			self.listRectAppear.append(selectedAction)#########################
			#self.listRect.append(self.listRectAppear[0])
			#print("listActionRect22222222"+str(self.listActionRect[selection]))
			#print("creat rect"+str(self.listRectAppear))
		
		self.canvas.delete(objectId)
	
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
		listCoord.append(self.objectId)
		listCoord.append(2)
		listCoord.append('gray')
		listCoord.append(None)
		return listCoord
    
	def deselectAll(self,idRect):
		#self.listRectAppear.remove(idRect)
		self.canvas.delete(idRect)
	
	def deleteAllRectAppear(self):
		for i in range(0,len(self.listRectAppear)):
			self.canvas.delete(self.listRectAppear[i])
		
	def deleteRect(self,selection,idRect):
		#print("delete rect")
		listActionRect=self.listFileWithActionRect[self.currentFile]
		list1=[]
		list1=listActionRect[selection]
		
		del listActionRect[selection]
		#print("listFileWithActionRect " +str(self.listFileWithActionRect))
		#self.listRect.remove(idRect)
		self.canvas.delete(idRect)
	
	def deselectRect(self):
		list1=[]
		list1=self.listRectAppear
		return list1
		
	def clearListRectAppear(self):
		self.listRectAppear.clear()
		
	def creatRect(self,actionRect,coordRect,wd=None, colOutline=None, colFill=None):
		#print("currentFile " +self.currentFile) 
		#list2=[]
		list2=self.listFileWithActionRect[self.currentFile]
		#print("listFileWithActionRect with?????" + str(list2))
		#print("self.listActionRect " + str(self.listActionRect))
		#list1=[]
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
		if selectedAction not in self.listRectAppear : 
			self.listRectAppear.append(selectedAction)
		return self.listRectAppear
	
