# -*- coding: utf-8 -*-
"""
Created on Wed May 16 09:34:19 2018

@author: rachel
"""

from __future__ import print_function
#from wand import *
from Wand.image import Image
#from PIL import Image, ImageFont, ImageDraw, ImageTk



#nb le chemin du fichier source
def pdfToPng(namefile,nameProjet): #'test1/source1.pdf'
    page=0
    listImg =[]
    with Image(filename=namefile,resolution=30) as img: #30 == low quality(utilisée pour l'app java) 60== high quality utilisé pour le traitement de l'img
            print('pages = ', len(img.sequence))
            img.compression_quality = 99
            with img.convert('png') as converted:
                converted.save(filename='ImgFromPdf/' + namefile + 'page' + page + '.png')    #nb le chemin des results
                #'test1/result/page_n.png'
                listImg.append('ImgFromPdf/' + namefile + '/'+ 'page' + page + '.png')
                page += 1