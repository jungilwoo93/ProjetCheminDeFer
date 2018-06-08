"""
Created on Mon May  30 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
from PIL import Image, ImageFont, ImageDraw, ImageTk
import xlrd
import os
#import signal
#import pyautogui
import pyperclip
 

pathOfExcel = 'fichiersExcel/Référence et page pdf Jardin apollon.xlsx'
numbutton=0

def completeTab():
	numButton=numbutton
	wb = xlrd.open_workbook(pathOfExcel)
	sh = wb.sheet_by_name(u'Feuil1')
	colonneB = sh.col_values(1)
	case=[]
	caractere = " "
	lines=0
	for l in colonneB :
		line = l.split(caractere)
		if line[0]=='Page':
			print('ca commence par page')
			print(numButton)
			print(line[1])
			if int(line[1])==int(numButton):
				print('c est les meme')
				#os.kill(signal.CTRL_C_EVENT, 0)#1
				#pyautogui.hotkey('ctrl', 'c')
				print('cccoopppiierrrr')
				
				case = sh.col_values(0)[lines]
				pyperclip.copy(case)
		lines+=1
					#pour windows
					#on met le curseur sur le pixel 400 par 400 
					#windll.user32.SetCursorPos(400,400) 
					#time.sleep(0.1) 
					#on presse le bouton gauche de la souris 
					#windll.user32.mouse_event(2,0,0,0,0) 


def posMouse(MouseX, MouseY, widthBigIm, heightBigIm, numPage, dimention, sizeY):
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
					#print('k par trop grand')
					#print(abs(posX-MouseX))
					#print(abs(posY-MouseY))
					#print(posX)
					#print(MouseX)
					if (abs(posX-MouseX) < 16) and (abs(posY-MouseY) < 16) :
						#print('bouton num')
						#print(k)
						global numbutton
						numbutton=k
						return k
						
					posX+=wimg
					k += 1
			posY+=himg
			posX=wimg-10
		



def creatButton(canvas, widthBigIm, heightBigIm, numPage, dimention, master,sizeY):
		img = Image.open('guillemets.jpg')
		sizeButton=10
		buttonList=[]
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
					bt = tk.Button(master, image=photo , command=completeTab)#master,#command=lambda: self.canvas.config(bg="green")
					buttonList.append(bt)
					#bt_w = canvas.create_window(posX, posY, window=bt)
					posX+=wimg
					k += 1
			posY+=himg
			posX=wimg-10
		
		return buttonList



