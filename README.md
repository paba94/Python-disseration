# Python-disseration
The project focused on solving a aircraft-stand allocation problem for Terminal 5 at Heathrow Airport, through a heuristic approach.  
The 2 primary objectives for this project were:
1.	Automate the data manipulation process to compute the turnaround times of flights.
2.	Construct and implement a heuristic that allocates stands to aircraft such the number of pier-served passengers would be maximised.

The other aims of the project were to have:
1.  an automated data manipulation process that was feasible with yearly flight data;
2.	a constructed heuristic that assigned a feasible stand to all the flights;
3.	a heuristic that accounted for the potential delays or early arrivals of flights.


Methodology

The flight turnarounds were calculated, and the turnarounds splitting was performed. This separated the flights into “overnight parking operations” and “stand operations” that arrive and leave on the same day.

The Stand Allocation Heuristic formulated was a hybrid heuristic that combined concepts from the Greedy heuristic and the Breakout Local Search heuristic. It followed a “first come, first assigned” policy because it is a common practise in the industry. Thus, flights with the earliest arrival times were chosen greedily to be allocated first. If more than one feasible pier-served or remote stand was available, the heuristic chose to allocate to the stand that had served the highest number of passengers.

The heuristic produced an initial schedule which was then checked to identify flights, in each stand, that didn’t adhere to the buffer times restriction. If any overlapping existed, these flights were removed from the schedule and reallocated to other feasible stands. 

The procedure of the Stand Allocation heuristic segregated the flight data by fleet type (F, E, D, C) and made allocations one fleet at a time. This was because the compatibility of stands depended strongly on the size of the aircraft. This was because stands that could facilitate larger aircraft were big enough to hold smaller aircraft but not vice versa. 

In industry, airport planners create the stand allocation schedules daily due to the high probability of changes in the flight schedule. For this reason, the Stand Allocation heuristic was also designed to work with daily flight data. 
	
All the models, for data manipulation and the heuristic, were made using the programming language Python. The models were then tested on the flight schedule for the 21st July 2017.
