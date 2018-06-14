# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:37:31 2018

@author: Rachel NOIREAU & Liuyan PAN
"""

#cette fonction n'as finalement pas etait utiliser
#permet d'obtenir l'id d'une page un cliquant dessus
def selectPage(x, y, mouseX, mouseY, sizeX, sizeY, dimention,numPage,w,h,posIm):

	if numPage%dimention[0] ==0 :
		numLines=numPage/dimention[0]
	else:
		numLines=int(numPage/dimention[0])+1
	widthImg=w/dimention[0]
	heightImg=h/numLines
	
	posX=int((abs(mouseX-posIm[0]))/widthImg)
	posY=int((abs(mouseY-posIm[1]))/heightImg)
	numImg=(posY*dimention[0])+posX

	return numImg

