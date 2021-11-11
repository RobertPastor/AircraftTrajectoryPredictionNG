'''
Created on 9 oct. 2021

@author: robert

https://simpleflying.com/turnaround-time-importance/

Turnaround time
The turnaround time (TAT) of an aircraft is the time that passes from landing until take off for a new flight. 
While stationary, the airline is not earning any revenue with its plane, while facing many costs at the same time. 
Examples include airport fees, leasing costs or depreciation, and some fixed costs, which can be partially attributed to each flight. 
On top of that, one should not forget about the opportunity cost of the tickets, which would have been sold, if the plane was not grounded.

Providing a numerical estimate of the hourly cost of a grounded aircraft is quite complicated, given its high variability. 
There are many factors affecting cost-of-grounding, such as aircraft financing, aircraft type, route, fuel expenses, load factors, and more. 
Turnaround becomes more critical in short-haul operations, where they account for a higher percentage of the flight time. 
This is why efficiencies there are more important.




Let’s assume that an average short-haul airliner will fly one-hour segments all day long, starting at 08:00 and finishing at 22:00. 
If the turnaround time is roughly an hour, the daily operational window will suffice for seven flights (and one hour spare). 
However, if the turnaround time was shortened by 8 minutes or 13%, the airline would be able to operate an extra flight that day, potentially increasing the revenues by tens of thousands of dollars.
This example explains the importance of fighting for every minute when it comes to taxiing, unloading, reloading, boarding, and pushback.

Many airlines, especially the low-cost ones, have achieved a close-to mastery in turnaround time efficiency. 
The LCC’s begin boarding and line people up, long before the airplane touches down. 
It takes Ryanair just 25 minutes to complete this fast-paced, challenging process, while Wizzair oscillates around 30 minutes, similarly to Southwest. 
For most traditional carriers, such as American Airlines, Lufthansa, or British Airways, the turnaround-times average around an hour.


'''


class AirlineTurnAroundTimes(object):
    pass

    def __init__(self):
        pass


class AirlineTurnAroundTimesDatabase(object):
    ''' defines a Turn Time duration in seconds (or hours and minutes) for a given aircraft of the fleet 
    to turn from the arrival airport to the same departure airport '''
    
    ''' the airport city playing both a role or arrival and of departure airport '''
    airportICAOcode = ""

    def __init__(self):
        pass
        #self.airportCity = _airportICAOcode
        #self.turnAroundTimeInSeconds = _turnAroundTimeInSeconds
        
    def getTurnAroundTimeInSeconds(self,  aircraftICAOcode , airportICAOcode):
        ''' return 1 hour default value '''
        ''' the bigger the aircraft , the more number of seats, the more increased turn time is needed '''
        ''' the bigger the airport, the more crowed airport, the more increased turn time is needed '''
        return ( 1 * 60 * 60 )
    
    def getTurnAroundTimeInHours(self,  aircraftICAOcode , airportICAOcode):
        ''' return 1 hour default value '''
        ''' the bigger the aircraft , the more number of seats, the more increased turn time is needed '''
        ''' the bigger the airport, the more crowed airport, the more increased turn time is needed '''
        return ( 1. )
    
    