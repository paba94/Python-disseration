# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 10:49:05 2018

@author: Paba
"""
import pandas as pd
import numpy as np


def D_fl():
    global D, D_UK, D_Int, D_Remote, ind_DUK_Arr, ind_DUK_Dep, ind_DRemote, ind_DInt
    
    Fleet = Turnarounds.groupby(['ICAO'])
    #Filter into groups of Fleets (C, D, E and F)
    #C = Fleet.get_group('C')
    D = Fleet.get_group('D')
   # E = Fleet.get_group('E')
   # F = Fleet.get_group('F') 
    DPier = D.loc[(D['Stand_Arrive'] != 'R')]
    DRemote = D.loc[(D['Stand_Arrive'] == 'R')]
    # Domestic Flights #
    DUK_Arr = DPier.loc[(DPier['Origin_Country'] == 'United Kingdom')]
    DUK_Dep = DPier.loc[(DPier['Origin_Country'] != 'United Kingdom') & (DPier['Dest_Country'] == 'United Kingdom')]
    # International Flights #
    DInt = DPier.loc[(DPier['Origin_Country'] != 'United Kingdom') & (DPier['Dest_Country'] != 'United Kingdom')]
    
    
    #Stands#
    D_Remote = np.array([581, 505, 508])
    D_UK = np.array([505, 508])
    D_Int = np.array([512, 513, 505, 508])
    
    ind_DRemote = np.array(DRemote.index.tolist())
    ind_DUK_Arr = np.array(DUK_Arr.index.tolist())
    ind_DUK_Dep = np.array(DUK_Dep.index.tolist())
    ind_DInt = np.array(DInt.index.tolist())
    #D= D.reset_index()


def allo_checker(ICAO, Stands):
    f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(Stands)]
    f_allo = f_allo[f_allo['ICAO'] == str(ICAO)]

    for (f, row) in f_allo.iterrows():
        stand = f_allo.loc[f, 'Stand_Arrive']
        f_allo1 = (f_allo[f_allo['Stand_Arrive'] == stand]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
        for (i, row) in f_allo1.iloc[1:].iterrows():
            Arrival_Check =(f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'])
            Buffer = (f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
            if Buffer == True and Arrival_Check == True:
                continue
            else:
                index1 = int(f_allo1.loc[i, 'index'])
                Turnarounds.loc[index1, 'Stand_Arrive'] = ''
                Turnarounds.loc[index1, 'Stand_Depart'] = ''

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#    
def Remote_D():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_DRemote:
            if Turnarounds.index[i]  == ind_DRemote[0]:
                Turnarounds.loc[i, 'Stand_Arrive'] = D_Remote[0]
                Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive'] 
                continue
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_DRemote:
            if Turnarounds.index[i]  in ind_DRemote[1:]:
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                #df[['Stand_Arrive']] = df[['Stand_Arrive']].apply(pd.to_numeric)
                   #df = df.dropna(subset = ['Stand_Depart'])
                df = df[df['Stand_Arrive'].isin(D_Remote)]

                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='Scheduled_Timestamp_Depart',ascending= True).reset_index()

                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])

                    Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(D_Remote == stand)[0]
                        stand = np.int(D_Remote[(index +1) % 3])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])

                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive'] > Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes')
                            if Arrival_Check == True and Buffer == True:
                                Turnarounds.loc[i, 'Stand_Arrive'] = stand
                                #Departure Stand
                                Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                                #break
                            else:
                                continue
                        else:
                            Turnarounds.loc[i, 'Stand_Arrive'] = stand
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                            break

        else:
            pass
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def RemoteD_to_FPier():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_DRemote:
            if Turnarounds.loc[i, 'Stand_Arrive'] == 'R':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()

                for k in F_Pier:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k, 'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k, 'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                           #print(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] , k)
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] + pd.to_timedelta('25 minutes'))

                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:

                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                            
                            
    f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(F_Pier)]
    f_allo = f_allo[f_allo['ICAO'] == 'D']

    for (f, row) in f_allo.iterrows():
        stand = f_allo.loc[f, 'Stand_Arrive']
        f_allo1 = (f_allo[f_allo['Stand_Arrive'] == stand]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
        for (i, row) in f_allo1.iloc[1:].iterrows():
            Arrival_Check =(f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'])
            Buffer = (f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
            if Buffer == True and Arrival_Check == True:
                continue
            else:
                index1 = int(f_allo1.loc[i, 'index'])
                Turnarounds.loc[index1, 'Stand_Arrive'] = 'R'
                Turnarounds.loc[index1, 'Stand_Depart'] = 'R'
            

    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_DRemote:
            if Turnarounds.loc[i, 'Stand_Arrive']  == 'R':
                f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(F_Pier)]
                #f_allo = f_allo[f_allo['ICAO'] == 'E']
   
                for f in F_Pier:
                   #stand = f_allo[f_allo['Stand_Arrive'] == f]
                   f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= False).reset_index()
                   f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', keep = 'first')
           
                   Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1['Scheduled_Timestamp_Depart'])
                   Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1['Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                   if all(Buffer) == True and all(Arrival_Check) == True:
                       index1 = int(f_allo1[ 'index'])
                       Turnarounds.loc[i, 'Stand_Arrive'] = int(f_allo1['Stand_Arrive'])
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                   
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#        
def RemoteD_to_EPier():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_DRemote:
            if Turnarounds.loc[i, 'Stand_Arrive'] == 'R':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()

                for k in E_Pier:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k, 'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k, 'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                           #print(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] , k)
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] + pd.to_timedelta('25 minutes'))

                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:

                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                            

    f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(E_Pier)]
    f_allo = f_allo[f_allo['ICAO'] == 'D']

    for (f, row) in f_allo.iterrows():
        stand = f_allo.loc[f, 'Stand_Arrive']
        f_allo1 = (f_allo[f_allo['Stand_Arrive'] == stand]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
        for (i, row) in f_allo1.iloc[1:].iterrows():
            Arrival_Check =(f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'])
            Buffer = (f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
            if Buffer == True and Arrival_Check == True:
                continue
            else:
                index1 = int(f_allo1.loc[i, 'index'])
                Turnarounds.loc[index1, 'Stand_Arrive'] = 'R'
                Turnarounds.loc[index1, 'Stand_Depart'] = 'R'
                
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_DRemote:
            if Turnarounds.loc[i, 'Stand_Arrive']  == 'R':
                f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(E_Pier)]
                #f_allo = f_allo[f_allo['ICAO'] == 'E']
   
                for f in E_Pier:
                   #stand = f_allo[f_allo['Stand_Arrive'] == f]
                   f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= False).reset_index()
                   f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', keep = 'first')
           
                   Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1['Scheduled_Timestamp_Depart'])
                   Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1['Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                   if all(Buffer) == True and all(Arrival_Check) == True:
                       index1 = int(f_allo1[ 'index'])
                       Turnarounds.loc[i, 'Stand_Arrive'] = int(f_allo1['Stand_Arrive'])
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#                           
def UKArr_D():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_DUK_Arr:
        
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()

                for k in D_UK:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k, 'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k, 'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                           #print(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] , k)
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] + pd.to_timedelta('25 minutes'))

                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:

                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                            break
                        else:
                            continue
                        
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#                           
def UKDep_D():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_DUK_Dep:
            if Turnarounds.loc[i, 'Stand_Arrive']  == '':
                f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(D_UK)]
                #f_allo = f_allo[f_allo['ICAO'] == 'E']

                for f in D_UK:
                   #stand = f_allo[f_allo['Stand_Arrive'] == f]
                   f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
                   f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', keep = 'first')

                   Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1['Scheduled_Timestamp_Depart'])
                   Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1['Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                   if all(Buffer) == True and all(Arrival_Check) == True:
                       index1 = int(f_allo1[ 'index'])
                       Turnarounds.loc[i, 'Stand_Arrive'] = int(f_allo1['Stand_Arrive'])
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                       

    allo_checker('D', D_UK)
    
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------#    
def Int_D():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_DInt:
            if Turnarounds.index[i]  == ind_DInt[0]:
                Turnarounds.loc[i, 'Stand_Arrive'] = D_Int[0]
                Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive'] 
                continue
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_DInt:
            if Turnarounds.index[i] in ind_DInt[1:]:
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                   #df = df.dropna(subset = ['Stand_Depart'])
                df = df[df['Stand_Arrive'].isin(D_Int)]
                df[['Stand_Arrive']] = df[['Stand_Arrive']].apply(pd.to_numeric)
                
                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='col1_sum',ascending= False).reset_index()

                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])

                    Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(D_Int == stand)[0]
                        stand = np.int(D_Int[(index +1) % 4])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                                   
                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive'] > Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes')
                            if Arrival_Check == True and Buffer == True:
                                Turnarounds.loc[i, 'Stand_Arrive'] = stand
                                #Departure Stand
                                Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                            else:
                                pass
                        else:
                            Turnarounds.loc[i, 'Stand_Arrive'] = stand
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                            break

        else:
            pass
    
    

    allo_checker('D', D_Int)
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def PierD_to_EPier():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.loc[i, 'ICAO']  == 'D':
            if Turnarounds.loc[i, 'Stand_Arrive']  == '':
                f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(E_Pier)]
                #f_allo = f_allo[f_allo['ICAO'] == 'E']

                for f in E_Pier:
                   #stand = f_allo[f_allo['Stand_Arrive'] == f]
                   f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
                   f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', keep = 'first')

                   Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1['Scheduled_Timestamp_Depart'])
                   Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1['Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                   if all(Buffer) == True and all(Arrival_Check) == True:
                       index1 = int(f_allo1[ 'index'])
                       Turnarounds.loc[i, 'Stand_Arrive'] = int(f_allo1['Stand_Arrive'])
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                       break
                   else:
                       continue
                   

    f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(E_Pier)]
    #f_allo = f_allo[f_allo['ICAO'] == str(ICAO)]

    for (f, row) in f_allo.iterrows():
        stand = f_allo.loc[f, 'Stand_Arrive']
        f_allo1 = (f_allo[f_allo['Stand_Arrive'] == stand]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
        for (i, row) in f_allo1.iloc[1:].iterrows():
            Arrival_Check =(f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'])
            Buffer = (f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
            if Buffer == True and Arrival_Check == True:
                continue
            else:
                index1 = int(f_allo1.loc[i, 'index'])
                Turnarounds.loc[index1, 'Stand_Arrive'] = ''
                Turnarounds.loc[index1, 'Stand_Depart'] = ''
                
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#                
def PierD_to_FRemote():                
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.loc[i, 'ICAO']  == 'D':
            if Turnarounds.loc[i, 'Stand_Arrive']  == '':
                f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(F_Remote)]
                #f_allo = f_allo[f_allo['ICAO'] == 'E']

                for f in F_Remote:
                   #stand = f_allo[f_allo['Stand_Arrive'] == f]
                   f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
                   f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', keep = 'first')

                   Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1['Scheduled_Timestamp_Depart'])
                   Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1['Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                   if all(Buffer) == True and all(Arrival_Check) == True:
                       index1 = int(f_allo1[ 'index'])
                       Turnarounds.loc[i, 'Stand_Arrive'] = int(f_allo1['Stand_Arrive'])
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                       

    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.loc[i, 'ICAO']  == 'D':
            if Turnarounds.loc[i, 'Stand_Arrive']  == '':
                f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(F_Remote)]
                #f_allo = f_allo[f_allo['ICAO'] == 'E']

                for f in F_Remote:
                   #stand = f_allo[f_allo['Stand_Arrive'] == f]
                   f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
                   f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', keep = 'first')

                   Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] < f_allo1['Scheduled_Timestamp_Arrive'])
                   Buffer = (f_allo1['Scheduled_Timestamp_Arrive'] -  Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                   if all(Buffer) == True and all(Arrival_Check) == True:
                       index1 = int(f_allo1[ 'index'])
                       Turnarounds.loc[i, 'Stand_Arrive'] = int(f_allo1['Stand_Arrive'])
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']                
 
def Schedule_D():
    
    D_fl()
    Remote_D()

    RemoteD_to_FPier()

    RemoteD_to_EPier()

    UKArr_D()

    UKDep_D()

    Int_D()
    PierD_to_EPier()
    PierD_to_FRemote()