# -*- coding: utf-8 -*-
"""
Created on Wed May 16 09:34:19 2018

@author: rachel NOIREAU & Liuyan PAN
"""
#ce fichier contient la fonction pour convertir le fichier pdf en png, il va couper chaque page de pdf et la convertir en png
from __future__ import print_function
from wand.image import Image
import os.path

numberPage=0

#nb le chemin du fichier source
def pdfToPng(namefile,nameProjet,resol): 
	if len(namefile) > 0: 
		if not os.path.exists('imgFromPdf/' + nameProjet):
			os.makedirs('imgFromPdf/' + nameProjet)
			listImg =[]
			with Image(filename=namefile,resolution=resol) as img: #pour resol 30 == low quality(utilisée pour l'app java) 60== high quality utilisé pour le traitement de l'imgage
				global numberPage
				numberPage=len(img.sequence)
				img.compression_quality = 99
				for i in range (len(img.sequence)) :
					listImg.append('imgFromPdf/' + splitPath(namefile) + '/'+ splitPath(namefile) + 'page-' + str(i) + '.png') #stoker les paths d'image
				
				with img.convert('png') as converted: #convertir les pages de pdf en png
					converted.save(filename='imgFromPdf/' + nameProjet + '/' + splitPath(namefile) + 'page' + '.png')    #nb le chemin des results
			return listImg
		else:
			return 0
				
def splitPath(path): #couper les paths
	(filePath,tempfileName) = os.path.split(path)
	(shotName,extension) = os.path.splitext(tempfileName)
	return shotName
	
#retourne le nombre de page du pdf 
def getCountPage():#path
	return numberPage