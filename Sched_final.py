# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 00:11:59 2018

@author: User
"""



def Daily_Sched(date):
    Schedule_F()
    Schedule_E()
    Schedule_D()
    Schedule_C()
    
    #Save file
    Turnarounds.to_csv( 'Allocation_'+date+'.csv', index=False)
    
def Monthly_Sched(month):

    global schedule,Schedule
    #update datatypes for the dates and times
    flight_schedule[['Scheduled.Timestamp']] = flight_schedule[['Scheduled.Timestamp']]\
              .apply(pd.to_datetime, dayfirst = True)
#get terminal 5 data(schedule['Terminal'] == 5) &
    Schedule = flight_schedule.loc[(flight_schedule['Scheduled.Timestamp']\
                                    .dt.month == month) & \
                                    (flight_schedule['Terminal'] == 5)]
    
    for i, day in Schedule.groupby(Schedule['Scheduled.Timestamp'].dt.date):
        schedule = Schedule.loc[(Schedule['Scheduled.Timestamp'].dt.date == i)]
        Sort_cols()
        Create_Turns()
        Turnaround()
        Splitting()
        final_Turnarounds()
        
        Daily_Sched(i)
        # save to new dir   
        Turnarounds.to_csv(r"C:/Users/User/Documents/Paba/DISS/July/"+ "Turnarounds"+str(i)+'.csv', index=False)
