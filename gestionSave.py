# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:53:00 2018

@author: rachel NOIREAU et Liuyan PAN
"""

# on ecrit dans le fichier txt le nom du projet et le numero de la page auquel on en est 
def writeInText(nameProjet,numPage):
    fichier = open("elemSave.txt", "a")
    fichier.write(nameProjet + ' ' + str(numPage)+' \n')
    fichier.close()
   

#tenir a jour la page a laquel on est
def update(nameProjet,numPage):
	lines = None
	with open('elemSave.txt', 'r') as file:
		lines = file.readlines()
	with open('elemSave.txt', 'w') as file:
		for line in lines :
			if nameProjet.lower() in line.lower() :
				if 'CDF' in line :
					line=nameProjet + ' ' + str(numPage) +' CDF' +' \n'
				else:
					line=nameProjet + ' ' + str(numPage) + ' \n'
			if line != "":
				file.write(line)

#verifier si le projet existe
def projetExist(nameProjet) :
    lines = None
    with open('elemSave.txt', 'r') as file:
        lines = file.readlines()
    for line in lines :
        esp = line.count(" ")
        deb = 0
        fin = line.index(" ")
        projetLigne = []
        for i in range(0, esp + 1):
            projetLigne.append(line[deb:fin])
            line=line[fin+1:]
            if line.count(" ")!=0:
                fin = line.index(" ")
            else:
                fin = len(line) 
            if projetLigne[0]==nameProjet :
                return True
    return False
            
#retourne la liste de tout les projet déjà commencé
def getListProjet():
    lines = None
    projetList = []
    with open('elemSave.txt', 'r') as file:
        lines = file.readlines()
    for line in lines :
        esp = line.count(" ")
        deb = 0
        fin = line.index(" ")
        projetLigne = []
        for i in range(0, esp + 1):
            projetLigne.append(line[deb:fin])
            line=line[fin+1:]
            if line.count(" ")!=0:
                fin = line.index(" ")
            else:
                fin = len(line)
        projetList.append(projetLigne[0])
    return projetList
    
#savoir a quelle page on en est pour un projet particulier
def getAvancementProjet(nameProjet):
    lines = None
    with open('elemSave.txt', 'r') as file:
        lines = file.readlines()
        
        for line in lines :
            if nameProjet.lower() in line.lower() :
                esp = line.count(" ")
                deb = 0
                fin = line.index(" ")
                projetLigne = []
 
                for i in range(0, esp + 1):
                    projetLigne.append(line[deb:fin])
                    line=line[fin+1:]
                    if line.count(" ")!=0:
                        fin = line.index(" ")
                    else:
                        fin = len(line)
                return projetLigne[1]



#savoir si le chemin de ce projet a déjà etait generer ou non
def cheminIsDone(nameProjet):
    lines = None
    with open('elemSave.txt', 'r') as file:
        lines = file.readlines()
        
        for line in lines :
            if nameProjet.lower() in line.lower() :
                esp = line.count(" ")
                deb = 0
                fin = line.index(" ")
                projetLigne = []
 
                for i in range(0, esp + 1):
                    projetLigne.append(line[deb:fin])
                    line=line[fin+1:]
                    if line.count(" ")!=0:
                        fin = line.index(" ")
                    else:
                        fin = len(line)
                if len(projetLigne)==4:
                    return projetLigne[2]=='CDF'

#ecrit que le chemin de fer vient d'etre fait
def doChemin(nameProjet, numPage):
	lines = None
	with open('elemSave.txt', 'r') as file:
		lines = file.readlines()
	with open('elemSave.txt', 'w') as file:
		for line in lines :
			if nameProjet.lower() in line.lower() :
				line=nameProjet + ' ' + str(numPage) + ' ' +'CDF' +' \n'
			if line!= "":
				file.write(line)
