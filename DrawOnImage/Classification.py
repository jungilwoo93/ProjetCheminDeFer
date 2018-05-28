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
         fileList.append(xmlFiles[x][39:])
    return fileList
    
def extractUnlabelledPaths(path):
    xmlFiles=glob.glob(path+"/*.xml")
    fileList=list()
    for x in range(0,len(xmlFiles)):
         fileList.append(xmlFiles[x][75:])
    return fileList
    



def feedList(tp,x,y,w,h): #type,point x, pointY, RectangleWidth,RectangleHeight
   
    if tp == "Paragraphe":
        dataSet.append([x,y,w,h,1])
        
    elif tp == "Titre":
         dataSet.append([x,y,w,h,2])
    
def feedUnlabelledList(tp,x,y,w,h,i):
   
    if tp == "unknown":
        unknownSet.append([x,y,w,h,i])

def extractUnlabelledData(path):
	fileNames=extractUnlabelledPaths(path)
	#file=root.iter('page/file')
	for x in range(0,len(fileNames)):#fileNames
		tree = ET.parse(path+''+fileNames[x])
		root = tree.getroot()
		file=root.iter('page/file')
		for component in root.iter('page/element'):
			feedUnlabelledList(component.attrib['type'],component.find('posX').text,component.find('posY').text,component.find('width').text,component.find('height').text,file[x])

def extractData(path):
    fileNames=extractPaths(path)
    for x in range(0,len(fileNames)):
        tree = ET.parse(path+''+fileNames[x])
        root = tree.getroot()
        for component in root.iter('page/element'):
            feedList(component.attrib['type'],component.find('posX').text,component.find('posY').text,component.find('width').text,component.find('height').text)

def rewriteXml():
   if len(unknownSet)!=0:
       
       for x in range(0,len(unknownSet)):
                tree = ET.parse('workshop_test/'+unknownSet[x][4])#C:/Users/DL9/Desktop/Machine Learning/Projet3A/Draw on image/
                root = tree.getroot()
                for component in root.iter('element'):
                    
                    if component.attrib['type'].text=="unknown":
                        #print(x)
                        if y_pred[x]==1:
                            component.attrib['type']="Paragraphe"
                        else:
                            component.attrib['type']="Titre"
                        tree.write('workshop_test/'+unknownSet[x][4])#C:/Users/DL9/Desktop/Machine Learning/Projet3A/Draw on image/
                        break
                        
                    

                  

extractData('XMLTrainingData/')#C:/Users/DL9/Desktop/

extractUnlabelledData("workshop_test/")#C:/Users/DL9/Desktop/Machine Learning/Projet3A/Draw on image/


'''transforming our dataset into a pandaDataFrame'''

pdDataSet = pd.DataFrame(dataSet)
pdUnlabelledData=pd.DataFrame(unknownSet)

'''test train split 25% 75%'''
#ajuster taille des array
x_train,x_test,y_train,y_test=train_test_split(pdDataSet.iloc[:,[0,3]].values ,pdDataSet.iloc[:,[4]].values,test_size=0.25,random_state=0)

scaler = StandardScaler()

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
