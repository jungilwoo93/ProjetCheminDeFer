# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:53:46 2018

@author: rachel NOIREAU & liuyan PAN
"""
import lxml.etree as le
from lxml import etree
import os.path
#import xml.etree.ElementTree as et
#import xml.etree as xe
import xml.etree.cElementTree as ET
#import xml.dom.minidom as dm


#recupere un xml déjà cree   
def getExistingXml(nameProjet):
		tree = le.parse('DrawOnImage/XmlTrainingData/' + nameProjet + '.xml')
		root = tree.getroot()
		return root


#recupere le xml existant pour en modifier les erreurs dans la fenetre prevu pour
def getXmlToModif(nameProjet,numPage):
	tree = le.parse('DrawOnImage/workshop_test/'+nameProjet+'/page-' + str(numPage) + '.png-Unlabelled.xml')
	root = tree.getroot()
	return root
 
    
#verifie l'exisance d'un fichier

def checkFileExiste(nameFile):
    return os.path.exists(nameFile)

#crée un nouveau xml 
def newProjet(nameProjet):
	if os.path.exists('DrawOnImage/XMLTrainingData/' + nameProjet +'.xml'):
		print('ce projet est déjà commencé')
		return continuePoject(nameProjet)
	else:
		xmlProjet = etree.Element('Book')
		return xmlProjet,False

def continuePoject(nameProjet):
	xmlProjet=getExistingXml(nameProjet)
	return xmlProjet,True

#ajouter une balise "page"
def addPage(pathPage,numPage,xmlProjet):
	page = etree.SubElement(xmlProjet,'page')
	page.set('id',str(numPage)) 
	file = etree.SubElement(page,'file')
	file.set('path',pathPage)
	return page
    
#sauvegarder le projet
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
        
#ajouter une balise "element"
def addElement(typeEl, idEl, posiX, posiY, widthEl, heightEl, nameProjet, numPage, xmlProjet):
	page=foundPage(nameProjet, numPage, xmlProjet)
	element = etree.SubElement(page,'element')
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

#suprimer une balise "element"
def delectElement(nameProjet,numPage,numElem,xmlProjet):
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			for e1 in e.findall('element'):
				if e1.attrib['id']==str(numElem):
					listChild=xmlProjet.getchildren() 
					listChild=e.getchildren()
					e.remove(e1)
					return xmlProjet
     
#suprimer une balise "page" 
def delectPage(nameProjet,numPage,xmlProjet):
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			xmlProjet.remove(e)
			return xmlProjet



#changer le type d'un element
def replace(nameProjet, numPage, numElem, newType,xmlProjet) :
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			for e1 in e.findall('element'):
				if not(e1 is None):
					if e1.attrib['id']==str(numElem):
						e1.attrib['type'] = newType
						return xmlProjet

#verifier si une page existe
def pageExist(nameProjet, numPage,xmlProjet)  : 
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			return True
	return False

#chercher une page à partir de sont numéros     
def foundPage(nameProjet, numPage, xmlProjet) : 
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			return e

#faire la liste des pages
def findAllPage(xmlProject):
	listPage=[]
	for e in xmlProject.findall('page'):
		listPage.append(e)
	return listPage

#sauvegarde un element déjà prescedament sauvegardé
def reSave(nameProjet, numPage, numElem, xmlProjet) :    
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			for e1 in e.findall('element'):
				if not(e1 is None):
					if e1.attrib['id']==str(numElem):
						return True 
	return False

#verifier que 2 element sont de même type
def sameType(nameProjet, numPage, numElem, newType, xmlProjet):
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			for e1 in e.findall('element'):
				if not(e1 is None):
					if e1.attrib['id']==str(numElem):
						if e1.attrib['type']==newType:
							return True
	return False
 
#obtenir le coordonnée des rectangles d'une page
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

#obtenir les coordonnées des rectangle d'une page à partir de la fenetre de modification
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
	

#trouver la bonne page pour modification
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

#obtenir le plus grand id de rectangle
def getLastRectangleId(xmlProjet):
	maxId=0
	for page in xmlProjet.findall('page'):
		for elem in page.findall('element'):
			id=elem.attrib['id']
			if int(id)>maxId:
				maxId=id
	return maxId+1
	


def foundPageSelfDone(xmlProjet) : 
	for e in xmlProjet.findall('page'):
		return e
		
#ajouter une page faite au resultat final pour etre bien sur que celle là au moins sont classé corectementet qu'il n'y ai pas besoin de corriger
def addRectSelfDone(nameProjet, xmlProjet, idEl, type, w, h, x, y):
	page = foundPageSelfDone(xmlProjet)
	element = etree.SubElement(page,'element')
	element.set('type',type)#recurere le typele l'element de la liste
	element.set('id',str(idEl))
	posX = etree.SubElement(element,'posX')
	posX.text= str(x)
	posY = etree.SubElement(element,'posY')
	posY.text= str(y)
	width = etree.SubElement(element,'width')
	width.text= str(w)
	height = etree.SubElement(element,'height')
	height.text= str(h)
	
	
def endSelfDone(nameProjet, xmlProjet, numPage):
	path='DrawOnImage/workshop_test/'+ nameProjet
	if not(os.path.exists('DrawOnImage/workshop_test')) :
			os.mkdir('DrawOnImage/workshop_test')
	if not(os.path.exists(path)) :
		os.mkdir(path)
	with open(path + '/page-' + str(numPage) + '.png-Unlabelled.xml','w') as fichier:
			fichier.write(etree.tostring(xmlProjet,pretty_print=True).decode('utf-8'))#cree premiere balise
			fichier.close()
			
			