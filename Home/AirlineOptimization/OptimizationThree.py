'''
Created on 1 sept. 2021

@author: robert
'''
import os

import time
import unittest

from ortools.linear_solver import pywraplp
import numpy as np

from Home.AirlineCosts.AirlineAircraftRoutesCostsDatabaseFile import AirlineAircraftRoutesCosts
from Home.AirlineRoutes.AirlineRoutesAirportsReader import AirlineRoutesAirportsDataBase

from Home.AirlineFleet.AirlineFleetReader import AirlineFleetDataBase
from Home.AirlineFleet.AirlineFleetReader import AirlineAircraft

class TestMethods(unittest.TestCase):
#============================================

    def computeMaxOfFlightLegDurationHours(self, flightLegDepartureArrivalAirports , airlineAircraftICAOcodeList, airlineAircraftRoutesCosts): 
        ''' compute max of duration for all aircrafts '''
        maxDurationHours = 0.0
        
        departureAirportICAOcode = str(flightLegDepartureArrivalAirports).split("-")[0]
        arrivalAirportICAOcode = str(flightLegDepartureArrivalAirports).split("-")[1]
                    
        for i in range(len(airlineAircraftICAOcodeList)):
            aircraftICAOcode = airlineAircraftICAOcodeList[i]
                    
            durationHours = airlineAircraftRoutesCosts.getFlightLegDurationInHours(aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode)

            if ( durationHours > maxDurationHours):
                maxDurationHours = durationHours
            
        print ( "Flight Leg = {0} - max Duration = {1} Hours".format( flightLegDepartureArrivalAirports , maxDurationHours))
        return maxDurationHours
    
    
    def test_one(self):
    
        t0 = time.clock()
        
        # Create the MIP solver with the SCIP backend.
        solver = pywraplp.Solver.CreateSolver('SCIP')
        
        print ("-----------airline fleet aircrafts---------")
        airlineFleet = AirlineFleetDataBase()
        ret = airlineFleet.read()
        self.assertTrue( ret == True )
        ret = airlineFleet.extendDatabase()
        self.assertTrue( ret == True )

        print ("-----------airline fleet aircrafts with ICAO codes---------")

        airlineAircraftFullNameList = []
        airlineAircraftICAOcodeList = []
        airlineAircraftNumberOfSeatsList = []
        airlineAircraftInstancesList = []
        for airlineAircraft in airlineFleet.getAirlineAircrafts():
            self.assertTrue( isinstance( airlineAircraft , AirlineAircraft ) )
            if ( airlineAircraft.hasICAOcode() ):
                print ( airlineAircraft.getAircraftFullName() , "--->>>---" , airlineAircraft.getAircraftICAOcode() )
                
                aircraftICAOcode = airlineAircraft.getAircraftICAOcode()
                nbAircraftsAvailable = airlineFleet.getAircraftNumberOfInstances( aircraftICAOcode )
                for j in range(nbAircraftsAvailable):
                    ''' as there are once more than 99 aircrafts from the same type -> need to pad with 00 zeros '''
                    acInstance =  '{0}-{1}'.format( aircraftICAOcode , str(j).zfill(3)) 
                    
                    airlineAircraftInstancesList.append( acInstance )
                    airlineAircraftFullNameList.append( airlineAircraft.getAircraftFullName() )
                    airlineAircraftICAOcodeList.append( airlineAircraft.getAircraftICAOcode() )
                    airlineAircraftNumberOfSeatsList.append( airlineAircraft.getMaximumNumberOfPassengers())

                
        print ( "length of airline aircraft list = {0}".format( len ( airlineAircraftICAOcodeList ) ) )
        
        print ("------------- airline routes reader --------------")
        airlineRoutesAirports = AirlineRoutesAirportsDataBase()
        ret = airlineRoutesAirports.read()
        self.assertTrue( ret == True )
        
        print ("------------- airline routes airports OR flight legs --------------")
        airlineFlightLegsList = []
        for route in airlineRoutesAirports.getRoutes():
            print (route)
            airlineFlightLegsList.append( route.getFlightLegAsString() )

        print ( "length of airline flight legs list = {0}".format( len ( airlineFlightLegsList ) ) )
        
        
        print ("-----------airline routes costs---------")

        airlineAircraftRoutesCosts = AirlineAircraftRoutesCosts()
        airlineCosts_np_array = airlineAircraftRoutesCosts.read()
        print ( airlineCosts_np_array )
        self.assertTrue( airlineCosts_np_array is not None )

        
        ''' define a daily schedule made of minutes from 00h00 to 23h59 '''
        dailyHoursMinutes = []
        dailyMinutesSpan = 2360
        for i in range(dailyMinutesSpan):
            print ( i )
            dailyHoursMinutes.append( i )
            
        schedule = {}
        for n in range(len(airlineAircraftInstancesList)):
            acInstance = airlineAircraftInstancesList[n]
            for d in range(len(airlineFlightLegsList)):
                flightLeg = airlineFlightLegsList[d]
                for s in range(len(dailyHoursMinutes)):
                    dailyHour = dailyHoursMinutes[s]
                    key = '{0} - {1} - {2}'.format( acInstance , flightLeg, dailyHour) 
                    print ( key )
                    schedule[(n, d, s)] = solver.IntVar(0, 1, key)
                    
        #shifts[(n, d, s)] equals 1 if shift s is assigned to nurse n on day d, and 0 otherwise.

        ''' assign aircrafts to shifts / schedules '''
        for d in range(len(airlineFlightLegsList)):
            for s in range(len(dailyHoursMinutes)):
                solver.Add(sum(schedule[(n, d, s)] for n in range(len(airlineAircraftInstancesList))) == 1)
        
        ''' Next, here's the code that requires that each nurse works at most one shift per day. '''
        for n in range(len(airlineAircraftInstancesList)):
            for d in range(len(airlineFlightLegsList)):
                solver.Add(sum(schedule[(n, d, s)] for s in  range(len(dailyHoursMinutes))) <= 1)
                
        ''' frequency = number of flights for each flight leg per day '''
        ''' start with 20 hours a day and divide by flight duration + Duration Turn Around Time '''
        flightLegFrequency = {}
        flightLegDurationHours = {}
        turnAroundDurationHours = 0.5
        for d in range(len(airlineFlightLegsList)):
            flightLegStr = airlineFlightLegsList[j]
            #print ( flightLegStr )
            flightLegDurationHours[d] = self.computeMaxOfFlightLegDurationHours(flightLegStr , airlineAircraftICAOcodeList, airlineAircraftRoutesCosts)
            flightLegFrequency[d] =  int ( 20. / ( flightLegDurationHours[d] + turnAroundDurationHours ) )
            print ( "flight leg = {0} - max flight leg duration in hours {1} - frequency for 20 hours = {2}".format( flightLegStr , flightLegDurationHours[d] , flightLegFrequency[d]) )


        "for i in range(len(airports)):\n",
        "    for j in range(len(airports)):\n",
        "        prob += pulp.lpSum(20 * x[i][j][k] for k in range(len(aircrafts))) >= frequency[i][j] * time_flight[i][j],'Availability Constraint: {} to {}'.format(airports[i],airports[j])\n",
        for d in range(len(airlineFlightLegsList)):
            for s in range(len(dailyHoursMinutes)):
                solver.Add(sum( [20 * schedule[n, d, s] for n in range(len(airlineAircraftInstancesList))] ) >= ( flightLegFrequency[d] * flightLegDurationHours[d] ) )

        
        print (' --------- invoke the solver -------------')
        status = solver.Solve()
        
        print ("---------- solving -----------")
        print ('----- solver status= {0} - optimal= {1} - feasible= {2}'.format(status, pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE))
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print ('solver status - Optimal = {0} - Feasible = {1} - solver result value = {0}'.format(pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE, status))

        else:
            print(" solver status is neither OPTIMAL nor FEASIBLE")
                
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
           

if __name__ == '__main__':
    unittest.main()