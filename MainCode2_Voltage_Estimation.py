# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 18:43:02 2021

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
from datetime import date
import data_functions
import Read_ML_model

MainDir = os.getcwd()
InputsDir = os.path.join(MainDir,'Inputs','InputData')
MLmodelDir = os.path.join(MainDir,'ML_models')
ResultsDir = os.path.join(MainDir,'Outputs','Results')


Feeder='test'


print('A')
print(datetime.now())
dfAMI_xfmr = pd.read_csv(os.path.join(InputsDir,'Meter_XFMR_'+Feeder+'.csv'))
print('B')
print(datetime.now())
dfAMI_V = pd.read_csv(os.path.join(InputsDir,'AMI_V_'+Feeder+'.csv'))
print('C')
print(datetime.now())
dfAMI_P = pd.read_csv(os.path.join(InputsDir,'AMI_L_'+Feeder+'.csv'))
print('D')
print(datetime.now())
dfXFMR_Pagg = pd.read_csv(os.path.join(InputsDir,'XFMR_L_'+Feeder+'.csv'),low_memory=False)
print('E')
print(datetime.now())

start_year='2019'
start_month='08'
start_day='02'

end_year='2019'
end_month='09'
end_day='30'


V_t1=start_year+'-'+start_month+'-'+start_day+'T00:00:00'
V_t2=end_year+'-'+end_month+'-'+end_day+'T23:55:00'

# L_t1=start_year+'-'+start_month+'-'+start_day+' 00:00:00'
# L_t2=end_year+'-'+end_month+'-'+end_day+' 00:00:00'
L_t1=str(int(start_month))+'/'+str(int(start_day))+'/'+str(int(start_year))+' 0:00'
L_t2=str(int(end_month))+'/'+str(int(end_day))+'/'+str(int(end_year))+' 0:00'

start_date = date(int(start_year), int(start_month), int(start_day))
end_date = date(int(end_year), int(end_month), int(end_day))
day_length =  (end_date-start_date).days+1


Data_len_V=day_length*288
Data_len_L=day_length*24

xfmr_list,xfmr_ami = data_functions.AMI_xfmr_mapping(dfAMI_xfmr)

xfmr=0
Datafullrecord=[]

dfResults = pd.DataFrame(columns=['xfmr_id','day','hour','value'])


for xfmr in range(0,len(xfmr_list)):
#for xfmr in range(0,20):
    print(xfmr)
    print(datetime.now())

    if len(xfmr_ami[xfmr])>1:    
        #Get location of meter data
        V_loc,L_loc=data_functions.Get_Ami_loc(dfAMI_V,dfAMI_P,xfmr_ami,xfmr)
        #Get AMI number for service transformer
        ami1,ami2,ami1_V_loc,ami2_V_loc,ami1_L_loc,ami2_L_loc=data_functions.Get_Ami_loc_num(V_loc,L_loc,xfmr_ami,xfmr)
        #Get all AMI voltage data
        Meter_V_ami1,Meter_V_ami2=data_functions.Get_Ami_meter_V_data(dfAMI_V,ami1_V_loc,ami2_V_loc)
        #Get all AMI load data
        Meter_L_ami1,Meter_L_ami2=data_functions.Get_Ami_meter_L_data(dfAMI_P,ami1_L_loc,ami2_L_loc)
        #Get AMI votlage data for selected duration
        Meter_V_len_ami1,Meter_V_len_ami2=data_functions.Get_Ami_meter_len_V_data(Data_len_V,V_t1,V_t2,Meter_V_ami1,Meter_V_ami2)
        #Get AMI load data for selected duration
        Meter_L_len_ami1,Meter_L_len_ami2=data_functions.Get_Ami_meter_len_L_data(Data_len_L,L_t1,L_t2,Meter_L_ami1,Meter_L_ami2)
        #Get all transformer load data
        Meter_L_xfmr=data_functions.Get_XFMR_L_data(dfXFMR_Pagg,xfmr_list,xfmr,Feeder)
        #Get transformer load data for selected duration
        Meter_L_len_xfmr=data_functions.Get_XFMR_L_len_data(Data_len_L,L_t1,L_t2,Meter_L_xfmr,xfmr)
        #Check if this transformer has all date required for the algorithm
        Data_full_flag=data_functions.Get_data_full_flag(Meter_V_len_ami1,Meter_V_len_ami2,Meter_L_len_ami1,Meter_L_len_ami2,Meter_L_len_xfmr,Data_len_V,Data_len_L,xfmr)
        
        Datafullrecord.append(Data_full_flag)
        
        if Data_full_flag==1:
            
            dfxfmr = pd.DataFrame(columns=['xfmr_id','day','hour','value'])
            
            Ami1_V,Ami2_V,Ami1_L,Ami2_L,Ami_loc_change=data_functions.Process_all_data(Meter_V_len_ami1,Meter_V_len_ami2,Meter_L_len_ami1,Meter_L_len_ami2)
            
            V1,V2,L1,L2,L0=data_functions.Get_input_data(Ami1_V,Ami2_V,Ami1_L,Ami2_L,Meter_L_len_xfmr,Data_len_V,Data_len_L)
            
            V_pred=Read_ML_model.Read_ML_model(V1,V2,L1,L2,L0,Data_len_L,xfmr_list,xfmr,MLmodelDir)
            
            dfxfmr['xfmr_id'] = [xfmr_list[xfmr]]*Data_len_L             
            dfxfmr['day'] = Meter_L_len_ami1['Day']
            dfxfmr['hour'] = Meter_L_len_ami1['Hour']
            dfxfmr['value'] = V_pred
            
            dfResults = dfResults.append(dfxfmr, ignore_index = True)
            
    else:
        
        print('Data not full for transformer '+str(xfmr))
        
        #pd.DataFrame(V_pred).to_csv(ResultsDir+'\\'+xfmr_list[xfmr]+'.csv')
        
dfResults.to_csv(ResultsDir+'\\Results_all_'+Feeder+'.csv')