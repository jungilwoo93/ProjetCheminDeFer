# -*- coding: utf-8 -*-
"""
Created on Mon May 21 19:23:16 2018

@author: Liuyan PAN
"""
#problème:recréer trop de fois d'image et buttons
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

#import de nos autres fichiers
from UseCheminDeFer import editPage as ep
from UseCheminDeFer import export as exp

sizeXimg=[20,20]
sizeYimg=[20,20]
pageSelected=0
buttonList=[]

class AutoScrollbar(ttk.Scrollbar):
	#scrollbar automatiquement
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')

class Zoom_Advanced(ttk.Frame):
	dimention=[4,4]
	numPage=0
	buttonResetList={}
	imageid=None
	nameProjet='new'
	selectClick=0
	''' Advanced zoom of the image '''
	def __init__(self, mainframe, path,dim,numberPage,nameProj): #constructeur
		''' Initialize the main Frame '''
		self.dimention=dim
		self.numPage=numberPage
		self.nameProjet=nameProj
		ttk.Frame.__init__(self, master=mainframe)
        # Vertical and horizontal scrollbars for canvas
		self.vbar = AutoScrollbar(self.master, orient='vertical')
		self.hbar = AutoScrollbar(self.master, orient='horizontal')
		self.vbar.grid(row=0, column=1, sticky='ns')
		self.hbar.grid(row=1, column=0, sticky='we')
        # Create canvas and put image on it
		self.canvas = tk.Canvas(self.master, highlightthickness=0,
							xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
		self.canvas.grid(row=0, column=0, sticky='nswe')
		self.canvas.update()  # wait till canvas is created
		self.vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
		self.hbar.configure(command=self.scroll_x)
		# Make the canvas expandable
		self.master.rowconfigure(0, weight=3)
		self.master.columnconfigure(0, weight=1)
		# Bind events to the Canvas
		self.canvas.bind('<Configure>', self.createButton)  # canvas is resized
		self.canvas.bind('<ButtonPress-1>', self.move_from)
		self.canvas.bind('<B1-Motion>',     self.move_to)
		self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
		self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
		self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
		self.canvas.bind('<Motion>', self.posMouse)
		self.image = Image.open(path) # open image
		self.width, self.height = self.image.size
		self.wb=self.width
		self.hgb=self.height
		self.isMoved=False
		self.isWheel=False
		self.imscale = 1.0  # scale for the canvaas image
		self.delta = 1.3  # zoom magnitude
		self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
		self.show_image()
	
	def completeTab(self): #copier le text dans excel
		global selectClick
		selectClick=pageSelected
		exp.completeTab(pageSelected,self.nameProjet)

	
	def scroll_y(self, *args, **kwargs):
		''' Scroll canvas vertically and redraw the image '''
		self.canvas.yview(*args, **kwargs)		# scroll vertically
		self.isMoved=True
		self.show_image() 
		#recuperer la position de scrollbar pour calculer la distance pour que les bouttons sont bougés
		(s,f)=self.vbar.get()
		diff=(f-s)/self.himg
		if len(self.buttonResetList)>0 : 
			for idButton in self.buttonResetList:
				self.canvas.delete(idButton)
		self.img = Image.open('guillemets.jpg')
		self.sizeButton=15
		self.imag = self.img.resize((self.sizeButton,self.sizeButton))
		self.photo = ImageTk.PhotoImage(self.imag)
		buttonMoveList=self.buttonResetList
		self.buttonResetList={}
		self.k=0
		newLigne=0
		listIdButton=[]
		while self.k < self.numPage : #quand k inferieur de nombre de page
			for idButton in buttonMoveList:
				listIdButton.append(idButton)
			for j in range (0,self.dimention[0]):#dimention par defaut est 4, donc j = 0,1,2,3
				if self.k < self.numPage :
					buttonPosList=[]
					newbuttonPosList=buttonMoveList[listIdButton[self.k]]
					self.bt_expo = tk.Button(self.master, text=str(self.k), image=self.photo , command=self.completeTab)
					buttonCreated = self.canvas.create_window(newbuttonPosList[0], newbuttonPosList[1]-diff, window=self.bt_expo)
					buttonPosList.append(newbuttonPosList[0])
					buttonPosList.append(newbuttonPosList[1]-diff)
					self.buttonResetList[buttonCreated]=buttonPosList
					self.k += 1
			newLigne+=1

	def scroll_x(self, *args, **kwargs):
		''' Scroll canvas horizontally and redraw the image '''
		self.canvas.xview(*args, **kwargs)  # scroll horizontally
		self.show_image()  # redraw the image
		self.isMoved=True
		self.canvas.update() 
		#recuperer la position de scrollbar pour calculer la distance pour que les bouttons sont bougés
		(s,f)=self.hbar.get()
		diff=(f-s)/self.wimg
		if len(self.buttonResetList)>0 : 
			for idButton in self.buttonResetList:
				self.canvas.delete(idButton)
		self.img = Image.open('guillemets.jpg')
		self.sizeButton=15
		self.imag = self.img.resize((self.sizeButton,self.sizeButton))
		self.photo = ImageTk.PhotoImage(self.imag)
		buttonMoveList=self.buttonResetList
		self.buttonResetList={}
		self.k=0
		newLigne=0
		listIdButton=[]
		while self.k < self.numPage : #quand k inferieur de nombre de page
			for idButton in buttonMoveList:
				listIdButton.append(idButton)
			for j in range (0,self.dimention[0]):#dimention par defaut est 4, donc j = 0,1,2,3
				if self.k < self.numPage :
					buttonPosList=[]
					newbuttonPosList=buttonMoveList[listIdButton[self.k]]
					self.bt_expo = tk.Button(self.master, text=str(self.k), image=self.photo , command=self.completeTab)
					buttonCreated = self.canvas.create_window(newbuttonPosList[0]-diff, newbuttonPosList[1], window=self.bt_expo)
					buttonPosList.append(newbuttonPosList[0]-diff)
					buttonPosList.append(newbuttonPosList[1])
					self.buttonResetList[buttonCreated]=buttonPosList
					self.k += 1
			newLigne+=1
	
	#regarde autour de quel bouton est la souris
	def posMouse(self,event):
		mouseX = self.canvas.canvasx(event.x)
		mouseY = self.canvas.canvasy(event.y)
		Pselected,findButton=exp.posMouse(mouseX,mouseY, self.width, self.height, self.numPage, self.dimention, sizeYimg,self.wb,self.hgb,self.canvas.coords(self.imageid),self.buttonResetList,self.nameProjet)
		if findButton:
			global pageSelected
			pageSelected = Pselected
	#fonction non utiliser 
	
	#apple la fonction qui renvoie l'id de la page sur laquel on à cliqué
	def selectPage(self, event):
		mouseX = event.x
		mouseY = event.y
		x = self.canvas.canvasx(event.x)
		y = self.canvas.canvasy(event.y)
		sizeX = sizeXimg
		sizeY = sizeYimg


	def move_from(self, event):
		''' Remember previous coordinates for scrolling with the mouse '''
		self.selectPage(event)
		self.canvas.scan_mark(event.x, event.y)
		self.startX=event.x
		self.startY=event.y

	def move_to(self, event):
		''' Drag (move) canvas to the new position '''
		self.canvas.scan_dragto(event.x, event.y, gain=1)
		self.isMoved=True
		self.show_image() # redraw the image
		self.canvas.update() 
		diffX=(self.startX-event.x)/self.wimg
		diffY=(self.startY-event.y)/self.himg
		#supprimer les buttons qu'on a crée avant
		if len(self.buttonResetList)>0 : 
			for idButton in self.buttonResetList:
				self.canvas.delete(idButton)
		self.img = Image.open('guillemets.jpg')
		self.sizeButton=15
		self.imag = self.img.resize((self.sizeButton,self.sizeButton))
		self.photo = ImageTk.PhotoImage(self.imag)
		buttonMoveList=self.buttonResetList
		self.buttonResetList={}
		self.k=0
		newLigne=0
		listIdButton=[]
		while self.k < self.numPage : #quand k inferieur de nombre de page
			for idButton in buttonMoveList:
				listIdButton.append(idButton)
			for j in range (0,self.dimention[0]):#dimention par defaut est 4, donc j = 0,1,2,3
				if self.k < self.numPage :
					buttonPosList=[]
					newbuttonPosList=buttonMoveList[listIdButton[self.k]]
					self.bt_expo = tk.Button(self.master, text=str(self.k), image=self.photo , command=self.completeTab)
					buttonCreated = self.canvas.create_window(newbuttonPosList[0]-diffX/50, newbuttonPosList[1]-diffY/50, window=self.bt_expo)
					buttonPosList.append(newbuttonPosList[0]-diffX/50)
					buttonPosList.append(newbuttonPosList[1]-diffY/50)
					self.buttonResetList[buttonCreated]=buttonPosList
					self.k += 1
			newLigne+=1
		bbox1 = self.canvas.bbox(self.container)  # get image area
		# Remove 1 pixel shift at the sides of the bbox1
		bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
		bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
				self.canvas.canvasy(0),
				self.canvas.canvasx(self.canvas.winfo_width()),
				self.canvas.canvasy(self.canvas.winfo_height()))
		bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
				max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
		if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
			bbox[0] = bbox1[0]
			bbox[2] = bbox1[2]
		if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
			bbox[1] = bbox1[1]
			bbox[3] = bbox1[3]
		if int(self.x2 - self.x1) > 0 and int(self.y2 - self.y1) > 0: 
			#print("entrer !!!!!!!!!!!!!1")
			x = min(int(self.x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
			y = min(int(self.y2 / self.imscale), self.height)  # ...and sometimes not
			image = self.image.crop((int(self.x1 / self.imscale), int(self.y1 / self.imscale), x, y))#selectionner une partie d'une image
			imagetk = ImageTk.PhotoImage(image.resize((int(self.x2 - self.x1), int(self.y2 - self.y1))))
			if self.imageid is not None:
				self.canvas.delete(self.imageid)
			self.imageid = self.canvas.create_image((max(bbox2[0], bbox1[0])-diffX)/self.imscale, (self.posImgY-diffY)/self.imscale,
								anchor='nw', image=imagetk)
		self.canvas.update() 

	def wheel(self, event):
		''' Zoom with mouse wheel '''
		x = self.canvas.canvasx(event.x)#retourne la coordonnée x du canvas
		y = self.canvas.canvasy(event.y)
		bbox = self.canvas.bbox(self.container)  # get image area
		if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
		else: return  # zoom only inside image area
		scale = 1.0
		# Respond to Linux (event.num) or Windows (event.delta) wheel event
		if event.num == 5 or event.delta == -120:  # scroll down
			i = min(self.width, self.height)
			if int(i * self.imscale) < 30: return  # image is less than 30 pixels
			self.imscale /= self.delta
			scale        /= self.delta
		if event.num == 4 or event.delta == 120:  # scroll up
			i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
			if i < self.imscale: return  # 1 pixel is bigger than the visible area
			self.imscale *= self.delta
			scale        *= self.delta
		self.wb*=scale
		self.hgb*=scale
		self.canvas.scale(self.imageid,x,y,scale,scale)
		self.canvas.scale(self.container,x,y,scale,scale)

		self.isMoved=False
		self.isWheel=True
		self.show_image()
		self.isWheel=False
		

	def show_image(self, event=None):
		''' Show image on the Canvas '''
		bbox1 = self.canvas.bbox(self.container)  # get image area
		# Remove 1 pixel shift at the sides of the bbox1
		bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
		bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
				self.canvas.canvasy(0),
				self.canvas.canvasx(self.canvas.winfo_width()),
				self.canvas.canvasy(self.canvas.winfo_height()))
		bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
				max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
		if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
			bbox[0] = bbox1[0]
			bbox[2] = bbox1[2]
		if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
			bbox[1] = bbox1[1]
			bbox[3] = bbox1[3]
		self.canvas.configure(scrollregion=bbox)  # set scroll region
		self.x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
		self.y1 = max(bbox2[1] - bbox1[1], 0)
		self.x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
		self.y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        
		x1img = min(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
		y1img = min(bbox2[1] - bbox1[1], 0)
		x2img = max(bbox2[2], bbox1[2]) - bbox1[0]
		y2img = max(bbox2[3], bbox1[3]) - bbox1[1]
		if int(self.x2 - self.x1) > 0 and int(self.y2 - self.y1) > 0:  # show image if it in the visible area
			x = min(int(self.x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
			y = min(int(self.y2 / self.imscale), self.height)  # ...and sometimes not
			image = self.image.crop((int(self.x1 / self.imscale), int(self.y1 / self.imscale), x, y))#selectionner une partie d'une image
			imagetk = ImageTk.PhotoImage(image.resize((int(self.x2 - self.x1), int(self.y2 - self.y1))))

			global sizeXimg
			global sizeYimg
			self.sizeXimg = [x2img ,x1img]
			self.sizeYimg = [y2img , y1img]
			if self.imageid is not None:
				self.canvas.delete(self.imageid)
			self.imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
								anchor='nw', image=imagetk)
			if self.isMoved is not True:
				self.posImgX=max(bbox2[0], bbox1[0])
				self.posImgY=max(bbox2[1], bbox1[1])
			self.canvas.lower(self.imageid)  # set image into background
			self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
		
			global buttonPosList
			if len(self.buttonResetList)>0 : 
				for idButton in self.buttonResetList:

					self.canvas.delete(idButton)
			
			
			self.img = Image.open('guillemets.jpg')
			self.sizeButton=15
			self.imag = self.img.resize((self.sizeButton,self.sizeButton))
			self.photo = ImageTk.PhotoImage(self.imag)

			self.mwd=self.wb
			self.mhg=self.hgb
			
			self.wimg=self.mwd/self.dimention[0]
			if self.numPage%self.dimention[0] ==0 :
				self.himg=self.mhg/(int(self.numPage/self.dimention[0]))
			else:
				self.himg=self.mhg/(int(self.numPage/self.dimention[0]+1))
			self.k=0
			newLigne=0
			if self.isMoved is not True:
				self.buttonResetList={}
				while self.k < self.numPage : #quand k inferieur de nombre de page
					(self.posX,self.posY)=self.canvas.coords(self.imageid)#retourne les coordonnées de id image
					
					self.posX-=10
					self.posY=self.posY+10+newLigne*self.himg
					self.rect=None
					for j in range (0,self.dimention[0]):#dimention par defaut est 4, donc j = 0,1,2,3
						if self.k < self.numPage :
							buttonPosList=[]
							self.bt_expo = tk.Button(self.master, text=str(self.k), image=self.photo , command=self.completeTab)
							self.posX+=self.wimg
							if self.isWheel is True:
								self.posX-=int(self.x1/ self.imscale)
								self.posY-=int(self.y1 / self.imscale)
								buttonCreated = self.canvas.create_window(self.posX, self.posY, window=self.bt_expo)
								buttonPosList.append(self.posX)
								buttonPosList.append(self.posY)
							else:
								buttonCreated = self.canvas.create_window(self.posX, self.posY, window=self.bt_expo)
								buttonPosList.append(self.posX)
								buttonPosList.append(self.posY)
							
							self.buttonResetList[buttonCreated]=buttonPosList
							
							self.k += 1
					newLigne+=1
					
	#supprime les boutons
	def deleteAllButton(self):
		self.canvas.delete("all");
		self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
		self.canvas.update() 
	#mister les boutons
	def findAll(self): #imprimer tous les items de canvas, par exemple les buttons,l'image
		print(str(self.canvas.find_all()))
		
	def createButton(self,event): #L’utilisateur a modifié la taille d’un widget, par exemple en déplaçant un coin ou un côté de la fenêtre.
		self.show_image()
		self.canvas.update() 


#return le numero de la page selectionner avec les boutons
def getNumPage():
    return selectClick
   