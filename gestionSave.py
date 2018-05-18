# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:53:00 2018

@author: rachel
"""

def writeInText(nameProjet,numPage):
    fichier = open("elemSave.txt", "w")
    fichier.write(nameProjet + ' ' + numPage)
    fichier.close()
    
def mettreAJour(nameProjet,numPage):
    lines = None
    with open('elemSave.txt', 'r') as file:
        lines = file.readlines()
        #lines = [l in file.readlines() if l.contain(nameProjet)]
    with open('elemSave.txt', 'w') as file:
        for line in lines :
            file.write("\r\n".join(lines))
    