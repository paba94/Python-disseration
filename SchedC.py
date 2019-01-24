# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 17:01:20 2018

@author: User
"""

import pandas as pd
import numpy as np

    
def C_fl():
    global C,  CTA, C_Remote, C_AllPier, C_UK_Arr, C_UK_Dep, C_Int,  ind_CRemote, ind_CUK_Arr, ind_CUK_Dep, ind_CTA, ind_CInt
    
    Fleet = Turnarounds.groupby(['ICAO'])
    #Filter into groups of Fleets (C, D, E and F)
    C = Fleet.get_group('C')
   
    CPier = C.loc[(C['Stand_Arrive'] != 'R')]
    CRemote = C.loc[(C['Stand_Arrive'] == 'R')]
    
    #CTA#
    C_CTA = CPier.loc[(CPier['Origin_City'] == 'Dublin')]
    # Domestic Flights #
    CUK_Arr = CPier.loc[(CPier['Origin_Country'] == 'United Kingdom')]
    CUK_Dep = CPier.loc[(CPier['Origin_Country'] != 'United Kingdom') & (CPier['Origin_City'] != 'Dublin') & (CPier['Dest_Country'] == 'United Kingdom')]
    # International Flights #
    CInt = CPier.loc[(CPier['Origin_Country'] != 'United Kingdom') & (CPier['Origin_City'] != 'Dublin') & (CPier['Dest_Country'] != 'United Kingdom')]
    
     #Stands#
    C_Remote = np.array([524, 525, 526, 527])
    C_AllPier = np.array([501, 502, 503, 506, 507, 509, 511, 515, 517, 519, 520, 521, 522, 523])
    C_UK_Arr = np.array([501, 502, 503, 506, 507])
    C_UK_Dep = np.array([506, 507, 509, 511, 519, 522])
    CTA = np.array([523])
    C_Int = np.array([515, 517, 520, 521, 522, 519, 511, 509,507, 506])
    
    ind_CRemote = np.array(CRemote.index.tolist())
    ind_CUK_Arr = np.array(CUK_Arr.index.tolist())
    ind_CUK_Dep = np.array(CUK_Dep.index.tolist())
    ind_CInt = np.array(CInt.index.tolist())
    ind_CTA = np.array(C_CTA.index.tolist())
    #D= D.reset_index()

#####################################################################################
def C_allo_checker(Stands):
    f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(Stands)]


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
            
                
                
######################################    DOMESTIC FLIGHTS    ###########################################################
    
def Remote_C():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CRemote:
            if Turnarounds.index[i]  == ind_CRemote[0]:
                Turnarounds.loc[i, 'Stand_Arrive'] = C_Remote[0]
                Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive'] 
                continue
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CRemote:
            if Turnarounds.index[i]  in ind_CRemote[1:]:
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                #df[['Stand_Arrive']] = df[['Stand_Arrive']].apply(pd.to_numeric)
                   #df = df.dropna(subset = ['Stand_Depart'])
                df = df[df['Stand_Arrive'].isin(C_Remote)]

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
                        index = np.where(C_Remote == stand)[0]
                        stand = np.int(C_Remote[(index +1) % 4])
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
        
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CRemote:
            if Turnarounds.loc[i, 'Stand_Arrive']  == 'R':
                Turnarounds.loc[i, 'Stand_Arrive'] = C_AllPier[0]
                Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive'] 
                break

    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CRemote:
            if Turnarounds.loc[i, 'Stand_Arrive']  == 'R':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                #df[['Stand_Arrive']] = df[['Stand_Arrive']].apply(pd.to_numeric)
                   #df = df.dropna(subset = ['Stand_Depart'])
                df = df[df['Stand_Arrive'].isin(C_AllPier)]

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
                        index = np.where(C_AllPier == stand)[0]
                        stand = np.int(C_AllPier[(index +1) % 14])
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
def RemoteC_to_EPier():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CRemote:
            if Turnarounds.loc[i, 'Stand_Arrive'] == 'R':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g:\
                                g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',\
                                                            ascending= False)
                df = df.reset_index()
                for k in E_Pier:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k, \
                                           'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k,\
                                          'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.\
                                                                empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] =\
                                            Turnarounds.loc[i, 'Stand_Arrive']
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
                                              - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] \
                                              + pd.to_timedelta('25 minutes'))

                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True\
                                    and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True\
                                    and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:

                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = \
                                            Turnarounds.loc[i, 'Stand_Arrive']
                            

    f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(E_Pier)]

    for (f, row) in f_allo.iterrows():
        stand = f_allo.loc[f, 'Stand_Arrive']
        f_allo1 = (f_allo[f_allo['Stand_Arrive'] == stand]).\
        sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
        for (i, row) in f_allo1.iloc[1:].iterrows():
            Arrival_Check =(f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] \
                            > f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'])
            Buffer = (f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] \
                      - f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'] \
                      >= pd.to_timedelta('25 minutes'))
            if Buffer == True and Arrival_Check == True:
                continue
            else:
                index1 = int(f_allo1.loc[i, 'index'])
                Turnarounds.loc[index1, 'Stand_Arrive'] = 'R'
                Turnarounds.loc[index1, 'Stand_Depart'] = 'R'
            

    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CRemote:
            if Turnarounds.loc[i, 'Stand_Arrive']  == 'R':
                f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(E_Pier)]
                

                for f in E_Pier:
                    f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).\
                    sort_values(by='Scheduled_Timestamp_Arrive',\
                                ascending= False).reset_index()
                    f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', \
                                                      keep = 'first')

                    Arrival_Check =(Turnarounds.loc[i, \
        'Scheduled_Timestamp_Arrive'] > f_allo1['Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive']\
    - f_allo1['Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                    if all(Buffer) == True and all(Arrival_Check) == True:
                       index1 = int(f_allo1[ 'index'])
                       Turnarounds.loc[i, 'Stand_Arrive'] =\
                                                   int(f_allo1['Stand_Arrive'])
                       Turnarounds.loc[i, 'Stand_Depart'] = \
                                             Turnarounds.loc[i, 'Stand_Arrive']
                           
 #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#      
def RemoteC_to_FPier():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CRemote:
            if Turnarounds.loc[i, 'Stand_Arrive'] == 'R':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g:\
                                        g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',\
                                    ascending= False)
                df = df.reset_index()
                for k in F_Pier:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k
                                           , 'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k, \
                                          'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] =\
                        Turnarounds.loc[i, 'Stand_Arrive']
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
                                  - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] \
                                  + pd.to_timedelta('25 minutes'))
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True \
                        and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True \
                        and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:
                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = \
                            Turnarounds.loc[i, 'Stand_Arrive']
                            

    f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(F_Pier)]
    for (f, row) in f_allo.iterrows():
        stand = f_allo.loc[f, 'Stand_Arrive']
        f_allo1 = (f_allo[f_allo['Stand_Arrive'] == stand]).\
        sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
        for (i, row) in f_allo1.iloc[1:].iterrows():
            Arrival_Check =(f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] \
                            > f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'])
            Buffer = (f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] \
                      - f_allo1.loc[i-1,'Scheduled_Timestamp_Depart']\
                      >= pd.to_timedelta('25 minutes'))
            if Buffer == True and Arrival_Check == True:
                continue
            else:
                index1 = int(f_allo1.loc[i, 'index'])
                Turnarounds.loc[index1, 'Stand_Arrive'] = 'R'
                Turnarounds.loc[index1, 'Stand_Depart'] = 'R'
            

    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CRemote:
            if Turnarounds.loc[i, 'Stand_Arrive']  == 'R':
                f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(F_Pier)]

                for f in F_Pier:
                    #stand = f_allo[f_allo['Stand_Arrive'] == f]
                    f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).\
                    sort_values(by='Scheduled_Timestamp_Arrive',\
                                ascending= False).reset_index()
                    f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', \
                                                      keep = 'first')

                    Arrival_Check =(Turnarounds.loc[i, \
        'Scheduled_Timestamp_Arrive'] > f_allo1['Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
    - f_allo1['Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                    if all(Buffer) == True and all(Arrival_Check) == True:
                       index1 = int(f_allo1[ 'index'])
                       Turnarounds.loc[i, 'Stand_Arrive'] = \
                       int(f_allo1['Stand_Arrive'])
                       Turnarounds.loc[i, 'Stand_Depart'] = \
                       Turnarounds.loc[i, 'Stand_Arrive']


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#      

######################################    CTA FLIGHTS    ###########################################################
def CTA_C():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CTA:
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g:\
                                        g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',\
                                    ascending= True)
                df = df[df['Stand_Arrive'].isin(CTA)]
                #pick stand with largest number of passsengers
                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='Scheduled_Timestamp_Depart',\
                                      ascending= True).reset_index()
                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                    Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
    > Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
    - Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'] \
                                            >= pd.to_timedelta('25 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] = \
                       Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(CTA == stand)[0]
                        stand = np.int(CTA[(index +1) % 1])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive'] \
                            > Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
                            - Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']\
                            >= pd.to_timedelta('25 minutes')
                            if Arrival_Check == True and Buffer == True:
                                Turnarounds.loc[i, 'Stand_Arrive'] = stand
                                #Departure Stand
                                Turnarounds.loc[i, 'Stand_Depart'] = \
                                            Turnarounds.loc[i, 'Stand_Arrive']
                            else:
                                continue
                        else:
                            Turnarounds.loc[i, 'Stand_Arrive'] = stand
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] =\
                                            Turnarounds.loc[i, 'Stand_Arrive']
                            break

        else:
            pass
    
    C_allo_checker(CTA)

# Allocate remaining flights to C_Int Stands #   
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CTA:
            if Turnarounds.loc[i, 'Stand_Arrive']  == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g:\
                                g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',\
                                    ascending= True)
                df = df[df['Stand_Arrive'].isin(C_Int)]

                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='Scheduled_Timestamp_Depart',\
                                      ascending= True).reset_index()
                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                    Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive']\
> Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive']\
- Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'] \
>= pd.to_timedelta('25 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] = \
                       Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(C_Int == stand)[0]
                        stand = np.int(C_Int[(index +1) % 10])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive']\
> Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive']\
- Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart'] \
>= pd.to_timedelta('25 minutes')
                            if Arrival_Check == True and Buffer == True:
                                Turnarounds.loc[i, 'Stand_Arrive'] = stand
                                #Departure Stand
                                Turnarounds.loc[i, 'Stand_Depart'] = \
                                Turnarounds.loc[i, 'Stand_Arrive']
                            else:
                                continue
                        else:
                            Turnarounds.loc[i, 'Stand_Arrive'] = stand
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = \
                            Turnarounds.loc[i, 'Stand_Arrive']
                            break

        else:
            pass
    
    C_allo_checker(C_Int)
    
                   
######################################    DOMESTIC FLIGHTS    ###########################################################
    
def UKArr_C():
#Set stand for first flight#
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] == ind_CUK_Arr[0]:
            #if Turnarounds.loc[i, 'Stand_Arrive']  == 'R':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: \
                                        g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',\
                                    ascending= True)
                df = df[df['Stand_Arrive'].isin(C_UK_Arr)]

                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='Scheduled_Timestamp_Depart',\
                                      ascending= True).reset_index()
                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])

                    Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
> Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
- Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'] \
>= pd.to_timedelta('25 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] =\
                       Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(C_UK_Arr == stand)[0]
                        stand = np.int(C_UK_Arr[(index +1) % 5])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])

                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive'] \
> Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
- Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart'] \
>= pd.to_timedelta('25 minutes')
                            if Arrival_Check == True and Buffer == True:
                                Turnarounds.loc[i, 'Stand_Arrive'] = stand
                                #Departure Stand
                                Turnarounds.loc[i, 'Stand_Depart'] =\
                                Turnarounds.loc[i, 'Stand_Arrive']
                            else:
                                continue
                        else:
                            Turnarounds.loc[i, 'Stand_Arrive'] = stand
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] =\
                            Turnarounds.loc[i, 'Stand_Arrive']
                            break
                        
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] == ind_CUK_Dep[0]:
            if Turnarounds.loc[i, 'Stand_Arrive']  == '':
                Turnarounds.loc[i, 'Stand_Arrive'] = C_UK_Dep[0]
                #Departure Stand
                Turnarounds.loc[i, 'Stand_Depart'] = \
                Turnarounds.loc[i, 'Stand_Arrive']
                continue
            
#Set stands for rest of the flights#
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CUK_Arr[1:]:
            df = Turnarounds[Turnarounds.index.isin(ind_CUK_Arr)]
            df = df.groupby('Stand_Arrive').apply(lambda g:\
                               g.assign(col1_sum=g.Total_Pax_Depart.sum()))
            df.index = df.index.droplevel(level=0)
            df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
            df = df[df['Stand_Arrive'].isin(C_UK_Arr)]

            df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
            df1 = df1.sort_values(by='col1_sum',ascending= True).reset_index()
            for (j, rows) in df1.iterrows():
                stand = df1['Stand_Arrive'][j]
                index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
> Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
- Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'] \
>= pd.to_timedelta('25 minutes'))
                if Buffer == True and Arrival_Check == True:
                    Turnarounds.loc[i, 'Stand_Arrive'] = stand
                    #Departure Stand
                    Turnarounds.loc[i, 'Stand_Depart'] =\
                       Turnarounds.loc[i, 'Stand_Arrive']
                    break
                else:
                    index = np.where(C_UK_Arr == stand)[0]
                    stand = np.int(C_UK_Arr[(index +1) % 5])
                    if stand in np.array(df1['Stand_Arrive']): 
                        f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                        Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive'] \
> Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                        Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
 - Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']\
 >= pd.to_timedelta('25 minutes')
                        if Arrival_Check == True and Buffer == True:
                            Turnarounds.loc[i, 'Stand_Arrive'] = stand
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] =\
                                Turnarounds.loc[i, 'Stand_Arrive']
                        else:
                            continue
                    else:
                        Turnarounds.loc[i, 'Stand_Arrive'] = stand
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] =\
                            Turnarounds.loc[i, 'Stand_Arrive']
                        break

    C_allo_checker(C_UK_Arr)

#Set unallocated flights to E stands #
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CUK_Arr:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: \
                                g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',\
                                    ascending= False)
                df = df.reset_index()
                for k in E_Pier:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k,\
                                           'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k,\
                                          'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] = \
                        Turnarounds.loc[i, 'Stand_Arrive']
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
                                  - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] \
                                  + pd.to_timedelta('25 minutes'))

                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True \
                        and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True \
                        and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:

                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = \
                            Turnarounds.loc[i, 'Stand_Arrive']
    C_allo_checker(E_Pier)

#Set unallocated flights to F stands #
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CUK_Arr:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
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
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
                                  - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] \
                                  + pd.to_timedelta('25 minutes'))

                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True \
                        and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True \
                        and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:

                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = \
                            Turnarounds.loc[i, 'Stand_Arrive']
    C_allo_checker(F_Pier)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# 
def UKDep_C():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] == ind_CUK_Dep[0]:
            
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: \
                                g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= True)
                df = df[df['Stand_Arrive'].isin(C_UK_Dep)]

                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='Scheduled_Timestamp_Depart',\
                                      ascending= True).reset_index()
                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                    Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive']\
> Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
 - Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] =\
                       Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(C_UK_Dep == stand)[0]
                        stand = np.int(C_UK_Dep[(index +1) % 6])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive']\
> Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
- Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('25 minutes')
                            if Arrival_Check == True and Buffer == True:
                                Turnarounds.loc[i, 'Stand_Arrive'] = stand
                                #Departure Stand
                                Turnarounds.loc[i, 'Stand_Depart'] = \
                                Turnarounds.loc[i, 'Stand_Arrive']
                            else:
                                continue
                        else:
                            Turnarounds.loc[i, 'Stand_Arrive'] = stand
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = \
                            Turnarounds.loc[i, 'Stand_Arrive']
                            

        else:
            pass

    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] == ind_CUK_Dep[0]:
            if Turnarounds.loc[i, 'Stand_Arrive']  == '':
                Turnarounds.loc[i, 'Stand_Arrive'] = C_UK_Dep[0]
                #Departure Stand
                Turnarounds.loc[i, 'Stand_Depart'] = \
                Turnarounds.loc[i, 'Stand_Arrive']
                continue
                        
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CUK_Dep[1:]:
           
                df = Turnarounds[Turnarounds.index.isin(ind_CUK_Dep)]
                df = df.groupby('Stand_Arrive').apply(lambda g:\
                              g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df[df['Stand_Arrive'].isin(C_UK_Dep)]

                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='col1_sum',ascending= True).reset_index()

                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])

                    Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
> Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
- Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart']\
 >= pd.to_timedelta('25 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(C_UK_Dep == stand)[0]
                        stand = np.int(C_UK_Dep[(index +1) % 6])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])

                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive'] \
> Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
- Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']\
 >= pd.to_timedelta('25 minutes')
                            if Arrival_Check == True and Buffer == True:
                                Turnarounds.loc[i, 'Stand_Arrive'] = stand
                                #Departure Stand
                                Turnarounds.loc[i, 'Stand_Depart'] =\
                                Turnarounds.loc[i, 'Stand_Arrive']
                                #break
                            else:
                                continue
                        else:
                            Turnarounds.loc[i, 'Stand_Arrive'] = stand
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] =\
                            Turnarounds.loc[i, 'Stand_Arrive']
                            break

        else:
            pass
    C_allo_checker(C_UK_Dep)
    
#Set unallocated flights to F-Remote Stands #
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CUK_Dep:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g:\
                                g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()
                for k in F_Remote:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k,\
                                           'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k, \
                                          'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] + pd.to_timedelta('25 minutes'))
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True \
                        and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True \
                        and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:
                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = \
                            Turnarounds.loc[i, 'Stand_Arrive']         
    C_allo_checker(F_Remote)
        
#Set unallocated flights to D-Remote Stands #      
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CUK_Dep:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g:\
                                g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()
                for k in D_Remote:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k,\           
                                         'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k, \
                                          'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.\
                    empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] = \
                        Turnarounds.loc[i, 'Stand_Arrive']
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
                                  - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] \
                                  + pd.to_timedelta('25 minutes'))
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True\
                        and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True \
                        and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:

                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] =\
                            Turnarounds.loc[i, 'Stand_Arrive']
    C_allo_checker(D_Remote)
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------# 
def Int_C():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] == ind_CInt[0]:
            
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g:\
                                g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= True)
                df = df[df['Stand_Arrive'].isin(C_Int)]

                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='Scheduled_Timestamp_Depart',\
                                      ascending= True).reset_index()
                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                    Arrival_Check =(Turnarounds.\
                loc[i, 'Scheduled_Timestamp_Arrive']> Turnarounds.\
                loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
    - Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart']\
    >= pd.to_timedelta('25 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] =\
                       Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(C_Int == stand)[0]
                        stand = np.int(C_Int[(index +1) % 10])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                            Arrival_Check = Turnarounds.\
                loc[i,'Scheduled_Timestamp_Arrive'] > Turnarounds.\
                loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
        - Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart'] \
        >= pd.to_timedelta('25 minutes')
                            if Arrival_Check == True and Buffer == True:
                                Turnarounds.loc[i, 'Stand_Arrive'] = stand
                                #Departure Stand
                                Turnarounds.loc[i, 'Stand_Depart'] =\
                                Turnarounds.loc[i, 'Stand_Arrive']
                            else:
                                continue
                        else:
                            Turnarounds.loc[i, 'Stand_Arrive'] = stand
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] =\
                            Turnarounds.loc[i, 'Stand_Arrive']
                            

        else:
            pass
       

    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] == ind_CInt[0]:
            if Turnarounds.loc[i, 'Stand_Arrive']  == '':
                Turnarounds.loc[i, 'Stand_Arrive'] = C_Int[0]
                #Departure Stand
                Turnarounds.loc[i, 'Stand_Depart'] = \
                Turnarounds.loc[i, 'Stand_Arrive']
                continue
    
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CInt[1:]:         
                df = Turnarounds[Turnarounds.index.isin(ind_CInt)]
                df = df.groupby('Stand_Arrive').apply(lambda g:\
                               g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',\
                                    ascending= False)
                df = df[df['Stand_Arrive'].isin(C_Int)]

                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='col1_sum',\
                                      ascending= True).reset_index()
                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                    Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive']\
> Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
- Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart']
 >= pd.to_timedelta('25 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] = \
                       Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(C_Int == stand)[0]
                        stand = np.int(C_Int[(index +1) % 10])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive']
> Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
- Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart'] \
>= pd.to_timedelta('25 minutes')
                            if Arrival_Check == True and Buffer == True:
                                Turnarounds.loc[i, 'Stand_Arrive'] = stand
                                #Departure Stand
                                Turnarounds.loc[i, 'Stand_Depart'] = \
                                Turnarounds.loc[i, 'Stand_Arrive']
                            else:
                                continue
                        else:
                            Turnarounds.loc[i, 'Stand_Arrive'] = stand
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = \
                            Turnarounds.loc[i, 'Stand_Arrive']
                            break

        else:
            pass
    C_allo_checker(C_Int)
    
# Set unallocated flights to pier-served 'F' stands #
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CInt:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g:\
                                g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',\
                                    ascending= False)
                df = df.reset_index()
                for k in F_Pier:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k,\
                                           'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k, \
                                          'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.\
                    empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] =\
                        Turnarounds.loc[i, 'Stand_Arrive']
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] \
                                  - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart']\
                                  + pd.to_timedelta('25 minutes'))
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True \
                        and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True\
                        and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False\
                        and Depart_Check2 == False:

                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = 
                            Turnarounds.loc[i, 'Stand_Arrive']         
    
                        
    C_allo_checker(F_Pier)

# Set unallocated flights to remote 'F' stands #
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CInt:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: \
                                g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()
                for k in F_Remote:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k,\
                                           'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k,\
                                          'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] =\
                        Turnarounds.loc[i, 'Stand_Arrive']
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive']\
                                  - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart']\
                                  + pd.to_timedelta('25 minutes'))
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True\
                        and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True\
                        and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:
                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] =\
                            Turnarounds.loc[i, 'Stand_Arrive']
    C_allo_checker(F_Remote)    

# Set unallocated flights to remote 'C' stands #
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CInt:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g:\
                                g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()
                for k in C_Remote:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k,\
                                           'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k,\
                                          'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] = \
                        Turnarounds.loc[i, 'Stand_Arrive']
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive']\
                                  - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart']\
                                  + pd.to_timedelta('25 minutes'))
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True \
                        and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True \
                        and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:
                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] =\
                            Turnarounds.loc[i, 'Stand_Arrive']
    C_allo_checker(C_Remote)

# Set unallocated flights to remote 'E' stands #
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CInt:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: \
                                g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()
                for k in E_Remote:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k,\
                                           'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k,\
                                          'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] =\
                        Turnarounds.loc[i, 'Stand_Arrive']
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive']\
                                  - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] \
                                  + pd.to_timedelta('25 minutes'))
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True\
                        and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True\
                        and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:
                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = \
                            Turnarounds.loc[i, 'Stand_Arrive']
    C_allo_checker(E_Remote)
    
# Set unallocated flights to pier-served 'E' stands #
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_CInt:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g:\
                                g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()
                for k in E_Pier:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k, \
                                           'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k,\
                                          'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] =\
                        Turnarounds.loc[i, 'Stand_Arrive']
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive']\
                                  - pd.to_timedelta('25 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] \
                                  + pd.to_timedelta('25 minutes'))
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True \
                        and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True\
                        and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:
                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] =\
                            Turnarounds.loc[i, 'Stand_Arrive']
                        
    C_allo_checker(E_Pier)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#        
def Schedule_C():
    C_fl()
    # Towed flights
    Remote_C()
    #Reallocate remote flights to E and F stands
    RemoteC_to_EPier()
    RemoteC_to_FPier()
    # CTA: Flights from Dublin #
    CTA_C()
    # Domestic Flights #
    UKArr_C()
    UKDep_C()
    # International flights #
    Int_C()
    