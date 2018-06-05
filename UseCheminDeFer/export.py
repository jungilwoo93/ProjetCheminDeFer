"""
Created on Mon May  30 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
from PIL import Image, ImageFont, ImageDraw, ImageTk
import xlrd
import os
#import signal
import pyautogui
 

pathOfExcel = 'fichiersExcel/Référence et page pdf Jardin apollon.xlsx'
numbutton=0

def completeTab():
	numButton=numbutton
	wb = xlrd.open_workbook(pathOfExcel)
	sh = wb.sheet_by_name(u'Feuil1')
	colonneB = sh.col_values(1)
	case=[]
	caractere = " "
	for l in colonneB :
		line = l.split(caractere)
		if line[0]=='Page':###peut etre pas utile
			if int(line[1])==int(numButton):
				print('c est les meme')
				#os.kill(signal.CTRL_C_EVENT, 0)#1
				pyautogui.hotkey('ctrl', 'c')
				print('cccoopppiierrrr')
					#pour windows
					#on met le curseur sur le pixel 400 par 400 
					#windll.user32.SetCursorPos(400,400) 
					#time.sleep(0.1) 
					#on presse le bouton gauche de la souris 
					#windll.user32.mouse_event(2,0,0,0,0) 


def posMouse(event, widthBigIm, heightBigIm, numPage, dimention, sizeY):
		MouseX=event.x
		MouseY=event.y
		sizeButton=10
		k=0
		mwd=widthBigIm
		mhg=heightBigIm
		wimg=mwd/dimention[0]
		if numPage%dimention[0] ==0 :
			himg=(sizeY[0]-sizeY[1])/(int(numPage/dimention[0]))
		else:
			himg=(sizeY[0]-sizeY[1])/(int(numPage/dimention[0])+1)
		posX=wimg-10
		posY=10
		while k < numPage :
			for j in range (0,dimention[0]):
				if k <= numPage :
					if (abs(posX-MouseX) < 15) and (abs(posY-MouseY) < 15) :
						print('bouton num')
						print(k)
						global numbutton
						numbutton=k
					posX+=wimg
					k += 1
			posY+=himg
			posX=wimg-10



def creatButton(canvas, widthBigIm, heightBigIm, numPage, dimention, master,sizeY):
		img = Image.open('guillemets.jpg')
		sizeButton=10
		imag = img.resize((sizeButton,sizeButton))
		photo = ImageTk.PhotoImage(imag)
		k=0
		mwd=widthBigIm
		mhg=heightBigIm
		wimg=mwd/dimention[0]
		if numPage%dimention[0] ==0 :
			himg=(sizeY[0]-sizeY[1])/(int(numPage/dimention[0]))
		else:
			himg=(sizeY[0]-sizeY[1])/(int(numPage/dimention[0])+1)
		posX=wimg-10
		posY=10
		while k < numPage :
			for j in range (0,dimention[0]):
				if k <= numPage :
					bt_green = tk.Button(master, image=photo , command=completeTab)#master,#command=lambda: self.canvas.config(bg="green")
					bt_green_w = canvas.create_window(posX, posY, window=bt_green)
					posX+=wimg
					k += 1
			posY+=himg
			posX=wimg-10
			


