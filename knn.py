# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 09:54:53 2018

@author: 1
"""
from numpy import *
from matplotlib import cm
import operator
from os import listdir
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签  
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号  
'''显示数据图
ax=[];ay=[];bx=[];by=[]
for label in range(len(l)):
    if l[label]=='A':
        ax.append(g[label,0])
        ay.append(g[label,1])
    else:
         bx.append(g[label,0])
         by.append(g[label,1])
plt.scatter(ax,ay,color='red',label='A')
plt.scatter(bx,by,color='yellow',label='B')
plt.legend()
'''
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet#tile（a,b）作用，重复a,b次
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()     
    classCount={}          
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return   
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector

#print(datingDataMat[:5],datingLabels[:5])
'''数据3d图
fig = plt.figure(); ax = Axes3D(fig)
X, Y, Z =datingDataMat[:, 0], datingDataMat[:, 1], datingDataMat[:, 2]
for x, y, z, s in zip(X, Y, Z, datingLabels):
    c = cm.rainbow(int(255*s/9)); ax.text(x, y, z, s, backgroundcolor=c)
ax.set_xlim(X.min(), X.max()); ax.set_ylim(Y.min(), Y.max()); ax.set_zlim(Z.min(), Z.max())
plt.show()'''
'''
显示三类人
ax=[];ay=[];bx=[];by=[];cx=[];cy=[];
for i in range(len(datingLabels)):
    if datingLabels[i]==1:
        ax.append(datingDataMat[i,0])
        ay.append(datingDataMat[i,1])
    elif datingLabels[i]==2:
        bx.append(datingDataMat[i,0])
        by.append(datingDataMat[i,1])
    else:
        cx.append(datingDataMat[i,0])
        cy.append(datingDataMat[i,1])
#plt.scatter(datingDataMat[:, 1], datingDataMat[:, 2],color='cyan',alpha=0.5)
plt.figure()
plt.scatter(ax,ay,c='chartreuse',alpha=0.5,label=u'不喜欢')
plt.scatter(bx,by,c='r',alpha=0.5,label=u'魅力一般')
plt.scatter(cx,cy,c='m',alpha=0.5,label=u'极具魅力')
plt.xlabel(u'玩视频游戏所占的时间比',fontsize=15)
plt.ylabel(u'玩视频游戏所占的时间比',fontsize=15)
plt.legend()
plt.show()'''
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))   #element wise divide
    return normDataSet, ranges, minVals
def datingClassTest():
    hoRatio = 0.10      #hold out 10%
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       #load data setfrom file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print( "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print ("the total error rate is: %f" % (errorCount/float(numTestVecs)))
    print (errorCount)
#datingClassTest()
#datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
#normMat,ranges,minVals=autoNorm(datingDataMat)
#print(normMat[:5],ranges,minVals)
def classifyPerson():
    resultList=['not at all','in small dosses','in large doses']
    percentTats=float(input('percent of time spent playing video games?'))
    ffMiles=float(input('frequent flier miles earned per year?'))
    iceCream=float(input('liters of ice cream consumed per year?'))
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResults=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print('you will probably like this person : %s'%resultList[classifierResults-1])
classifyPerson()