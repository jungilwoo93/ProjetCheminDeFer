# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:37:31 2018

@author: Rachel NOIREAU & Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf
import os

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

def setDimention(x,y):
	global dimention
	dimention=[x,y]



def getListImg(nameProjet):
	listImg = os.listdir('DrawOnImage/finalResult/' + nameProjet)
	chrono = lambda v: os.path.getmtime(os.path.join('DrawOnImage/finalResult/' + nameProjet, v))
	listImg.sort(key = chrono)
	return listImg



