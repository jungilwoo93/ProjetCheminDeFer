"""
Created on Mon May  30 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

photo = PhotoImage(file='guillemet2.jpg')
button = Button(root, image=photo)


bt_green = Button(root, image=photo, command=lambda: can.config(bg="green"))
bt_green_w = can.create_window(40, 60, window=bt_green)