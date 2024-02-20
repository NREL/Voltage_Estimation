# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 18:30:34 2021

@author: jwang4
"""

from __future__ import division
import pandas as pd
import numpy as np
from numpy import *
import math
import json
import sys
import os
import scipy.io
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import cross_val_score
import pickle
import seaborn as sns


def Read_ML_model(V1,V2,L1,L2,L0,Data_len_L,xfmr_list,xfmr,MLmodelDir):
    
    filename = MLmodelDir+'\\'+str(xfmr_list[xfmr])+'.sav'

    Md = pickle.load(open(filename, 'rb'))

    V1_tes=V1
    V2_tes=V2
    P1_tes=L1
    P2_tes=L2

    
    Xdata=pd.DataFrame()
    Xdata['V1']=V1_tes
    Xdata['L1']=P1_tes
    Xdata['V2']=V2_tes
    Xdata['L2']=P2_tes

    
    V_pred_comb=zeros(Data_len_L)
    
    Xin=array(Xdata)
    
    for j in range(0,Data_len_L):
        V_pred_comb[j]=Md.predict([Xin[j]])
        
    print('Estimation finished for XFMR '+str(xfmr)+': '+str(xfmr_list[xfmr]))
        
    return V_pred_comb