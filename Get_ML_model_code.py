# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 18:07:46 2021

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


def Get_ML_model(V_pred_phy,V1,V2,L1,L2,L0,Data_len_V,Data_len_L,training_size,Train_length,xfmr_list,xfmr,MLmodelDir,Base_kv):

    Vc_ = V1
    Vf_ = V2
    Pc_ = L1
    Pf_ = L2
    
    V1_tes=Vc_[0:training_size]
    V2_tes=Vf_[0:training_size]
    P1_tes=Pc_[0:training_size]
    P2_tes=Pf_[0:training_size]
    
    V_pred_phy_2=V_pred_phy
    
    
    V_drop_sec=mean(abs(V1_tes[0:Train_length]-V2_tes[0:Train_length]))
    
    V_drop_tran=mean(abs(V_pred_phy_2[0:Train_length]*240/(Base_kv*1000/sqrt(3))-V1_tes[0:Train_length]))
    
    L1_total=sum(abs(L1[0:Train_length]))
    L2_total=sum(abs(L2[0:Train_length]))
    L0_total=sum(abs(L0[0:Train_length]))
    
    # V_drop_factor=10
    V_drop_factor=4+16*L1_total/L0_total
    
    
    if V_drop_tran>V_drop_factor*V_drop_sec:
        V_drop_comp=V_drop_tran-V_drop_factor*V_drop_sec
    else:
        V_drop_comp=0
    
    
    Xdata=pd.DataFrame()
    Xdata['V1']=V1_tes
    Xdata['L1']=P1_tes
    Xdata['V2']=V2_tes
    Xdata['L2']=P2_tes
    
    Ydata=pd.DataFrame()
    Ydata['V0']=V_pred_phy_2-V_drop_comp*Base_kv*1000/sqrt(3)/240
    
    Xin=array(Xdata)
    Yout=array(Ydata)
    
    regr = RandomForestRegressor(max_depth=10, random_state=0, n_estimators=100)
    
    
    regr.fit(Xin[0:Train_length], Yout[0:Train_length].ravel())
    filename = MLmodelDir+'\\'+str(xfmr_list[xfmr])+'.sav'
    pickle.dump(regr, open(filename, 'wb'))
    print('Model finished for XFMR '+str(xfmr)+': '+str(xfmr_list[xfmr]))