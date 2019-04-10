# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 09:04:36 2018

@author: 1
"""
import numpy as np
def loadDataSet(fileName):
    numFeat=len(open(fileName).readline().split('\t'))-1
    dataMat=[];labelMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        lineArr=[]
        curLine=line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        if float(curLine[-1])==0.0:
            curLine[-1]=-1.0
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat
data,label=loadDataSet('horseColicTraining.txt')



def perceptron(data,label,yita=0.1):
    data=np.mat(data)
    b=0.0
    w=np.zeros((np.shape(data)[1],1))
    for i in range(np.shape(data)[0]):
        res=np.matmul(data[i],w)+b
        if res>0:
            res=1.0
        else:
            res=-1.0
        if res!=label[i]:
            w+=yita*label[i]*np.transpose(data[i])
            b+=yita*label[i]
            
    return w,b
             
w0,b0=perceptron(data,label,yita=0.1)  
testdata,testlabel=loadDataSet('horseColicTest.txt')
def test_perceptron_accuracy(data,label,w,b):
     acc=0.0
     for i in range(np.shape(data)[0]):
        res=np.matmul(data[i],w)+b
        if res>0:
            res=1.0
        else:
            res=-1.0
        if res==label[i]:
            acc+=1.0
     return acc/(float(np.shape(data)[0]))

acc=test_perceptron_accuracy(testdata,testlabel,w0,b0)
print('accuracy is %.2f%%'%(acc*100))