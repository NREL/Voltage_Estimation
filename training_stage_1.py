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


def training_stage_1(x,V1,V2,I1,I2,n_tra,nt,circuit):
    
    #training_stage_1(x[:,i],V1_tra,V2_tra,I1_tra,I2_tra,n_tra,nt,circuit)
    
    r1=0
    r2=0
    r3=0
    kuhat=np.zeros(n_tra)
    vphat=np.zeros(n_tra)
    vhat1=np.zeros(n_tra)
    vhat2=np.zeros(n_tra)
    
    if circuit[0:-1]=='circuit1':
        r1=x[0]
        r2=x[1]
        
        for i in range(0,n_tra):
            vhat1[i]=V1[i]+r1*(I1[i]+I2[i])
            vhat2[i]=V2[i]+r1*(I1[i]+I2[i]+r2*I2[i])
            
    elif circuit[0:-1]=='circuit2':
        r1=x[0]
        r2=x[1]
        r3=x[2]
        
        for i in range(0,n_tra):
            vhat1[i]=V1[i]+r1*(I1[i]+I2[i])+r3*I1[i]
            vhat2[i]=V2[i]+r1*(I1[i]+I2[i])+r2*I2[i]
            
    elif circuit[0:-1]=='circuit3' or circuit[0:-1]=='circuit4' or circuit[0:-1]=='circuit5' or circuit[0:-1]=='circuit6' or circuit[0:-1]=='circuit7' or circuit[0:-1]=='SDGE':
        r1=x[0]
        r2=x[1]
        vphat=x[2:(2+n_tra)]
        kuhat=x[(2+n_tra):]
        
        for i in range(0,n_tra):
            vhat1[i]=nt*V1[i]+nt*(I1[i]+I2[i])*r1+nt*kuhat[i]
            vhat2[i]=nt*V2[i]+nt*(I1[i]+I2[i])*r1+nt*I2[i]*r2+nt*kuhat[i]
            
    else:
        
        r1=x[0]
        r2=x[1]
        vphat=x[2:(2+n_tra)]
        kuhat=x[(2+n_tra):]
        
        for i in range(0,n_tra):
            vhat1[i]=nt*V1[i]+nt*(I1[i]+I2[i])*r1+nt*kuhat[i]
            vhat2[i]=nt*V2[i]+nt*(I1[i]+I2[i])*r1+nt*I2[i]*r2+nt*kuhat[i]
        
    max_delta=abs(vhat1-vhat2).max(axis=0)

    
    return r1,r2,r3,kuhat,vphat,vhat1,vhat2,max_delta















