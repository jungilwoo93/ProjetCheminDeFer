# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:37:31 2018

@author: Rachel NOIREAU & Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf
import os
from PIL import Image, ImageFont, ImageDraw, ImageTk
from UseCheminDeFer import zoomImag as zi

listImgOfCanvas=[]

# def ChooseWhereSave():
	# f=tkinter.filedialog.asksaveasfile(
		# title="Enregistrer sous … un fichier",
		# filetypes=[('PDF files','.pdf')])
	# print(f.name) 
	





def fullRect(full):
	return not(full)




def getListImg(nameProjet,rectFull):
	if rectFull:
		rect='fullRect'
	else:
		rect='emptyRect'
	listImg = os.listdir('DrawOnImage/finalResult/' + nameProjet + '/' +rect)
	#chrono = lambda v: os.path.getmtime(os.path.join('DrawOnImage/finalResult/' + nameProjet + '/' +rect, v))
	#listImg.sort(key = chrono)
	size = len(listImg)
	listImgOrder=[]
	for i in range (0,size):
		listImgOrder.append('classified-page-' + str(i) + '.png')
	print(listImgOrder)#########################################
	return listImgOrder
	
	
def setCanvas(canva,dicimg,listImg,mwd,mhg,dm,nameProjet,rectFull):
	if rectFull:
		rect='fullRect'
	else:
		rect='emptyRect'
	posX=0
	posY=0
	widthImg=dm[0]
	img=Image.open('DrawOnImage/finalResult/'+ nameProjet +'/' +rect + '/' + listImg[0])
	wd,hg=img.size
	h=len(listImg)%dm[0]
	col=int(len(listImg)/dm[0])
	spacing=3
	if h != 0:
		col+=1
	new_im = Image.new('RGB',(int(wd*widthImg),int(hg*col)))
	for image in listImg:
		img=Image.open('DrawOnImage/finalResult/'+ nameProjet + '/' +rect +'/'+ image)
		wd,hg=img.size
		hg-=spacing
		wd-=spacing
		new_im.paste(img,(int(posX),int(posY)))
		posX+=wd+spacing
		if posX>=(wd*widthImg) :
			posY+=hg+spacing
			posX=0
	#posX=0
	#posY=0
	#scale= 1.0*wd/mwd
	#newImg=img.resize((int((mwd-widthImg*2)/widthImg),int((hg/wd)*((mwd-widthImg*2)/widthImg))),Image.ANTIALIAS)	
	#canva.config(width=mwd)#height=mhg
	#photo = ImageTk.PhotoImage(newImg)
	#canva.image=photo
	#imgCreated=canva.create_image(posX,posY,image=photo,anchor="nw")
	#listImgOfCanvas.append(imgCreated)
	#dicimg[photo] = photo
		
	#posX+=mwd/widthImg+2
	#if posX>mwd :
	#	posY+=((hg/wd)*((mwd-widthImg*2)/widthImg))+2
	#	posX=0
	#size=[]
	#size.append(canva.winfo_width())
	#size.append(canva.winfo_height())
	#canva.saveAsImage('D:\\S4\\ProjetCheminDeFer\\UseCheminDeFer\\img.png',None,'PNG')
	#im = Image.new('RGBA', size, (255, 255, 255, 255))
	#draw=ImageDraw.Draw(im)
	#canva.postscript(file='D:\\S4\\ProjetCheminDeFer\\UseCheminDeFer\\img.ps')
	path='UseCheminDeFer/img.jpg'
	new_im.save(path,'JPEG',quality=1000)
	zi.Zoom_Advanced(canva,path,dm,getNumberImg(nameProjet))
	
	#new_im.show()

#recuper le nombre de page
def getNumberImg(nameProjet):
		return len(os.listdir('DrawOnImage/finalResult/'+ nameProjet + '/emptyRect' ))#que les rectangles soit plein ou pas il y a antant de page


def deleteCanvas(canva):
	global listImgOfCanvas
	for img in listImgOfCanvas:
		canva.delete(img)

def zoomImage(canva, dimention):
	zoom_ad = Zoom_Advanced(canva,path,dimention)