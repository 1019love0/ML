# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 08:45:30 2018

@author: fengzhenXu
"""
from numpy import *
def loadDataSet(fileName):
    dataMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        curLine=line.strip().split('\t')
        fltLine=list(map(float,curLine))
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA,vecB):
    return sqrt(sum(power(vecA-vecB,2)))

def randCent(dataSet,k):
    n=shape(dataSet)[1]
    centroids=mat(zeros((k,n)))
    for j in range(n):
        minJ=min(dataSet[:,j])
        rangeJ=float(max(dataSet[:,j])-minJ)
        centroids[:,j]=mat(minJ+rangeJ*random.rand(k,1))
    return centroids

def kMeans(dataSet,k,distMeas=distEclud,createCent=randCent):
    m=shape(dataSet)[0]
    clusterAssment=mat(zeros((m,2)))
    
    centroids=createCent(dataSet,k)
    clusterChanged=True
    while clusterChanged:
        clusterChanged=False
        for i in range(m):
            minDist=inf;minIndex=-1
            for j in range(k):
                distJI=distMeas(centroids[j,:],dataSet[i,:])
                if distJI<minDist:
                    minDist=distJI;minIndex=j
            if clusterAssment[i,0] != minIndex:clusterChanged=True
            clusterAssment[i,:]=minIndex,minDist**2
        #print(centroids)
        for cent in range(k):
            ptsInClust=dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:]=mean(ptsInClust,axis=0)
    return centroids,clusterAssment
dat=mat(loadDataSet('testSet2.txt'))
#c,clu=kMeans(dat,4)
#print(type(c))
import matplotlib.pyplot as plt
def plotSca(dataSet,clusterAssment,centroids):
    n_c=shape(centroids)[0]
    m=shape(dataSet)[0]
    ccx=[];ccy=[]
    for i in range(n_c):
        ccx.append(centroids[i,0])
        ccy.append(centroids[i,1])
    ax=[];ay=[];bx=[];by=[];cx=[];cy=[];dx=[];dy=[]       
    for i in range(m):
        for j in range(n_c):
            if clusterAssment[i,0]==1.0:
               ax.append(dataSet[i,0])
               ay.append(dataSet[i,1])
            elif clusterAssment[i,0]==2.0:
                bx.append(dataSet[i,0])
                by.append(dataSet[i,1])
            elif clusterAssment[i,0]==3.0:
                cx.append(dataSet[i,0])
                cy.append(dataSet[i,1])
            else:
                dx.append(dataSet[i,0])
                dy.append(dataSet[i,1])
    
    plt.figure()
    plt.scatter(ax,ay,marker='v',color='deeppink')
    plt.scatter(bx,by,marker='^',color='darkviolet')
    plt.scatter(cx,cy,marker='s',color='cyan')
    plt.scatter(dx,dy,marker='*',color='lawngreen')
    plt.scatter(ccx,ccy,marker='+',color='red',s=100)
    plt.show()    
#plotSca(dat,clu,c)    
def biKmeans(dataSet,k,distMeas=distEclud):
    m=shape(dataSet)[0]
    clusterAssment=mat(zeros((m,2)))
    centroid0=mean(dataSet,axis=0).tolist()[0]
    centList=[centroid0]
    for j in range(m):
        clusterAssment[j,1]=distMeas(mat(centroid0),dataSet[j,:])**2
    while (len(centList) < k):
        lowestSSE=inf
        for i in range(len(centList)):
            ptsInCurrCluster=dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]
            centroidMat,splitClustAss=kMeans(ptsInCurrCluster,2,distMeas)
            sseSplit=sum(splitClustAss[:,1])
            sseNotSplit=sum(clusterAssment[nonzero(clusterAssment[:,0].A !=i)[0],1])
            print("sseSplit, and notSplit:",sseSplit,sseNotSplit)
            if (sseSplit+sseNotSplit) < lowestSSE:
                bestCentToSplit=i
                bestNewCents=centroidMat
                bestClustAss=splitClustAss.copy()
                lowestSSE=sseSplit+sseNotSplit
        bestClustAss[nonzero(bestClustAss[:,0].A==1)[0],0]=len(centList)
        bestClustAss[nonzero(bestClustAss[:,0].A==0)[0],0]=bestCentToSplit
        print('the bestCentToSplit is :',bestCentToSplit)
        print('the len of bestClustAss is :',len(bestClustAss))
        centList[bestCentToSplit]=bestNewCents[0,:].tolist()[0]
        centList.append(bestNewCents[1,:].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A==bestCentToSplit)[0],:]=bestClustAss
    return mat(centList),clusterAssment
c,ca=biKmeans(dat,3)
print(c)
plotSca(dat,ca,c)            
            
import urllib.request
import urllib.parse
import json
from time import sleep
def geoGrab(stAddress,city):
    apiStem='http://where.yahooapis.com/geocode?'
    params={}
    params['flags']='J'
    params['appid']='aaa0VN6K'
    params['location']='%s %s'%(stAddress,city)
    url_params=urllib.parse.urlencode(params)
    yahooApi=apiStem+url_params
    print(yahooApi)
    c=urllib.request.urlopen(yahooApi)
    return json.loads(c.read())         

def massPlaceFind(fileName):
    fw=open('place.txt','w')
    for line in open(fileName).readlines():
        lineArr=line.strip().split('\t')
        retDict=geoGrab(lineArr[1],lineArr[2])
        if retDict['ResultSet']['Error']==0:
            lat=float(retDict['ResultSet']['Results'][0]['latitude'])
            lng=float(retDict['ResultSet']['Result'][0]['longitude'])
            print("%s\t%f\t%f"%(lineArr[0],lat,lng))
            fw.write('%s\t%f\t%f\n'%(line,lat,lng))
        else:print('error fetching')
        sleep(1)
    fw.close()

def distSLC(vecA,vecB):
    a=sin(vecA[0,1]*pi/180) * sin(vecB[0,1]*pi/180)
    b=cos(vecA[0,1]*pi/180) * cos(vecB[0,1]*pi/180)*cos(pi * (vecB[0,0]-vecA[0,0])/180)
    return arccos(a+b)*6371.0


import matplotlib
def clusterClubs(numClust=None):
    datList=[]
    for line in open('places.txt').readlines():
        lineArr=line.split('\t')
        datList.append([float(lineArr[4]),float(lineArr[3])])
    datMat=mat(datList)
    myCentroids,clustAssing=biKmeans(datMat,numClust,distMeas=distSLC)
    fig=plt.figure()
    rect=[0.1,0.1,0.8,0.8]
    scatterMarkers=['s','o','^','8','p','d','v','h','>','<']
    axprops=dict(xticks=[],yticks=[])
    imgP=plt.imread('Portland.png')
    ax0=fig.add_axes(rect,label='ax0',**axprops)
    ax0.imshow(imgP)
    ax1=fig.add_axes(rect,label='ax1',frameon=False)
    for i in range(numClust):
       ptsInCurrCluster = datMat[nonzero(clustAssing[:,0].A==i)[0],:]
       markerStyle = scatterMarkers[i % len(scatterMarkers)]
       ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0], ptsInCurrCluster[:,1].flatten().A[0], marker=markerStyle, s=90)
    ax1.scatter(myCentroids[:,0].flatten().A[0], myCentroids[:,1].flatten().A[0], marker='+', s=300)
    plt.show()
clusterClubs(4)
 





























            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    