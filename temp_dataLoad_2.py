# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 22:31:33 2018

@author: Paba
"""

import pandas as pd
import numpy as np

# needs input of the file names for flight schedule & airport data #
def Load_File(Schedule_file, Airport_file): 

    global flight_schedule, Airport_Details
    #Read flight schedule
    flight_schedule = pd.read_csv('C:/Users/Paba/OneDrive - University of Southampton/Disseration/Data_Manipulation/'\
                           + Schedule_file)
    #Drop irrelevant data
    flight_schedule = flight_schedule.drop(columns = ['Scheduled.Date', 'Scheduled.Time',
                             'Stand.Date', 'Stand.Time',
                             'Actual.Date', 'Actual.Time', 'Flight.Type',
                             'Actual.Timestamp','Stand.Timestamp'])
    
    fields = ['AIRPORT_IATA_CODE', 'AIRPORT_CITY', 'AIRPORT_COUNTRY']
    #Read airport details
    Airport_DF = pd.read_csv('C:/Users/Paba/OneDrive - University of Southampton/Disseration/Data_Manipulation/'\
                             + Airport_file)
    #Exctract useful information only
    Airport_Details = pd.DataFrame(columns=fields, data=Airport_DF[fields])

def Select_Data(month, date):
    global schedule
    #update datatypes for the dates and times
    flight_schedule[['Scheduled.Timestamp']] = flight_schedule[['Scheduled.Timestamp']]\
              .apply(pd.to_datetime, dayfirst = True)

    schedule = flight_schedule.loc[(flight_schedule['Scheduled.Timestamp'].dt.month == month)  \
                                   & (flight_schedule['Scheduled.Timestamp'].dt.day == date)\
                                   & (flight_schedule['Terminal'] == 5)]
  

def Sort_cols():
    global schedule, cols
    
    cols = schedule.columns.tolist()
    cols.insert(0, cols.pop(cols.index('Reg.No')))
    schedule = schedule.loc[:, cols]
    schedule['ID'] = schedule.index
    #schedule = schedule[cols]

def Create_Turns():
#sort schedule by Origin/Destination, Registration & Scheduled Time
    sort_cols = ['ID','Reg.No', 'Scheduled.Timestamp']
    schedule.sort_values(by=sort_cols, inplace = True)
#convert index into column and create new shifted id
    schedule['nextID'] = schedule.groupby(sort_cols[1])['ID'].shift(1)
    
#filter arrivals & departures and outer join by IDs
#create turnsarounds table 
    global turns
    turns = schedule[schedule['A.D'] == 'A'].merge(schedule[schedule['A.D'] == 'D'],
                           how='outer',
                           left_on= 'ID',
                           right_on='nextID',
                           suffixes=('_Arr','_Dep')) 
#coalesce turnarounds to better format
    for c in sort_cols:
        turns['sort_'+ c] = turns[c + '_Arr']\
                                    .combine_first(turns[c + '_Dep'])
    turns.sort_values(by=['sort_{}'.format(c) for c in sort_cols], 
                                inplace = True)
    turns = turns[['{}_Arr'.format(c) for c in cols] +
                               ['{}_Dep'.format(c) for c in cols]]

#Create final format of turnarounds table
def Turnaround():
    global Turnarounds,Turnarounds_loc
    
    Cols = ['Airline','Aircraft_Gen','Aircraft_Spec','ICAO','Reg_No',
            'Scheduled_Timestamp_Arrive',
            'Flight_No_Arrive',
            'Terminal_Arrive',
            'Origin',
            'Seats_Arrive',
            'Total_Pax_Arrive',
            'Transfer_Pax_Arrive',
            'Transit_Pax_Arrive',
            'Load_Factor_Arrive',
            'Transfer_Share_Arrive',
            'Scheduled_Timestamp_Depart',
            'Flight_No_Depart',
            'Terminal_Depart',
            'Destination',
            'Seats_Depart',
            'Total_Pax_Depart',
            'Transfer_Pax_Depart',
            'Transit_Pax_Depart',
            'Load_Factor_Depart',
            'Transfer_Share_Depart']
    
    Turnarounds = pd.DataFrame(columns = Cols)
    Turnarounds['Airline'] = turns['Airline_Arr'].fillna(turns['Airline_Dep'])
    Turnarounds['Aircraft_Gen'] = turns['Aircraft.General_Arr'].fillna(turns['Aircraft.General_Dep'])
    Turnarounds['Aircraft_Spec'] = turns['Aircraft.Specific_Arr'].fillna(turns['Aircraft.Specific_Dep'])
    Turnarounds['ICAO'] = turns['ICAO.Code_Arr'].fillna(turns['ICAO.Code_Dep'])
    Turnarounds['Reg_No'] = turns['Reg.No_Arr'].fillna(turns['Reg.No_Dep'])
#input arrivals info
    Turnarounds[['Scheduled_Timestamp_Arrive',
                'Flight_No_Arrive',
                'Terminal_Arrive',
                'Origin',
                'Seats_Arrive',
                'Total_Pax_Arrive',
                'Transfer_Pax_Arrive',
                'Transit_Pax_Arrive',
                'Load_Factor_Arrive',
                'Transfer_Share_Arrive']] = turns[['Scheduled.Timestamp_Arr',
                                                    'Flight.No_Arr',
                                                    'Terminal_Arr',
                                                    'O.D_Arr',
                                                    'Seats_Arr',
                                                    'Total.Pax_Arr',
                                                    'Transfer.Pax_Arr',
                                                    'Transit.Pax_Arr',
                                                    'Load.Factor_Arr',
                                                    'Transfer.Share_Arr']]
#input departure info
    Turnarounds[['Scheduled_Timestamp_Depart',
                'Flight_No_Depart',
                'Terminal_Depart',
                'Destination',
                'Seats_Depart',
                'Total_Pax_Depart',
                'Transfer_Pax_Depart',
                'Transit_Pax_Depart',
                'Load_Factor_Depart',
                'Transfer_Share_Depart']] = turns[['Scheduled.Timestamp_Dep',
                                                    'Flight.No_Dep',
                                                    'Terminal_Dep',
                                                    'O.D_Dep',
                                                    'Seats_Dep',
                                                    'Total.Pax_Dep',
                                                    'Transfer.Pax_Dep',
                                                    'Transit.Pax_Dep',
                                                    'Load.Factor_Dep',
                                                    'Transfer.Share_Dep']]  
    
    
    #Turnarounds_loc = Turnarounds.copy()
    Turnarounds['Stand_Arrive'] =""
    Turnarounds['Origin_City'] =""
    Turnarounds['Origin_Country'] =""
    Turnarounds['Stand_Depart'] =""
    Turnarounds['Dest_City'] =""
    Turnarounds['Dest_Country'] =""
    Turnarounds['Turnover'] = ""
 
    cols2 = Turnarounds.columns.tolist()
    # reorder columns
    cols2 = cols2[:8] + [cols2[-7]] +[cols2[-6]] +[cols2[-5]]+ cols2[8:18] + [cols2[-4]]+ [cols2[-3]] + [cols2[-2]]+ cols2[18:25]+[cols2[-1]]
    # "commit" the reordering
    Turnarounds = Turnarounds[cols2]

#def cities():
    Turnarounds['Origin_City'] = Turnarounds['Origin'].map(Airport_Details.set_index('AIRPORT_IATA_CODE')['AIRPORT_CITY'])
    Turnarounds['Origin_Country'] = Turnarounds['Origin'].map(Airport_Details.set_index('AIRPORT_IATA_CODE')['AIRPORT_COUNTRY'])
    Turnarounds['Dest_City'] = Turnarounds['Destination'].map(Airport_Details.set_index('AIRPORT_IATA_CODE')['AIRPORT_CITY'])
    Turnarounds['Dest_Country'] = Turnarounds['Destination'].map(Airport_Details.set_index('AIRPORT_IATA_CODE')['AIRPORT_COUNTRY'])
    Turnarounds['Turnover'] = pd.to_timedelta((Turnarounds['Scheduled_Timestamp_Depart'] - Turnarounds['Scheduled_Timestamp_Arrive']))
    
#def Sort_Turns():
    
    Turnarounds = Turnarounds.sort_values(by=['Scheduled_Timestamp_Arrive'], ascending = [True])
    
def Splitting():
    global Turn_NaTDep, Turn_NaTArr, Turn_8hrsE, Turn_8hrsF, Turn_11hrsC, Turn_11hrsD, Turn_unsplit
      
    Turn_NaTDep = Turnarounds[pd.isnull(Turnarounds['Scheduled_Timestamp_Depart']) == True]
    Turn_NaTArr = Turnarounds[pd.isnull(Turnarounds['Scheduled_Timestamp_Arrive']) == True]
    Turn_8hrsF = Turnarounds.loc[(Turnarounds['Turnover'] > pd.to_timedelta('480 minutes')) & (Turnarounds['ICAO'] == 'F')]
    Turn_8hrsE = Turnarounds.loc[(Turnarounds['Turnover'] > pd.to_timedelta('480 minutes')) & (Turnarounds['ICAO'] == 'E')]
    Turn_11hrsC = Turnarounds.loc[(Turnarounds['Turnover'] > pd.to_timedelta('690 minutes')) & (Turnarounds['ICAO'] == 'C')]
    Turn_11hrsD = Turnarounds.loc[(Turnarounds['Turnover'] > pd.to_timedelta('690 minutes')) & (Turnarounds['ICAO'] == 'D')]
   
    Turn_unsplit = pd.concat([Turnarounds,Turn_8hrsE, Turn_8hrsF, Turn_11hrsC, Turn_11hrsD, Turn_NaTArr, Turn_NaTDep]).drop_duplicates(keep= False)
#################################################################################################################################
    
    Turn_NaTDep = pd.DataFrame(np.repeat(Turn_NaTDep.values,2,axis=0), columns=Turnarounds.columns)

    for i in Turn_NaTDep.index:
        TimeStamp = pd.to_datetime(str((Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Arrive']).date() + pd.to_timedelta('1 day')) + ' 12:00AM')
        if Turn_NaTDep.loc[i, 'ICAO'] == 'C':
            if (pd.isnull(Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart'])) == True:
                Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('45 minutes')
 
                Turn_NaTDep.loc[i+1 , 'Scheduled_Timestamp_Arrive'] = Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart']
                Turn_NaTDep.loc[i+1, 'Scheduled_Timestamp_Depart'] = TimeStamp
                Turn_NaTDep.loc[i+1, 'Stand_Arrive'] = 'R'
            else:
                pass
        if Turn_NaTDep.loc[i, 'ICAO'] == 'D':
            if (pd.isnull(Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart'])) == True:
                Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('60 minutes')
          
                Turn_NaTDep.loc[i+1 , 'Scheduled_Timestamp_Arrive'] = Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart']
                Turn_NaTDep.loc[i+1, 'Scheduled_Timestamp_Depart'] = TimeStamp
                Turn_NaTDep.loc[i+1, 'Stand_Arrive'] = 'R'
            else:
                pass
        if Turn_NaTDep.loc[i, 'ICAO'] == 'E':
            if (pd.isnull(Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart'])) == True:
                Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('90 minutes')

                Turn_NaTDep.loc[i+1 , 'Scheduled_Timestamp_Arrive'] = Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart']
                Turn_NaTDep.loc[i+1, 'Scheduled_Timestamp_Depart'] = TimeStamp
                Turn_NaTDep.loc[i+1, 'Stand_Arrive'] = 'R'
            else:
                pass
        if Turn_NaTDep.loc[i, 'ICAO'] == 'F':
            if (pd.isnull(Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart'])) == True:
                Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('100 minutes')

                Turn_NaTDep.loc[i+1 , 'Scheduled_Timestamp_Arrive'] = Turn_NaTDep.loc[i, 'Scheduled_Timestamp_Depart']
                Turn_NaTDep.loc[i+1, 'Scheduled_Timestamp_Depart'] = TimeStamp
                Turn_NaTDep.loc[i+1, 'Stand_Arrive'] = 'R'
            else:
                pass
#################################################################################################################
    
    Turn_NaTArr = pd.DataFrame(np.repeat(Turn_NaTArr.values,2,axis=0), columns=Turnarounds.columns)

    for i in Turn_NaTArr.index:
        TimeStamp =pd.to_datetime(str((Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart']).date()) + ' 12:00AM')
        if Turn_NaTArr.loc[i, 'ICAO'] == 'C':
            if (pd.isnull(Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Arrive'])) == True:
                Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Arrive'] = TimeStamp
                Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart'] - pd.to_timedelta('45 minutes')
                Turn_NaTArr.loc[i, 'Stand_Arrive'] = 'R'
                
                Turn_NaTArr.loc[i+1 , 'Scheduled_Timestamp_Arrive'] = Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart']
            else:
                pass
        if Turn_NaTArr.loc[i, 'ICAO'] == 'D':
            if (pd.isnull(Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Arrive'])) == True:
                Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Arrive'] = TimeStamp
                Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart'] - pd.to_timedelta('60 minutes')
                Turn_NaTArr.loc[i, 'Stand_Arrive'] = 'R'

                Turn_NaTArr.loc[i+1 , 'Scheduled_Timestamp_Arrive'] = Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart']
            else:
                pass
        if Turn_NaTArr.loc[i, 'ICAO'] == 'E':
            if (pd.isnull(Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Arrive'])) == True:
                Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Arrive'] = TimeStamp
                Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart'] - pd.to_timedelta('100 minutes')
                Turn_NaTArr.loc[i, 'Stand_Arrive'] = 'R'
                
                Turn_NaTArr.loc[i+1 , 'Scheduled_Timestamp_Arrive'] = Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart']
            else:
                pass
        if Turn_NaTArr.loc[i, 'ICAO'] == 'F':
            if (pd.isnull(Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Arrive'])) == True:
                Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Arrive'] = TimeStamp
                Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart'] - pd.to_timedelta('120 minutes')
                Turn_NaTArr.loc[i, 'Stand_Arrive'] = 'R'
                
                Turn_NaTArr.loc[i+1 , 'Scheduled_Timestamp_Arrive'] = Turn_NaTArr.loc[i, 'Scheduled_Timestamp_Depart']
            else:
                pass
########################################################################################################################
   
    Turn_8hrsF = pd.DataFrame(np.repeat(Turn_8hrsF.values,3,axis=0), columns=Turnarounds.columns)

    for i in Turn_8hrsF.index:
            if i == 0:
                Turn_8hrsF.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_8hrsF.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('100 minutes')
            elif i in Turn_8hrsF.index[1: len(Turn_8hrsF)-1]:
                if Turn_8hrsF.loc[i, 'Reg_No'] == Turn_8hrsF.loc[i-1, 'Reg_No'] == Turn_8hrsF.loc[i+1, 'Reg_No']:
                    Turn_8hrsF.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_8hrsF.loc[i-1, 'Scheduled_Timestamp_Depart']
                    Turn_8hrsF.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_8hrsF.loc[i, 'Scheduled_Timestamp_Depart'] - pd.to_timedelta('120 minutes')
                    Turn_8hrsF.loc[i, 'Stand_Arrive'] = 'R'
                    continue
                elif Turn_8hrsF.loc[i, 'Reg_No'] == Turn_8hrsF.loc[i-1, 'Reg_No'] != Turn_8hrsF.loc[i+1, 'Reg_No']:
                    Turn_8hrsF.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_8hrsF.loc[i-1, 'Scheduled_Timestamp_Depart']
                    continue
                elif Turn_8hrsF.loc[i, 'Reg_No'] == Turn_8hrsF.loc[i+1, 'Reg_No'] != Turn_8hrsF.loc[i-1, 'Reg_No']:
                    Turn_8hrsF.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_8hrsF.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('100 minutes')
            elif i == len(Turn_8hrsF)-1:
                Turn_8hrsF.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_8hrsF.loc[i-1, 'Scheduled_Timestamp_Depart']
#################################################################################################################################
    
    Turn_8hrsE = pd.DataFrame(np.repeat(Turn_8hrsE.values,3,axis=0), columns=Turnarounds.columns)

    for i in Turn_8hrsE.index:
            if i == 0:
                Turn_8hrsE.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_8hrsE.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('90 minutes')
            elif i in Turn_8hrsE.index[1: len(Turn_8hrsE)-1]:
                if Turn_8hrsE.loc[i, 'Reg_No'] == Turn_8hrsE.loc[i-1, 'Reg_No'] == Turn_8hrsE.loc[i+1, 'Reg_No']:
                    Turn_8hrsE.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_8hrsE.loc[i-1, 'Scheduled_Timestamp_Depart']
                    Turn_8hrsE.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_8hrsE.loc[i, 'Scheduled_Timestamp_Depart'] - pd.to_timedelta('100 minutes')
                    Turn_8hrsE.loc[i, 'Stand_Arrive'] = 'R'
                    continue
                elif Turn_8hrsE.loc[i, 'Reg_No'] == Turn_8hrsE.loc[i-1, 'Reg_No'] != Turn_8hrsE.loc[i+1, 'Reg_No']:
                    Turn_8hrsE.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_8hrsE.loc[i-1, 'Scheduled_Timestamp_Depart']
                    continue
                elif Turn_8hrsE.loc[i, 'Reg_No'] == Turn_8hrsE.loc[i+1, 'Reg_No'] != Turn_8hrsE.loc[i-1, 'Reg_No']:
                    Turn_8hrsE.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_8hrsE.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('90 minutes')
            elif i == len(Turn_8hrsE)-1:
                Turn_8hrsE.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_8hrsE.loc[i-1, 'Scheduled_Timestamp_Depart']
####################################################    C   #########################################################################
    
    Turn_11hrsC = pd.DataFrame(np.repeat(Turn_11hrsC.values,3,axis=0), columns=Turnarounds.columns)

    for i in Turn_11hrsC.index:
            if i == 0:
                Turn_11hrsC.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_11hrsC.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('45 minutes')
            elif i in Turn_11hrsC.index[1: len(Turn_11hrsC)-1]:
                if Turn_11hrsC.loc[i, 'Reg_No'] == Turn_11hrsC.loc[i-1, 'Reg_No'] == Turn_11hrsC.loc[i+1, 'Reg_No']:
                    Turn_11hrsC.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_11hrsC.loc[i-1, 'Scheduled_Timestamp_Depart']
                    Turn_11hrsC.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_11hrsC.loc[i, 'Scheduled_Timestamp_Depart'] - pd.to_timedelta('45 minutes')
                    Turn_11hrsC.loc[i, 'Stand_Arrive'] = 'R'
                    continue
                elif Turn_11hrsC.loc[i, 'Reg_No'] == Turn_11hrsC.loc[i-1, 'Reg_No'] != Turn_11hrsC.loc[i+1, 'Reg_No']:
                    Turn_11hrsC.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_11hrsC.loc[i-1, 'Scheduled_Timestamp_Depart']
                    continue
                elif Turn_11hrsC.loc[i, 'Reg_No'] == Turn_11hrsC.loc[i+1, 'Reg_No'] != Turn_11hrsC.loc[i-1, 'Reg_No']:
                    Turn_11hrsC.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_11hrsC.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('45 minutes')
            elif i == len(Turn_11hrsC)-1:
                Turn_11hrsC.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_11hrsC.loc[i-1, 'Scheduled_Timestamp_Depart']

##################################################################################################################################

    Turn_11hrsD = pd.DataFrame(np.repeat(Turn_11hrsD.values,3,axis=0), columns=Turnarounds.columns)

    for i in Turn_11hrsD.index:
            if i == 0:
                Turn_11hrsD.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_11hrsD.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('45 minutes')
            elif i in Turn_11hrsD.index[1: len(Turn_11hrsD)-1]:
                if Turn_11hrsD.loc[i, 'Reg_No'] == Turn_11hrsD.loc[i-1, 'Reg_No'] == Turn_11hrsD.loc[i+1, 'Reg_No']:
                    Turn_11hrsD.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_11hrsD.loc[i-1, 'Scheduled_Timestamp_Depart']
                    Turn_11hrsD.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_11hrsD.loc[i, 'Scheduled_Timestamp_Depart'] - pd.to_timedelta('45 minutes')
                    Turn_11hrsD.loc[i, 'Stand_Arrive'] = 'R'
                    continue
                elif Turn_11hrsD.loc[i, 'Reg_No'] == Turn_11hrsD.loc[i-1, 'Reg_No'] != Turn_11hrsD.loc[i+1, 'Reg_No']:
                    Turn_11hrsD.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_11hrsD.loc[i-1, 'Scheduled_Timestamp_Depart']
                    continue
                elif Turn_11hrsD.loc[i, 'Reg_No'] == Turn_11hrsD.loc[i+1, 'Reg_No'] != Turn_11hrsD.loc[i-1, 'Reg_No']:
                    Turn_11hrsD.loc[i, 'Scheduled_Timestamp_Depart'] = Turn_11hrsD.loc[i, 'Scheduled_Timestamp_Arrive'] + pd.to_timedelta('45 minutes')
            elif i == len(Turn_11hrsD)-1:
                Turn_11hrsD.loc[i , 'Scheduled_Timestamp_Arrive'] = Turn_11hrsD.loc[i-1, 'Scheduled_Timestamp_Depart']
##################################################################################################################################
    
    
# Combine split and unsplit turnarounds to create new turnarounds database #
def final_Turnarounds():
    global Turnarounds
    Turnarounds = pd.concat([Turn_unsplit, Turn_11hrsC, Turn_11hrsD, Turn_8hrsE, Turn_8hrsF, Turn_NaTArr, Turn_NaTDep])
    # Re-calculate Turnaround times
    Turnarounds['Turnover'] = pd.to_timedelta((Turnarounds['Scheduled_Timestamp_Depart'] - Turnarounds['Scheduled_Timestamp_Arrive']))

    Turnarounds = Turnarounds.sort_values(by=['Scheduled_Timestamp_Arrive'], ascending = [True]).reset_index(drop = True)
    Turnarounds.to_csv("Turnarounds_Final.csv", index=False)