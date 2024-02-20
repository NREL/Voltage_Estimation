# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 16:16:44 2021

@author: jwang4
"""


from __future__ import division
import pandas as pd
import numpy as np
from numpy import *
import math
from ckt_fun import *
from training_stage_1 import *
from pseudo_iu import *
import lsqlin
from pymoo.model.problem import FunctionalProblem
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.model.population import Population
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from datetime import datetime
from pymoo.model.problem import Problem


global training_size,nt,V1_tra,V2_tra,I12_tra,I2_tra,lb,ub

def physics_based_estimation(V1,V2,L1,L2,L0,Data_len_V,Data_len_L,training_size,Base_kv):

    circuit='SDGE'
    #circuit='circuit7d'
    
    reporting_rate='5min'
    
    print('Start Physics-based method')
    print(datetime.now())
     
    Vc_ = V1
    Vf_ = V2
    Pc_ = L1
    Pf_ = L2
    
    training = range(0,training_size)
    

    V1_tra=Vc_[training];
    V2_tra=Vf_[training];
    P1_tra=Pc_[training];
    P2_tra=Pf_[training];
    
    I1_tra=[]
    I2_tra=[]
    for i in training:
        I1_tra.append(P1_tra[i]/V1_tra[i])
        I2_tra.append(P2_tra[i]/V2_tra[i])
    
    n_tra=len(I1_tra)
    
    I12_tra=array(I1_tra)+array(I2_tra)
    
    V1_tes=Vc_[training];
    V2_tes=Vf_[training];
    P1_tes=Pc_[training];
    P2_tes=Pf_[training];
    I1_tes=P1_tes/V1_tes
    I2_tes=P2_tes/V2_tes
    n_tes=len(I1_tes)
    
    nt=Base_kv*1000/sqrt(3)/240
    
    error=np.zeros((100,n_tra))
    error2=np.zeros((100,n_tes))
    vhat1=np.zeros((100,n_tra))
    vhat2=np.zeros((100,n_tra))
    
    #options=optimoptions('lsqlin','algorithm','interior-point','display','off','diagnostics','off');
    cte=2
    par1=1*pow(10,cte)
    tol1=100000#216 # Tolerance: Maximum of 216 volts apart (3% error)
    iter1=0
    
    
    #####
    
    while 1:
        lbp=np.linspace(1*pow(10,-cte),1e0,par1)
        ubp=np.linspace(1*pow(10,+cte),1e0,par1)
        
        
        C,d,lb,ub=ckt(circuit,V1_tra,V2_tra,I1_tra,I2_tra,n_tra,par1,lbp,ubp,nt,Base_kv)
        
        nx=len(C[0])
        x=np.zeros((nx,par1))
        r1=np.zeros(par1)
        r2=np.zeros(par1)
        r3=np.zeros(par1)
        vphat=np.zeros((n_tra,par1))
        kuhat=np.zeros((n_tra,par1))
        vhat1=np.zeros((n_tra,par1))
        vhat2=np.zeros((n_tra,par1))
        max_delta=np.zeros(par1)
        
        
    
        
        d2=d.astype(np.double)
        
        for i in range(0,par1):
    
            
            Res_mid=lsqlin.lsqlin(C, d2, 0, None, None, None, None,  lb[i], ub[i], None, {'show_progress': False})['x'].T   
            x[:,i] = np.squeeze(np.asarray(Res_mid))
    
        
        
            r1[i],r2[i],r3[i],kuhat[:,i],vphat[:,i],vhat1[:,i],vhat2[:,i],max_delta[i]=training_stage_1(x[:,i],V1_tra,V2_tra,I1_tra,I2_tra,n_tra,nt,circuit)
         
        M=max_delta.min()
        I=argmin(max_delta)
        
        if M<tol1:
            print('Adjusted tolerance for training data successfully achieved.')
            break
        else:
            print('Adjusted tolerance for training data successfully achieved.')
            break
        
            #cte=cte+1
            par1=1*pow(10,cte)
            
        iter1=iter1+1
        if iter1>4:
            print('Error!!!!! === Training unsuccessfull after 4 iterations. ===')
    
    #####
    
    print('lsqlin finished')
    print(datetime.now())
    
    V_pred_phy=vphat[:,I]
    

    return V_pred_phy













