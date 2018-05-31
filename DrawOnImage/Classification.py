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
import os



def classif(nameProjet):
	dataSet=[] #training dataset
	unknownSet=[]
	#nameProjet='Batch'
	print(nameProjet)
	
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
			#fileList.append(xmlFiles[x][28:])#28:nombre de caractere du chemin
			fileList.append(splitPath(xmlFiles[x]))
		return fileList
    
	def extractUnlabelledPaths(path):
		xmlFiles=glob.glob(path+"/*.xml")
		fileList=list()
		for x in range(0,len(xmlFiles)):
			#fileList.append(xmlFiles[x][26:])#75:nbr de car
			fileList.append(splitPath(xmlFiles[x]))
		return fileList
    
	def splitPath(path):
		(filePath,tempfileName) = os.path.split(path)
		(shotName,extension) = os.path.splitext(tempfileName)
		return shotName + '.xml'


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
		for x in range(0,len(fileNames)):#fileNames
			tree = ET.parse(path+''+fileNames[x])
			root = tree.getroot()
			file=root.attrib['id']
			for component in root.iter('page'):
				for elem in component.iter('element'):
					feedUnlabelledList(elem.attrib['type'],elem.find('posX').text,elem.find('posY').text,elem.find('width').text,elem.find('height').text,file)

	def extractData(path):
		fileNames=extractPaths(path)
		for x in range(0,len(fileNames)):
			if fileNames[x]==nameProjet + '.xml' :
				tree = ET.parse(path+''+fileNames[x])
				print(path+''+fileNames[x])
				root = tree.getroot()
				for component in root.iter('page'):
					for elem in component.iter('element'):
						feedList(elem.attrib['type'],elem.find('posX').text,elem.find('posY').text,elem.find('width').text,elem.find('height').text)

	def rewriteXml():
		if len(unknownSet)!=0:
			for x in range(0,len(unknownSet)):
				tree = ET.parse('DrawOnImage/workshop_test/'+ nameProjet +'/'+unknownSet[x][4] + '-Unlabelled.xml')#C:/Users/DL9/Desktop/Machine Learning/Projet3A/Draw on image/
				root = tree.getroot()
				for component in root.iter('page'):
					for elem in component.iter('element'):
						if elem.attrib['type']=="unknown":
							if y_pred[x]==1:
								elem.attrib['type']="Paragraphe"
							else:
								elem.attrib['type']="Titre"
							tree.write('DrawOnImage/workshop_test/'+ nameProjet +'/'+unknownSet[x][4] + '-Unlabelled.xml')#C:/Users/DL9/Desktop/Machine Learning/Projet3A/Draw on image/
							break





	extractData('DrawOnImage/XMLTrainingData/')#C:/Users/DL9/Desktop/

	extractUnlabelledData("DrawOnImage/workshop_test/"+ nameProjet +'/')##C:/Users/DL9/Desktop/Machine Learning/Projet3A/Draw on image/


	'''transforming our dataset into a pandaDataFrame'''

	pdDataSet = pd.DataFrame(dataSet)#met sous forme de tableau a double entrée
	print('le unknownSet')
	print(unknownSet)
	pdUnlabelledData=pd.DataFrame(unknownSet)
	'''test train split 25% 75%'''
	#iloc:gets rows (or columns) at particular positions in the index
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