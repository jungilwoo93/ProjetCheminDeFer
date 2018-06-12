# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:53:46 2018

@author: rachel NOIREAU & liuyan PAN
"""
import lxml.etree as le
from lxml import etree
import os.path
#from xml.dom import minidom
import xml.etree.ElementTree as et
import xml.etree as xe
import xml.etree.cElementTree as ET
#import requests
#import lxml.etree._Element as el


import xml.dom.minidom as dm
#from PyQt4 import QtXml,  QtCore



#C:/Users/rachel/Documents/GitHub/ProjetCheminDeFer/docXml/
    
def getExistingXml(nameProjet):########
	#try:
	
		# def __init__(self):
			# file = QtCore.QFile("files//essai.xml")
			# file.open(mode_r)
			# doc = QtXml.QDomDocument()
			# doc.setContent(self.file)
			# file.close()
			# file.open(mode_w)
			# out = QtCore.QTextStream(self.file)
			# root = self.doc.documentElement()
		#doc = dm.parse('docXml/' + nameProjet + '.xml')
		#root=doc.getElementsByTagName('Batch')[0]
		#root=ET.iterparse('docXml/' + nameProjet + '.xml')
        #print (self.root.tagName())
		#r = requests.get('docXml/' + nameProjet + '.xml')
		#xml = r.json()['items'].encode('utf-8')
		#parser=etree.XMLParser(encoding='utf-8')
		tree = le.parse('DrawOnImage/XmlTrainingData/' + nameProjet + '.xml')#str(nameProjet) +
		#root = etree.fromstring(xml, parser=etree.XMLParser(encoding='utf-8'))
		root = tree.getroot()#getroottree()
		#print('ccccccccccccccccccccccoooooooouuuuuuucou')
		#print(type(root))
		#oSetroot = etree.Element(root.tag)
		#doc = minidom.parse('docXml/' + nameProjet + '.xml')
		#root = doc.documentElement
		#root.find()
		#NewSub = etree.SubElement ( root, nameProjet )
		#tree.write('docXml/' + nameProjet + '.xml')
		#rootXml=ET.XML(root)
		#avec dom
		#doc = parse('docXml/' + nameProjet + '.xml') # parse an XML file by name
		#doc.documentElement
		#datasource = open('docXml/' + nameProjet + '.xml')
		#dom2 = parse(datasource)
		#docXml=doc.toxml()
		#dom3 = parseString(docXml)
		#conference=doc.getElementsByTagName('Batch')
		#rootXml=ET.XML(docXml)
		#bla=et.fromstring('docXml/' + nameProjet + '.xml')
		#NewSub#oSetroot
		return root
	#except: #xe.XMLSyntaxError
		#print('probleme de parse')
	
def getXmlToModif(nameProjet,numPage):
	tree = le.parse('DrawOnImage/workshop_test/'+nameProjet+'/page-' + str(numPage) + '.png-Unlabelled.xml')
	root = tree.getroot()
	return root
 
    
#def duplicationProjet() : #pas forcement necessaire
#    print(xmlProjets[0])
#    for i in range (0 ,len(xmlProjets[0])):
#        listProjets.append(xmlProjets[0][i])


def checkFileExiste(nameFile):
    #nameFile.exists()
    return os.path.exists(nameFile)


def newProjet(nameProjet):
	print('newwww proooojj')
	print(os.path.exists('imgFromPdf/' + nameProjet))
	if os.path.exists('imgFromPdf/' + nameProjet):
		print('ce projet est déjà commencé')
		return continuePoject(nameProjet)#xmlProjet,bool=
	else:
		xmlProjet = etree.Element(nameProjet)#fait recommencer
		return xmlProjet,os.path.exists('imgFromPdf/' + nameProjet)

def continuePoject(nameProjet):
	xmlProjet=getExistingXml(nameProjet) #etree.Element(nameProjet)
	return xmlProjet,True

def addPage(pathPage,numPage,xmlProjet):
	page = etree.SubElement(xmlProjet,'page')
	page.set('id',str(numPage)) 
	file = etree.SubElement(page,'file')
	file.set('path',pathPage)
	return page
    

def endProjet(nameProjet,xmlProjet) :   
    #xmlProjet = etree.Element(nameProjet)
	path='DrawOnImage/XmlTrainingData'
	try:
		if not(os.path.exists(path)) :
			os.mkdir(path)
		with open(path + '/' + nameProjet +'.xml','w') as fichier:
        #En-tête du fichier xml
			#fichier.write('<?xml version="1.0" encoding="UTF_8"?>\n')#pb d'encodage
            #index=xmlProjets[0].index(nameProjet)
            #xmlProjets[1][index]=xmlProjet
			fichier.write(etree.tostring(xmlProjet,pretty_print=True).decode('utf-8'))#cree premiere balise
            #xmlProjet = etree.Element(nameProjet)
			fichier.close()
			return xmlProjet
	except IOError:
		print('Problème rencontré lors de l\'écriture ...')
		exit(1)
        

def addElement(typeEl, idEl, posiX, posiY, widthEl, heightEl, nameProjet, numPage, xmlProjet):
	page=foundPage(nameProjet, numPage, xmlProjet)
	#print(page)
#    page = etree.SubElement(xmlProjet,'page')
#    page.set('id',bytes(numero))
	element = etree.SubElement(page,'element') #ou append
	element.set('type',typeEl)#recurere le typele l'element de la liste
	element.set('id',str(idEl))
    
    #truc du prof
#    position = etree.SubElement(element,'element')
#    position.set('posX','mobile')
#    position.set('posY','mobile')
#    position.set('width','mobile')
#    position.set('height','mobile')
    
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
					return xmlProject
     
    #xmlProjet.replace(e, e)
#    
#    
#    with open('docXml\\' + nameProjet + '.xml','r') as f:
#        lines = f.readlines()
#    
#    ligneefface=0
#    with open('docXml\\' + nameProjet + '.xml','w') as f:
#        for line in lines:
#            # str.lower permet de ne pas s'occuper des majuscules
#            if (chaine.lower() in line.lower()):
#                line = remplace
#            #f.write(line)
#                ligneefface=4
#                print('on remplace')
#                f.write(line)
#                ligneefface -=1
#            if ligneefface==0 :
#                f.write(line)
#                print('yo')
#            else :
#                ligneefface -=1
#    
#    
##    root = et.XML(etree.tostring(xmlProjet,pretty_print=True).decode('utf-8'))
##    p  = root.find(nameProjet + '/page')  # le père
##    e = p.find('posX') # le fils
##    p.remove(e) # supression
##    print (et.tostring(root))

##    xml = etree.parse('monfichier.xml')
##    for ma_balise in xml.getchildren():
##    if 'mon_attribut' in ma_balise.attrib and ma_balise.attrib['mon_attribut'] == 'ok':
##        ma_balise.text = 'nouvelle valeur'
##        # Si besoin d'une section CDATA
##        # ma_balise.text = etree.CDATA('nouvelle valeur')
##                
##    with open('monfichier.xml', 'w') as f1:
##    f1.write(etree.tounicode(xml))           
#                
#    #index=xmlProjets[0].index(nameProjet)
#    #xmlProjets[1][index]=xmlProjet
        
def replace(nameProjet, numPage, numElem, newType,xmlProjet) :
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			for e1 in e.findall('element'):
				if not(e1 is None):
					#print(str(e1.attrib['id']))
					if e1.attrib['id']==str(numElem):
						e1.attrib['type'] = newType
						return xmlProjet
#xmlProjet.replace(e, e)

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
		#if e.attrib['id']==str(numPage) :
		#	return e

def reSave(nameProjet, numPage, numElem, xmlProjet) : #peut retirer name project    
	for e in xmlProjet.findall('page'):
		if e.attrib['id']==str(numPage) :
			#print('passe numpage')
			for e1 in e.findall('element'):
				if not(e1 is None):
					if e1.attrib['id']==str(numElem):
						return True 
	return False
            #addElement(typeEl, idEl, posiX, posiY, widthEl, heightEl, e)

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
	#page=foundPage(nameProjet,numPage,xmlProjet)
	allPage=findAllPage(xmlProjet)
	#print("all page " +str(allPage))
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
	#page=foundPage(nameProjet,numPage,xmlProjet)
	allPage=findAllPage(xmlProjet)
	#print("all page " +str(allPage))
	listRect=[]
	numR=0
	for page in allPage:
			#if page.attrib['id']==str(numPage):
			for rect in page.findall('element'):
				typeRect=rect.attrib['type'] 
				#numrect=rect.attrib['id'] 
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


