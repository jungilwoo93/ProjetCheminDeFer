# -*- coding: utf-8 -*-
"""
Created on Mon May  7 16:26:16 2018

@author: Rachel Noireau et Liuyan PAN
"""

import tkinter as tk
import tkinter.filedialog as tf
from PIL import Image, ImageFont, ImageDraw, ImageTk
import os
from os.path import basename

#### nos autre fichier
import DrawRect as rect
import creatXml as xl
import gestionSave as gs
#import pdfToImg as pti

#########################################################  fenetre principale ##################################################
#créer la fenêtre d'application
root = tk.Tk()
#récupérer la taille d'écran d'ordi
ecran_width = root.winfo_screenwidth()*0.9
ecran_height = root.winfo_screenheight()*0.85
#définir la taille d'écran d'or comme la fenêtre d'application
#root.geometry(str(ecran_width)+'x'+str(ecran_height))
root.geometry('%dx%d+%d+%d' % (ecran_width, ecran_height, 1, 1))
#mettre le title et background pour l'application
root.title("trainning Chemin de Fer")
root.resizable(width=False,height=False)

colorDefault="#F5F5DC" #bd=-2 #supprime bordure
#F5F5DC #beige

####################################################### frame entier ########################################################3
f=tk.Frame(root,bg=colorDefault ,width=ecran_width,height=ecran_height)
#scrollbar pour la fenetre pricipqle
#vsb = tk.Scrollbar(f, orient=tk.VERTICAL)
#vsb.grid(row=0, column=3, rowspan=4, sticky=tk.N+tk.S+tk.E)#
#vsb.grid(row=0,column=2,rowspan=5,sticky=tk.E+tk.N+tk.S)
#hsb = tk.Scrollbar(f, orient=tk.HORIZONTAL)
#hsb.grid(row=1,column=0,sticky=tk.W)

#hsb.grid(row=1, column=0,columnspan=5, sticky=tk.E+tk.W)
#c = tk.Canvas(f, yscrollcommand=vsb.set, xscrollcommand=hsb.set, width=ecran_width, height=ecran_height,bd=0,highlightthickness=0)
c=tk.Canvas(f,width=ecran_width, height=ecran_height,bd=0,highlightthickness=0,bg=colorDefault)
#c.yview_moveto(1)
#c.xview_moveto(1)
c.grid(row=0, column=0, sticky=tk.W+tk.N + tk.S)#,sticky="news"
#vsb.config(command=c.yview)#c.yview
#hsb.config(command=c.xview)
#root.grid_rowconfigure(0, weight=1)
#root.grid_columnconfigure(0, weight=1)

######################################################## variable global #######################################################
var=tk.StringVar()
var.set("Paragraphe")
typeZone={"Titre","Paragraphe","Lettrine","Image"}
listPath=[]
drawRect=None
nbConfirm=0
dict1={}
selectedAction=None
nameProjet='new'
numPage=0

#################################################### toutes les fonctions  ####################################################
# fonction de buttonConfirm
def confirmer():
    global nbConfirm
    nbConfirm+=1
    listAction.insert(tk.END,var.get()+'-'+str(nbConfirm))
    dict1[var.get()+'-'+str(nbConfirm)]=drawRect.getCoordonnes()
    print(drawRect.getCoordonnes())
    
# parcours choit du fichier
def chooseFile():
    #choice=fenetre.FileDialog(tf.msoFileDialogOpen)
    choice = tf.askopenfilenames() #fichier uniquement
    #choice = tf.askdirectory()  #repertoire uniquement
    #defaultextension='.png'
    #filetypes=[('BMP FILES','*.bmp')]#pas sure
    #filetypes=[('PNG FILES','*.png')]
    #("JPEG",'*.jpg')
    #print(choice)
    #choiceBoth=tf.
    #os.listdir #pour recupereelement d'un dosier
    nbSelected=len(choice)
    #recupere le nom apartir du chemin
    for i in range (0,nbSelected):
        ext = os.path.splitext(choice[i])[1]
        nomExt=basename(choice[i])
        #nom=choice[i]
        nom=os.path.splitext(nomExt)[0]
        if ext == '.pdf':
            global nameProjet
            nameProjet=nom
            print('c est un pdf')
            
            ##########################################a remetre 
            
            #listImg = pti.pdfToPng(choice[i],'mon projet')
            #size=len(listImg)
            #for k in range (0, size) :
             #   listFiles.insert(listFiles.size(),basename(listImg[k])) 
              #  listPath.append(listImg[i])
            
            
        else :
            if nom!="": #sinon quand on clic sur parcourir mais qu'on ne choisi rien ça rajoute un espace blanc
                listFiles.insert(listFiles.size(),nom) 
                #listFiles.
                listPath.append(choice[i])
               # listFiles.TopIndex = listFiles.ListCount
                #i+=1
    #pour trier par ordre alpha et enlever les boutons            
