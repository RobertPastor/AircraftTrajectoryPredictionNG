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

        print ("----------- define a task as a flight leg IN, a turn around time and a flight leg OUT / return ")

        listOfCities = airlineRoutesAirports.getAirportsICAOcode()
        print ( "Number of different cities= {0}".format(len(listOfCities)))

        index = 1
        for i in range(len(listOfCities)):
            print ("index= {0} - Airline City= {1}".format(index, listOfCities[i]))
            index = index + 1

        print ("------------- airline routes airports OR flight legs --------------")

        index = 1
        tasks_data = []
        flightLegsList = airlineRoutesAirports.getFlightLegList()
        for l in range(len(flightLegsList)):
            print ("index= {0} - Airline Flight Leg= {1}".format(index, flightLegsList[l]))
            index = index + 1
            inFlightLeg = flightLegsList[l]
            for k in range(len(flightLegsList)):
                outFlightLeg = flightLegsList[k]
                if ( inFlightLeg != outFlightLeg) and ( str(inFlightLeg).split("-")[0] == str(outFlightLeg).split("-")[1] ) and ( str(inFlightLeg).split("-")[1] == str(outFlightLeg).split("-")[0] ):
                    tasks_data.append( inFlightLeg + "*" + outFlightLeg )
              
        print ("------------- tasks ------------")
        index = 0
        for k , task_data in enumerate(tasks_data):
            print ("index= {0} - task = {1}".format( index, task_data) )
            index = index + 1

        stop()

        print ("-----------airline routes costs---------")

        airlineAircraftRoutesCosts = AirlineAircraftRoutesCosts()
        airlineCosts_np_array = airlineAircraftRoutesCosts.read()
        print ( airlineCosts_np_array )
        self.assertTrue( airlineCosts_np_array is not None )
        
        print ( " ----------- create the costs table ------------------ ")
        ''' it is an array of arrays '''
        costs = []
        
        for i in range(len(airlineAircraftInstancesList)):
                    
            acInstance = airlineAircraftInstancesList[i]
            print ( acInstance )
            ''' here we are building the costs for one aircraft instance '''
            aircraftInstanceCosts = []
                
            #print ( airlineAircraft.getAircraftICAOcode() )
            ''' Warning - should result in the same index as in the above mentioned lists '''
            for route in airlineRoutesAirports.getRoutes():
                #print (route)
                for airlineCost in airlineCosts_np_array:
                    #print ("=== airline cost ===")
                    #print ( airlineCost[1] , airlineCost[3] , airlineCost[5] )
                    # airline cost [1] = ICAO code
                    if ( airlineCost[1] == airlineAircraftICAOcodeList[i] ) and \
                        ( airlineCost[3] == route.getDepartureAirportICAOcode() )  and \
                        ( airlineCost[5] == route.getArrivalAirportICAOcode() ):
                        ''' airline cost [3] = departure airport ICAO code '''
                        ''' airline cost [5] = arrival airport ICAO code '''
                        ''' airlineCost[7] -> operational costs in dollars '''
                        print ( "{0}-{1}-{2}-{3}".format(acInstance, route.getDepartureAirportICAOcode(), route.getArrivalAirportICAOcode(), airlineCost[8] ))
                        aircraftInstanceCosts.append( airlineCost[8] + airlineCost[10] * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars )
                    
            print ( aircraftInstanceCosts )
            costs.append(aircraftInstanceCosts)
                
        print ( " ----------- costs table with Kerosene ------------------ ")
        print ( costs )
        print ( " ----------- costs table with Kerosene ------------------ ")

        num_aircrafts = len(costs)
        print (" number of aircrafts Instances = {0}".format(num_aircrafts))
        
        num_flight_legs = len(costs[0])
        print (" number of flight legs = {0}".format(num_flight_legs))
        
        xnum_flight_legs = len(airlineFlightLegsList)
        print (" another number of flight legs = {0}".format(xnum_flight_legs))

        '''  x[i, j] is an array of 0-1 variables, which will be 1 '''
        '''  if worker i (aircraft type) - instance j - is assigned to task k. task k being a flight leg '''
        x = {}        
        for i in range(len(airlineAircraftInstancesList)):

            acInstance = airlineAircraftInstancesList[i]
            #print ( acInstance )
            for k in range(num_flight_legs):
                x[i, k] = solver.IntVar(0, 1, acInstance)
                        
                        
        '''  Each aircraft is assigned to at most 1 flight leg. '''
        for i in range(len(airlineAircraftInstancesList)):
            pass
            solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= 1)
        
        ''' Each flight leg is assigned to exactly one instance of aircraft '''
        for j in range(num_flight_legs):
            pass
            solver.Add(solver.Sum([x[i, j] for i in range(num_aircrafts)]) == 1)
            
        ''' number of available aircrafts of each category '''
        #for i in range(num_aircrafts):
        #    aircraftICAOcode = airlineAircraftICAOcodeList[i]
        #    #print ( aircraftICAOcode )
        #    aircraftICAOcode = airlineAircraftICAOcodeList[i]
        #    nbAircraftsAvailable = airlineFleet.getAircraftNumberOfInstances( aircraftICAOcode )
        #    solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= nbAircraftsAvailable )
            
        ''' frequency = number of flights for each flight leg per day '''
        ''' start with 20 hours a day and divide by flight duration + Duration Turn Around Time '''
        flightLegFrequency = {}
        flightLegDurationHours = {}
        turnAroundDurationHours = 0.5
        for j in range(num_flight_legs):
            flightLegStr = airlineFlightLegsList[j]
            #print ( flightLegStr )
            flightLegDurationHours[j] = self.computeMaxOfFlightLegDurationHours(flightLegStr , airlineAircraftICAOcodeList, airlineAircraftRoutesCosts)
            flightLegFrequency[j] =  int ( 20. / ( flightLegDurationHours[j] + turnAroundDurationHours ) )
            print ( "flight leg = {0} - max flight leg duration in hours {1} - frequency for 20 hours = {2}".format( flightLegStr , flightLegDurationHours[j] , flightLegFrequency[j]) )


        "for i in range(len(airports)):\n",
        "    for j in range(len(airports)):\n",
        "        prob += pulp.lpSum(20 * x[i][j][k] for k in range(len(aircrafts))) >= frequency[i][j] * time_flight[i][j],'Availability Constraint: {} to {}'.format(airports[i],airports[j])\n",
        for j in range(num_flight_legs):
            solver.Add(solver.Sum( [20 * x[i, j] for i in range(num_aircrafts)] ) >= ( flightLegFrequency[j] * flightLegDurationHours[j] ) )
 
 
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
            
            
            for i in range(len(airlineAircraftInstancesList)):
                acInstance = airlineAircraftInstancesList[i]
                    
                for j in range(num_flight_legs):
                    if x[i, j].solution_value() > 0.5:
                                
                        print('aircraft {0} assigned to flight leg {1} - Costs = {2:.2f} in US dollars'.format( i, j, costs[i][j]))
                        print('aircraft {0} - ICAO code {1} - assigned to flight leg {2} - Cost = {3:.2f} US dollars for the flight duration'.format( airlineAircraftFullNameList[i], acInstance, airlineFlightLegsList[j], costs[i][j] ) )
                        print('aircraft {0} - ICAO code {1} - assigned to flight leg {2} - number of seats = {3} for the selected aircraft'.format( airlineAircraftFullNameList[i], acInstance, airlineFlightLegsList[j], airlineAircraftNumberOfSeatsList[i] ) )
                        departureAirportICAOcode = str(airlineFlightLegsList[j]).split("-")[0]
                        arrivalAirportICAOcode = str(airlineFlightLegsList[j]).split("-")[1]
                        durationHours = airlineAircraftRoutesCosts.getFlightLegDurationInHours(aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode)
                        print('aircraft {0} - ICAO code {1} - assigned to flight leg {2} - duration of flight in Hours = {3} for the selected aircraft and the selected flight leg'.format( airlineAircraftFullNameList[i], acInstance, airlineFlightLegsList[j], durationHours ) )
                        seatCostDollars = costs[i][j] / airlineAircraftNumberOfSeatsList[i]
                        print('aircraft {0} - ICAO code {1} - assigned to flight leg {2} - seat costs  = {3:.2f} in US dollars for the selected aircraft and the selected flight leg'.format( airlineAircraftFullNameList[i], acInstance, airlineFlightLegsList[j], seatCostDollars ) )
                        print ( "===== next ======")
                                

        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        
if __name__ == '__main__':
    unittest.main()