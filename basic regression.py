# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 09:40:01 2018

@author: 1
"""
from numpy import *

def loadDataSet(fileName):      #general function to parse tab -delimited floats
    numFeat = len(open(fileName).readline().split('\t')) - 1 #get number of fields 
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def standRegres(xArr,yArr):
    xMat = mat(xArr); yMat = mat(yArr).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        print( "This matrix is singular, cannot do inverse")
        return
    ws = xTx.I * (xMat.T*yMat)
    return ws
if __name__=='__main__':
    xArr,yArr=loadDataSet('ex0.txt')
    print(xArr[:2])
    ws=standRegres(xArr,yArr)
    print(ws[:2])
    xMat=mat(xArr)
    yMat=mat(yArr)
    yHat=xMat*ws
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(xMat[:,1].flatten().A[0],yMat.T[:,0].flatten().A[0])
    #ax.scatter(xMat[:,1],yMat)
    xcopy=xMat.copy()
    xcopy.sort(0)
    yHat=xcopy*ws
    ax.plot(xcopy[:,1],yHat)
    plt.show()
    print(corrcoef(yHat.T,yMat))