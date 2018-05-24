# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:37:31 2018

@author: Rachel NOIREAU & Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf

def ChooseWhereSave():
	f=tkinter.filedialog.asksaveasfile(
		title="Enregistrer sous … un fichier",
		filetypes=[('PDF files','.pdf')])
	print(f.name) 
	

def exportToPdf():
	print('export pdf')


#peut etre 2 ensemble si rien a rajouter
def fullRect():
	global rectFull
	rectFull=True

def emptyRect():
	global rectFull
	rectFull=False