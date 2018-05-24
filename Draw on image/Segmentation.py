# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 14:04:46 2018

@author: DL9
"""

import cv2
import xml.etree.cElementTree as ET

for x in range(130, 169):  # les images chargées pour la segmentation image130 à image 169
    id_img="page_n-"+str(x)+".png"
    
    
    root = ET.Element('Image',id=id_img)
    components = ET.SubElement(root, "element")
    
    
    
    or_im=cv2.imread("imgFromPdf/"+id_img)  #les images extraite en haute qualité se trouve dans le dossier /images
    kernel1 = cv2.getStructuringElement(cv2.MORPH_CROSS, (1, 2)) 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 1))
    
    #Read a grayscale image
    im_gray = cv2.imread("imgFromPdf/"+id_img, cv2.IMREAD_GRAYSCALE)
    
    #Convert grayscale image to binary
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    #inverting the colors since opencv uses black as a background
    im_bw=cv2.bitwise_not(im_bw)
    im_bw1=im_bw
    
    im_bw=cv2.erode(im_bw,kernel, iterations=1)
    im_bw = cv2.dilate(im_bw,kernel1, iterations=2)
    
    #finding lettrines
    _, contours, _=  cv2.findContours(im_bw, cv2.RETR_LIST,
    	cv2.CHAIN_APPROX_NONE)
    
    for contour in contours:
             [x, y, w, h] = cv2.boundingRect(contour)
             if w <500 and h <50 :    #finding the big bigblocks aka "paragraphes"
    
             component = ET.SubElement(components, "element")
             ET.SubElement(component, "type").text = "lettrine"
             ET.SubElement(component, "width").text = str(w)
             ET.SubElement(component, "height").text = str(h)
             ET.SubElement(component, "posX").text = str(x)
             ET.SubElement(component, "posY").text = str(y)
             
             cv2.rectangle(or_im, (x, y), (x + w, y + h), (255, 0, 0), 3)
             cv2.putText(or_im, "letr", (x - 20, y - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
             
    im_bw1 = cv2.dilate(im_bw1,kernel, iterations=5)   
    
    
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    im_bw1 = cv2.morphologyEx(im_bw1, cv2.MORPH_CLOSE, kernel2)
    _, contours1, _=  cv2.findContours(im_bw1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #finding bigblocks
    for contour in contours1:
             [x, y, w, h] = cv2.boundingRect(contour)
             if w <80 and h <40 :  #les lettrines en generales sans assez petites
                 continue
    
             component = ET.SubElement(components, "element")
             ET.SubElement(component, "type").text = "unknown"
             ET.SubElement(component, "width").text = str(w)
             ET.SubElement(component, "height").text = str(h)
             ET.SubElement(component, "posX").text = str(x)
             ET.SubElement(component, "posY").text = str(y)
             cv2.rectangle(or_im, (x, y), (x + w, y + h), (0, 255, 0), 1)
             cv2.putText(or_im, "txt", (x - 20, y - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)   #cette ligne permet de dessiner sur l'image segmenter pour verifier la segmentation, cela est optionnel
    
    #saving
    tree = ET.ElementTree(root)
    tree.write("Results/xml_results/"+id_img+"-Unlabelled.xml")     #writing elements to an unlabelled xml(it's unlabelled since we have not classified it yet)
    cv2.imwrite('bw_image.png', im_bw1)        #optionnel visuel d'une image en "mi-processing"
    cv2.imwrite("Results/"+id_img, or_im)      #optionnel image segmenter