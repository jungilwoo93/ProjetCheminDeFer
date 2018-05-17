# -*- coding: utf-8 -*-
"""
Created on Tue May 15 09:53:46 2018

@author: rachel NOIREAU & liuyan PAN
"""
from lxml import etree
import os.path
#from xml.dom import minidom
import xml.etree.ElementTree as et



#C:/Users/rachel/Documents/GitHub/ProjetCheminDeFer/docXml/
global xmlProjet
global numero
global xmlProjets

try :
    xmlProjets[0][0]
except :
    xmlProjets = [[],[]]
    
#name=[]
#memoire=[]
#xmlProjet.append(name)
#xmlProjet.append(memoire)


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
        

def addElement(typeEl, idEl, posiX, posiY, widthEl, heightEl, page):
    
#    page = etree.SubElement(xmlProjet,'page')
#    page.set('id',bytes(numero))

    element = etree.SubElement(page,'element') #ou append
    element.set('type',typeEl)#recurere le typele l'element de la liste
    element.set('id',typeEl)
    
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


def delectElement(nameProjet,numPage,numElem):
    numPage = "7"#☺\n        <posY>2</posY> \n"# <width>3</width> <height>4</height> </element>" # Texte à rechercher
    #remplace = "salut"
    numElem="1"
    for e in xmlProjet.findall('page'):
        if e.attrib['id']==numPage :
            e1=e.find('element')
            if e1.attrib['id']==numElem:
                listChild=xmlProjet.getchildren() 
                listChild=e.getchildren()
                print(listChild)
                print(e1)
                e.remove(e1)
     
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
#                
#          
#     
#    
#
##    
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
        
def replace(nameProjet, numPage, numElem, newType) :
    numElem="1"
    for e in xmlProjet.findall('page'):
        if e.attrib['id']==numPage :
            e1=e.find('element')
            if e1.attrib['id']==numElem:
                e1.attrib['type'] = newType
                #listChild=xmlProjet.getchildren() 
                #listChild=e.getchildren()
                #e.remove(e1)
                #xmlProjet.replace(e, e)
            

def reSave(nameProjet, numPage, numElem) :     
    for e in xmlProjet.findall('page'):
        if e.attrib['id']==numPage :
            e1=e.find('element')
            if e1.attrib['id']==numElem:
                return True 
            #addElement(typeEl, idEl, posiX, posiY, widthEl, heightEl, e)

def chageType(nameProjet, numPage, numElem, newType):
    for e in xmlProjet.findall('page'):
        if e.attrib['id']==numPage :
            e1=e.find('element')
            if e1.attrib['id']==numElem:
                if e1.attrib['ty']==newType:
                    return True
           
nameProjet='NewProjet'
#newProjet(nameProjet)     
continuePoject(nameProjet)       
 



#p=newPage('page original me revoila')
#addElement('para',1,2,3,4,p)
#addElement('paruhjkl',7,2,3,4,p)
delectElement(nameProjet)  
#endProjet(nameProjet)
#ajouterElement('paruhjkl',7,2,3,4,p)
endProjet(nameProjet)