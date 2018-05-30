# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:37:31 2018

@author: Rachel NOIREAU & Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf
import os
from PIL import Image, ImageFont, ImageDraw, ImageTk
import zoomImg as zi

listImgOfCanvas=[]

def ChooseWhereSave():
	f=tkinter.filedialog.asksaveasfile(
		title="Enregistrer sous … un fichier",
		filetypes=[('PDF files','.pdf')])
	print(f.name) 
	

def exportToPdf():
	print('export pdf')


#peut etre 2 ensemble si rien a rajouter
def fullRect(full):
	global rectFull
	#contrary=not(rectFull)
	rectFull=not(full)#not(rectFull)

#def emptyRect():
#	global rectFull
#	rectFull=False

def setDimention():
	x=4
	y=8
	print('changement de dimention')
	global dimention
	dimention=[x,y]



def getListImg(nameProjet):
	listImg = os.listdir('DrawOnImage/finalResult/' + nameProjet)
	chrono = lambda v: os.path.getmtime(os.path.join('DrawOnImage/finalResult/' + nameProjet, v))
	listImg.sort(key = chrono)
	return listImg
	
def setCanvas(canva,dicimg,listImg,mwd,mhg,dm):
	posX=0
	posY=0
	widthImg=dm[0]
	for image in listImg:
		img=Image.open('DrawOnImage/finalResult/'+ 'test'+ '/' + image)
		wd,hg=img.size
		scale= 1.0*wd/mwd
		newImg=img.resize((int((mwd-widthImg*2)/widthImg),int((hg/wd)*((mwd-widthImg*2)/widthImg))),Image.ANTIALIAS)
		canva.config(width=mwd)#height=mhg
		photo = ImageTk.PhotoImage(newImg)
		canva.image=photo
		imgCreated=canva.create_image(posX,posY,image=photo,anchor="nw")
		listImgOfCanvas.append(imgCreated)
		dicimg[photo] = photo
		posX+=mwd/widthImg+2
		if posX>mwd :
			posY+=((hg/wd)*((mwd-widthImg*2)/widthImg))+2
			posX=0
	im = Image.new('RGBA', canva, (255, 255, 255, 255))
	im.save('D:\\S4\\ProjetCheminDeFer\\UseCheminDeFer\\img.png')

def deleteCanvas(canva):
	global listImgOfCanvas
	for img in listImgOfCanvas:
		canva.delete(img)

def zoomImage(canva):
	zoom_ad = Zoom_Advanced(canva,path)