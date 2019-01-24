# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 22:54:15 2018

@author: Paba
"""
import pandas as pd
import numpy as np
#from temp_dataLoad_2 import Turnarounds

def F_fl():
    global F, F_Pier, F_Remote, ind_F, ind_FRemote, ind_FPier
    
    Fleet = Turnarounds.groupby(['ICAO'])
    #Filter into groups of Fleets (C, D, E and F)
    F = Fleet.get_group('F') 
    
    ## ALL FLIGHTS OF TYPE 'F' ARE INTERNATIONAL ##
    ## ALL STANDS THAT CAN ACCOMADATE TYPE 'F' AIRCRAFT ONLY SERVE INTERNATIONAL FLIGHTS ##
    
    F_Pier = np.array([555, 556, 557, 561, 562, 563, 564, 565, 544, 545, 546, 547])
    F_Remote = np.array([558, 575, 576])
    
    ind_FRemote = np.array((F.loc[F['Stand_Arrive']=='R']).index.tolist())
    ind_FPier = np.array((F.loc[F['Stand_Arrive']!='R']).index.tolist())
    #D= D.reset_index()
    
    
def Remote_F():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_FRemote:
            if Turnarounds.index[i]  == ind_FRemote[0]:
                Turnarounds.loc[i, 'Stand_Arrive'] = F_Remote[0]
                Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive'] 
                continue
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_FRemote:
            if Turnarounds.index[i]  in ind_FRemote[1:]:
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df[df['Stand_Arrive'].isin(F_Remote)]

                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='col1_sum',ascending= False).reset_index()

                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])

                    Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('30 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(F_Remote == stand)[0]
                        stand = np.int(F_Remote[(index +1) % 3])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                                   
                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive'] > Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('30 minutes')
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

#-------------------------------------------------------------------------------------------------------------------------------------------#
        
def Pier_F():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_FPier:
            if Turnarounds.index[i]  == ind_FPier[0]:
                Turnarounds.loc[i, 'Stand_Arrive'] = F_Pier[0]
                Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive'] 
                continue
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_FPier:
            if Turnarounds.index[i] in ind_FPier[1:]:
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                   #df = df.dropna(subset = ['Stand_Depart'])
                df = df[df['Stand_Arrive'].isin(F_Pier)]
                df[['Stand_Arrive']] = df[['Stand_Arrive']].apply(pd.to_numeric)
                
                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='col1_sum',ascending= False).reset_index()

                for (j, rows) in df1.iterrows():
                    stand = df1['Stand_Arrive'][j]
                    index1 = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])

                    Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'])
                    Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - Turnarounds.loc[Turnarounds.index[index1],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('30 minutes'))
                    if Buffer == True and Arrival_Check == True:
                       Turnarounds.loc[i, 'Stand_Arrive'] = stand
                       #Departure Stand
                       Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                       break
                    else:
                        index = np.where(F_Pier == stand)[0]
                        stand = np.int(F_Pier[(index +1) % 12])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                                   
                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive'] > Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('30 minutes')
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
        
#----------------------------------------------------------------------------------------------------------------------------------------------------#
            
def Schedule_F():
    #   Manipulate 'F' aircraft data to use in scheduling aglorithm    #
    F_fl()
    #   Allocate towed flights to Remote stands first - so they don't block up pier-served stands   #
    Remote_F()
    #   Allocate flights to the Pier-served stands  #
    Pier_F()