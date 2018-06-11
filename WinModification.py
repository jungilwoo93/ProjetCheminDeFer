# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:53:46 2018

@author: rachel NOIREAU & liuyan PAN
"""
import tkinter as tk
#root=tk.Toplevel()
import os
import commun as co

### variable global ###
#root = tk.Tk()
#var=tk.StringVar()
#var.set("Paragraphe")
numIm=0

def creatWin(root,nameProjet,numPage):#pathIMG,
	global numIM
	numIm=numPage
	var=tk.StringVar()
	pathIMG='imgFromPdf/' + nameProjet + '/' + nameProjet + 'page-' + str(numPage) +'.png'
	var.set("Paragraphe")
	func=co.FunctionCommun()
	screen_width = root.winfo_screenwidth()*0.9
	screen_height = root.winfo_screenheight()*0.85
	func.setSizeScreen(screen_width,screen_height)
	root.geometry('%dx%d+%d+%d' % (screen_width, screen_height, 1, 1))
	root.title("Modification")
	root.resizable(width=False,height=False)
	f=tk.Frame(root,bg=func.colorDefault ,width=screen_width,height=screen_height)
	f.grid(row=0,column=0,sticky=tk.W+tk.N)
	c=tk.Canvas(f,width=screen_width, height=screen_height,bd=0,highlightthickness=0,bg=func.colorDefault)
	c.grid(row=0, column=0, sticky=tk.W+tk.N + tk.S)
	f1=tk.Frame(c,bg=func.colorDefault,height=screen_height,width=screen_width*0.4)
	f1.grid(row=0,column=0,sticky=tk.S+tk.W+tk.N,pady=100)
	labelZoneChoix=tk.Label(f1,text='La zone choisie est : ', bg=func.colorDefault)
	labelZoneChoix.config(font=('Arial',18))
	labelZoneChoix.grid(row=0, sticky=tk.W)
	zoneRadioButton=tk.Frame(f1, bg=func.colorDefault)
	
	def setVar():
		func.setVar(var.get())
	a=0
	for i,v in enumerate(func.typeZone):
		tk.Radiobutton(zoneRadioButton, text=v, variable=var, value = v, bg=func.colorDefault,command=setVar).grid(row=0, column=a,sticky=tk.W,padx=20)
		a+=1
	zoneRadioButton.grid(row=1,sticky=tk.W,pady=5)
	buttonConfirm=tk.Button(f1,text="Confirmer",command=func.confirmer).grid(row=2,column=0,pady=5,sticky=tk.S)
	labelAction=tk.Label(f1,text="Les actions : ", bg=func.colorDefault)
	labelAction.config(font=('Arial',18))
	labelAction.grid(row=3,column=0,pady=5,sticky=tk.W)
	
	
	#listAction = tk.Listbox(f1,width=70,height=8,selectmode=tk.MULTIPLE)
	#listAction.grid(row=4,column=0,pady=5)
	
	listFrame2=tk.Frame(f1)
	###################### scrollbar vertical et horizontal
	yDefilB = tk.Scrollbar(listFrame2, orient='vertical')
	yDefilB.grid(row=0, column=1, sticky='ns')
	xDefilB = tk.Scrollbar(listFrame2, orient='horizontal')
	xDefilB.grid(row=1, column=0, sticky='ew')

	listAction = tk.Listbox(listFrame2,
		xscrollcommand=xDefilB.set,
		yscrollcommand=yDefilB.set,width=70,height=8,selectmode=tk.MULTIPLE)
	listAction.grid(row=0)
	xDefilB['command'] = listAction.xview
	yDefilB['command'] = listAction.yview
	listFrame2.grid(row=4,column=0,pady=5, padx=20, sticky=tk.W)
	

	listAction.bind('<<ListboxSelect>>', func.onSelectAction)  
	for i in range(0,listAction.size()):
		listAction.selection_set(i)
	func.setListBoxAction(listAction)
	fButtons=tk.Frame(f1, bg=func.colorDefault)
	buttonDeselect=tk.Button(fButtons,text="Deselect/Select all",command=func.de_select).grid(row=0,column=0,padx=20,sticky=tk.S)
	buttonDelete=tk.Button(fButtons,text="Supprimer",command=func.deleteSelection).grid(row=0,column=1,padx=20,sticky=tk.S)
	buttonLast=tk.Button(fButtons,text="Annuler",command=quit).grid(row=0,column=2,padx=20,sticky=tk.S)
	buttonSave=tk.Button(fButtons,text="Enregistrer",command=lambda : func.saveModif(nameProjet,numPage)).grid(row=0,column=3,padx=20,sticky=tk.S)
	fButtons.grid(row=5,column=0,pady=20)
	
	fImg=tk.Frame(c,width=screen_width*0.65,height=screen_height, bg=func.colorDefault)
	fImg.grid(row=0,column=1,sticky=tk.N+tk.S)
	cadre=tk.Canvas(c, bg=func.colorDefault, bd=-2)
	cadre.grid(row=0,column=1)
	func.setImageForModif(pathIMG,cadre)
	#func.setActionToListbox(pathIMG,nameProjet)
	func.getCoordsFromXml(pathIMG,nameProjet,numIm)
	
	root.mainloop()
	

