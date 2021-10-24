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

from Home.AirlineTurnAroundTimes.AirlineTurnTimesFile import AirlineTurnAroundTimesDatabase

kerosene_kilo_to_US_gallons = 0.33
US_gallon_to_US_dollars = 3.25

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
        for airlineAircraft in airlineFleet.getAirlineAircrafts():
            self.assertTrue( isinstance( airlineAircraft , AirlineAircraft ) )
            if ( airlineAircraft.hasICAOcode() ):
                print ( airlineAircraft.getAircraftFullName() , "--->>>---" , airlineAircraft.getAircraftICAOcode() )
                
                #nbAircraftsAvailable = airlineFleet.getAircraftNumberOfInstances( aircraftICAOcode )
                
                airlineAircraftFullNameList.append( airlineAircraft.getAircraftFullName() )
                airlineAircraftICAOcodeList.append( airlineAircraft.getAircraftICAOcode() )
                airlineAircraftNumberOfSeatsList.append( airlineAircraft.getMaximumNumberOfPassengers())

        nbAircraftTypes = len(airlineAircraftICAOcodeList)
        print ( "Number of different aircraft types= {0}".format(nbAircraftTypes))
        
        index = 1
        for k in range(len(airlineAircraftICAOcodeList)):
            print ("index= {0} - Airline fleet - aircraft type = {1}".format(index, airlineAircraftICAOcodeList[k]))
            index = index + 1

        print ("------------- airline routes reader --------------")
        airlineRoutesAirports = AirlineRoutesAirportsDataBase()
        ret = airlineRoutesAirports.read()
        self.assertTrue( ret == True )
        
        listOfCities = airlineRoutesAirports.getAirportsICAOcode()
        print ( "Number of different cities= {0}".format(len(listOfCities)))

        index = 1
        flightLegsList = airlineRoutesAirports.getFlightLegList()
        for l in range(len(flightLegsList)):
            print ("index= {0} - Airline Flight Leg= {1}".format(index, flightLegsList[l]))
            index = index + 1
        
        index = 1
        for i in range(len(listOfCities)):
            print ("index= {0} - Airline City= {1}".format(index, listOfCities[i]))
            index = index + 1
            
        listOfDepartureAirports =  airlineRoutesAirports.getDepartureAirportsICAOcodeList()
        index = 1
        for l in range(len(listOfDepartureAirports)):
            print ("index= {0} - Departure Airport= {1}".format(index, listOfDepartureAirports[l]))
            index = index + 1
            
            
        listOfArrivalAirports =  airlineRoutesAirports.getArrivalAirportsICAOcodeList()
        index = 1
        for l in range(len(listOfArrivalAirports)):
            print ("index= {0} - Arrival Airport= {1}".format(index, listOfArrivalAirports[l]))
            index = index + 1

        
        print('------------ daily hour minutes schedule -------------')
        dailyHoursMinutes = []
        dailyMinutesSpan = 2360
        for t in range(dailyMinutesSpan):
            #print ( i )
            dailyHoursMinutes.append( t )
            
        departureTime = []
        for t in range(dailyMinutesSpan):
            departureTime.append(t)
            
        arrivalTime = []
        for t in range(dailyMinutesSpan):
            arrivalTime.append(t)
            
        print ("-----------airline routes costs---------")

        airlineAircraftRoutesCosts = AirlineAircraftRoutesCosts()
        airlineCosts_np_array = airlineAircraftRoutesCosts.read()
        print ( airlineCosts_np_array )
        self.assertTrue( airlineCosts_np_array is not None )


        print ( " ----------- create the costs table ------------------ ")
        costs = []
        
        for airlineAircraft in airlineFleet.getAirlineAircrafts():
            if ( airlineAircraft.hasICAOcode() ):
                ''' here we are building the costs for one aircraft '''
                aircraftCosts = []
                print ( airlineAircraft.getAircraftICAOcode() )
                ''' Warning - should result in the same index as in the above mentioned lists '''
                for route in airlineRoutesAirports.getRoutes():
                    #print (route)
                    for airlineCost in airlineCosts_np_array:
                        #print ("=== airline cost ===")
                        #print ( airlineCost[1] , airlineCost[3] , airlineCost[5] )
                        # airline cost [1] = ICAO code
                        if ( airlineCost[1] == airlineAircraft.getAircraftICAOcode() ) and \
                            ( airlineCost[3] == route.getDepartureAirportICAOcode() )  and \
                            ( airlineCost[5] == route.getArrivalAirportICAOcode() ):
                            ''' airline cost [3] = departure airport ICAO code '''
                            ''' airline cost [5] = arrival airport ICAO code '''
                            ''' airlineCost[7] -> operational costs in dollars '''
                            print ( "{0}-{1}-{2}-{3}".format(airlineAircraft.getAircraftICAOcode(), route.getDepartureAirportICAOcode(), route.getArrivalAirportICAOcode(), airlineCost[8] ))
                            aircraftCosts.append( airlineCost[8] + airlineCost[10] * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars )
                print ( aircraftCosts )
                costs.append(aircraftCosts)
                
        print ( " ----------- costs table with Kerosene ------------------ ")
        print ( costs )
        print ( " ----------- costs table with Kerosene ------------------ ")

        num_aircrafts = len(costs)
        print (" number of aircrafts = {0}".format(num_aircrafts))
        
        num_flight_legs = len(costs[0])
        print (" number of flight legs = {0}".format(num_flight_legs))
        
        print ( " ----------- turn around times  ------------------ ")
        
        airlineTurnAroundTimesDatabase = AirlineTurnAroundTimesDatabase()
        
        for k in range(len(airlineAircraftICAOcodeList)):
            aircraftICAOcode = airlineAircraftICAOcodeList[k]
            print ( aircraftICAOcode )
            for i in range(len(listOfCities)):
                print ("Airline City= {0}".format( listOfCities[i]))
                airportICAOcode = listOfCities[i]
                turnAroundTimeInSeconds = airlineTurnAroundTimesDatabase.getTurnAroundTimeInSeconds( aircraftICAOcode , airportICAOcode )
                #print ("turn around time in seconds = {0}".format( turnAroundTimeInSeconds ) )

        print ( " ----------- aircraft available instances  ------------------ ")
        for k in range(len(airlineAircraftICAOcodeList)):
            aircraftICAOcode = airlineAircraftICAOcodeList[k]
        
            nbAircraftsAvailable = airlineFleet.getAircraftNumberOfInstances( aircraftICAOcode )
            print ("Number of available aircrafts for aircraft ICAO code= {0} - nb instances = {1}".format( aircraftICAOcode , nbAircraftsAvailable ) ) 


        ''' derived sets to be completed '''
        ''' nodes[k,i] set of times '''
        nodes = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            for i in range(len(listOfCities)):
                nodes[k , i] = 0

        ''' ------------ variable ------------'''
        '''  x[i, j] is an array of 0-1 variables, which will be 1 '''
        '''  if worker i is assigned to task j. '''
        x = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            #print ( airlineAircraftICAOcodeList[k])
            #acICAOcode = 
            for l in range(len(flightLegsList)):
                #print ( flightLegsList[l] )
                x[k, l] = solver.IntVar(0, 1, '{0}-{1}'.format(airlineAircraftICAOcodeList[k] , flightLegsList[l]))

        ''' -------- variable -------- number of aircrafts on the ground '''
        y = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            for i in range(len(listOfCities)):
                for t in range(dailyMinutesSpan):
                    y[k, i , t] =  solver.IntVar(0, 999, '{0}-{1}'.format(airlineAircraftICAOcodeList[k] , listOfCities[i] , nodes[k, i]))

        ''' --------- variable -> number of used aircrafts ----------'''
        z = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            z[k] = solver.IntVar(0, 999, '{0}'.format(airlineAircraftICAOcodeList[k] ))

                    
        ''' ----------- constraints ---------- '''
            

        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        
if __name__ == '__main__':
    unittest.main()
                
                