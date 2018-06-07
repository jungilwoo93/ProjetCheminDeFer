# -*- coding: utf-8 -*-
"""
Created on Tue May 22 09:37:31 2018

@author: Rachel NOIREAU & Liuyan PAN
"""

#pas besoin de mouseX et mouseY
def selectPage(x, y, mouseX, mouseY, sizeX, sizeY, dimention,numPage):
	#pbsize dimention de la fenetre
	if numPage%dimention[0] ==0 :
		numLines=numPage/dimention[0]
	else:
		numLines=int(numPage/dimention[0])+1
	widthImg=(sizeX[0]-sizeX[1])/dimention[0]
	heightImg=(sizeY[0]-sizeY[1])/numLines
	posX=int((x+sizeX[1])/widthImg)#mouseX-
	posY=int((y+sizeY[1])/heightImg)#mouseY-
	numImg=(posY*dimention[0])+posX
	print(numImg)
	return numImg
	#return numImg
	#import WinModification as modif 
	#root.Toplevel()
	#moodif.creatWin(root,selection[numImg],self.nameProjet)

