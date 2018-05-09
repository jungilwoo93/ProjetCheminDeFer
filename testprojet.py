# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: rachel
"""

from tkinter import *

fenetre = Tk()
fenetre.attributes("-fullscreen", 1)
w=fenetre.winfo_screenwidth()
h=fenetre.winfo_screenheight() 
fenetre.configure(width=w-2,height=h-50)
#Button(fenetre, text="Quit", command=fenetre.destroy).pack()
fenetre.mainloop()

