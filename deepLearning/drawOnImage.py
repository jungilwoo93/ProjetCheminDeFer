# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 02:49:11 2017

@author: DL9
"""


from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import glob

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
        xmlFiles=glob.glob("workshop_test/*.xml")
        fileList=list()
        for x in range(0,len(xmlFiles)):
             fileList.append(xmlFiles[x])
        return fileList  
        
    def run(self):
        fl=self.extractPaths()
        for x in range(0,len(fl)):
            tree = ET.parse(fl[x])
            root = tree.getroot()
    
            for component in root.iter('component'):
                img13.addComponent(component.find('type').text,component.find('PointX').text,component.find('PointY').text,component.find('RectangleWidth').text,component.find('RectangleHeight').text)
                self.dataSizeCounter =self.dataSizeCounter+1
            img13.printall(fl[x][14:])#file name starts at the position 14 of the string
            self.dataSizeCounter=0
        
    def printall(self,img): #this method draws on image after data extraction
        im = Image.open("workshop_test/"+img.split("-U")[0]) # path+ the name of the image 
        im=im.convert("RGB")
        
        color=(100,255,0)
        draw = ImageDraw.Draw(im)
        for i in range(self.dataSize-self.dataSizeCounter,self.dataSize):
            if self.types[i]=="Titre":
                color=(0,0,255)
                
            elif self.types[i]=="Paragraphe": # chaque type a un couleur 
                color=(255,100,0)
            else:
                color=(100,255,0)
                
            
            draw.text((int(self.x[i])-15,int(self.y[i])-15),self.types[i],fill=color)#self.types[i]'''
            draw.rectangle((int(self.x[i]),int(self.y[i]),int(self.w[i])+int(self.x[i]),int(self.h[i])+int(self.y[i])), fill=None, outline=color)
        im.save("classified-"+img.split("-U")[0], "PNG")



 
img13=imgData(13)
img13.run()
    




#draw.rectangle((10, 10, 30, 30), fill=None, outline=(255, 0, 0))




    
    