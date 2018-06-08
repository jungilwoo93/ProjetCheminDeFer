# -*- coding: utf-8 -*-
"""
Created on Mon May 21 19:23:16 2018

@author: rachel
"""
"""columns=0
lines=0

def show():
    for ligne in range(5):
        for colonne in range(5):
            Button(fenetre, text='L%s-C%s' % (ligne, colonne), borderwidth=1).grid(row=ligne, column=colonne)
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
	''' Advanced zoom of the image '''
	def __init__(self, mainframe, path,dim,numberPage):
		''' Initialize the main Frame '''
		global dimention
		dimention=dim
		global numPage
		numPage=numberPage
		ttk.Frame.__init__(self, master=mainframe)
        #self.master.title('Zoom with mouse wheel')
        # Vertical and horizontal scrollbars for canvas
		vbar = AutoScrollbar(self.master, orient='vertical')
		hbar = AutoScrollbar(self.master, orient='horizontal')
		vbar.grid(row=0, column=1, sticky='ns')
		hbar.grid(row=1, column=0, sticky='we')
        # Create canvas and put image on it
		self.canvas = tk.Canvas(self.master, highlightthickness=0,
							xscrollcommand=hbar.set, yscrollcommand=vbar.set)
		self.canvas.grid(row=0, column=0, sticky='nswe')
		self.canvas.update()  # wait till canvas is created
		vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
		hbar.configure(command=self.scroll_x)
		# Make the canvas expandable
		self.master.rowconfigure(0, weight=3)
		self.master.columnconfigure(0, weight=1)
		# Bind events to the Canvas
		self.canvas.bind('<Configure>', self.show_image)  # canvas is resized
		self.canvas.bind('<ButtonPress-1>', self.move_from)
		self.canvas.bind('<B1-Motion>',     self.move_to)
		self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
		#self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
		#self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
		self.canvas.bind('<Motion>', self.posMouse)
		self.image = Image.open(path)  # open image
		
		
		self.width, self.height = self.image.size
		
		
		
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

	
	def scroll_y(self, *args, **kwargs):
		''' Scroll canvas vertically and redraw the image '''
		self.canvas.yview(*args, **kwargs)  # scroll vertically
		self.show_image()  # redraw the image

	def scroll_x(self, *args, **kwargs):
		''' Scroll canvas horizontally and redraw the image '''
		self.canvas.xview(*args, **kwargs)  # scroll horizontally
		self.show_image()  # redraw the image
	
	
	def posMouse(self, event):
		mouseX = self.canvas.canvasx(event.x)
		mouseY = self.canvas.canvasy(event.y)
		exp.posMouse(mouseX,mouseY, self.width, self.height, numPage, dimention, sizeYimg)
	
	def selectPage(self, event):
		#print('ca clic')
		
		mouseX = event.x
		mouseY = event.y
		x = self.canvas.canvasx(event.x)
		y = self.canvas.canvasy(event.y)
		sizeX = sizeXimg#a simplifier
		sizeY = sizeYimg
		global pageSelected
		pageSelected = ep.selectPage(x, y, mouseX, mouseY, sizeX, sizeY,dimention, numPage)#root ou canva?

	def move_from(self, event):
		''' Remember previous coordinates for scrolling with the mouse '''
		self.selectPage(event)
		self.canvas.scan_mark(event.x, event.y)

	def move_to(self, event):
		''' Drag (move) canvas to the new position '''
		self.canvas.scan_dragto(event.x, event.y, gain=1)
		self.show_image()  # redraw the image

	def wheel(self, event):
		''' Zoom with mouse wheel '''
		x = self.canvas.canvasx(event.x)
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
		self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
		self.show_image()

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
		x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
		y1 = max(bbox2[1] - bbox1[1], 0)
		x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
		y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        
		x1img = min(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
		y1img = min(bbox2[1] - bbox1[1], 0)
		x2img = max(bbox2[2], bbox1[2]) - bbox1[0]
		y2img = max(bbox2[3], bbox1[3]) - bbox1[1]
		if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
			x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
			y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
			image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
			imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
			global sizeXimg
			global sizeYimg
			sizeXimg = [x2img ,x1img]
			sizeYimg = [y2img , y1img]
			imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
								anchor='nw', image=imagetk)
			self.canvas.lower(imageid)  # set image into background
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
		
		
		self.img = Image.open('guillemets.jpg')
		self.sizeButton=15
		self.imag = self.img.resize((self.sizeButton,self.sizeButton))
		self.photo = ImageTk.PhotoImage(self.imag)
		self.mwd=self.width
		self.mhg=self.height
		self.wimg=self.mwd/dimention[0]
		if numPage%dimention[0] ==0 :
			self.himg=(sizeYimg[0]-sizeYimg[1])/(int(numPage/dimention[0]))
		else:
			self.himg=(sizeYimg[0]-sizeYimg[1])/(int(numPage/dimention[0])+1)
		posX=self.wimg-13
		posY=13
		self.k=0
		while self.k < numPage :
			for j in range (0,dimention[0]):
				if self.k <= numPage :
					self.bt_expo = tk.Button(self.master, text=str(self.k), image=self.photo , command=exp.completeTab)
					self.bt_expo_w = self.canvas.create_window(posX, posY, window=self.bt_expo)
					#print(self.bt_expo['text'])
					posX+=self.wimg
					self.k += 1
			posY+=self.himg
			posX=self.wimg-13
			
		def posMouse(self,event):
			exp.posMouse(event, self.width, self.height, numPage, dimention, sizeYimg)
		
		#self.canvas.bind('<Motion>' ,posMouse)
		#lambda : 
		
		
		
		#exp.creatButton(self.canvas, self.width, self.height,numPage,dimention, self.master,sizeYimg)
    
def getNumPage():
    return pageSelected
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