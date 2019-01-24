# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 11:55:29 2018

@author: Paba
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 22:31:33 2018

@author: Paba
"""

import pandas as pd

#import raw rt file
def Load_File(FilePath):
#FilePath = 'C:/Users/User/OneDrive - University of Southampton/Disseration/Data_Manipulation/Schedule_2017.csv'
    global schedule
    schedule = pd.read_csv(FilePath)
    schedule = schedule.drop(columns = ['Scheduled.Date', 'Scheduled.Time',
                             'Stand.Date', 'Stand.Time',
                             'Actual.Date', 'Actual.Time'])
def Select_Data():
    global schedule
    #update datatypes for the dates and times
    schedule[['Scheduled.Timestamp']] = schedule[['Scheduled.Timestamp']]\
              .apply(pd.to_datetime, dayfirst = True)
#get terminal 5 data(schedule['Terminal'] == 5) &
    schedule = schedule[schedule['Scheduled.Timestamp'].dt.month == 7]
    schedule = schedule[schedule['Scheduled.Timestamp'].dt.day == 21]
    
def Sort_cols():
    global schedule, cols
    
    cols = schedule.columns.tolist()
    cols.insert(0, cols.pop(cols.index('Reg.No')))
    schedule = schedule.loc[:, cols]
    #schedule = schedule[cols]

#create arrivals and departures
def Arr_Dep():
    global Arrive
    Arrive = schedule[schedule['A.D'] == 'A']
    
    global Depart
    Depart = schedule[schedule['A.D'] == 'D']

def Create_Turns():
#sort schedule by Origin/Destination, Registration & Scheduled Time
    #sort_cols = ['Reg.No', 'Scheduled.Timestamp']
    #schedule.sort_values(by=sort_cols, inplace = True)
#convert index into column and create new shifted id
    #schedule['nextID'] = schedule.groupby(sort_cols[0])['Reg.No'].shift(1)
    
#filter arrivals & departures and outer join by IDs
#create turnsarounds table 
    global turnarounds
    turnarounds = Arrive.merge( Depart,
                           how='left',
                           on = 'Reg.No',
                           suffixes=('_Arrival','_Depart')) 
#coalesce turnarounds to better format
 
#ensure the arrival is always before departure
    #turnarounds = turnarounds[turnarounds['Scheduled.Timestamp_Arrival'] < turnarounds['Scheduled.Timestamp_Depart']]
    #turnarounds = turnarounds[turnarounds['Scheduled.Timestamp_Arrival'].dt.hour < turnarounds['Scheduled.Timestamp_Depart'].dt.hour]
    #turnarounds =turnarounds.drop_duplicates(subset = ['Reg.No_Arrival', 'Scheduled.Timestamp_Arrival'], keep = 'first')
    
   
    
                
    