#    listFiles.Sorted = True
#    listPath.sort()
#    j=0
#    while j < (listFiles.size() - 1) :
#        if (listFiles.get(j + 1,j+1) == listFiles.get(j,j)) :
#            listFiles.delete(j,j)
#            listPath.remove(listPath[j])
#            j = 0
#        else :
#            j += 1
    #listPath.reverse()??????????????????????????
    
            
 
# supprimer de la liste tout les fichiers
def delecteAll():
    #cs=listFiles.curselection()
    #listFiles.delete(0,cs[0] -1)
    listFiles.delete(0,tk.END) 
    listPath.clear()
    
def nextPage():  #a mettre dans enregister #voir si onSelect se fait tout seul
    global numPage
    if gs.projetExist(nameProjet):
        gs.update(nameProjet,numPage)
    else :
        gs.writeInText(nameProjet,numPage)
    
    
    if numPage<listFiles.size() :
        numPage += 1
        #print(numPage)
        listFiles.selection_clear(0, tk.END)
        listFiles.selection_set(numPage)
        selectByButton() 
     
    
def lastPage():
    global numPage
    if numPage>0 :
        numPage -= 1
        #print(numPage)
        listFiles.selection_clear(0, tk.END)
        listFiles.selection_set(numPage)
        selectByButton()
  
############################# Barre menu 
def newProjet():
    global numPage
    numPage=0
    chooseFile()
    xl.newProjet(nameProjet)

def projetToContinu(listProjet):   
    global nameProjet
    nameProjet =listProjet.get(listProjet.curselection())
    global numPage
    numPage=gs.getAvancementProjet(nameProjet)
    listFiles.selection_set(numPage)
    
def continueProjet():
    
    rootpop = tk.Tk()
    rootpop.title("choisit le projet")
    listFrame=tk.Frame(rootpop)
    
    yDefilB = tk.Scrollbar(listFrame, orient='vertical')
    yDefilB.grid(row=0, column=1, sticky='ns')
    xDefilB = tk.Scrollbar(listFrame, orient='horizontal')
    xDefilB.grid(row=1, column=0, sticky='ew')
    
    listProjet = tk.Listbox(listFrame,
        xscrollcommand=xDefilB.set,
        yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE)
    listProjet.grid(row=0)#'nsew'
    #listFiles.pack(side="left",fill="y")  
    xDefilB['command'] = listProjet.xview
    yDefilB['command'] = listProjet.yview
    
    #global xl.xmlProjets
    #xl.duplicationProjet()
    #print(len(xl.listProjets))
    Projetlist=xl.getListProjet()
    for i in range (0 ,len(Projetlist)):
        listProjet.insert(1,Projetlist[i])
    listFrame.grid(row=0,pady=0,padx=15,sticky=tk.W+tk.N +tk.E)
    listProjet.grid(row=0,pady=0,padx=15,sticky=tk.W+tk.N +tk.E)
    
    listProjet.bind('<<ListboxSelect>>', projetToContinu(listProjet))


menubar=tk.Menu(root)
root.config(menu = menubar)
menufichier = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label="Fichier", menu=menufichier)


menufichier.add_command(label="Nouveau Projet", command=newProjet)
menufichier.add_command(label="Continuer Projet", command = continueProjet) 
menufichier.add_separator() 
menufichier.add_command(label="Quitter", command=root.destroy) 

