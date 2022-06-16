'''
Created on 11 sept. 2021

@author: robert
'''
import time
import unittest

from ortools.linear_solver import pywraplp

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
            flightLegOneWay = route.getFlightLegAsString()
            flightLegReturn = str(flightLegOneWay).split("-")[1] + "-" + str(flightLegOneWay).split("-")[0]
            
            if ( flightLegOneWay in airlineFlightLegsList) or ( flightLegReturn in airlineFlightLegsList):
                pass
            else:
                print ( "{0} ---- {1}".format( flightLegOneWay , flightLegReturn ) )
                airlineFlightLegsList.append( flightLegOneWay )

        print ( "Fleet Assignment - length of airline flight legs list = {0}".format( len ( airlineFlightLegsList ) ) )
        #stop()

        print ("-----------Fleet Assignment - airline routes costs---------")

        airlineAircraftRoutesCosts = AirlineAircraftRoutesCosts()
        airlineCosts_np_array = airlineAircraftRoutesCosts.read()
        print ( airlineCosts_np_array )
        self.assertTrue( airlineCosts_np_array is not None )
        
        print ( " ----------- create the costs table ------------------ ")
        costs = []
        
        for i in range(len(airlineAircraftICAOcodeList)):
            aircraftICAOcode = airlineAircraftICAOcodeList[i]
            print ( aircraftICAOcode )
            ''' Warning - should result in the same index as in the above mentioned lists '''
            aircraftCosts = []

            for j in range(len(airlineFlightLegsList)):
                print (airlineFlightLegsList[j])
                departureAirportICAOcode = str(airlineFlightLegsList[j]).split("-")[0]
                arrivalAirportICAOcode = str(airlineFlightLegsList[j]).split("-")[1]
                for airlineCost in airlineCosts_np_array:
                    #print ("=== airline cost ===")
                    print ( airlineCost[1] , airlineCost[3] , airlineCost[5] )
                    # airline cost [1] = ICAO code
                    if ( airlineCost[1] == aircraftICAOcode) and \
                        ( airlineCost[3] == departureAirportICAOcode )  and \
                        ( airlineCost[5] == arrivalAirportICAOcode ):
                        ''' airline cost [3] = departure airport ICAO code '''
                        ''' airline cost [5] = arrival airport ICAO code '''
                        ''' airlineCost[7] -> operational costs in dollars '''
                        print ( "{0}-{1}-{2}-{3}".format(aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode, airlineCost[8] ))
                        aircraftCosts.append( airlineCost[8] + airlineCost[10] * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars )
                        
            print ( aircraftCosts )
            costs.append(aircraftCosts)
                
        print ( " ----------- costs table with Kerosene ------------------ ")
        print ( costs )
        print ( " ----------- costs table with Kerosene ------------------ ")

        num_aircrafts = len(costs)
        print ("number of aircrafts = {0}".format(num_aircrafts))
        
        num_flight_legs = len(costs[0])
        print ("number of flight legs = {0}".format(num_flight_legs))
        
        xnum_flight_legs = len(airlineFlightLegsList)
        print ("another number of flight legs = {0}".format(xnum_flight_legs))


        '''  x[i, j] is an array of 0-1 variables, which will be 1 '''
        '''  if worker i is assigned to task j. '''
        x = {}
        for i in range(num_aircrafts):
            print ( "{0}".format(airlineAircraftICAOcodeList[i]))
            for j in range(num_flight_legs):
                #print ( '{0}-{1}'.format(airlineAircraftICAOcodeList[i], airlineFlightLegsList[j]) )
                x[i, j] = solver.IntVar(0, 1, '{0}-{1}'.format(airlineAircraftICAOcodeList[i], airlineFlightLegsList[j]))
                
        '''  Each aircraft is assigned to at most 1 flight leg. '''
        for i in range(num_aircrafts):
            pass
            solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= 1)
        
        
        ''' Each flight leg is assigned to exactly one aircraft '''
        for j in range(num_flight_legs):
            pass 
            solver.Add(solver.Sum([x[i, j] for i in range(num_aircrafts)]) == 1)

        ''' --------- objective --------------'''
        objective_terms = []
        for i in range(num_aircrafts):
            for j in range(num_flight_legs):
                objective_terms.append(costs[i][j] * x[i, j])
                
        ''' minimize the costs '''
        solver.Minimize(solver.Sum(objective_terms))
        
        ''' invoke the solver '''
        status = solver.Solve()
        
        print ("---------- costs with Kerosene -----------")
        
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print ('solver status - Optimal = {0} - Feasible = {1} - solver result value = {0}'.format(pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE, status))
            print('Total costs = {0:.2f} in US dollars'.format( solver.Objective().Value() ) )
            for i in range(num_aircrafts):
                for j in range(num_flight_legs):
                    # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                    if x[i, j].solution_value() > 0.5:
                        print('aircraft {0} assigned to flight leg {1} - Costs = {2:.2f} in US dollars'.format( i, j, costs[i][j]))
                        print('aircraft {0} - ICAO code {1} - assigned to flight leg {2} - Cost = {3:.2f} US dollars for the flight duration'.format( airlineAircraftFullNameList[i], airlineAircraftICAOcodeList[i], airlineFlightLegsList[j], costs[i][j] ) )
                        print('aircraft {0} - ICAO code {1} - assigned to flight leg {2} - number of seats = {3} for the selected aircraft'.format( airlineAircraftFullNameList[i], airlineAircraftICAOcodeList[i], airlineFlightLegsList[j], airlineAircraftNumberOfSeatsList[i] ) )
                        departureAirportICAOcode = str(airlineFlightLegsList[j]).split("-")[0]
                        arrivalAirportICAOcode = str(airlineFlightLegsList[j]).split("-")[1]
                        durationHours = airlineAircraftRoutesCosts.getFlightLegDurationInHours(airlineAircraftICAOcodeList[i], departureAirportICAOcode, arrivalAirportICAOcode)
                        print('aircraft {0} - ICAO code {1} - assigned to flight leg {2} - duration of flight in Hours = {3} for the selected aircraft and the selected flight leg'.format( airlineAircraftFullNameList[i], airlineAircraftICAOcodeList[i], airlineFlightLegsList[j], durationHours ) )
                        seatCostDollars = costs[i][j] / airlineAircraftNumberOfSeatsList[i]
                        print('aircraft {0} - ICAO code {1} - assigned to flight leg {2} - seat costs  = {3:.2f} in US dollars for the selected aircraft and the selected flight leg'.format( airlineAircraftFullNameList[i], airlineAircraftICAOcodeList[i], airlineFlightLegsList[j], seatCostDollars ) )
                        print ( "===== next ======")

        else:
            print ("solver status = {0} - Optimal= {1} - Feasible= {2}".format(status, pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE))

        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        
if __name__ == '__main__':
    unittest.main()