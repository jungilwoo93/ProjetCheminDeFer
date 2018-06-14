"""
Created on Wed May 16 09:34:19 2018

@author: rachel NOIREAU & Liuyan PAN
"""
from fpdf import FPDF
from PIL import Image
import tkinter as tk
import tkinter.filedialog as tf
import os



def ChooseWhereSave():
	f=tf.asksaveasfile(
		title="Enregistrer sous …",
		filetypes=[('PDF files','.pdf')],
		defaultextension=".pdf")
	#print(f.name) 
	return f.name
	

#mettre les images dans un pdf
def pngToPdf(nameProjet,dimention,isFull,pathSave):
	marge=20#marge entre image et bord de la feuille#peut etre changé sans problemes
	spacing=5#espace entre les images #peut etre changé sans problemes
	numPage=0
	path, imageList = getImg(nameProjet, isFull)
	x=0+marge
	y=0+marge
	#pour A4 : 2480 x 3508 pixels.
	#210 mm × 297 mm 
	mwd=210
	img=Image.open(path +'/' +imageList[0])
	wd,hg=img.size
	w=int(((mwd-dimention[0]*spacing)-2*marge)/dimention[0])
	h=int((hg/wd)*(((mwd-dimention[0]*spacing)-2*marge)/dimention[0]))
	pdf = FPDF(format='A4')#orientation = 'P'(ou L), unit = 'mm',
	k=0
	while k< len(imageList):
		if not(k == len(imageList)):
			pdf.add_page()
		for i in range (0, dimention[1]):
			for j in range (0, dimention[0]):
				if not(k == len(imageList)):
					img=Image.open(path + '/' + imageList[k])
					pdf.image(path + '/' + imageList[k], x, y, w, h)
					k += 1
					x += w + spacing
			x = 0 + marge
			y += h + spacing
		pdf.set_y(-297+10)
		pdf.set_font('Arial', 'I', 7)#I pour italique
		pdf.cell(0, 10, nameProjet + ' Page ' + str(pdf.page_no()), 0, 0, 'C')#mettre un numero de page
		y=0+marge
	pdf.output(pathSave, "F")

def getImg(nameProjet, isFull):
	if isFull:
		rect='fullRect'
	else:
		rect='emptyRect'
	path='DrawOnImage/finalResult/' + nameProjet + '/' + rect
	listImg = os.listdir(path)
	size = len(listImg)
	listImgOrder=[]
	for i in range (0,size):
		listImgOrder.append('classified-page-' + str(i) + '.png')
	return path, listImgOrder
	
