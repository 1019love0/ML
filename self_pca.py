# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 10:34:26 2018

@author: fengzhenXu
"""
from numpy import *
import matplotlib.pyplot as plt
def loadDataSet(fileName,delim='\t'):
    fr=open(fileName)
    stringArr=[line.strip().split(delim) for line in fr.readlines()]
    datArr=[list(map(float,line)) for line in stringArr]
    return mat(datArr)
def pca(dataMat,topNfeat=9999999):
    meanVals=mean(dataMat,axis=0)
    meanRemoved=dataMat-meanVals
    covMat=cov(meanRemoved,rowvar=0)
    eigVals,eigVects=linalg.eig(mat(covMat))#一列组成一个特征向量
    #print(eigVals)
    #print(eigVects)
    eigValInd=argsort(eigVals)
    eigValInd=eigValInd[:-(topNfeat+1):-1] 
    #print(eigValInd)
    redEigVects=eigVects[:,eigValInd]
    #print(redEigVects)
    lowDDataMat=meanRemoved*redEigVects
    reconMat=(lowDDataMat*redEigVects.T)+meanVals
    return lowDDataMat,reconMat
d=loadDataSet('testSet.txt')
ldm,rm=pca(d,1)
#print(ldm)
#print(rm)
dataMat=loadDataSet('testSet.txt')
lowDMat,reconMat=pca(dataMat,1)
import matplotlib.pyplot as plt
fig=plt.figure()
plt.scatter(dataMat[:,0].flatten().tolist(),dataMat[:,1].flatten().tolist(),marker='^',s=90,c='turquoise',alpha=0.5)

plt.scatter(reconMat[:,0].flatten().tolist(),reconMat[:,1].flatten().tolist(),marker='o',s=50,c='yellow',alpha=0.5)
plt.show()

def replaceNanWithMean():
    datMat=loadDataSet('secom.data',' ')
    numFeat=shape(datMat)[1]
    for i in range(numFeat):
        print(type(datMat[:,i]))
        meanVal=mean(datMat[nonzero(~isnan(datMat[:,i]))[0],i])
        datMat[nonzero(isnan(datMat[:,i]))[0],i]=meanVal
    return datMat
dataMat=replaceNanWithMean()
meanVals=mean(dataMat,axis=0)
meanRemoved=dataMat-meanVals
covMat=cov(meanRemoved,rowvar=0)
eigVals,eigVects = linalg.eig(mat(covMat))
eigValInd = argsort(eigVals)            #sort, sort goes smallest to largest
eigValInd = eigValInd[:-(6+1):-1]
covMat=covMat[:,eigValInd]   
plt.plot(sort(sum(covMat,axis=0)).tolist())