############################################################ frame à gauche ####################################################
#f1=tk.Frame(root,bg='gold', width=ecran_width+1000, height=ecran_height)
#f1.config(width=ecran_width+1000, height=ecran_height)
#f1.grid(column=0,columnspan=1000,sticky=tk.E)
f1=tk.Frame(c,bg=colorDefault,height=ecran_height,width=ecran_width*0.4)
f1.grid(row=0,column=0,sticky=tk.S+tk.W+tk.N)

####################### label fichiers choisis
labelFichier=tk.Label(f1,text='Les fichiers choisis : ', bg=colorDefault)
labelFichier.config(font=('Forte',18))
labelFichier.grid(row=0,sticky=tk.W,pady=5)

################################ frame pour listeBox et leur scrollbar
listFrame=tk.Frame(f1)

###################### scrollbar vertical et horizontal
yDefilB = tk.Scrollbar(listFrame, orient='vertical')
yDefilB.grid(row=0, column=1, sticky='ns')
xDefilB = tk.Scrollbar(listFrame, orient='horizontal')
xDefilB.grid(row=1, column=0, sticky='ew')

##################### listBox pour afficher les fichiers choisis
listFiles = tk.Listbox(listFrame,
     xscrollcommand=xDefilB.set,
     yscrollcommand=yDefilB.set,width=70,height=15,selectmode=tk.SINGLE)
listFiles.grid(row=0)#'nsew'
#listFiles.pack(side="left",fill="y")  
xDefilB['command'] = listFiles.xview
yDefilB['command'] = listFiles.yview
listFrame.grid(row=1,pady=5,padx=20,sticky=tk.W)

################### frame pour les buttons parcourir, supprimer, vider
#zoneButton=tk.Frame(f1)
"""boutonParcourir=tk.Button(zoneButton,text="Parcourir",command=chooseFile).grid(row=1, column=0,sticky=tk.S,padx=40)
boutonSupprimer=tk.Button(zoneButton,text="Supprimer",command=delecteSelection).grid(row=1, column=1,sticky=tk.S,padx=40)
boutonSupprimer=tk.Button(zoneButton,text="Vider",command=delecteAll).grid(row=1, column=2,sticky=tk.S,ipadx=10,padx=40)"""
#zoneButton.grid(row=2,pady=5)

################## label pour la zone choisie
labelZoneChoix=tk.Label(f1,text='La zone choisie est : ', bg=colorDefault)#,  gold
labelZoneChoix.config(font=('Forte',18))
labelZoneChoix.grid(row=2, sticky=tk.W)

########################3 frame pour afficher les radiobuttons des choix
zoneRadioButton=tk.Frame(f1, bg=colorDefault)
a=0
for i,v in enumerate(typeZone):
    tk.Radiobutton(zoneRadioButton, text=v, variable=var, value = v, bg=colorDefault).grid(row=0, column=a,sticky=tk.W,padx=20)
    a+=1
zoneRadioButton.grid(row=3,sticky=tk.W,pady=5)

################ button pour comfirmer le choix avec la zone choisit sur image
buttonConfirm=tk.Button(f1,text="Confirmer",command=confirmer).grid(row=4,column=0,pady=5,sticky=tk.S)

################ listebox pour les Actions
def onSelectAction(evt):
    global selectedAction
    if selectedAction is not None:
        cadre.delete(selectedAction)
    selection=listAction.get(listAction.curselection())
    list1=[]
    list1=dict1[selection]
    selectedAction=cadre.create_rectangle(list1[0],list1[1],list1[0]+list1[2],list1[1]+list1[3],width=5)
    
labelAction=tk.Label(f1,text="Les actions : ", bg=colorDefault)
labelAction.config(font=('Forte',18))
labelAction.grid(row=5,column=0,pady=5,sticky=tk.W)
listAction = tk.Listbox(f1,width=70,height=8)
listAction.grid(row=6,column=0,pady=5)
listAction.bind('<<ListboxSelect>>', onSelectAction)  

# supprimer de la liste les fichiers selectionnés
def deleteSelection():#pour liste des actions
    selection = listAction.curselection()
    listAction.delete(selection[0])
    #listPath.remove(selection[0])

