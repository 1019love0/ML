# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 19:18:54 2018

@author: fengzhenXu
"""
from numpy import *
import numpy.linalg as la
U,Sigma,VT=linalg.svd([[1,1],[7,7]])
#print(U)
#print(Sigma)
#print(VT)
import svdRec
data=svdRec.loadData()
U,Sigma,VT=linalg.svd(data)
#print(U)
#print(Sigma)
#print(VT)
Sig3=mat([[Sigma[0],0,0],[0,Sigma[1],0],[0,0,Sigma[2]]])
#print(U[:,:3]*Sig3*VT[:3,:])

def euclidSim(inA,inB):
    return 1.0/(1.0+la.norm(inA-inB))
def pearsSim(inA,inB):
    if len(inA)<3:return 1.0
    return 0.5+0.5*corrcoef(inA,inB,rowvar=0)[0][1]
def cosSim(inA,inB):
    num=float(inA.T*inB)
    denom=la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)
#data=mat(data)
#print(cosSim(data[:,1],data[:,1]))
def standEst(dataMat,user,simMeas,item):
    n=shape(dataMat)[1]
    simTotal=0.0;ratSimTotal=0.0
    for j in range(n):
        userRating=dataMat[user,j]
        if userRating==0:continue
        overlap=nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]
        if len(overlap)==0:similarity=0
        else:similarity=simMeas(dataMat[overlap,item],dataMat[overlap,j])
        simTotal+=similarity
        ratSimTotal+=similarity*userRating
    if simTotal==0:return 0
    else:return ratSimTotal/simTotal 
def recommend(dataMat,user,N=3,simMeas=cosSim,estMethod=standEst):
    unratedItems=nonzero(dataMat[user,:]==0)[1]
    if len(unratedItems)==0:return "you rated everthing"
    itemScores=[]
    for item in unratedItems:
        estimatedScore=estMethod(dataMat,user,simMeas,item)
        itemScores.append((item,estimatedScore))
    return sorted(itemScores,key=lambda jj :jj[1],reverse=True)[:N]

'''
Data=mat(svdRec.loadExData2())
Data[0,1]=Data[0,0]=Data[1,0]=Data[2,0]=4
Data[3,3]=2
print(recommend(Data,5,simMeas=euclidSim))
U,Sigma,VT=la.svd(mat(svdRec.loadExData2()))
Sig2=Sigma**2''

print(sum(Sig2)*0.9)
print(sum(Sig2[:3]))'''
def svdEst(dataMat, user, simMeas, item):
    n = shape(dataMat)[1]
    print(shape(dataMat))
    simTotal = 0.0; ratSimTotal = 0.0
    U,Sigma,VT = la.svd(dataMat)
    Sig4 = mat(eye(4)*Sigma[:4]) #arrange Sig4 into a diagonal matrix
    xformedItems = dataMat.T * U[:,:4] * Sig4.I #create transformed items
    print(shape(xformedItems))
    for j in range(n):
        userRating = dataMat[user,j]
        if userRating == 0 or j==item: continue
        similarity = simMeas(xformedItems[item,:].T,\
                             xformedItems[j,:].T)
        #print 'the %d and %d similarity is: %f' % (item, j, similarity)
        simTotal += similarity
        ratSimTotal += similarity * userRating
    if simTotal == 0: return 0
    else: return ratSimTotal/simTotal
data=svdRec.loadExData2()
data=mat(data)
print(recommend(data,1,estMethod=svdEst))
def printMat(inMat, thresh=0.8):
    for i in range(32):
        for k in range(32):
            if float(inMat[i,k]) > thresh:
                print( 1,)
            else: print (0,)
        print ('')

def imgCompress(numSV=3, thresh=0.8):
    myl = []
    for line in open('0_5.txt').readlines():
        newRow = []
        for i in range(32):
            newRow.append(int(line[i]))
        myl.append(newRow)
    myMat = mat(myl)
    print ("****original matrix******")
    printMat(myMat, thresh)
    U,Sigma,VT = la.svd(myMat)
    SigRecon = mat(zeros((numSV, numSV)))
    for k in range(numSV):#construct diagonal matrix from vector
        SigRecon[k,k] = Sigma[k]
    reconMat = U[:,:numSV]*SigRecon*VT[:numSV,:]
    print ("****reconstructed matrix using %d singular values******" % numSV)
    printMat(reconMat, thresh)
imgCompress(2)










































