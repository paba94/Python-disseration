# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 12:38:41 2018

@author: Paba
"""

import pandas as pd
import numpy as np
#from temp_dataLoad_2 import Turnarounds

def E_fl():
    global E, E_Pier, E_Remote, ind_EPier, ind_ERemote
    
    Fleet = Turnarounds.groupby(['ICAO'])
    #Filter into groups of Fleets (C, D, E and F)
    E = Fleet.get_group('E') 
    
    ## ALL FLIGHTS OF TYPE 'E' ARE INTERNATIONAL ##
    ## ALL STANDS THAT CAN ACCOMADATE TYPE 'E' AIRCRAFT ONLY SERVE INTERNATIONAL FLIGHTS ##
    
    E_Pier = np.array([518, 532, 533, 534, 535, 536, 537, 538, 539, 542, 543, 552, 553, 554, 566])
    E_Remote = np.array([531, 541, 548, 551, 567, 568, 572, 573])
    
    ind_ERemote = np.array((E.loc[E['Stand_Arrive']=='R']).index.tolist())
    ind_EPier = np.array((E.loc[E['Stand_Arrive']!='R']).index.tolist())
    #D= D.reset_index()
    
    
def allo_checker(ICAO, Stands):
    f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(Stands)]
    f_allo = f_allo[f_allo['ICAO'] == str(ICAO)]

    for (f, row) in f_allo.iterrows():
        stand = f_allo.loc[f, 'Stand_Arrive']
        f_allo1 = (f_allo[f_allo['Stand_Arrive'] == stand]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
        for (i, row) in f_allo1.iloc[1:].iterrows():
            Arrival_Check =(f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'])
            Buffer = (f_allo1.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1.loc[i-1,'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('30 minutes'))
            if Buffer == True and Arrival_Check == True:
                continue
            else:
                index1 = int(f_allo1.loc[i, 'index'])
                Turnarounds.loc[index1, 'Stand_Arrive'] = ''
                Turnarounds.loc[index1, 'Stand_Depart'] = ''
                
        
def Remote_E():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_ERemote:
            if Turnarounds.index[i]  == ind_ERemote[0]:
                Turnarounds.loc[i, 'Stand_Arrive'] = E_Remote[0]
                Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive'] 
                continue
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_ERemote:
            if Turnarounds.index[i]  in ind_ERemote[1:]:
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                #df[['Stand_Arrive']] = df[['Stand_Arrive']].apply(pd.to_numeric)
                   #df = df.dropna(subset = ['Stand_Depart'])
                df = df[df['Stand_Arrive'].isin(E_Remote)]

                df1 = df.drop_duplicates('Stand_Arrive', keep = 'first')
                df1 = df1.sort_values(by='Scheduled_Timestamp_Depart',ascending= True).reset_index()

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
                        index = np.where(E_Remote == stand)[0]
                        stand = np.int(E_Remote[(index +1) % 8])
                        if stand in np.array(df1['Stand_Arrive']): 
                            f = int(df1.loc[df1['Stand_Arrive'] == stand, 'index'])
                                   
                            Arrival_Check = Turnarounds.loc[i,'Scheduled_Timestamp_Arrive'] > Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart']
                            Buffer = Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - Turnarounds.loc[Turnarounds.index[f],'Scheduled_Timestamp_Depart'] >= pd.to_timedelta('30 minutes')
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

def Remote_Eleft():
    for (i, row) in Turnarounds.iterrows():
       if Turnarounds.index[i] in ind_ERemote:
           if Turnarounds.loc[i, 'Stand_Arrive']  == 'R':
               
                   df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Depart.sum()))
                   df.index = df.index.droplevel(level=0)
                   df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                   df = df.reset_index()
                   
                   for k in F_Remote:
                       Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - pd.to_timedelta('30 minutes'))
                       Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] + pd.to_timedelta('30 minutes'))
                       df1 = df[df['Stand_Arrive'] == k]
                       if df1.empty == True:
                           Turnarounds.loc[i, 'Stand_Arrive'] = k
                           #Departure Stand
                           Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                           break
                       else:
                            for (j, rows) in df1.iterrows():
                                Arrival_Check = (Arrive < df1.loc[j, 'Scheduled_Timestamp_Arrive']) ==True and (df1.loc[j, 'Scheduled_Timestamp_Arrive']< Depart) == True
                                Depart_Check = (Arrive < df1.loc[j, 'Scheduled_Timestamp_Depart']) ==True and (df1.loc[j, 'Scheduled_Timestamp_Depart']< Depart) == True
                       
                                if Arrival_Check == False and Depart_Check == False:
                                    Turnarounds.loc[i, 'Stand_Arrive'] = k
                                    #Departure Stand
                                    Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                                    break
                                else:
                                    pass
    
                            
#-------------------------------------------------------------------------------------------------------------------------------------------#
        
def Pier_E():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_EPier:
            if Turnarounds.index[i]  == ind_EPier[0]:
                Turnarounds.loc[i, 'Stand_Arrive'] = E_Pier[0]
                Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive'] 
                continue
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_EPier:
            if Turnarounds.index[i] in ind_EPier[1:]:
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                   #df = df.dropna(subset = ['Stand_Depart'])
                df = df[df['Stand_Arrive'].isin(E_Pier)]
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
                        index = np.where(E_Pier == stand)[0]
                        stand = np.int(E_Pier[(index +1) % 15])
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
def E_to_FPier():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_EPier:
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
                           #print(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] , k)
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - pd.to_timedelta('30 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] + pd.to_timedelta('30 minutes'))
                        
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:
                        
                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']

#Check of errors in allocations and correct                            
    allo_checker('E', F_Pier)
    
                
#Reallocate to better gates
    for (i, row) in Turnarounds.iterrows():
      if Turnarounds.index[i] in ind_EPier:
          if Turnarounds.loc[i, 'Stand_Arrive']  == '':
            f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(F_Pier)]
            #f_allo = f_allo[f_allo['ICAO'] == 'E']
    
            for f in F_Pier:
                #stand = f_allo[f_allo['Stand_Arrive'] == f]
                f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= False).reset_index()
                f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', keep = 'first')
            
                Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1['Scheduled_Timestamp_Depart'])
                Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1['Scheduled_Timestamp_Depart'] >= pd.to_timedelta('30 minutes'))
                if all(Buffer) == True and all(Arrival_Check) == True:
                    index1 = int(f_allo1[ 'index'])
                    Turnarounds.loc[i, 'Stand_Arrive'] = int(f_allo1['Stand_Arrive'])
                    Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                    
                    
#----------------------------------------------------------------------------------------------------------------------------------------------------#
def E_to_ERemote():
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_EPier:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()
                       
                for k in E_Remote:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k, 'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k, 'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                           #print(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] , k)
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - pd.to_timedelta('30 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] + pd.to_timedelta('30 minutes'))
                        
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:
                        
                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']

#Check of errors in allocations and correct
    allo_checker('E', E_Remote)                            
               
#Reallocate to better gates
    
    for (i, row) in Turnarounds.iterrows():
      if Turnarounds.index[i] in ind_EPier:
          if Turnarounds.loc[i, 'Stand_Arrive']  == '':
            f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(E_Remote)]
            #f_allo = f_allo[f_allo['ICAO'] == 'E']

            for f in E_Remote:
                #stand = f_allo[f_allo['Stand_Arrive'] == f]
                f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
                f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', keep = 'first')

                Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1['Scheduled_Timestamp_Depart'])
                Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1['Scheduled_Timestamp_Depart'] >= pd.to_timedelta('30 minutes'))
                if all(Buffer) == True and all(Arrival_Check) == True:
                    index1 = int(f_allo1[ 'index'])
                    Turnarounds.loc[i, 'Stand_Arrive'] = int(f_allo1['Stand_Arrive'])
                    Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                    

    allo_checker('E', E_Remote)

#----------------------------------------------------------------------------------------------------------------------------------------------------#
def E_to_FRemote():                               
    for (i, row) in Turnarounds.iterrows():
        if Turnarounds.index[i] in ind_EPier:
            if Turnarounds.loc[i, 'Stand_Arrive'] == '':
                df = Turnarounds.groupby('Stand_Arrive').apply(lambda g: g.assign(col1_sum=g.Total_Pax_Arrive.sum()))
                df.index = df.index.droplevel(level=0)
                df = df.sort_values(by='Scheduled_Timestamp_Arrive',ascending= False)
                df = df.reset_index()
                       
                for k in F_Remote:    
                    SchedArrivals = df.loc[df['Stand_Arrive'] == k, 'Scheduled_Timestamp_Arrive']
                    SchedDeparts = df.loc[df['Stand_Arrive'] == k, 'Scheduled_Timestamp_Depart']
                    if SchedArrivals.empty == True and SchedDeparts.empty == True:
                        Turnarounds.loc[i, 'Stand_Arrive'] = k
                        #Departure Stand
                        Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                           #print(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] , k)
                        break
                    else:
                        Arrive = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - pd.to_timedelta('30 minutes'))
                        Depart = (Turnarounds.loc[i, 'Scheduled_Timestamp_Depart'] + pd.to_timedelta('30 minutes'))
                        
                        Arrival_Check2 = (SchedArrivals < Arrive).all() == True and (Arrive < SchedDeparts).all() == True
                        Depart_Check2 = (SchedArrivals < Depart).all() == True and (Depart < SchedDeparts).all() == True
                        if Arrival_Check2 == False and Depart_Check2 == False:
                        
                            Turnarounds.loc[i, 'Stand_Arrive'] = k
                            #Departure Stand
                            Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
                            

    allo_checker('E', F_Remote)

 
    for (i, row) in Turnarounds.iterrows():
      if Turnarounds.index[i] in ind_EPier:
          if Turnarounds.loc[i, 'Stand_Arrive']  == '':
            f_allo = Turnarounds[Turnarounds['Stand_Arrive'].isin(F_Remote)]
            #f_allo = f_allo[f_allo['ICAO'] == 'E']

            for f in F_Remote:
                #stand = f_allo[f_allo['Stand_Arrive'] == f]
                f_allo1 = (f_allo[f_allo['Stand_Arrive'] == f]).sort_values(by='Scheduled_Timestamp_Arrive',ascending= True).reset_index()
                f_allo1 = f_allo1.drop_duplicates('Stand_Arrive', keep = 'first')

                Arrival_Check =(Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] > f_allo1['Scheduled_Timestamp_Depart'])
                Buffer = (Turnarounds.loc[i, 'Scheduled_Timestamp_Arrive'] - f_allo1['Scheduled_Timestamp_Depart'] >= pd.to_timedelta('30 minutes'))
                if all(Buffer) == True and all(Arrival_Check) == True:
                    index1 = int(f_allo1[ 'index'])
                    Turnarounds.loc[i, 'Stand_Arrive'] = int(f_allo1['Stand_Arrive'])
                    Turnarounds.loc[i, 'Stand_Depart'] = Turnarounds.loc[i, 'Stand_Arrive']
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#                
def Schedule_E():
    #   Manipulate 'E' aircraft data to use in scheduling aglorithm    #
    E_fl()
    #   Allocate towed flights to Remote stands first - so they don't block up pier-served stands   #
    Remote_E()
    #   Allcoate unallocated towed flights to Remote 'F' stands   #
    Remote_Eleft()
    #   Allocate flights to the Pier-served stands  #
    Pier_E()
    #   Allcoate unallocated flights to pier-served 'F' stands   #
    E_to_FPier()
    #   Allcoate unallocated flights to Remote 'E' stands  #
    E_to_ERemote()
    #   Allocate unallocated flights to Remote 'F' stands   #
    E_to_FRemote()
