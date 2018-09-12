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
import time

#nos variable
listImgOfCanvas=[]
zoomImg=None




#inverser l'etat des rectangle entre plein et vide
def fullRect(full):
	return not(full)


#retourner la liste des images
def getListImg(nameProjet,rectFull):
	if rectFull:
		rect='fullRect'
	else:
		rect='emptyRect'
	listImg = os.listdir('DrawOnImage/finalResult/' + nameProjet + '/' +rect)
	size = len(listImg)
	listImgOrder=[]
	for i in range (0,size):
		listImgOrder.append('classified-page-' + str(i) + '.png')
	return listImgOrder
	
#mise a jour le canvas	
def setCanvas(canva,dicimg,listImg,mwd,mhg,dm,nameProjet,rectFull,newWin,root):
	global zoomImg
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
	path='UseCheminDeFer/img.jpg'
	#new_im.resize((canva.winfo_width(),canva.winfo_height()))
	new_im.save(path,'JPEG',quality=1000)
	
	
	def callback():
		global zoomImg
		zoomImg=None
		canva.destroy()
	canva.protocol("WM_DELETE_WINDOW",callback)
	
	if newWin is not None:
		zoomImg=None
	if zoomImg is None:
		canva.wm_state('iconic')
		zoomImg=zi.Zoom_Advanced(canva,path,dm,getNumberImg(nameProjet),nameProjet,root)
	else:
		#zoomImg.deleteAllButton()
		canva.wm_state('iconic')
		zoomImg==zi.Zoom_Advanced(canva,path,dm,getNumberImg(nameProjet),nameProjet,root)
	canva.wm_state('normal')


#recuper le nombre de page
def getNumberImg(nameProjet):
		return len(os.listdir('DrawOnImage/finalResult/'+ nameProjet + '/emptyRect' ))#que les rectangles soit plein ou pas il y a antant de page

#supprime les image du canvas
def deleteCanvas(canva):
	global listImgOfCanvas
	for img in listImgOfCanvas:
		canva.delete(img)
		
#permet de zoomer et de se deplacer sur l'image
def zoomImage(canva, dimention):
	zoom_ad = Zoom_Advanced(canva,path,dimention)