#################fonctio de generation du xml
def save():
    if not(xl.pageExist(nameProjet, numPage)) :
        page = xl.addPage('nom Page')
    else :
        page = xl.foundPage(nameProjet, numPage)
    sizelist=listAction.size()
    #w=evt.widget
    for k in range (0,sizelist) :
        #if len(w.curselection())!=0 :
        selection = listAction.curselection()
        typeEl = selection[0]
        index = int(listAction.curselection()[0])#.w
        posiX=1
        posiY=1
        widthEl=1
        heightEl=1
        #numPage=2
        numElem=2
        if not(xl.reSave(nameProjet, numPage, numElem)) :
            xl.addElement(typeEl, posiX, posiY, widthEl, heightEl,page)
            xl.endProjet(nameProjet)
        else :
            if not(xl.sameType(nameProjet, numPage, numElem, typeEl)):
                xl.replace(nameProjet, numPage, numElem, typeEl)
                xl.endProjet(nameProjet)
    nextPage()
        

                

################ button pour confirmer le choix des element de la page ##############
fButtons=tk.Frame(f1, bg=colorDefault)
buttonDelete=tk.Button(fButtons,text="Supprimer",command=deleteSelection).grid(row=0,column=0,padx=40,sticky=tk.S)
buttonLast=tk.Button(fButtons,text="Précédent",command=lastPage).grid(row=0,column=1,padx=40,sticky=tk.S)
buttonSave=tk.Button(fButtons,text="Enregistrer et Suivant",command=save).grid(row=0,column=2,padx=40,sticky=tk.S)
#buttonSave=tk.Button(fButtons,text="Suivant",command=suivant).grid(row=0,column=1,padx=50,sticky=tk.S)
fButtons.grid(row=7,column=0,pady=20)

############################################### frame à droite pour afficher l'image ##########################################
#f0 = tk.Frame(f1)
#f0.grid(fill=tk.BOTH)
#f0.pack(fill=tk.BOTH)
#c.grid(sticky=tk.E)
#c.create_window(0, 0,  window=f1)

 
#c.create_window(0, 0,  window=f0)
#f0.update_idletasks()
#c.config(scrollregion=c.bbox("all"))#a mettre a la fin

#afficher image dés qu'on selectionne un element
#zoneImage=tk.Frame(root,bg="black")
#zoneImage.grid(row=2,column=10,rowspan=2,columnspan=8,sticky=tk.E )
fImg=tk.Frame(c,width=ecran_width*0.6,height=ecran_height, bg=colorDefault)
fImg.grid(row=0,column=1,sticky=tk.N+tk.S)
cadre=tk.Canvas(c, bg=colorDefault, bd=-2)
cadre.grid(row=0,column=1)

def selectByButton():
    dicimg = {}
    global numPage
    img=Image.open(listPath[numPage])
    wd,hg=img.size
    mwd=ecran_width
    mhg=ecran_height
    if wd>mwd :
            scale= 1.0*wd/mwd
            newImg=img.resize((int(wd/scale),int(hg/scale)),Image.ANTIALIAS)
            cadre.config(width=wd/scale,height=hg/scale)
            photo = ImageTk.PhotoImage(newImg)
            dicimg['img1'] = photo
            cadre.image=photo
            cadre.create_image(0,0,image=photo,anchor="nw") 
    elif hg > mhg:
            scale = 1.0*hg/mhg
            newImg = img.resize((int(wd/scale),int(hg/scale)), Image.ANTIALIAS)
            cadre.config(width=wd/scale,height=hg/scale)
            photo = ImageTk.PhotoImage(newImg)
            dicimg['img1'] = photo
            cadre.image=photo
            cadre.create_image(0,0,image=photo,anchor="nw") 
    else:
            cadre.config(width=wd,height=hg)
            photo = ImageTk.PhotoImage(img)
            dicimg['img1'] = photo
            cadre.image=photo
            cadre.create_image(0,0,image=photo,anchor="nw") 
    drawRect=rect.CanvasEventsDemo(cadre)
    cadre.bind('<ButtonPress-1>', drawRect.onStart)  
    cadre.bind('<B1-Motion>',     drawRect.onGrow)   
    cadre.bind('<Double-1>',      drawRect.onClear)  
    cadre.bind('<ButtonPress-3>', drawRect.onMove)   
    cadre.bind('<ButtonRelease-1>', drawRect.onFinal)
    gs.mettreAJour(nameProjet,numPage)

    
