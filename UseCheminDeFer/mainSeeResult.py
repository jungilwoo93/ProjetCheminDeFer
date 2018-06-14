# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:37:31 2018

@author: Rachel NOIREAU & Liuyan PAN
"""
#la fenêtre pour afficher chemin de fer, nous pouvons agrandir ou réduire l'image, si on appuie un button ", on peut copier une référence dans un fichier excel, et ou on peut choisir l'image qu'on veut modifier
import tkinter as tk
import tkinter.filedialog as tf

#import de nos autre fichiers
from UseCheminDeFer import zoomImag as zi
from UseCheminDeFer import imgToPdf as itp
from UseCheminDeFer import buttonFunction as bf
import commun as co


####variable
dimention=[4,4] #dimension par défault
rectFull=False
colorDefault="#F5F5DC" #couleur du fond
func=co.FunctionCommun()


def creatChemin(nameProjet,dm=None,newWin=None):
	global dimention
	if dm is not None:
		dimention=dm
	####fenetre
	root = tk.Toplevel()#pour ouvrirune fenetre dans une autre fenetre
	ecran_width = root.winfo_screenwidth()*0.9
	ecran_height = root.winfo_screenheight()*0.85
	root.geometry('%dx%d+%d+%d' % (ecran_width, ecran_height, 1, 1))
	root.title("Chemin de Fer")
	root.resizable(width=False,height=False)
	
	####menu barrre
	menubar=tk.Menu(root)
	root.config(menu = menubar)
	menufile = tk.Menu(menubar,tearoff=0)
	view = tk.Menu(menubar,tearoff=0)
	editmenu = tk.Menu(menubar,tearoff=0)
	menubar.add_cascade(label="Fichier", menu=menufile)
	menubar.add_cascade(label="Affichage", menu=view)
	menubar.add_cascade(label="Modifier", menu=editmenu)
	
	#export le chemin de fer sous format pdf
	def PngToPdf():
		path=itp.ChooseWhereSave()
		itp.pngToPdf(nameProjet,dimention,rectFull,path)
		
#barre de menu suite
	menufile.add_command(label="Exporter en pdf", command=PngToPdf)
	menufile.add_separator() 
	menufile.add_command(label="Quitter", command=root.destroy) 

	#metre a jour l'etat des rectangle
	def fullRec():
		global rectFull
		rect=bf.fullRect(rectFull)
		rectFull=rect
		bf.setCanvas(root,dicimg,listImg,mwd,mhg,dimention,nameProjet,rectFull,newWin)
	rect= tk.Menu(view,tearoff=0)
	dim= tk.Menu(view,tearoff=0)
	view.add_cascade(label="rectangle", menu=rect)
	view.add_cascade(label="dimention", menu=dim)
	rect.add_checkbutton(label="Plein", command=fullRec)

	#ouverture de la fenetre de modification
	def edit():
		global dimention
		numPage=zi.getNumPage()
		root.destroy()
		func.openModif(nameProjet, numPage,dimention)
		path='imgFromPdf/' + nameProjet + '/' + nameProjet +'page-'+ str(numPage) +'png'
	editmenu.add_command(label="modifier une erreur", command=edit)
	if dimention is None:
		nitem=tk.IntVar()
		nitem.set(4)# bouton seletionner par defaut doit etre le meme que celui selectionner en haut
	else:
		nitem=tk.IntVar()
		nitem.set(dimention[0])
	#########nombre de page par feuille
	def setDimention():
		global dimention
		value=nitem.get()
		dimention[0]=value
		dimention[1]=value
		bf.setCanvas(root,dicimg,listImg,mwd,mhg,dimention,nameProjet,rectFull,newWin)
		
		
	#les differentes dimentions possibles
	dim.add_radiobutton(label="2*2",  variable=nitem, value=2,  command=setDimention)
	dim.add_radiobutton(label="3*3", variable=nitem, value=3,  command=setDimention)
	dim.add_radiobutton(label="4*4",  variable=nitem, value=4,  command=setDimention)
	dim.add_radiobutton(label="5*5",  variable=nitem, value=5,  command=setDimention)
	dim.add_radiobutton(label="6*6",  variable=nitem, value=6,  command=setDimention)
	dim.add_radiobutton(label="7*7",  variable=nitem, value=7,  command=setDimention)
	dim.add_radiobutton(label="8*8",  variable=nitem, value=8,  command=setDimention)
	dim.add_radiobutton(label="9*9",  variable=nitem, value=9,  command=setDimention)
	dim.add_radiobutton(label="10*10",  variable=nitem, value=10,  command=setDimention)



	dicimg={}

	mwd=ecran_width
	mhg=ecran_height
	listImg=bf.getListImg(nameProjet, rectFull)
	posX=0
	posY=0

	###########l'aperçu
	bf.setCanvas(root,dicimg,listImg,mwd,mhg,dimention,nameProjet,rectFull,newWin)
	

	root.mainloop()