# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 15:23:19 2021

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
import physics_based_method
import Get_ML_model_code
import Read_ML_model

MainDir = os.getcwd()
InputsDir = os.path.join(MainDir,'Inputs','InputData')
MLmodelDir = os.path.join(MainDir,'ML_models')
ResultsDir = os.path.join(MainDir,'Outputs','Results')

Feeder='test'

Base_kv=12

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
Phy_training_size=500
ML_training_size=500

# Ami_V_Name=dfAMI_V['Name'].tolist()
# Ami_P_Name=dfAMI_P['ID_MTR_KEY'].tolist()

xfmr_list,xfmr_ami = data_functions.AMI_xfmr_mapping(dfAMI_xfmr)

xfmr=0
Datafullrecord=[]
Model_Record=pd.DataFrame(columns=['Name','AMI1','AMI2','DataFull','MLModel','Ami_loc_change'])
#Model_Record=pd.read_csv(MLmodelDir+'\\Model_Record_'+Feeder+'.csv',index_col=0)
for xfmr in range(0,len(xfmr_list)):
#for xfmr in range(0,20): #20 to 60 is running #60 to 100 is running #100 to 120 is running #120 to 180 is running #180 to 200 is running #200 to 240 is running #240 to 260 is running
    print(xfmr)
    print(len(xfmr_list))
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
        
        Ami_loc_change=0
        
        if Data_full_flag==1:
            
            Ami1_V,Ami2_V,Ami1_L,Ami2_L,Ami_loc_change=data_functions.Process_all_data(Meter_V_len_ami1,Meter_V_len_ami2,Meter_L_len_ami1,Meter_L_len_ami2)
            
            V1,V2,L1,L2,L0=data_functions.Get_input_data(Ami1_V,Ami2_V,Ami1_L,Ami2_L,Meter_L_len_xfmr,Data_len_V,Data_len_L)
            
            V_pred_phy=physics_based_method.physics_based_estimation(V1,V2,L1,L2,L0,Data_len_V,Data_len_L,Phy_training_size,Base_kv)
            
            Get_ML_model_code.Get_ML_model(V_pred_phy,V1,V2,L1,L2,L0,Data_len_V,Data_len_L,Phy_training_size,ML_training_size,xfmr_list,xfmr,MLmodelDir,Base_kv)
            
            # V_pred=Read_ML_model.Read_ML_model(V1,V2,L1,L2,L0,Data_len_L,xfmr_list,xfmr,MLmodelDir)
            
    else:
        
        Data_full_flag=0
        ami1=0
        ami2=0
        Ami_loc_change=0
        Datafullrecord.append(Data_full_flag)
        print('Data not full for transformer '+str(xfmr))
        
        
    Model_Record.loc[xfmr]=[xfmr_list[xfmr]]+[str(ami1)]+[str(ami2)]+[str(Data_full_flag)]+[str(Data_full_flag)]+[str(Ami_loc_change)]
    
Model_Record.to_csv(MLmodelDir+'\\Model_Record_'+Feeder+'.csv')
        
                      
        





 