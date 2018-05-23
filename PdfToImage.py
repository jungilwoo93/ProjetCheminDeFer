# -*- coding: utf-8 -*-
"""
Created on Wed May 16 10:34:42 2018

@author: panpa
"""
import tkinter.filedialog as tk
#from PIL import Image, ImageFont, ImageDraw, ImageTk
#from __future__ import print_function
from wand.image import Image
from wand.color import Color
import PyPDF2 as pdf
import os

#print(os.environ['MAGICK_HOME'])
root = tk.Tk()

drawing = False #si le souris click, devient true
positionCurrent=None
ix,iy = -1,-1
#panelA=None
root.title("Projet")
#récupérer la taille d'écran d'ordi
ecran_width = root.winfo_screenwidth()-500
ecran_height = root.winfo_screenheight()-100
#définir la taille d'écran d'or comme la fenêtre d'application
root.geometry(str(ecran_width)+'x'+str(ecran_height))
f1=tk.Frame(root)
f1.grid(row=0,column=1)

def pdfToPng():
    global path
    path = tk.askopenfilename()
    if len(path) > 0: 
        splitPath(path)
        """print("filepath= " +filePath)
        print("tempfilename="+tempfileName)
        print("shotname="+shotName)
        print("extention="+extension)"""
        #nb le chemin du fichier source
        #### 1 ####
        """with Image(filename=path,resolution=500) as img:
            img.compression_quality = 99
            with Image(width=img.width, height=img.height, background=Color("white")) as bg:
                bg.composite(img,0,0)
                bg.save(filename='page.png')"""
                ####1####
    #partie 1 convert juste une page
                #bg.save(filename="D://S4//ProjetCheminDeFer//image.png")
    #partie 2 convert tous les pages
    ### 2#####
        with Image(filename=path,resolution=30) as img:
            print('pages = ', len(img.sequence))
            img.compression_quality = 99
            with img.convert('jpeg') as converted:
                converted.save(filename='page.jpg')   #nb le chemin des results
    ####2####
def splitPath(path):
    global filePath,tempfileName,shotName,extension
    (filePath,tempfileName) = os.path.split(path)
    (shotName,extension) = os.path.splitext(tempfileName)
 
def getCountPage(path):
    sourcePDF=pdf.PdfFileReader(open(path,'rb'))
    countPage=sourcePDF.getNumPages()
    print(countPage)
    return countPage

"""def convertToJPG(path,page,res=120):
    splitPath(path)
    img = Image(filename=path,resolution=res)
    img.format='jpeg'
    img.compression_quality=90
    img.background_color = Color("white")"""
    #img_path = '%s%d.jpg' % ()
    
    """def pdf_to_jpg(pdfPath, pages):
    # print pdf using jpg printer
    # 'pages' is the number of pages in the pdf
    path = pdfPath.rsplit('/', 1)[0]
    filename = pdfPath.rsplit('/', 1)[1]

    #print pdf to jpg using jpg printer
    tempprinter = "ImagePrinter Pro"
    printer = '"%s"' % tempprinter
    win32api.ShellExecute(0, "printto", filename, printer,  ".",  0)

    # Add time delay to ensure pdf finishes printing to file first
    fileFound = False
    if pages > 1:
        jpgName = filename.split('.')[0] + '_' + str(pages - 1) + '.jpg'
    else:
        jpgName = filename.split('.')[0] + '.jpg'
    jpgPath = filepath + '/' + jpgName
    waitTime = 30
    for i in range(waitTime):
        if os.path.isfile(jpgPath):
            fileFound = True
            break
        else:
            time.sleep(1)

    # print Error if the file was never found
    if not fileFound:
        print "ERROR: " + jpgName + " wasn't found after " + str(waitTime)\
              + " seconds"

    return jpgPath"""
    
#btn = tk.Button(root, text="Select an image", command=select_file)
#btn.grid(row=0, column=0,padx="10", pady="10")






root.mainloop()