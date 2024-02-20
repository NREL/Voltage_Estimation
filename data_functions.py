# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 19:04:21 2021

@author: jwang4
"""


from __future__ import division
import pandas as pd
import datetime
import numpy as np


def AMI_xfmr_mapping(dfAMI_xfmr):    
    xfmr_ls = dfAMI_xfmr["TransformerID"].unique().tolist()
    xfmr_ami = []
    xfmr_list=[]
  
    for xfmr in xfmr_ls:
        
        xfmr_ami_ids = dfAMI_xfmr[dfAMI_xfmr['TransformerID'] == xfmr]['MeterID'].tolist()
        xfmr_ami.append(xfmr_ami_ids)
        xfmr_list.append(xfmr)

    return xfmr_list,xfmr_ami


def Get_Ami_loc(dfAMI_V,dfAMI_P,xfmr_ami,xfmr):

    V_loc=[]
    L_loc=[]
    
    for i in range(0,len(xfmr_ami[xfmr])):

        V_loc.append(np.where(dfAMI_V['Name'] == xfmr_ami[xfmr][i])[0])
        L_loc.append(np.where(dfAMI_P['ID_MTR_KEY'] == xfmr_ami[xfmr][i])[0])
        
    return V_loc,L_loc


def Get_Ami_loc_num(V_loc,L_loc,xfmr_ami,xfmr):
    
    V_loc_num=[]
    L_loc_num=[]

    V_loc_num2=[]
    L_loc_num2=[]

    for i in range(0,len(xfmr_ami[xfmr])):
        
        V_loc_num.append(len(V_loc[i]))
        L_loc_num.append(len(L_loc[i]))

        V_loc_num2.append(len(V_loc[i]))
        L_loc_num2.append(len(L_loc[i]))
        
    ami1_loc=np.argmax(V_loc_num)
    V_loc_num2[ami1_loc]=0
    ami2_loc=np.argmax(V_loc_num2)
    
    ami1=xfmr_ami[xfmr][ami1_loc]
    ami2=xfmr_ami[xfmr][ami2_loc]
    
    ami1_V_loc=V_loc[ami1_loc]
    ami1_L_loc=L_loc[ami1_loc]
    
    ami2_V_loc=V_loc[ami2_loc]
    ami2_L_loc=L_loc[ami2_loc]
        
    return ami1,ami2,ami1_V_loc,ami2_V_loc,ami1_L_loc,ami2_L_loc


def Get_Ami_meter_V_data(dfAMI_V,ami1_V_loc,ami2_V_loc):
    
    Meter_V_ami1=pd.DataFrame(columns=['Name','Time','rowV','MaxV','MinV','Vh'])
    Meter_V_ami2=pd.DataFrame(columns=['Name','Time','rowV','MaxV','MinV','Vh'])
   
    if len(ami1_V_loc)!=0:
        
        Meter_V_ami1['Name']=dfAMI_V['Name'][ami1_V_loc[0]:ami1_V_loc[-1]+1]
        Meter_V_ami1['Time']=dfAMI_V['Timestamp'][ami1_V_loc[0]:ami1_V_loc[-1]+1]
        Meter_V_ami1['rowV']=range(ami1_V_loc[0],ami1_V_loc[-1]+1,1)
        Meter_V_ami1['MaxV']=dfAMI_V['Max V(a)'][ami1_V_loc[0]:ami1_V_loc[-1]+1]
        Meter_V_ami1['MinV']=dfAMI_V['Min V(a)'][ami1_V_loc[0]:ami1_V_loc[-1]+1]
        Meter_V_ami1['Vh']=dfAMI_V['Vh(a)'][ami1_V_loc[0]:ami1_V_loc[-1]+1]

    if len(ami2_V_loc)!=0:
        
        Meter_V_ami2['Name']=dfAMI_V['Name'][ami2_V_loc[0]:ami2_V_loc[-1]+1]
        Meter_V_ami2['Time']=dfAMI_V['Timestamp'][ami2_V_loc[0]:ami2_V_loc[-1]+1]
        Meter_V_ami2['rowV']=range(ami2_V_loc[0],ami2_V_loc[-1]+1,1)
        Meter_V_ami2['MaxV']=dfAMI_V['Max V(a)'][ami2_V_loc[0]:ami2_V_loc[-1]+1]
        Meter_V_ami2['MinV']=dfAMI_V['Min V(a)'][ami2_V_loc[0]:ami2_V_loc[-1]+1]
        Meter_V_ami2['Vh']=dfAMI_V['Vh(a)'][ami2_V_loc[0]:ami2_V_loc[-1]+1]

    return Meter_V_ami1,Meter_V_ami2


def Get_Ami_meter_L_data(dfAMI_P,ami1_L_loc,ami2_L_loc):
    
    Meter_L_ami1=pd.DataFrame(columns=['Name','Day','Hour','rowP','KwH'])
    Meter_L_ami2=pd.DataFrame(columns=['Name','Day','Hour','rowP','KwH'])

   
    if len(ami1_L_loc)!=0:
        Meter_L_ami1['Name']=dfAMI_P['ID_MTR_KEY'][ami1_L_loc[0]:ami1_L_loc[-1]+1]
        Meter_L_ami1['Day']=dfAMI_P['INTRVL_DATE'][ami1_L_loc[0]:ami1_L_loc[-1]+1]
        Meter_L_ami1['Hour']=dfAMI_P['INTRVL_HOUR'][ami1_L_loc[0]:ami1_L_loc[-1]+1]
        Meter_L_ami1['rowP']=range(ami1_L_loc[0],ami1_L_loc[-1]+1,1)
        Meter_L_ami1['KwH']=dfAMI_P['KwH'][ami1_L_loc[0]:ami1_L_loc[-1]+1]

    if len(ami2_L_loc)!=0:
        Meter_L_ami2['Name']=dfAMI_P['ID_MTR_KEY'][ami2_L_loc[0]:ami2_L_loc[-1]+1]
        Meter_L_ami2['Day']=dfAMI_P['INTRVL_DATE'][ami2_L_loc[0]:ami2_L_loc[-1]+1]
        Meter_L_ami2['Hour']=dfAMI_P['INTRVL_HOUR'][ami2_L_loc[0]:ami2_L_loc[-1]+1]
        Meter_L_ami2['rowP']=range(ami2_L_loc[0],ami2_L_loc[-1]+1,1)
        Meter_L_ami2['KwH']=dfAMI_P['KwH'][ami2_L_loc[0]:ami2_L_loc[-1]+1]

    return Meter_L_ami1,Meter_L_ami2


def Get_Ami_meter_len_V_data(Data_len_V,V_t1,V_t2,Meter_V_ami1,Meter_V_ami2):
    
    Meter_V_len_ami1=pd.DataFrame(columns=['Name','Time','rowV','MaxV','MinV','Vh'])
   
    Fd_mid_1 = np.where(Meter_V_ami1['Time'] == V_t1)[0]
    Fd_mid_2 = np.where(Meter_V_ami1['Time'] == V_t2)[0]
    
    
    if len(Fd_mid_1)==1 and len(Fd_mid_2)==1:
        
        Meter_V_len_ami1['Name']=Meter_V_ami1['Name'][Fd_mid_1[0]:Fd_mid_2[0]+1]
        Meter_V_len_ami1['Time']=Meter_V_ami1['Time'][Fd_mid_1[0]:Fd_mid_2[0]+1]
        Meter_V_len_ami1['rowV']=Meter_V_ami1['rowV'][Fd_mid_1[0]:Fd_mid_2[0]+1]
        Meter_V_len_ami1['MaxV']=Meter_V_ami1['MaxV'][Fd_mid_1[0]:Fd_mid_2[0]+1]
        Meter_V_len_ami1['MinV']=Meter_V_ami1['MinV'][Fd_mid_1[0]:Fd_mid_2[0]+1]
        Meter_V_len_ami1['Vh']=Meter_V_ami1['Vh'][Fd_mid_1[0]:Fd_mid_2[0]+1]

    Meter_V_len_ami2=pd.DataFrame(columns=['Name','Time','rowV','MaxV','MinV','Vh'])
   
    Fd_mid_1 = np.where(Meter_V_ami2['Time'] == V_t1)[0]
    Fd_mid_2 = np.where(Meter_V_ami2['Time'] == V_t2)[0]
    
    
    if len(Fd_mid_1)==1 and len(Fd_mid_2)==1:
        
        Meter_V_len_ami2['Name']=Meter_V_ami2['Name'][Fd_mid_1[0]:Fd_mid_2[0]+1]
        Meter_V_len_ami2['Time']=Meter_V_ami2['Time'][Fd_mid_1[0]:Fd_mid_2[0]+1]
        Meter_V_len_ami2['rowV']=Meter_V_ami2['rowV'][Fd_mid_1[0]:Fd_mid_2[0]+1]
        Meter_V_len_ami2['MaxV']=Meter_V_ami2['MaxV'][Fd_mid_1[0]:Fd_mid_2[0]+1]
        Meter_V_len_ami2['MinV']=Meter_V_ami2['MinV'][Fd_mid_1[0]:Fd_mid_2[0]+1]
        Meter_V_len_ami2['Vh']=Meter_V_ami2['Vh'][Fd_mid_1[0]:Fd_mid_2[0]+1]        
        
    Meter_V_len_ami1.reset_index(inplace=True)
    Meter_V_len_ami2.reset_index(inplace=True)
    
    return Meter_V_len_ami1,Meter_V_len_ami2


def Get_Ami_meter_len_L_data(Data_len_L,L_t1,L_t2,Meter_L_ami1,Meter_L_ami2):
    
    Meter_L_len_ami1=pd.DataFrame(columns=['Name','Day','Hour','rowP','KwH'])
    
    Fd_mid_3 = np.where(Meter_L_ami1['Day'] == L_t1)[0]
    Fd_mid_4 = np.where(Meter_L_ami1['Day'] == L_t2)[0]
    
    if len(Fd_mid_3)==24 and len(Fd_mid_4)==24:
    
        Meter_L_len_ami1['Name']=Meter_L_ami1['Name'][Fd_mid_3[0]:Fd_mid_4[23]+1]
        Meter_L_len_ami1['Day']=Meter_L_ami1['Day'][Fd_mid_3[0]:Fd_mid_4[23]+1]
        Meter_L_len_ami1['Hour']=Meter_L_ami1['Hour'][Fd_mid_3[0]:Fd_mid_4[23]+1]
        Meter_L_len_ami1['rowP']=Meter_L_ami1['rowP'][Fd_mid_3[0]:Fd_mid_4[23]+1]
        Meter_L_len_ami1['KwH']=Meter_L_ami1['KwH'][Fd_mid_3[0]:Fd_mid_4[23]+1]

    Meter_L_len_ami2=pd.DataFrame(columns=['Name','Day','Hour','rowP','KwH'])
    
    Fd_mid_3 = np.where(Meter_L_ami2['Day'] == L_t1)[0]
    Fd_mid_4 = np.where(Meter_L_ami2['Day'] == L_t2)[0]
    
    if len(Fd_mid_3)==24 and len(Fd_mid_4)==24:
    
        Meter_L_len_ami2['Name']=Meter_L_ami2['Name'][Fd_mid_3[0]:Fd_mid_4[23]+1]
        Meter_L_len_ami2['Day']=Meter_L_ami2['Day'][Fd_mid_3[0]:Fd_mid_4[23]+1]
        Meter_L_len_ami2['Hour']=Meter_L_ami2['Hour'][Fd_mid_3[0]:Fd_mid_4[23]+1]
        Meter_L_len_ami2['rowP']=Meter_L_ami2['rowP'][Fd_mid_3[0]:Fd_mid_4[23]+1]
        Meter_L_len_ami2['KwH']=Meter_L_ami2['KwH'][Fd_mid_3[0]:Fd_mid_4[23]+1]

    Meter_L_len_ami1.reset_index(inplace=True)
    Meter_L_len_ami2.reset_index(inplace=True)
    
    return Meter_L_len_ami1,Meter_L_len_ami2


def Get_XFMR_L_data(dfXFMR_Pagg,xfmr_list,xfmr,Feeder):


    Fd_mid=np.where(dfXFMR_Pagg['ID_TRANSFMR'] == '0'+str(xfmr_list[xfmr]))

    
    if len(Fd_mid[0])==0:
        Fd_mid=np.where(dfXFMR_Pagg['ID_TRANSFMR'] == xfmr_list[xfmr])
    
    Fd_mid2 = pd.DataFrame(Fd_mid)

    Meter_L_xfmr=pd.DataFrame(columns=['Day','Hour','P'])

    if len(Fd_mid[0])>0:
        Meter_L_xfmr['Day']=dfXFMR_Pagg['INTRVL_DATE'][Fd_mid2[0].iloc[0]:Fd_mid2[Fd_mid2.columns[-1]][0]+1]
        Meter_L_xfmr['Hour']=dfXFMR_Pagg['INTRVL_HOUR'][Fd_mid2[0].iloc[0]:Fd_mid2[Fd_mid2.columns[-1]][0]+1]
        Meter_L_xfmr['P']=dfXFMR_Pagg['DIRECTIONAL_KWH'][Fd_mid2[0].iloc[0]:Fd_mid2[Fd_mid2.columns[-1]][0]+1]

    Meter_L_xfmr.reset_index(inplace=True)
    
    return Meter_L_xfmr


def Get_XFMR_L_len_data(Data_len_L,L_t1,L_t2,Meter_L_xfmr,xfmr):
    
    
    Fd_mid_3 = np.where(Meter_L_xfmr['Day'] == L_t1)[0] 

    Fd_mid_4 = np.where(Meter_L_xfmr['Day'] == L_t2)[0]

    if len(Fd_mid_3)==24 and len(Fd_mid_4)==24:
        
        Meter_L_len_xfmr=Meter_L_xfmr['P'][Fd_mid_3[0]:Fd_mid_4[23]+1]
        
    else:
        
        Meter_L_len_xfmr=pd.DataFrame(np.zeros(Data_len_L))
        print('No Load data for Transformer '+str(xfmr))

    if len(Meter_L_len_xfmr)!=Data_len_L:
        Meter_L_len_xfmr=pd.DataFrame(np.zeros(Data_len_L))
        print('No Load data for Transformer '+str(xfmr))
    
    Meter_L_len_xfmr=Meter_L_len_xfmr.reset_index(drop=True)   
    
    return Meter_L_len_xfmr


def Get_data_full_flag(Meter_V_len_ami1,Meter_V_len_ami2,Meter_L_len_ami1,Meter_L_len_ami2,Meter_L_len_xfmr,Data_len_V,Data_len_L,xfmr):
    
    Data_full_flag=1
    
    if len(Meter_V_len_ami1)!=Data_len_V or len(Meter_V_len_ami2)!=Data_len_V:
        
        Data_full_flag=0
        print('Voltage data not full for transformer '+str(xfmr))
     
    if len(Meter_L_len_ami1)!=Data_len_L or len(Meter_L_len_ami2)!=Data_len_L or len(Meter_L_len_xfmr)!=Data_len_L :
        
        Data_full_flag=0
        print('Load data not full for transformer '+str(xfmr))
    
    if sum(Meter_V_len_ami1['Vh'])==0 or sum(Meter_V_len_ami2['Vh'])==0 or np.mean(Meter_V_len_ami1['Vh'])<15 or np.mean(Meter_V_len_ami2['Vh'])<15 or np.mean(Meter_V_len_ami1['Vh'])>25 or np.mean(Meter_V_len_ami2['Vh'])>25 or np.std(Meter_V_len_ami1['Vh'])<0.0001 or np.std(Meter_V_len_ami2['Vh'])<0.0001 or np.min(Meter_V_len_ami2['Vh'])<17:
        
        Data_full_flag=0
        print('Voltage data not full for transformer '+str(xfmr))
        
    if sum(Meter_L_len_ami1['KwH'])==0 or sum(Meter_L_len_ami2['KwH'])==0 or sum(Meter_L_len_xfmr)==0:
        
        Data_full_flag=0
        print('Load data not full for transformer '+str(xfmr))

    return Data_full_flag


def Process_all_data(Meter_V_len_ami1,Meter_V_len_ami2,Meter_L_len_ami1,Meter_L_len_ami2):
    
    if sum(Meter_V_len_ami1['Vh'][0:5])<sum(Meter_V_len_ami2['Vh'][0:5]):
        
        Ami_V1=Meter_V_len_ami2
        Ami_V2=Meter_V_len_ami1
        Ami_L1=Meter_L_len_ami2
        Ami_L2=Meter_L_len_ami1
        
        Ami_loc_change=1
        
    else:
        
        Ami_V1=Meter_V_len_ami1
        Ami_V2=Meter_V_len_ami2
        Ami_L1=Meter_L_len_ami1
        Ami_L2=Meter_L_len_ami2     
        
        Ami_loc_change=0
    
    Ami1_V=np.array(Ami_V1['Vh'])
    
    for jj in range(0,len(Ami1_V)):
        if np.isnan(Ami1_V[jj]) or Ami1_V[jj]==0:
            Ami1_V[jj]=Ami1_V[jj-1]

    Ami2_V=np.array(Ami_V2['Vh'])
    
    for jj in range(0,len(Ami2_V)):
        if np.isnan(Ami2_V[jj]) or Ami2_V[jj]==0:
            Ami2_V[jj]=Ami2_V[jj-1]

    Ami1_L=np.array(Ami_L1['KwH'])
    
    for jj in range(0,len(Ami1_L)):
        if np.isnan(Ami1_L[jj]):
            Ami1_L[jj]=Ami1_L[jj-1]

    Ami2_L=np.array(Ami_L2['KwH'])
    
    for jj in range(0,len(Ami2_L)):
        if np.isnan(Ami2_L[jj]):
            Ami2_L[jj]=Ami2_L[jj-1]
        
    return Ami1_V,Ami2_V,Ami1_L,Ami2_L,Ami_loc_change


def Get_input_data(Ami1_V,Ami2_V,Ami1_L,Ami2_L,Meter_L_len_xfmr,Data_len_V,Data_len_L):
    
    V1=np.zeros(Data_len_L)
    V2=np.zeros(Data_len_L)
      
    for j in range(0,Data_len_V,12):
        if Ami1_V[j]>0:
            V1[int(j/12-1)]=Ami1_V[j]*12
        if Ami2_V[j]>0:
            V2[int(j/12-1)]=Ami2_V[j]*12
            
    L1=Ami1_L*1000
    L2=Ami2_L*1000
    
    L0=np.array(Meter_L_len_xfmr)*1000
    
    return V1,V2,L1,L2,L0










