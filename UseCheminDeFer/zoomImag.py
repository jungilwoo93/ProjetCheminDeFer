# -*- coding: utf-8 -*-
"""
Created on Mon May 21 19:23:16 2018

@author: Liuyan PAN
"""




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
	def __init__(self, mainframe, path,dim,numberPage,nameProj):
		''' Initialize the main Frame '''
		#global dimention
		self.dimention=dim
		#global numPage
		self.numPage=numberPage
		self.nameProjet=nameProj

		ttk.Frame.__init__(self, master=mainframe)
        #self.master.title('Zoom with mouse wheel')
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
		#self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
		#self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
		self.canvas.bind('<Motion>', self.posMouse)
		self.image = Image.open(path) # open image
		self.width, self.height = self.image.size
		self.wb=self.width
		self.hgb=self.height
		self.isMoved=False
		self.isWheel=False
		#print("    " +str(self.buttonResetList))
		#self.created=True
		
		
		#les boutons 

		
		# self.img = Image.open('guillemets.jpg')
		# self.sizeButton=40
		# self.imag = self.img.resize((self.sizeButton,self.sizeButton))
		# self.photo = ImageTk.PhotoImage(self.imag)
		# self.posX=40
		# self.posY=60
		# self.bt_green = tk.Button(self.master, image=self.photo)#command=lambda: self.canvas.config(bg="green")
		# self.bt_green_w = self.canvas.create_window(self.posX, self.posY, window=self.bt_green)
		

		
		self.imscale = 1.0  # scale for the canvaas image
		self.delta = 1.3  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
		
		#exp.creatButton(self.canvas, self.width, self.height,numPage,dimention, self.master,sizeYimg)
		
		self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
		self.show_image()
	
	def completeTab(self):
		global selectClick
		selectClick=pageSelected
		
		exp.completeTab(pageSelected,self.nameProjet)

	
	def scroll_y(self, *args, **kwargs):
		''' Scroll canvas vertically and redraw the image '''
		self.canvas.yview(*args, **kwargs)		# scroll vertically
		self.isMoved=True
		self.show_image()
		#self.canvas.update() 
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
		#print("listButtonavant " +str(self.buttonResetList))
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
					#print("buttonPosList " +str(buttonPosList))
					self.bt_expo = tk.Button(self.master, text=str(self.k), image=self.photo , command=self.completeTab)
					buttonCreated = self.canvas.create_window(newbuttonPosList[0], newbuttonPosList[1]-diff, window=self.bt_expo)
					buttonPosList.append(newbuttonPosList[0])
					buttonPosList.append(newbuttonPosList[1]-diff)
					#buttonCreated=self.canvas.create_window(buttonList[i][0], buttonList[i][1], window=buttonList[i][2])
					self.buttonResetList[buttonCreated]=buttonPosList
					#self.buttonResetList.append(buttonCreated)
					self.k += 1
			newLigne+=1
		#print(" " + str(self.vbar.get()))
		#print(" " +str(self.hbar.get()))
		  # redraw the image

	def scroll_x(self, *args, **kwargs):
		''' Scroll canvas horizontally and redraw the image '''
		self.canvas.xview(*args, **kwargs)  # scroll horizontally
		#print("scoll_x")
		
		self.show_image()  # redraw the image
		self.isMoved=True
		self.canvas.update() 
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
		#print("listButtonavant " +str(self.buttonResetList))
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
					#print("buttonPosList " +str(buttonPosList))
					self.bt_expo = tk.Button(self.master, text=str(self.k), image=self.photo , command=self.completeTab)
					buttonCreated = self.canvas.create_window(newbuttonPosList[0]-diff, newbuttonPosList[1], window=self.bt_expo)
					buttonPosList.append(newbuttonPosList[0]-diff)
					buttonPosList.append(newbuttonPosList[1])
					#buttonCreated=self.canvas.create_window(buttonList[i][0], buttonList[i][1], window=buttonList[i][2])
					self.buttonResetList[buttonCreated]=buttonPosList
					#self.buttonResetList.append(buttonCreated)
					self.k += 1
			newLigne+=1
	
	def posMouse(self,event):
		mouseX = self.canvas.canvasx(event.x)
		mouseY = self.canvas.canvasy(event.y)
		#print(self.buttonResetList)
		Pselected,findButton=exp.posMouse(mouseX,mouseY, self.width, self.height, self.numPage, self.dimention, sizeYimg,self.wb,self.hgb,self.canvas.coords(self.imageid),self.buttonResetList,self.nameProjet)
		if findButton:
			global pageSelected
			pageSelected = Pselected

	def selectPage(self, event):
		#print('ca clic')
		
		mouseX = event.x
		mouseY = event.y
		x = self.canvas.canvasx(event.x)
		y = self.canvas.canvasy(event.y)
		sizeX = sizeXimg#a simplifier
		sizeY = sizeYimg
		#pour selection sur toute la page
		#pageSelected = ep.selectPage(x, y, mouseX, mouseY, sizeX, sizeY,dimention, numPage,self.wb,self.hgb,self.canvas.coords(self.imageid))#root ou canva?


	def move_from(self, event):
		''' Remember previous coordinates for scrolling with the mouse '''
		self.selectPage(event)
		#print("move from")
		self.canvas.scan_mark(event.x, event.y)
		self.startX=event.x
		self.startY=event.y

	def move_to(self, event):
		''' Drag (move) canvas to the new position '''
		self.canvas.scan_dragto(event.x, event.y, gain=1)
		#print("move_to")
		"""print("start " +str(self.startX) + " " +str(self.startY))
		print("event " +str(event.x) + " " +str(event.y))
		print("posx!!" + str(self.posX))
		print("posy!!" + str(self.posY))
		print("diffx " + str(diffX))
		print("diffy " +str(diffY))"""
		self.isMoved=True
		self.show_image() # redraw the image
		self.canvas.update() 
		diffX=(self.startX-event.x)/self.wimg
		diffY=(self.startY-event.y)/self.himg
				
		if len(self.buttonResetList)>0 : 
			for idButton in self.buttonResetList:
				self.canvas.delete(idButton)
		self.img = Image.open('guillemets.jpg')
		self.sizeButton=15
		self.imag = self.img.resize((self.sizeButton,self.sizeButton))
		self.photo = ImageTk.PhotoImage(self.imag)
		buttonMoveList=self.buttonResetList
		#print("listButtonavant " +str(self.buttonResetList))
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
					#print("buttonPosList " +str(buttonPosList))
					self.bt_expo = tk.Button(self.master, text=str(self.k), image=self.photo , command=self.completeTab)
					buttonCreated = self.canvas.create_window(newbuttonPosList[0]-diffX/50, newbuttonPosList[1]-diffY/50, window=self.bt_expo)
					buttonPosList.append(newbuttonPosList[0]-diffX/50)
					buttonPosList.append(newbuttonPosList[1]-diffY/50)
					#print("posx!! move_to"+str(buttonPosList[0]))
					#print("posy!! move_to"+str(buttonPosList[1]))
					"""print("posX avant " + str(newbuttonPosList[0]))
					print("posY avant " + str(newbuttonPosList[1]))
					print("posX apres " + str(newbuttonPosList[0]-diffX))
					print("posY apres " + str(newbuttonPosList[1]-diffY))"""
					#buttonCreated=self.canvas.create_window(buttonList[i][0], buttonList[i][1], window=buttonList[i][2])
					self.buttonResetList[buttonCreated]=buttonPosList
					#self.buttonResetList.append(buttonCreated)
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
		#(self.posX,self.posY)=self.canvas.coords(self.imageid)#retourne les coordonnées de id image
		#print(str(self.posX)+" move to "+str(self.posY))
		#print("listButton " +str(self.buttonResetList))

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
		"""if len(self.buttonResetList)>0 : 
			for idButton in self.buttonResetList:
				self.canvas.delete(idButton)"""
		self.canvas.scale(self.imageid,x,y,scale,scale)
		self.canvas.scale(self.container,x,y,scale,scale)
		
		"""buttonMoveList=self.buttonResetList
		self.buttonResetList={}
		for idButton in buttonMoveList:
			buttonPosList=[]
			newbuttonPosList=buttonMoveList[idButton]
			self.canvas.move(idButton,newbuttonPosList[0]/scale,newbuttonPosList[1]/scale)
			#self.canvas.scale(idButton,newbuttonPosList[0],newbuttonPosList[1],scale,scale)
			buttonPosList.append(newbuttonPosList[0]/scale)
			buttonPosList.append(newbuttonPosList[1]/scale)
			self.buttonResetList[idButton]=buttonPosList"""
		#self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
		self.isMoved=False
		self.isWheel=True
		self.show_image()
		#print("wheel")
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
			#print("x " +str(x))
			y = min(int(self.y2 / self.imscale), self.height)  # ...and sometimes not
			#print("y " +str(y))
			#print("crop " + str(int(self.x1 / self.imscale)) + "  " +str(int(self.y1 / self.imscale)))
			#print("crop " +str(x) + " "+str(y))
			image = self.image.crop((int(self.x1 / self.imscale), int(self.y1 / self.imscale), x, y))#selectionner une partie d'une image
			imagetk = ImageTk.PhotoImage(image.resize((int(self.x2 - self.x1), int(self.y2 - self.y1))))
			#print("x2-x1 " + str(int(self.x2 - self.x1)))
			#print("y2-y1 " +str(int(self.y2 - self.y1)))
			global sizeXimg
			global sizeYimg
			self.sizeXimg = [x2img ,x1img]
			self.sizeYimg = [y2img , y1img]
			#print("sizeXimg " +str(sizeXimg))
			#print("sizeYimg " +str(sizeYimg))
			if self.imageid is not None:
				self.canvas.delete(self.imageid)
			self.imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
								anchor='nw', image=imagetk)
			#print("id image " +str(self.imageid))
			if self.isMoved is not True:
				self.posImgX=max(bbox2[0], bbox1[0])
				self.posImgY=max(bbox2[1], bbox1[1])
			#print("x y de image " +str(max(bbox2[0], bbox1[0])) +" " +str(max(bbox2[1], bbox1[1])))
			#print(str(max(bbox2[0], bbox1[0])))
			#print(str())
			#print(str())
			#print(str())
			self.canvas.lower(self.imageid)  # set image into background
			self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
		
		#creatButton
		# img = Image.open('guillemets.jpg')
		# sizeButton=20
		# imag = img.resize((sizeButton,sizeButton))
		# photo = ImageTk.PhotoImage(imag)
		# k=0
		# mwd=self.width
		# mhg=self.height
		# wimg=mwd/dimention[0]
		# if numPage%dimention[0] ==0 :
			# himg=(sizeYimg[0]-sizeYimg[1])/(int(numPage/dimention[0]))
		# else:
			# himg=(sizeYimg[0]-sizeYimg[1])/(int(numPage/dimention[0])+1)
		# posX=wimg-10
		# posY=10
		# while k < numPage :
			# for j in range (0,dimention[0]):
				# if k <= numPage :
					# bt_expo = tk.Button(self.master, image=photo , command=exp.completeTab)#master,#command=lambda: self.canvas.config(bg="green")
					# bt_expo_w = self.canvas.create_window(posX, posY, window=bt_expo)
					# posX+=wimg
					# k += 1
			# posY+=himg
			# posX=wimg-10
			global buttonPosList
			#print("buttonCreatedList1 "+str(self.buttonResetList))
			if len(self.buttonResetList)>0 : 
				for idButton in self.buttonResetList:
					#print("idbutton !!" + str(idButton))
					self.canvas.delete(idButton)
					#print("delete ")
			#print("buttonCreatedList2 "+str(self.buttonResetList))
			
			
			self.img = Image.open('guillemets.jpg')
			self.sizeButton=15
			self.imag = self.img.resize((self.sizeButton,self.sizeButton))
			self.photo = ImageTk.PhotoImage(self.imag)
			#print(str(self.canvas.coords(self.imageid)))
			
			#print("width "+str(self.width))
			#print("height " +str(self.height))
			#print("imagewidth "+str(image.width))
			#print("imageheight " +str(image.height))
			"""if self.created == True:
				self.mwd=self.width
				self.mhg=self.height
				self.created=False
				print("first")
			else:"""
			self.mwd=self.wb
			self.mhg=self.hgb
			
			self.wimg=self.mwd/self.dimention[0]
			#print("wimg "+str(self.wimg))
			if self.numPage%self.dimention[0] ==0 :
				self.himg=self.mhg/(int(self.numPage/self.dimention[0]))
				#self.himg=(sizeYimg[0]-sizeYimg[1])/(int(numPage/dimention[0]))
			else:
				self.himg=self.mhg/(int(self.numPage/self.dimention[0]+1))
				#self.himg=(sizeYimg[0]-sizeYimg[1])/(int(numPage/dimention[0])+1)
			#print("himg "+str(self.himg))
			#posX+=self.wimg
			#posX=self.wimg-13
			#posY=13
			self.k=0
			newLigne=0
			if self.isMoved is not True:
				#print("isMoved false")
				self.buttonResetList={}
				while self.k < self.numPage : #quand k inferieur de nombre de page
					(self.posX,self.posY)=self.canvas.coords(self.imageid)#retourne les coordonnées de id image
					
					#self.posX=max(bbox2[0], bbox1[0])
					#self.posY=max(bbox2[1], bbox1[1])
					#print(str(self.posX)+" cou cou "+str(self.posY))
					#self.canvas.create_rectangle(self.posX,self.posY,10,10,fill='red')
					self.posX-=10
					self.posY=self.posY+10+newLigne*self.himg
					#print("numpage" + str(numPage))
					self.rect=None
					for j in range (0,self.dimention[0]):#dimention par defaut est 4, donc j = 0,1,2,3
						if self.k < self.numPage :
							buttonPosList=[]
							self.bt_expo = tk.Button(self.master, text=str(self.k), image=self.photo , command=self.completeTab)
							self.posX+=self.wimg
							if self.isWheel is True:
								#print("true !!!!!!!!!!")
								self.posX-=int(self.x1/ self.imscale)
								self.posY-=int(self.y1 / self.imscale)
								buttonCreated = self.canvas.create_window(self.posX, self.posY, window=self.bt_expo)
								buttonPosList.append(self.posX)
								buttonPosList.append(self.posY)
							else:
								buttonCreated = self.canvas.create_window(self.posX, self.posY, window=self.bt_expo)
								buttonPosList.append(self.posX)
								buttonPosList.append(self.posY)
							
							#buttonList.append([posX, posY,self.bt_expo])
							#self.bt_expo_w = self.canvas.create_window(posX, posY, window=self.bt_expo)
							#print(self.bt_expo['text'])
							
							#print("wimg!!!!!!!!!!!! ")
							#print("self.x " +str(self.x1))
							#print("self.x2 " +str(self.x2))

							"""if int(self.x1/self.imscale)!= 0 or int(self.y1 / self.imscale)!=0 :
								print("show_image " + str(int(self.x1 / self.imscale)) + "  " +str(int(self.y1 / self.imscale)))"""
							
							"""	buttonCreated = self.canvas.create_window(self.posX, self.posY, window=self.bt_expo)
								print("posX " +str(self.posX))
								print("posY " +str(self.posY))
								buttonPosList.append(self.posX)
								buttonPosList.append(self.posY)
							else:
								self.posX-=int(self.x1 / self.imscale)
								self.posY-=int(self.y1 / self.imscale)
								buttonCreated = self.canvas.create_window(self.posX, self.posY, window=self.bt_expo)
								buttonPosList.append(self.posX)
								buttonPosList.append(self.posY)"""
							
								#print("posx!! show_image"+str(self.posX))
								#print("posy!! show_image"+str(self.posY))
							
							#buttonCreated=self.canvas.create_window(buttonList[i][0], buttonList[i][1], window=buttonList[i][2])
							self.buttonResetList[buttonCreated]=buttonPosList
							#self.buttonResetList.append(buttonCreated)
							self.k += 1
					newLigne+=1
				
		#print("show_image")
			#print("new ligne"+str(newLigne))
			#print("listButton " +str(self.buttonResetList))
			#posX=10
			#self.posY+=self.himg
			#self.posX=self.wimg-10
		#for i in range (0, len(buttonList)):
			
			#self.buttonResetList.append(buttonCreated)
		#i=0
		#print("buttonCreatedList3 "+str(self.buttonResetList))
		
		"""def posMouse(self,event):
			exp.posMouse(event, self.width, self.height, numPage, dimention, sizeYimg)"""
		
		#self.canvas.bind('<Motion>' ,posMouse)
		#lambda : 
		
		
		
		#exp.creatButton(self.canvas, self.width, self.height,numPage,dimention, self.master,sizeYimg): 
		
	def deleteAllButton(self):
		self.canvas.delete("all");
		self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
		self.canvas.update() 
		"""print(str(self.buttonResetList))
		if len(self.buttonResetList)>0 :
			print("delete")
			for idButton in self.buttonResetList:
				self.canvas.delete(idButton)
		self.buttonResetList={}"""
		
	def findAll(self):
		print(str(self.canvas.find_all()))
		#exp.creatButton(self.canvas, self.width, self.height,numPage,dimention, self.master,sizeYimg)
	def createButton(self,event):
		#print("configure")
		self.show_image()
		self.canvas.update() 

		#print("createdbutton")
			#print("new ligne"+str(newLigne))
			#print("listButton " +str(self.buttonResetList))
	
def getNumPage():
    return selectClick#pageSelected
    # def selectPage(event):
        # print('ca clic')
        # mouseX = event.x
        # mouseY = event.y
        # x = self.canvas.canvasx(event.x)
        # y = self.canvas.canvasy(event.y)
        # sizeX = sizeXimg
        # sizeY = sizeYimg
        # ep.selectPage(x, y, sizeX, sizeY)
'''
path = 'UseCheminDeFer/test.png'  # place path to your image here
root = tk.Tk()
app = Zoom_Advanced(root, path=path)
aoo = Zoom_Advanced(root, path=path)
root.mainloop()'''