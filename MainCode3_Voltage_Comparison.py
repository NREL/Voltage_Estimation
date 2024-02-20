# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 23:32:46 2021

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
import datetime
from datetime import datetime
import comparison_functions

MainDir = os.getcwd()

ResultsDir = os.path.join(MainDir,'Outputs','Results')

Feeder='test'

Result_est = pd.read_csv(os.path.join(ResultsDir,'Results_all_'+Feeder+'.csv'))
V_act_all = pd.read_csv(os.path.join(MainDir,'Inputs','InputData','Actual_V_'+Feeder+'.csv'))




result_xfmrs = comparison_functions.get_result_id(Result_est)


start_year='2019'
start_month='08'
start_day='02'

end_year='2019'
end_month='09'
end_day='30'

result_days=['8/25/2019 0:00',
 '8/12/2019 0:00',
 '9/5/2019 0:00',
 '9/30/2019 0:00']


error_all=[]

Error_write = pd.DataFrame(columns=['xfmr_id','error'])

error_limit=0.005

error_large=pd.DataFrame(columns=['xfmr_id','error'])
xfmr_error_large=0
v_mismatch_all=[]

for xfmr in range(0,len(result_xfmrs)):
#for xfmr in range(0,1):
    print(xfmr)
    print(datetime.now())
    
    v_result=comparison_functions.get_result_voltage(result_xfmrs,Result_est,result_days,xfmr)
    v_act=comparison_functions.get_result_voltage(result_xfmrs,V_act_all,result_days,xfmr)
    
    
    v_mismatch=abs(np.array(v_act)-np.array(v_result))/np.array(v_act)
    
    error_all.append(np.mean(v_mismatch))
    v_mismatch_all.append(v_mismatch)
    
    if error_all[xfmr]>0.02:
        
         error_large.loc[xfmr_error_large]=[result_xfmrs[xfmr]]+[error_all[xfmr]]
         xfmr_error_large=xfmr_error_large+1
        
    
    Error_write.loc[xfmr]=[result_xfmrs[xfmr]]+[error_all[xfmr]]
    
Error_write.to_csv(ResultsDir+'\\Error_all_'+Feeder+'.csv')    
error_large.to_csv(ResultsDir+'\\high_mismatch_loc_'+Feeder+'.csv')  

