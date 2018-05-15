# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:53:46 2018

@author: rachel
"""
from lxml import etree
import os.path
#from xml.dom import minidom

#C:/Users/rachel/Documents/GitHub/ProjetCheminDeFer/docXml/
xmlProjet = etree.Element('newProject')
numero=0

def checkFileExiste(nameFile):
    #nameFile.exists()
    return os.path.exists(nameFile)

def newProjet(nameProjet):
    global xmlProjet
    xmlProjet = etree.Element(nameProjet)
    global numero 
    numero=0     

def newPage(pathPage):
    global numero 
    
    page = etree.SubElement(xmlProjet,'page')
    page.set('id',str(numero)) 
    
    file = etree.SubElement(page,'file')
    file.set('path',pathPage)
    numero +=  1;
    return page
    

def endProjet(nameProjet) :   
    #xmlProjet = etree.Element(nameProjet)
    try:
        with open(nameProjet +'.xml','w') as fichier:
        #En-tête du fichier xml
            fichier.write('<?xml version="1.0" encoding="UTF_8"?>\n')
            fichier.write(etree.tostring(xmlProjet,pretty_print=True).decode('utf-8'))#cree premiere balise
            #xmlProjet = etree.Element(nameProjet)
    except IOError:
        print('Problème rencontré lors de l\'écriture ...')
        exit(1)
        

def ajouterElement(typeEl, posiX, posiY, widthEl, heightEl,page):
    
#    page = etree.SubElement(xmlProjet,'page')
#    page.set('id',bytes(numero))
#    
    
    element = etree.SubElement(page,'element') #ou append
    element.set('type',typeEl)#recurere le typele l'element de la liste
    
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



newProjet('myNewProjet')
p=newPage('mynewPage')
ajouterElement('para',1,2,3,4,p)
endProjet('new')