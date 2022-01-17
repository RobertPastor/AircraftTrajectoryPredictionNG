
'''
Created on 1s November 2021

@author: robert PASTOR
'''
import os
import time
import unittest
import collections
#from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model


from Home.AirlineCosts.AirlineAircraftRoutesCostsDatabaseFile import AirlineAircraftRoutesCosts
from Home.AirlineRoutes.AirlineRoutesAirportsReader import AirlineRoutesAirportsDataBase

from Home.AirlineFleet.AirlineFleetReader import AirlineFleetDataBase
from Home.AirlineFleet.AirlineFleetReader import AirlineAircraft

kerosene_kilo_to_US_gallons = 0.33
US_gallon_to_US_dollars = 3.25

class TestMethods(unittest.TestCase):
#============================================

    def test_two(self):
    
        t0 = time.clock()
        
        # Create the MIP solver with the SCIP backend.
        #solver = pywraplp.Solver.CreateSolver('SCIP')
        model = cp_model.CpModel()
        
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
                airlineAircraftFullNameList.append( airlineAircraft.getAircraftFullName() )
                airlineAircraftICAOcodeList.append( airlineAircraft.getAircraftICAOcode() )
                airlineAircraftNumberOfSeatsList.append( airlineAircraft.getMaximumNumberOfPassengers())
                
        print ( "length of airline aircraft list = {0}".format( len ( airlineAircraftICAOcodeList ) ) )

 
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


        print ("-----------Job Shop Problem - airline routes costs---------")

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
                            print ( "{0}-{1}-{2}-costs= {3} in US dollars".format(airlineAircraft.getAircraftICAOcode(), route.getDepartureAirportICAOcode(), route.getArrivalAirportICAOcode(), airlineCost[8] ))
                            aircraftCosts.append( airlineCost[8] + airlineCost[10] * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars )
    
                            departureAirportICAOcode = route.getDepartureAirportICAOcode()
                            arrivalAirportICAOcode = route.getArrivalAirportICAOcode()
                            durationHours = airlineAircraftRoutesCosts.getFlightLegDurationInHours(airlineAircraft.getAircraftICAOcode(), departureAirportICAOcode, arrivalAirportICAOcode)
                            print ("{0}-{1}-{2}-duration= {3} in Hours".format(airlineAircraft.getAircraftICAOcode(), departureAirportICAOcode, arrivalAirportICAOcode,durationHours))
                                
                            
                print ( aircraftCosts )
                costs.append(aircraftCosts)
                
        print ( " ----------- costs table with Kerosene ------------------ ")
        print ( costs )
        print ( " ----------- costs table with Kerosene ------------------ ")


        print ("-------- a job is composed of tasks -----------")
        print ("-------- a task is either flying a flight leg - waiting a turn around time - and flying the return leg -----------")

        
        

        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        
if __name__ == '__main__':
    unittest.main()
    