def onselect(evt):
    
    global drawRect,isDraw,newImg
    #cadre=tk.Canvas(c,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=ecran_width-600,height=ecran_height-25,bg="black")#,bg="black"
    #cadre=tk.Label(f,yscrollcommand=vsb.set, xscrollcommand=hsb.set,width=320,height=240,bg="green")
    #cadre=tk.Canvas(root,width=ecran_width-500,height=ecran_height,bg="black")
    dicimg = {}
    #selection = listFiles.curselection()
    #print(selection[0])
    w=evt.widget
    if len(w.curselection())!=0 :
        index = int(w.curselection()[0])
        global numPage
        numPage=index
        #value = w.get(index)
        img=Image.open(listPath[index])
        #img.resize((320,240))
        #img.zoom(320/img.width(), 240/img.height())
        wd,hg=img.size
        mwd=ecran_width
        mhg=ecran_height
        if wd>mwd :
            scale= 1.0*wd/mwd
            newImg=img.resize((int(wd/scale),int(hg/scale)),Image.ANTIALIAS)
            cadre.config(width=wd/scale,height=hg/scale)
            photo = ImageTk.PhotoImage(newImg)
            dicimg['img1'] = photo
            cadre.image=photo
            cadre.create_image(0,0,image=photo,anchor="nw") 
        elif hg > mhg:
            scale = 1.0*hg/mhg
            newImg = img.resize((int(wd/scale),int(hg/scale)), Image.ANTIALIAS)
            cadre.config(width=wd/scale,height=hg/scale)
            photo = ImageTk.PhotoImage(newImg)
            dicimg['img1'] = photo
            cadre.image=photo
            cadre.create_image(0,0,image=photo,anchor="nw") 
        else:
            cadre.config(width=wd,height=hg)
            photo = ImageTk.PhotoImage(img)
            dicimg['img1'] = photo
            cadre.image=photo
            cadre.create_image(0,0,image=photo,anchor="nw") 
        #newImg.save(listPath[index])  
        #newImg.close() 
        
        drawRect=rect.CanvasEventsDemo(cadre)
        cadre.bind('<ButtonPress-1>', drawRect.onStart)  
        cadre.bind('<B1-Motion>',     drawRect.onGrow)   
        cadre.bind('<Double-1>',      drawRect.onClear)  
        cadre.bind('<ButtonPress-3>', drawRect.onMove)   
        cadre.bind('<ButtonRelease-1>', drawRect.onFinal)
        gs.mettreAJour(nameProjet,numPage)
        
        #zoneImage.grid(row=2,column=5000,rowspan=2,columnspan=8,sticky=tk.E)#,padx=20,pady=20
        #cadre.grid(row=2,column=500,rowspan=2,columnspan=30,sticky=tk.E)# padx=20,pady=20,
        #cadre.grid(row=0,column=1,sticky=tk.S)
        #cadre.create_window(0, 0,  window=f)
        #cadre.create_window(0,0,window=f1)
        #c.create_window(1,0,window=cadre)
        #f.update_idletasks()
        #f1.grid(row=0,column=0,sticky=tk.W+tk.S)
        
        #cadre.update_idletasks()
        #zoneImage.grid(row=0,column=1,rowspan=2,columnspan=8,sticky=tk.E )
        #cadre.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        #cadre.config(scrollregion=cadre.bbox("all"))

listFiles.bind('<<ListboxSelect>>', onselect)  #green
#buttonLast.bind('<Button-1>', onselect)
#buttonSave.bind('<Button-1>', onselect)
#démarrer du réceptionnaire d'événements

#c.create_window(0, 0,  window=f)

#f.update_idletasks()
#f1.update_idletasks()
c.config(scrollregion=c.bbox("all"))#pour scrooll
f.grid(row=0,column=0,sticky=tk.W+tk.N)
root.mainloop()

