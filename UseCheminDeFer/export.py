"""
Created on Mon May  30 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
from PIL import Image, ImageFont, ImageDraw, ImageTk
import xlrd
import os
import pyperclip
 
 
nameProjet='new'
numbutton=0

#permet de trouver la reference corespondant a la page et de la copier dans le presse papier
def completeTab(numButton,nameProj):
	pathOfExcel = 'placesTesExcelAvecReferencesIci/'+nameProj+'.xlsx'
	global numbutton
	numbutton=numButton
	wb = xlrd.open_workbook(pathOfExcel)
	sh = wb.sheet_by_name(u'Feuil1')
	colonneB = sh.col_values(1)
	case=[]
	caractere = " "
	lines=0
	for l in colonneB :
		line = l.split(caractere)
		if line[0]=='Page':
			if int(line[1])==int(numButton+1):
				case = sh.col_values(0)[lines]
				pyperclip.copy(case)
		lines+=1
 

#permet de savoir sur quel bouton on a clicker
def posMouse(MouseX, MouseY, widthBigIm, heightBigIm, numPage, dimention, sizeY,w,h,posIm,listPosRect,nameProj):#
		global nameProjet
		nameProjet=nameProj
		sizeButton=10
		k=0
		mwd=w
		mhg=h
		wimg=mwd/dimention[0]
		if numPage%dimention[0] ==0 :
			himg=h/(int(numPage/dimention[0]))
		else:
			himg=h/(int(numPage/dimention[0])+1)
		for idbutt in listPosRect:
			rect=listPosRect[idbutt]
			if (abs(rect[0]-MouseX) < 16) and (abs(rect[1]-MouseY) < 16) : #fait une petite zone autour du bouton si la sourie entre dans la zone avant le click c'est quel va clique sur lebouton
						global numbutton
						numbutton=k
						return k,True
			k += 1
		return 0,False






