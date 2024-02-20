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
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.ar_model import AutoReg


def pseudo_iu(kuh,r1h,t,training_size):
    
    if t==0:
        iu=kuh/r1h
    else:
        iu=kuh[t+1:]/r1h
        
    #yo=id
    
    #tol2=0.1
    tol2=-10000
    iter0=0
    order=3
    
    # while 1:
    #     mod = AutoReg(iu,order)
        
    #     res=mod.fit()
    #     if t==0:
    #         iu_pred=res.predict(start=0,end=290)
    #     else:
    #         iu_pred=res.predict(start=0,end=289)
        
    #     fit_score=1-np.linalg.norm(iu-iu_pred)**2/np.linalg.norm(iu-mean(iu_pred))**2
        
    #     if fit_score>tol2:
    #         break
    #     else:
    #         print('Adjusted tolerance for AR model fitting not achieved.')
    #         print('Refining solution for time step '+str(t)+' order='+str(order))
            
    #     iter0=iter0+1
    #     if iter0>10:
    #         print('Goodness of fit is poor'+str(fit_score))
            
    mod = AutoReg(iu,order)
    
    res=mod.fit()
    if t==0:
        iu_pred=res.predict(start=0,end=training_size+2)
    else:
        iu_pred=res.predict(start=0,end=training_size+1)
    
    fit_score=1-np.linalg.norm(iu-iu_pred)**2/np.linalg.norm(iu-mean(iu_pred))**2
    
    
    if t==0:        
        iuh=res.predict(start=training_size,end=training_size)
    else:
        iuh=res.predict(start=training_size-1,end=training_size-1)
    kuh=np.append(kuh,r1h*iuh)
    


# mod = AutoReg(iu,1)
# res=mod.fit()
# Aa=res.predict()

# mod = AutoReg(housing, 3,)

# res = mod.fit()

# res = mod.fit(cov_type="HC0")
    
    return iuh,kuh















