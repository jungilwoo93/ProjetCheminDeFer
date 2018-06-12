# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 02:49:11 2017

@author: DL9
"""


from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import glob
import os
import lxml.etree as le

def drawIm(pathIMG,nameProjet,scale):
	class imgData:

		types   = list()    
		x = list()    
		y   = list() 
		w = list()    
		h   = list() 
		dataSizeCounter=0
		modif=[]
		
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
			for x in range(0,len(fl)):
				tree = le.parse(fl[x])
				root = tree.getroot()
				numPage=0
				for page in root.iter('page'):
					for path in page.iter('file'):
						if path.attrib['path'] ==  pathIMG :
							for component in page.iter('element'):
								img13.addComponent(component.attrib['type'],component.find('posX').text,component.find('posY').text,component.find('width').text,component.find('height').text)
								self.dataSizeCounter =self.dataSizeCounter+1
							img13.printall(img13.splitPath(fl[x]),numPage)#file name starts at the position 14 of the string
							self.dataSizeCounter=0
						numPage+=1
	
		def printall(self, img, numPage): #this method draws on image after data extraction
			im = Image.open("imgFromPdf/"+nameProjet+ '/' + nameProjet + img.split("-U")[0])# # path+ the name of the image 
			imFull = Image.open("imgFromPdf/"+nameProjet+ '/' + nameProjet + img.split("-U")[0])# # path+ the name of the image 
			im=im.convert("RGB")
			imFull=imFull.convert("RGB")
			color=(100,255,0)
			draw = ImageDraw.Draw(im)
			drawFull = ImageDraw.Draw(imFull)
			for i in range(self.dataSize-self.dataSizeCounter,self.dataSize):
				if self.types[i]=="Titre":
					color='red'#(0,0,255)
				elif self.types[i]=="Paragraphe": # chaque type a un couleur 
					color='gray'#(255,100,0)
				else:
					color='blue'#(100,255,0)
				scale=1
				draw.text((int(int(self.x[i])*scale-15),int(int(self.y[i])*scale-15)),self.types[i],fill=color)#self.types[i]'''
				#plusieur rectangle pour un rectangle avec un tour plus epais
				X=int(int(self.x[i])*scale)
				Y=int(int(self.y[i])*scale)
				W=int(int(self.w[i])*scale)+X
				H=int(int(self.h[i])*scale) +Y
				draw.rectangle((X,Y,W,H), fill=None, outline=color)
				draw.rectangle((X-1,Y-1,W+1,H+1), fill=None, outline=color)
				draw.rectangle((X+1,Y+1,W-1,H-1), fill=None, outline=color)
				draw.rectangle((X-2,Y-2,W+2,H+2), fill=None, outline=color)
				draw.rectangle((X+2,Y+2,W-2,H-2), fill=None, outline=color)
				draw.rectangle((X-3,Y-3,W+3,H+3), fill=None, outline=color)
				draw.rectangle((X+3,Y+3,W-3,H-3), fill=None, outline=color)
				drawFull.text((int(int(self.x[i])*scale-15),int(int(self.y[i])*scale-15)),self.types[i],fill=color)#self.types[i]'''
				drawFull.rectangle(((int(int(self.x[i])*scale),int(int(self.y[i])*scale)),int((int(int(self.w[i])*scale)+int(int(self.x[i])*scale))),int((int(int(self.h[i])*scale)+int(int(self.y[i])*scale)))), fill=color, outline=color)
				
				self.modif.append('page ' + str(numPage) + ' pos( ' + str(self.x[i]) + ' , ' + str(self.y[i]) + ' )')
				
			if not os.path.exists("DrawOnImage/finalResult/"+nameProjet):
				os.makedirs("DrawOnImage/finalResult/" + nameProjet)
				os.makedirs("DrawOnImage/finalResult/" + nameProjet + "/fullRect")
				os.makedirs("DrawOnImage/finalResult/" + nameProjet + "/emptyRect")
			im.save("DrawOnImage/finalResult/"+ nameProjet+"/emptyRect/classified-"+img.split("-U")[0], "PNG")
			imFull.save("DrawOnImage/finalResult/"+ nameProjet+"/fullRect/classified-"+img.split("-U")[0], "PNG")

		def upDateExcel():
			pathOfExcel='fichiersExcel/' + nameProjet + '.xls'
			wb = xlrd.open_workbook(pathOfExcel)
			sh = wb.sheet_by_name(u'Feuil1')
			print(sh)
			colonneA = sh.col_values(0)
			case=[]
			caractere = " "
			lines=0
			colonneANew=[]
			modifAdd=False
			for l in colonneA :
				line = l.split(caractere)
				if line[0]=='page':
					if line[1]==str(numPage):
						if modifAdd :
							for j in range (0, len(modif)):
								colonneANew.append(modif[j])
							modifAdd=False
					else:
						colonneANew.append(line)
				
			book = Workbook()
			page1 = book.add_sheet('feuille 1',cell_overwrite_ok=True)
			page1.write(0,0,'coordonnée unique ')
			for i in range (1,len(colonneA)+1):
				line = page1.row(i)
				line.write(0,'page ' + colonneA[1] + ' pos( ' + colonneA[3] + ' , ' + colonneA[5] + ' )')
			page1.col(0).width = 10000
			book.save('fichiersExcel/' + nameProjet + '.xls')

	img13=imgData(13)
	img13.run()



#draw.rectangle((10, 10, 30, 30), fill=None, outline=(255, 0, 0))

#drawIm('Batch')    