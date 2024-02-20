# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 23:38:17 2021

@author: jwang4
"""


from __future__ import division
import pandas as pd
import datetime
import numpy as np
import os



def get_result_id(Result_est):    
    
    result_xfmrs = Result_est["xfmr_id"].unique().tolist()

    return result_xfmrs


def get_synergi_voltage_all(SynergiDir,month):
    
    synergi_voltage_all={}
    
    for i in range(0,len(month)):
    
        synergi_voltage_all[month[i]]=pd.read_excel(os.path.join(SynergiDir,'Del_Mar C68 - Transformer Voltages (Confidential).xlsx'),month[i])

    return synergi_voltage_all


def get_synergi_dates(synergi_info,month,year):
    
    result_days=[]
    
    for i in range(0,len(month)):
        
        Fd_mid = np.where(synergi_info['Month'] == month[i])[0][0]
        
        if Fd_mid+1>9:
            
            if synergi_info['PeakDay'][Fd_mid]>9:
               
                result_days.append(year+'-'+str(Fd_mid+1)+'-'+str(synergi_info['PeakDay'][Fd_mid])+' 00:00:00')
                
            else:
                
                result_days.append(year+'-'+str(Fd_mid+1)+'-0'+str(synergi_info['PeakDay'][Fd_mid])+' 00:00:00')
                
            if synergi_info['LowDay'][Fd_mid]>9:
               
                result_days.append(year+'-'+str(Fd_mid+1)+'-'+str(synergi_info['LowDay'][Fd_mid])+' 00:00:00')
                
            else:
                
                result_days.append(year+'-'+str(Fd_mid+1)+'-0'+str(synergi_info['LowDay'][Fd_mid])+' 00:00:00')
            
        else:

            if synergi_info['PeakDay'][Fd_mid]>9:
               
                result_days.append(year+'-0'+str(Fd_mid+1)+'-'+str(synergi_info['PeakDay'][Fd_mid])+' 00:00:00')
                
            else:
                
                result_days.append(year+'-0'+str(Fd_mid+1)+'-0'+str(synergi_info['PeakDay'][Fd_mid])+' 00:00:00')
                
            if synergi_info['LowDay'][Fd_mid]>9:
               
                result_days.append(year+'-0'+str(Fd_mid+1)+'-'+str(synergi_info['LowDay'][Fd_mid])+' 00:00:00')
                
            else:
                
                result_days.append(year+'-0'+str(Fd_mid+1)+'-0'+str(synergi_info['LowDay'][Fd_mid])+' 00:00:00')          

    return result_days


def get_synergi_id(result_xfmrs,Feeder):
    
    synergi_xfmrs=[]
    
    for i in range(0,len(result_xfmrs)):
        
        synergi_xfmrs.append(Feeder+'-'+str(int(str(result_xfmrs[i])[-4:])))
                
    return synergi_xfmrs


def get_result_voltage(result_xfmrs,Result_est,result_days,xfmr):
    
    Fd_mid=np.where(Result_est['xfmr_id'] == result_xfmrs[xfmr])[0]
    
    Voltage_result_all=pd.DataFrame(columns=['day','value'])
    
    Voltage_result_all['day']=Result_est['day'][Fd_mid[0]:Fd_mid[-1]+1]
    Voltage_result_all['value']=Result_est['value'][Fd_mid[0]:Fd_mid[-1]+1]
    
    Voltage_result_all.reset_index(inplace=True)
    
    v_result=[]
    
    for i in range(0,len(result_days)):
        
        Fd_mid2=np.where(Voltage_result_all['day'] == result_days[i])[0]
        
        for j in range(0,len(Fd_mid2)):
            v_result.append(Voltage_result_all['value'][Fd_mid2[j]])
        
    return v_result


def get_synergi_voltage(synergi_xfmrs,synergi_voltage_all,month,xfmr):
    
    v_synergi=[]
    
    for i in range(0,len(month)):
        
        Voltage_synergi_month=synergi_voltage_all[month[i]]
        
        Fd_mid=np.where(Voltage_synergi_month['Transformer'] == synergi_xfmrs[xfmr])[0]
        
        Voltage_synergi_all=pd.DataFrame(columns=['DayType','Volts'])
        
        Voltage_synergi_all['DayType']=Voltage_synergi_month['DayType'][Fd_mid[0]:Fd_mid[-1]+1]
        Voltage_synergi_all['Volts']=Voltage_synergi_month['Volts'][Fd_mid[0]:Fd_mid[-1]+1]
        
        Voltage_synergi_all.reset_index(inplace=True)
        
        Fd_mid2=np.where(Voltage_synergi_all['DayType'] == 'Peak')[0]
        
        for j in range(0,len(Fd_mid2)):
            
            v_synergi.append(Voltage_synergi_all['Volts'][Fd_mid2[j]]*6928.2/120)
        
        Fd_mid3=np.where(Voltage_synergi_all['DayType'] == 'Low')[0]
        
        for j in range(0,len(Fd_mid3)):
            
            v_synergi.append(Voltage_synergi_all['Volts'][Fd_mid3[j]]*6928.2/120)    
            
    return v_synergi
    
def get_section_name(synergi_xfmrs,synergi_dss,xfmr):
    
    Fd_mid=np.where(synergi_dss['DTranId'] == synergi_xfmrs[xfmr])[0][0]
    
    section_name=synergi_dss['SectionId'][Fd_mid]
    
    return section_name
        
def get_bus_name(synergi_section,synergi_line,xfmr):
    
    Fd_mid=np.where(synergi_line['SectionId'] == synergi_section)[0][0]
    
    bus_name=synergi_line['FromNodeId'][Fd_mid]
    
    phase_info=synergi_line['SectionPhases'][Fd_mid]
    
    return bus_name,phase_info        
        
    
    

        
    
    
