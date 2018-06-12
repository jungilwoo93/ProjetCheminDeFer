# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:37:31 2018

@author: Rachel NOIREAU & Liuyan PAN
"""

#pas besoin de mouseX et mouseY
def selectPage(x, y, mouseX, mouseY, sizeX, sizeY, dimention,numPage,w,h,posIm):
	
	#pbsize dimention de la fenetre
	if numPage%dimention[0] ==0 :
		numLines=numPage/dimention[0]
	else:
		numLines=int(numPage/dimention[0])+1
	widthImg=w/dimention[0]#sizeX[0]-sizeX[1]
	heightImg=h/numLines#sizeY[0]-sizeY[1]
	
	posX=int((abs(mouseX-posIm[0]))/widthImg)#+sizeX[1]#mouseX-
	posY=int((abs(mouseY-posIm[1]))/heightImg)#+sizeY[1]#mouseY-
	numImg=(posY*dimention[0])+posX
	print(numImg)
	return numImg
	#return numImg
	#import WinModification as modif 
	#root.Toplevel()
	#moodif.creatWin(root,selection[numImg],self.nameProjet)

