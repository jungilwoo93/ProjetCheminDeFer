# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:53:46 2018

@author: rachel
"""
from lxml import etree
import os.path
#from xml.dom import minidom

#C:/Users/rachel/Documents/GitHub/ProjetCheminDeFer/docXml/
xmlProjets

try :
    xmlProjets[0][0]
except IOError :
    xmlProjets = [[],[]]
#name=[]
#memoire=[]
#xmlProjet.append(name)
#xmlProjet.append(memoire)
xmlProjet
numero

def checkFileExiste(nameFile):
    #nameFile.exists()
    return os.path.exists(nameFile)


def newProjet(nameProjet):
    #if os.path.exists(nameProjet):
    print('ce nom est déjà prit')
    #demande de changer
    #else:
    global xmlProjet
    xmlProjet = etree.Element(nameProjet)#fait recommencer
    global xmlProjets
    #size=len(xmlProjets)
    #xmlProjets[0][size]=nameProjet
    #xmlProjets[1][size]=xmlProjet
    xmlProjets[0].append(nameProjet)
    xmlProjets[1].append(xmlProjet)
    global numero 
    numero=0     

def continuePoject(nameProjet):
    global xmlProjet
    #xmlProjet= etree.Element(nameProjet)
    index=xmlProjets[0].index(nameProjet)
    xmlProjet=xmlProjets[1][index]

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
        with open('docXml/' + nameProjet +'.xml','w') as fichier:
        #En-tête du fichier xml
            fichier.write('<?xml version="1.0" encoding="UTF_8"?>\n')
            index=xmlProjets[0].index(nameProjet)
            xmlProjets[1][index]=xmlProjet
            fichier.write(etree.tostring(xmlProjet,pretty_print=True).decode('utf-8'))#cree premiere balise
            #xmlProjet = etree.Element(nameProjet)
    except IOError:
        print('Problème rencontré lors de l\'écriture ...')
        exit(1)
        

def addElement(typeEl, posiX, posiY, widthEl, heightEl,page):
    
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


def delectElement():
    
nameProjet='myNewProjet'
#newProjet(nameProjet)
continuePoject(nameProjet)
p=newPage('page original me revoila')
ajouterElement('para',1,2,3,4,p)
#ajouterElement('paruhjkl',7,2,3,4,p)
endProjet(nameProjet)
ajouterElement('paruhjkl',7,2,3,4,p)
endProjet(nameProjet)