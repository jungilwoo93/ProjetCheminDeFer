# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:53:46 2018

@author: rachel
"""
from lxml import etree

xmlProjet = etree.Element('new')
numero=0


def NewPage(pathPage):
    #numero += 1;
    page = etree.SubElement(xmlProjet,'page')
    page.set('id',bytes(numero)) 
    
    file = etree.SubElement(page,'element')
    file.set('path',pathPage) 

def creeProjet(nameProjet) :   
    xmlProjet = etree.Element(nameProjet)
    try:
        with open(nameProjet +'.xml','w') as fichier:
        #En-tête du fichier xml
            fichier.write('<?xml version="1.0" encoding="UTF_8"?>\n')
            fichier.write(etree.tostring(xmlProjet,pretty_print=True).decode('utf-8'))
    except IOError:
        print('Problème rencontré lors de l\'écriture ...')
        exit(1)
        

def ajouterElement(typeEl, posiX, posiY, widthEl, heightEl):
    
    page = etree.SubElement(xmlProjet,'page')
    page.set('id',bytes(numero))
    
    
    element = etree.SubElement(page,'element') #ou append
    element.set('type',typeEl)#recurere le typele l'element de la liste
    
    #truc du prof
#    position = etree.SubElement(element,'element')
#    position.set('posX','mobile')
#    position.set('posY','mobile')
#    position.set('width','mobile')
#    position.set('height','mobile')
    
    posX = etree.SubElement(element,'posX')
    posX.text= posiX
    posY = etree.SubElement(element,'posY')
    posY.text= posiY
    
    width = etree.SubElement(element,'width')
    width.text= widthEl
    height = etree.SubElement(element,'height')
    height.text= heightEl
    
    
    #return 0

