"""
Created on Mon May  30 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
from PIL import Image, ImageFont, ImageDraw, ImageTk


def completeTab():
	print('ça va faire tab')



def creatButton(canvas, widthBigIm, heightBigIm, numPage, dimention, master,sizeY):
		img = Image.open('guillemets.jpg')
		sizeButton=10
		imag = img.resize((sizeButton,sizeButton))
		photo = ImageTk.PhotoImage(imag)
		k=0
		mwd=widthBigIm
		mhg=heightBigIm
		wimg=mwd/dimention[0]
		print(numPage)
		himg=(sizeY[0]-sizeY[1])/(numPage/dimention[0])
		print(himg)
		posX=wimg-10
		posY=10
		while k < numPage :
			print(dimention)
			for j in range (0,dimention[0]):
				if k <= numPage :
					print('colonne')
					bt_green = tk.Button( master, image=photo , command=completeTab)#master,#command=lambda: self.canvas.config(bg="green")
					bt_green_w = canvas.create_window(posX, posY, window=bt_green)
					posX+=wimg
					k += 1
			posY+=himg
			posX=wimg-10
			print(posY)
			


