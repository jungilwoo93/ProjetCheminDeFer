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
# fonction de buttonConfirm
def confirmer(listAction,var):
    listAction.insert(tk.END,var.get())
