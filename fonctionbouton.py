# -*- coding: utf-8 -*-
"""
Created on Wed May 16 10:20:06 2018

@author: rachel
"""
import tkinter as tk
import tkinter.filedialog as tf
from PIL import Image, ImageFont, ImageDraw, ImageTk
from os.path import basename
#################################################### toutes les fonctions  ####################################################
listFiles = tk.Listbox()
numPage=3

def nextPage():  #a mettre dans enregister #voir si onSelect se fait tout seul
    global numPage
    numPage += 1
    listFiles.selection_set(numPage)
    
    
def getNumPage() : #dés qu'on selectionne un truc
      listFiles.curselection()[0]
    