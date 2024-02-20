# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 00:47:17 2020

@author: jwang4
"""


from __future__ import division
import pandas as pd
import numpy as np
from numpy import *
import os
import matplotlib.pyplot as plt


def ckt(circuit,V1,V2,I1,I2,nm,nb,lbp,ubp,nt,Base_kv):
    
    if circuit=='circuit1':
        
        C,d,lb,ub = circuit1(V1,V2,I1,I2,nm,nb,lbp,ubp)
        
    elif circuit=='circuit2':
        
        C,d,lb,ub = circuit2(V1,V2,I1,I2,nm,nb,lbp,ubp)
        
    else:
        
        C,d,lb,ub = circuitX(V1,V2,I1,I2,nm,nb,lbp,ubp,nt,Base_kv)
        
    return C,d,lb,ub 


def circuit1(V1,V2,I1,I2,nm,nb,lbp,ubp):
    
    d=np.concatenate((V1,V2,V1-V2))
    
    c_m1=np.concatenate((-(array(I1)+array(I2)),-(array(I1)+array(I2)),np.zeros(nm)))
    c_m2=np.concatenate((np.zeros(nm),-array(I2),array(I2)))
    c_m3=np.concatenate((np.diag(np.ones(nm)),np.diag(np.ones(nm)),np.diag(np.zeros(nm))))
    c=np.concatenate((c_m1.reshape(-1,1),c_m2.reshape(-1,1),c_m3),axis=1)
    
    np_2=2
    
    lb=zeros((nb,np_2+nm))
    ub=zeros((nb,np_2+nm))
    
    for i in range(0,nb):
        lb[i]=np.concatenate((lbp[i]*np.ones(np_2),0.95*V1))
        ub[i]=np.concatenate((ubp[i]*np.ones(np_2),1.05*V1))
        
    return c,d,lb,ub

def circuit2(V1,V2,I1,I2,nm,nb,lbp,ubp):
    
    d=np.concatenate((V1,V2,V1-V2))
    
    c_m1=np.concatenate((-(array(I1)+array(I2)),-(array(I1)+array(I2)),np.zeros(nm)))
    c_m2=np.concatenate((np.zeros(nm),-array(I2),array(I2)))
    c_m3=np.concatenate((-array(I1),np.zeros(nm),array(I1)))
    c_m4=np.concatenate((np.diag(np.ones(nm)),np.diag(np.ones(nm)),np.diag(np.zeros(nm))))
    c=np.concatenate((c_m1.reshape(-1,1),c_m2.reshape(-1,1),c_m3.reshape(-1,1),c_m4),axis=1)
    
    np_2=3
    
    lb=zeros((nb,np_2+nm))
    ub=zeros((nb,np_2+nm))
    
    for i in range(0,nb):
        lb[i]=np.concatenate((lbp[i]*np.ones(np_2),0.95*V1))
        ub[i]=np.concatenate((ubp[i]*np.ones(np_2),1.05*V1))

    return c,d,lb,ub

def circuitX(V1,V2,I1,I2,nm,nb,lbp,ubp,nt,Base_kv):
    
    d=np.concatenate((V1,V2,V1-V2))
    
    c_m1=np.concatenate((-(array(I1)+array(I2)),-(array(I1)+array(I2)),np.zeros(nm)))
    c_m2=np.concatenate((np.zeros(nm),-array(I2),array(I2)))
    c_m3=np.concatenate(((1/nt)*np.diag(np.ones(nm)),(1/nt)*np.diag(np.ones(nm)),np.diag(np.zeros(nm))))
    c_m4=np.concatenate((-np.diag(np.ones(nm)),-np.diag(np.ones(nm)),np.diag(np.zeros(nm))))
    c=np.concatenate((c_m1.reshape(-1,1),c_m2.reshape(-1,1),c_m3,c_m4),axis=1)
    
    np_2=2
    
    lb=zeros((nb,np_2+nm+nm))
    ub=zeros((nb,np_2+nm+nm))
    
    for i in range(0,nb):
        lb[i]=np.concatenate((lbp[i]*np.ones(np_2),0.95*Base_kv*1000/sqrt(3)*np.ones(nm),0.001*240*np.ones(nm)))
        ub[i]=np.concatenate((ubp[i]*np.ones(np_2),1.05*Base_kv*1000/sqrt(3)*np.ones(nm),0.05*240*np.ones(nm)))

    return c,d,lb,ub        












