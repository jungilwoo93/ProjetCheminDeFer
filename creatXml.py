# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:53:46 2018

@author: rachel NOIREAU & liuyan PAN
"""
import lxml.etree as le
from lxml import etree
import os.path
import xml.etree.ElementTree as et
import xml.etree as xe
import xml.etree.cElementTree as ET
import xml.dom.minidom as dm

    
def getExistingXml(nameProjet):########
	tree = le.parse('DrawOnImage/XmlTrainingData/' + nameProjet + '.xml')
	root = tree.getroot()
	return root

#recupere le xml existant pour en modifier les erreurs dans la fenetre prevu pour
def getXmlToModif(nameProjet,numPage):
	tree = le.parse('DrawOnImage/workshop_test/'+nameProjet+'/page-' + str(numPage) + '.png-Unlabelled.xml')
	root = tree.getroot()
	return root
 

def checkFileExiste(nameFile):
    return os.path.exists(nameFile)


def newProjet(nameProjet):
	if os.path.exists('DrawOnImage/XMLTrainingData/' + nameProjet +'.xml'):
		return continuePoject(nameProjet)
	else:
		xmlProjet = etree.Element('Book')
		return xmlProjet,False

def continuePoject(nameProjet):
	xmlProjet=getExistingXml(nameProjet)
	return xmlProjet,True

def addPage(pathPage,numPage,xmlProjet):
	page = etree.SubElement(xmlProjet,'page')
	page.set('id',str(numPage)) 
	file = etree.SubElement(page,'file')
	file.set('path',pathPage)
	return page
    

def endProjet(nameProjet,xmlProjet) : 
	path='DrawOnImage/XmlTrainingData'
	try:
		if not(os.path.exists(path)) :
			os.mkdir(path)
		with open(path + '/' + nameProjet +'.xml','w') as fichier:
			fichier.write(etree.tostring(xmlProjet,pretty_print=True).decode('utf-8'))#cree premiere balise
			fichier.close()
			return xmlProjet
	except IOError:
		print('Problème rencontré lors de l\'écriture ...')
		exit(1)
        

def addElement(typeEl, idEl, posiX, posiY, widthEl, heightEl, nameProjet, numPage, xmlProjet):
	page=foundPage(nameProjet, numPage, xmlProjet)
	element = etree.SubElement(page,'element') #ou append
	element.set('type',typeEl)#recurere le typele l'element de la liste
	element.set('id',str(idEl))
	posX = etree.SubElement(element,'posX')
	posX.text= str(posiX)
	posY = etree.SubElement(element,'posY')
	posY.text= str(posiY)
	width = etree.SubElement(element,'width')
	width.text= str(widthEl)
	height = etree.SubElement(element,'height')
	height.text= str(heightEl)


def delectElement(nameProjet,numPage,numElem,xmlProjet):
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			for e1 in e.findall('element'):
				if e1.attrib['id']==str(numElem):
					listChild=xmlProjet.getchildren() 
					listChild=e.getchildren()
					e.remove(e1)
					return xmlProjet
     
	 
def delectPage(nameProjet,numPage,xmlProjet):
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			xmlProjet.remove(e)
			return xmlProjet
        
def replace(nameProjet, numPage, numElem, newType,xmlProjet) :
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			for e1 in e.findall('element'):
				if not(e1 is None):
					if e1.attrib['id']==str(numElem):
						e1.attrib['type'] = newType
						return xmlProjet

def pageExist(nameProjet, numPage,xmlProjet)  : #virer name project
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			return True
	return False
        
def foundPage(nameProjet, numPage, xmlProjet) : #nameProjet a virer
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			return e
def findAllPage(xmlProject):
	listPage=[]
	for e in xmlProject.findall('page'):
		listPage.append(e)
	return listPage

def reSave(nameProjet, numPage, numElem, xmlProjet) : #peut retirer name project    
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			for e1 in e.findall('element'):
				if not(e1 is None):
					if e1.attrib['id']==str(numElem):
						return True 
	return False

def sameType(nameProjet, numPage, numElem, newType, xmlProjet):#peut retirai nameProj
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			for e1 in e.findall('element'):
				if not(e1 is None):
					if e1.attrib['id']==str(numElem):
						if e1.attrib['type']==newType:
							return True
	return False
 

def getRect(nameProjet,numPage,xmlProjet):
	allPage=findAllPage(xmlProjet)
	listRect=[]
	for page in allPage:
		if page.attrib['id']==str(numPage):
			for rect in page.findall('element'):
				typeRect=rect.attrib['type'] 
				numrect=rect.attrib['id'] 
				elPosx=rect.find('posX')
				posx=elPosx.text
				elPosy=rect.find('posY')
				posy=elPosy.text
				elWidth=rect.find('width')
				width=elWidth.text
				elHeight=rect.find('height')
				height=elHeight.text
				listRect.append([numPage,typeRect,numrect,posx,posy,width,height])
	return listRect

	
def getRectModif(nameProjet,numPage,xmlProjet,scale):
	allPage=findAllPage(xmlProjet)
	listRect=[]
	numR=0
	for page in allPage:
			for rect in page.findall('element'):
				typeRect=rect.attrib['type'] 
				elPosx=rect.find('posX')
				posx=elPosx.text
				elPosy=rect.find('posY')
				posy=elPosy.text
				elWidth=rect.find('width')
				width=elWidth.text
				elHeight=rect.find('height')
				height=elHeight.text
				listRect.append([numPage,typeRect,numR,posx,posy,width,height])
				numR+=1
	return listRect
	
def getRectForModification(name,pathImg,xmlProjet,scale):
	num = None
	allPage=findAllPage(xmlProjet)
	for page in allPage:
		allPath = page.findall('file')
		for path in allPath:
			if path.attrib['path'] == pathImg:
				num = page.attrib['id']
	listRect=getRectModif(name,num,xmlProjet,scale)
	return listRect
	
def getLastRectangleId(xmlProjet):
	maxId=0
	for page in xmlProjet.findall('page'):
		for elem in page.findall('element'):
			id=elem.attrib['id']
			if int(id)>maxId:
				maxId=id
	return maxId+1


