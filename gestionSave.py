# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:53:00 2018

@author: rachel
"""
# on ecrit dans le fichier txt le nom du projet

def writeInText(nameProjet,numPage):
    fichier = open("elemSave.txt", "a")
    fichier.write(nameProjet + ' ' + str(numPage) + '\n')
    fichier.close()
   
    
def update(nameProjet,numPage):
    lines = None
    with open('elemSave.txt', 'r') as file:
        lines = file.readlines()
        #lines = [l in file.readlines() if l.contain(nameProjet)]
    with open('elemSave.txt', 'w') as file:
        for line in lines :
            if nameProjet.lower() in line.lower() :
                line=nameProjet + ' ' + str(numPage) +'\n'
            file.write(line)

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
    #for j in range(len(projetLigne)):
    return projetList
    

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
                #if projetLigne[0]==nameProjet :
                 #   return int(projetLigne[1])
        
        

#writeInText('coooouuuuuucccoouuuu',4)
#update('salut',100)
#print(getAvancementProjet('moche'))
#print(getListProjet())