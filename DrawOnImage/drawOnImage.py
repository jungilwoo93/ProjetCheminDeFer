# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 02:49:11 2017

@author: DL9
"""


from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import glob
import os
from xlwt import Workbook

def drawIm(nameProjet):
	class imgData:

		types   = list()    
		x = list()    
		y   = list() 
		w = list()    
		h   = list() 
		dataSizeCounter=0
	
		def __init__(self,imID ):
			self.imID =   imID
			self.dataSize =   0
	
		def addComponent(self,tp,x,y,w,h):
			self.types.append(tp)
			self.x.append(x)
			self.y.append(y)
			self.w.append(w)
			self.h.append(h)
			self.dataSize=self.dataSize+1
	
	
	
		def extractPaths(self):
			xmlFiles=glob.glob("DrawOnImage/workshop_test/"+ nameProjet +"/*.xml")
			fileList=list()
			for x in range(0,len(xmlFiles)):
				fileList.append(xmlFiles[x])
			return fileList  
		
		def splitPath(self,path):
			(filePath,tempfileName) = os.path.split(path)
			(shotName,extension) = os.path.splitext(tempfileName)
			return shotName + '.png'

		
		def run(self):
			fl=self.extractPaths()
			k=0
			elenum=0
			for x in range(0,len(fl)):
				tree = ET.parse(fl[x])
				root = tree.getroot()
				
				for page in root.iter('page'):
					for component in page.iter('element'):
						img13.addComponent(component.attrib['type'],component.find('posX').text,component.find('posY').text,component.find('width').text,component.find('height').text)
						self.dataSizeCounter =self.dataSizeCounter+1
						elenum+=1
					img13.printall(img13.splitPath(fl[x]),k, elenum)#file name starts at the position 14 of the string
					self.dataSizeCounter=0
					k+=1
	
		def printall(self,img,numPage,elenum): #this method draws on image after data extraction
			listLettrine=[]
			im = Image.open("imgFromPdf/"+nameProjet+ '/' + nameProjet + img.split("-U")[0])# # path+ the name of the image 
			imFull = Image.open("imgFromPdf/"+nameProjet+ '/' + nameProjet + img.split("-U")[0])# # path+ the name of the image 
			im=im.convert("RGB")
			imFull=imFull.convert("RGB")
			color=(100,255,0)
			draw = ImageDraw.Draw(im)
			drawFull = ImageDraw.Draw(imFull)
			for i in range(self.dataSize-self.dataSizeCounter,self.dataSize):
				if self.types[i]=="Titre":
					color='red' #(225,0,0)
				elif self.types[i]=="Paragraphe": # chaque type a un couleur 
					color='gray'#(255,100,0)
				else:
					color='blue'#(0,0,255)
					listLettrine.append([int(self.x[i]),int(self.y[i]),int(self.w[i])+int(self.x[i]),int(self.h[i])+int(self.y[i])])
				draw.text((int(self.x[i])-15,int(self.y[i])-15),self.types[i],fill=color)#self.types[i]'''
				#pour avoir un rectangle avec une plus grande epaiseur -> plusieur 
				draw.rectangle((int(self.x[i]),int(self.y[i]),int(self.w[i])+int(self.x[i]),int(self.h[i])+int(self.y[i])), fill=None, outline=color)#, width=5
				draw.rectangle((int(self.x[i])-1,int(self.y[i])-1,int(self.w[i])+int(self.x[i])+1,int(self.h[i])+int(self.y[i])+1), fill=None, outline=color)
				draw.rectangle((int(self.x[i])+1,int(self.y[i])+1,int(self.w[i])+int(self.x[i])-1,int(self.h[i])+int(self.y[i])-1), fill=None, outline=color)
				draw.rectangle((int(self.x[i])-2,int(self.y[i])-2,int(self.w[i])+int(self.x[i])+2,int(self.h[i])+int(self.y[i])+2), fill=None, outline=color)
				draw.rectangle((int(self.x[i])+2,int(self.y[i])+2,int(self.w[i])+int(self.x[i])-2,int(self.h[i])+int(self.y[i])-2), fill=None, outline=color)
				draw.rectangle((int(self.x[i])-3,int(self.y[i])-3,int(self.w[i])+int(self.x[i])+3,int(self.h[i])+int(self.y[i])+3), fill=None, outline=color)
				draw.rectangle((int(self.x[i])+3,int(self.y[i])+3,int(self.w[i])+int(self.x[i])-3,int(self.h[i])+int(self.y[i])-3), fill=None, outline=color)
				drawFull.text((int(self.x[i])-15,int(self.y[i])-15),self.types[i],fill=color)#self.types[i]'''
				drawFull.rectangle((int(self.x[i]),int(self.y[i]),int(self.w[i])+int(self.x[i]),int(self.h[i])+int(self.y[i])), fill=color, outline=color)
				
				#ecriture dans excel
				line = page1.row(elenum-self.dataSize+i+1)
				line.write(0,'page ' + str(numPage) + ' pos( ' + str(self.x[i]) + ' , ' + str(self.y[i]) + ' )')
			
			#pourvoir les lettrine même quand rectangle plein
			for j in range (0,len(listLettrine)):
				drawFull.rectangle(listLettrine[j], fill='blue', outline=color)
			
			if not os.path.exists("DrawOnImage/finalResult/"+nameProjet):
				os.makedirs("DrawOnImage/finalResult/" + nameProjet)
				os.makedirs("DrawOnImage/finalResult/" + nameProjet + "/fullRect")
				os.makedirs("DrawOnImage/finalResult/" + nameProjet + "/emptyRect")
			im.save("DrawOnImage/finalResult/"+ nameProjet+"/emptyRect/classified-"+img.split("-U")[0], "PNG")
			imFull.save("DrawOnImage/finalResult/"+ nameProjet+"/fullRect/classified-"+img.split("-U")[0], "PNG")

	book = Workbook()
	page1 = book.add_sheet('feuille 1',cell_overwrite_ok=True)
	page1.write(0,0,'coordonnée unique ')
	#wb = xlrd.open_workbook(pathOfExcel)
	
	img13=imgData(13)
	img13.run()
	page1.col(0).width = 10000
	book.save('fichiersExcel/' + nameProjet + '.xls')



#draw.rectangle((10, 10, 30, 30), fill=None, outline=(255, 0, 0))

#drawIm('Batch')    