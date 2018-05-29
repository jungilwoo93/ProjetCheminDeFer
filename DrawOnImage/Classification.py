# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 01:37:20 2018

@author: DL9
"""
import glob
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import xml.etree.ElementTree as ET
import pandas as pd





dataSet=[] #training dataset
unknownSet=[]
nameProjet='Batch'

class Component(object):

    def __init__(self,tp,x,y,w,h):
        self.type=tp
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        

def extractPaths(path):
	xmlFiles=glob.glob(path+"/*.xml")
	fileList=list()
	for x in range(0,len(xmlFiles)):
		fileList.append(xmlFiles[x][28:])#28:nombre de caractere du chemin
	return fileList
    
def extractUnlabelledPaths(path):
    xmlFiles=glob.glob(path+"/*.xml")
    fileList=list()
    for x in range(0,len(xmlFiles)):
         fileList.append(xmlFiles[x][26:])#75:nbr de car
    return fileList
    



def feedList(tp,x,y,w,h): #type,point x, pointY, RectangleWidth,RectangleHeight
    print('ajout a dataset')
    if tp == "Paragraphe":
        dataSet.append([x,y,w,h,1])
        
    elif tp == "Titre":
         dataSet.append([x,y,w,h,2])
    
def feedUnlabelledList(tp,x,y,w,h,i):
   
    if tp == "unknown":
        unknownSet.append([x,y,w,h,i])

def extractUnlabelledData(path):
	fileNames=extractUnlabelledPaths(path)
	#file=root.attrib['id']
	for x in range(0,len(fileNames)):#fileNames
		tree = ET.parse(path+''+fileNames[x])
		root = tree.getroot()
		file=root.attrib['id']
		for component in root.iter('page'):
			for elem in component.iter('element'):
				feedUnlabelledList(elem.attrib['type'],elem.find('posX').text,elem.find('posY').text,elem.find('width').text,elem.find('height').text,file)

def extractData(path):
	fileNames=extractPaths(path)
	print('fichier de xml')
	print(fileNames)
	for x in range(0,len(fileNames)):
		print('nomfichier')
		print(path+''+fileNames[x])
		if fileNames[x]==nameProjet + '.xml' :
			print('c est le bon xml')
			tree = ET.parse(path+''+fileNames[x])
			root = tree.getroot()
			for component in root.iter('page'):
				print('page trouve')
				for elem in component.iter('element'):
					print('elem trouver')
					feedList(elem.attrib['type'],elem.find('posX').text,elem.find('posY').text,elem.find('width').text,elem.find('height').text)

def rewriteXml():
	if len(unknownSet)!=0:
		for x in range(0,len(unknownSet)):
				tree = ET.parse('DrawOnImage/workshop_test/'+unknownSet[x][4] + '-Unlabelled.xml')#C:/Users/DL9/Desktop/Machine Learning/Projet3A/Draw on image/
				root = tree.getroot()
				for component in root.iter('page'):
					for elem in component.iter('element'):
						if elem.attrib['type']=="unknown":
							#print(x)
							if y_pred[x]==1:
								elem.attrib['type']="Paragraphe"
							else:
								elem.attrib['type']="Titre"
							tree.write('DrawOnImage/workshop_test/'+unknownSet[x][4] + '-Unlabelled.xml')#C:/Users/DL9/Desktop/Machine Learning/Projet3A/Draw on image/
							break





extractData('DrawOnImage/XMLTrainingData/')#C:/Users/DL9/Desktop/

extractUnlabelledData("DrawOnImage/workshop_test/")#C:/Users/DL9/Desktop/Machine Learning/Projet3A/Draw on image/


'''transforming our dataset into a pandaDataFrame'''

pdDataSet = pd.DataFrame(dataSet)#met sous forme de tableau a double entrée
pdUnlabelledData=pd.DataFrame(unknownSet)
print(pdDataSet)
'''test train split 25% 75%'''
#iloc:gets rows (or columns) at particular positions in the index
x_train,x_test,y_train,y_test=train_test_split(pdDataSet.iloc[:,[0,3]].values ,pdDataSet.iloc[:,[4]].values,test_size=0.25,random_state=0)

scaler = StandardScaler()
print('x_train::::::')
print(x_train)
print('x_test::::::')
print(x_test)
print('y_train::::::')
print(y_train)
print('y_test::::::')
print(y_test)
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

classifier=KNeighborsClassifier(n_neighbors=3,metric='minkowski',p=2)
classifier.fit(x_train,y_train)
''' testing our knn on the training data'''
y_pred=classifier.predict(x_test)


from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_pred) #la confusion_matrix permet de calculer l'erreur, mais il existe d'autre methode pour la calculer 



''' classifying unlabelled data from xml files'''
x_train=pdDataSet.iloc[:,[0,3]].values
y_train=pdDataSet.iloc[:,[4]].values

x_test=pdUnlabelledData.iloc[:,[0,3]].values



x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

classifier=KNeighborsClassifier(n_neighbors=3,metric='minkowski',p=2)
classifier.fit(x_train,y_train)
'''real classification'''
y_pred=classifier.predict(x_test)
'''rewriting the xml files after the classification of the unknown components'''
rewriteXml()