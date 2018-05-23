# -*- coding: utf-8 -*-
"""
Created on Wed May 16 09:34:19 2018

@author: rachel
"""

from __future__ import print_function
#from imagemagick import *
from wand.image import Image
import os.path


#nb le chemin du fichier source
def pdfToPng(namefile,nameProjet): #'test1/source1.pdf'
	#os.mkdir('imgFromPdf/' + nameProjet)
	if len(namefile) > 0: 
		
		os.makedirs('imgFromPdf/' + nameProjet)
		page=0
		listImg =[]
		with Image(filename=namefile,resolution=30) as img: #30 == low quality(utilisée pour l'app java) 60== high quality utilisé pour le traitement de l'img
			#print('pages = ', len(img.sequence))
			img.compression_quality = 99
			with img.convert('png') as converted:
				print("coucou") 
				print(str(page))
				converted.save(filename='imgFromPdf/' + nameProjet + '/' + splitPath(namefile) + 'page' + '.png')    #nb le chemin des results
				#'test1/result/page_n.png'
				listImg.append('imgFromPdf/' + splitPath(namefile) + '/'+ splitPath(namefile) + 'page-' + str(page) + '.png')
				page += 1
		return listImg
				
def splitPath(path):
	#global filePath,tempfileName,shotName,extension
	(filePath,tempfileName) = os.path.split(path)
	(shotName,extension) = os.path.splitext(tempfileName)
	return shotName
	
def getCountPage(path):
	sourcePDF=pdf.PdfFileReader(open(path,'rb'))
	countPage=sourcePDF.getNumPages()
	print(countPage)
	return countPage