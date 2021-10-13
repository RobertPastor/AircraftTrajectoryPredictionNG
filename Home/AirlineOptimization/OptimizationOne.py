'''
Created on 11 sept. 2021

@author: robert
'''
import time
import unittest

from ortools.linear_solver import pywraplp
import numpy as np

from Home.AirlineCosts.AirlineAircraftRoutesCostsDatabaseFile import AirlineAircraftRoutesCosts
from Home.AirlineRoutes.AirlineRoutesAirportsReader import AirlineRoutesAirportsDataBase

from Home.AirlineFleet.AirlineFleetReader import AirlineFleetDataBase
from Home.AirlineFleet.AirlineFleetReader import AirlineAircraft

kerosene_kilo_to_US_gallons = 0.33
US_gallon_to_US_dollars = 3.25
        
class TestMethods(unittest.TestCase):
#============================================

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
        for airlineAircraft in airlineFleet.getAirlineAircrafts():
            self.assertTrue( isinstance( airlineAircraft , AirlineAircraft ) )
            if ( airlineAircraft.hasICAOcode() ):
                print ( airlineAircraft.getAircraftFullName() , "--->>>---" , airlineAircraft.getAircraftICAOcode() )
                airlineAircraftFullNameList.append( airlineAircraft.getAircraftFullName() )
                airlineAircraftICAOcodeList.append( airlineAircraft.getAircraftICAOcode() )
                
        print ( "length of airline aircraft list = {0}".format( len ( airlineAircraftICAOcodeList ) ) )
        
        print ("------------- airline routes reader --------------")
        airlineRoutesAirports = AirlineRoutesAirportsDataBase()
        ret = airlineRoutesAirports.read()
        self.assertTrue( ret == True )
        print ("------------- airline routes airports OR flight legs --------------")
        airlineFlightLegsList = []
        for route in airlineRoutesAirports.getDepartureArrivalAirportICAOcode():
            print (route)
            airlineFlightLegsList.append( route )

        print ( "length of airline flight legs list = {0}".format( len ( airlineFlightLegsList ) ) )

        print ("-----------airline routes costs---------")

        airlineAircraftRoutesCosts = AirlineAircraftRoutesCosts()
        airlineCosts_np_array = airlineAircraftRoutesCosts.read()
        print ( airlineCosts_np_array )
        self.assertTrue( airlineCosts_np_array is not None )
        
        print ("------------- airline routes airports OR flight legs --------------")
        for route in airlineRoutesAirports.getDepartureArrivalAirportICAOcode():
            print (route)
            
        ''' create the costs table '''
        costs = []

        for airlineAircraft in airlineFleet.getAirlineAircrafts():
            if ( airlineAircraft.hasICAOcode() ):
                aircraftCosts = []
                print ( airlineAircraft.getAircraftICAOcode() )
                for route in airlineRoutesAirports.getDepartureArrivalAirportICAOcode():
                    #print (route)
                    for airlineCost in airlineCosts_np_array:
                        #print ("=== airline cost ===")
                        #print ( airlineCost[1] , airlineCost[3] , airlineCost[5] )
                        # airline cost [1] = ICAO code
                        if ( airlineCost[1] == airlineAircraft.getAircraftICAOcode() ) and ( airlineCost[3] == route[0] )  and ( airlineCost[5] == route[1] ):
                            ''' airline cost [3] = departure airport ICAO code '''
                            ''' airline cost [5] = arrival airport ICAO code '''
                            ''' airlineCost[7] -> operational costs in dollars '''
                            print ( "{0}-{1}-{2}-{3}".format(airlineAircraft.getAircraftICAOcode(), route[0], route[1], airlineCost[8] ))
                            #aircraftCosts.append( airlineCost[8] + airlineCost[10] * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars)
                            aircraftCosts.append( airlineCost[8] )
                print ( aircraftCosts )
                costs.append(aircraftCosts)
                
        print ( costs )
        
        num_aircrafts = len(costs)
        print (" number of aircrafts = {0}".format(num_aircrafts))
        num_flight_legs = len(costs[0])
        print (" number of flight legs = {0}".format(num_flight_legs))

        '''  x[i, j] is an array of 0-1 variables, which will be 1 '''
        '''  if worker i is assigned to task j. '''
        x = {}
        for i in range(num_aircrafts):
            for j in range(num_flight_legs):
                x[i, j] = solver.IntVar(0, 1, '')
                
        '''  Each aircraft is assigned to at most 1 flight leg. '''
        for i in range(num_aircrafts):
            solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= 1)
        
        ''' Each flight leg is assigned to exactly one aircraft '''
        for j in range(num_flight_legs):
            solver.Add(solver.Sum([x[i, j] for i in range(num_aircrafts)]) == 1)

        ''' minimize the costs '''
        objective_terms = []
        for i in range(num_aircrafts):
            for j in range(num_flight_legs):
                objective_terms.append(costs[i][j] * x[i, j])
                
        ''' minimize the costs '''
        solver.Minimize(solver.Sum(objective_terms))
        
        ''' invoke the solver '''
        status = solver.Solve()
        
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print ('solver status - Optimal = {0} - Feasible = {1} - solver result value = {0}'.format(pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE, status))
            print('Total costs = {0:.2f} in US dollars'.format( solver.Objective().Value() ) )
            for i in range(num_aircrafts):
                for j in range(num_flight_legs):
                    # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                    if x[i, j].solution_value() > 0.5:
                        print('aircraft {0} assigned to flight leg {1}  Cost = {2}'.format( i, j, costs[i][j]))
                        print('aircraft {0} ICAO code {1} assigned to flight leg {2}  Cost = {3} dollars for the flight duration'.format( airlineAircraftFullNameList[i], airlineAircraftICAOcodeList[i], airlineFlightLegsList[j], costs[i][j] ) )
                        print ( "===== next ======")

        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )


    def test_two(self):
    
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
        for airlineAircraft in airlineFleet.getAirlineAircrafts():
            self.assertTrue( isinstance( airlineAircraft , AirlineAircraft ) )
            if ( airlineAircraft.hasICAOcode() ):
                print ( airlineAircraft.getAircraftFullName() , "--->>>---" , airlineAircraft.getAircraftICAOcode() )
                airlineAircraftFullNameList.append( airlineAircraft.getAircraftFullName() )
                airlineAircraftICAOcodeList.append( airlineAircraft.getAircraftICAOcode() )
                
        print ( "length of airline aircraft list = {0}".format( len ( airlineAircraftICAOcodeList ) ) )
        
        print ("------------- airline routes reader --------------")
        airlineRoutesAirports = AirlineRoutesAirportsDataBase()
        ret = airlineRoutesAirports.read()
        self.assertTrue( ret == True )
        print ("------------- airline routes airports OR flight legs --------------")
        airlineFlightLegsList = []
        for route in airlineRoutesAirports.getDepartureArrivalAirportICAOcode():
            print (route)
            airlineFlightLegsList.append( route )

        print ( "length of airline flight legs list = {0}".format( len ( airlineFlightLegsList ) ) )

        print ("-----------airline routes costs---------")

        airlineAircraftRoutesCosts = AirlineAircraftRoutesCosts()
        airlineCosts_np_array = airlineAircraftRoutesCosts.read()
        print ( airlineCosts_np_array )
        self.assertTrue( airlineCosts_np_array is not None )
        
        print ("------------- airline routes airports OR flight legs --------------")
        for route in airlineRoutesAirports.getDepartureArrivalAirportICAOcode():
            print (route)
            
        print ( " ----------- create the costs table ------------------ ")
        costs = []
        
        for airlineAircraft in airlineFleet.getAirlineAircrafts():
            if ( airlineAircraft.hasICAOcode() ):
                aircraftCosts = []
                print ( airlineAircraft.getAircraftICAOcode() )
                for route in airlineRoutesAirports.getDepartureArrivalAirportICAOcode():
                    #print (route)
                    for airlineCost in airlineCosts_np_array:
                        #print ("=== airline cost ===")
                        #print ( airlineCost[1] , airlineCost[3] , airlineCost[5] )
                        # airline cost [1] = ICAO code
                        if ( airlineCost[1] == airlineAircraft.getAircraftICAOcode() ) and ( airlineCost[3] == route[0] )  and ( airlineCost[5] == route[1] ):
                            ''' airline cost [3] = departure airport ICAO code '''
                            ''' airline cost [5] = arrival airport ICAO code '''
                            ''' airlineCost[7] -> operational costs in dollars '''
                            print ( "{0}-{1}-{2}-{3}".format(airlineAircraft.getAircraftICAOcode(), route[0], route[1], airlineCost[8] ))
                            aircraftCosts.append( airlineCost[8] + airlineCost[10] * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars)
                print ( aircraftCosts )
                costs.append(aircraftCosts)
                
        print ( costs )
        
        num_aircrafts = len(costs)
        print (" number of aircrafts = {0}".format(num_aircrafts))
        
        num_flight_legs = len(costs[0])
        print (" number of flight legs = {0}".format(num_flight_legs))

        '''  x[i, j] is an array of 0-1 variables, which will be 1 '''
        '''  if worker i is assigned to task j. '''
        x = {}
        for i in range(num_aircrafts):
            for j in range(num_flight_legs):
                x[i, j] = solver.IntVar(0, 1, '')
                
        '''  Each aircraft is assigned to at most 1 flight leg. '''
        for i in range(num_aircrafts):
            solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= 1)
        
        ''' Each flight leg is assigned to exactly one aircraft '''
        for j in range(num_flight_legs):
            solver.Add(solver.Sum([x[i, j] for i in range(num_aircrafts)]) == 1)

        objective_terms = []
        for i in range(num_aircrafts):
            for j in range(num_flight_legs):
                objective_terms.append(costs[i][j] * x[i, j])
                
        ''' minimize the costs '''
        solver.Minimize(solver.Sum(objective_terms))
        
        ''' invoke the solver '''
        status = solver.Solve()
        
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print ('solver status - Optimal = {0} - Feasible = {1} - solver result value = {0}'.format(pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE, status))
            print('Total costs = {0:.2f} in US dollars'.format( solver.Objective().Value() ) )
            for i in range(num_aircrafts):
                for j in range(num_flight_legs):
                    # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                    if x[i, j].solution_value() > 0.5:
                        print('aircraft {0} assigned to flight leg {1} - Costs = {2}'.format( i, j, costs[i][j]))
                        print('aircraft {0} ICAO code {1} assigned to flight leg {2}  Cost = {3} dollars for the flight duration'.format( airlineAircraftFullNameList[i], airlineAircraftICAOcodeList[i], airlineFlightLegsList[j], costs[i][j] ) )
                        print ( "===== next ======")

        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        
if __name__ == '__main__':
    unittest.main()