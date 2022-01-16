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
            
        print ( ''' ----------- departure airports - flight leg origin ----------- ''' )
        listOfDepartureAirports =  airlineRoutesAirports.getDepartureAirportsICAOcodeList()
        index = 1
        for l in range(len(listOfDepartureAirports)):
            print ("index= {0} - Departure Airport= {1}".format(index, listOfDepartureAirports[l]))
            index = index + 1
            
        print ( ''' ----------- arrival airports - flight leg destination  ----------- ''' )
        listOfArrivalAirports =  airlineRoutesAirports.getArrivalAirportsICAOcodeList()
        index = 1
        for l in range(len(listOfArrivalAirports)):
            print ("index= {0} - Arrival Airport= {1}".format(index, listOfArrivalAirports[l]))
            index = index + 1

        
        print('------------ daily hour minutes schedule -------------')
        dailyHoursMinutes = []
        dailyMinutesSpan = 2360
        for hour in range(24):
            #print ( str(hour) )
            #print ( str(hour).zfill(2) )
            for minute in range(60):
                #print ( minute )
                #print ( str(minute).zfill(2) )
                #print ( str(hour).zfill(2) +  str(minute).zfill(2) )
                dailyHoursMinutes.append( str(hour).zfill(2) + ":" +  str(minute).zfill(2) )
            

        print ("-----------airline routes costs---------")

        airlineAircraftRoutesCosts = AirlineAircraftRoutesCosts()
        airlineCosts_np_array = airlineAircraftRoutesCosts.read()
        print ( airlineCosts_np_array )
        self.assertTrue( airlineCosts_np_array is not None )
        
        
        print (''' nodes [ k , i ] is the set of times when an arrival or a departure of an aircraft of type k may happen in the city i ''')
        

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
        
        turnAroundTimeInSeconds = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            aircraftICAOcode = airlineAircraftICAOcodeList[k]
            print ( aircraftICAOcode )
            for i in range(len(listOfCities)):
                print ("Airline City= {0}".format( listOfCities[i]))
                airportICAOcode = listOfCities[i]
                turnAroundTimeInSeconds[k , i] = airlineTurnAroundTimesDatabase.getTurnAroundTimeInSeconds( aircraftICAOcode , airportICAOcode )
                #print ("turn around time in seconds = {0}".format( turnAroundTimeInSeconds ) )

        print ( " ----------- aircraft available instances  ------------------ ")
        fleetSize = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            aircraftICAOcode = airlineAircraftICAOcodeList[k]
        
            nbAircraftsAvailable = airlineFleet.getAircraftNumberOfInstances( aircraftICAOcode )
            print ("Number of available aircrafts for aircraft ICAO code= {0} - nb instances = {1}".format( aircraftICAOcode , nbAircraftsAvailable ) ) 
            fleetSize[k] = nbAircraftsAvailable

        ''' ------------- departure time of each flight leg -------- '''
        flightLegDepartureTime = {}
        for l in range(len(flightLegsList)):
            flightLegDepartureTime[l] = str("0800")
        
        
        flightLegArrivalTime = {}
        for l in range(len(flightLegsList)):
            flightLegArrivalTime[l] = str("1300")


        ''' derived sets to be completed '''
        ''' nodes[k,i] set of times '''
        nodes = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            for i in range(len(listOfCities)):
                nodes[k , i] = 0

        ''' ------------ count air -------------'''
        ''' capture the set of cities where an aircraft of type k might be in the air at midnight '''
        countAircraftTypeInTheAir = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            pass
            countAircraftTypeInTheAir[k] = 0

        ''' ------------ count ground  -------------'''
        ''' capture the set of cities where an aircraft of type k might be sitting on the ground at midnight  '''
        countAircraftTypeOntheGround = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            pass
            countAircraftTypeOntheGround[k] = 0

        ''' ------------ variable ------------'''
        '''  x[i, j] is an array of 0-1 variables, which will be 1 '''
        '''  if worker i is assigned to task j. '''
        xFleetAssignments = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            #print ( airlineAircraftICAOcodeList[k])
            #acICAOcode = 
            aircraftICAOcode = airlineAircraftICAOcodeList[k]
            nbAircraftsAvailable = airlineFleet.getAircraftNumberOfInstances( aircraftICAOcode )

            for l in range(len(flightLegsList)):
                #print ( flightLegsList[l] )
                xFleetAssignments[k, l] = solver.IntVar(0, 1, '{0}-{1}'.format(airlineAircraftICAOcodeList[k] , flightLegsList[l]))


        ''' -------- variable -------- number of aircrafts on the ground '''
        yOnTheGround = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            for i in range(len(listOfCities)):
                for t in range(dailyMinutesSpan):
                    
                    aircraftICAOcode = airlineAircraftICAOcodeList[k]
                    nbAircraftsAvailable = airlineFleet.getAircraftNumberOfInstances( aircraftICAOcode )
                    
                    yOnTheGround[k, i , t] =  solver.IntVar(0, nbAircraftsAvailable, '{0}-{1}'.format(airlineAircraftICAOcodeList[k] , listOfCities[i] , nodes[k, i]))


        ''' --------- variable -> number of used aircrafts ----------'''
        zUsedAircrafs = {}
        for k in range(len(airlineAircraftICAOcodeList)):
            
            aircraftICAOcode = airlineAircraftICAOcodeList[k]
            nbAircraftsAvailable = airlineFleet.getAircraftNumberOfInstances( aircraftICAOcode )

            zUsedAircrafs[k] = solver.IntVar(0, nbAircraftsAvailable, '{0}'.format(airlineAircraftICAOcodeList[k] ))

                    
        ''' ----------- constraints ---------- '''
            
        ''' COVER - Each flight leg is assigned to exactly one aircraft '''
            
        ''' Each flight leg is assigned to exactly one aircraft type '''
        for l in range(len(flightLegsList)):
            for k in range(len(airlineAircraftICAOcodeList)):
                ''' sum of all ONEs for any aircraft different type for one leg is always ONE '''
                aircraftICAOcode = airlineAircraftICAOcodeList[k]
                nbAircraftsAvailable = airlineFleet.getAircraftNumberOfInstances( aircraftICAOcode )

                #solver.Add( xFleetAssignments[k,l]  <= nbAircraftsAvailable )
                solver.Add( xFleetAssignments[k,l]  == 1 )


        ''' constraint - for one aircraft type - number of instances are limited '''
        ''' number of aircraft on the ground PLUS number of aircraft in the air = size of a fleet '''
        for k in range(len(airlineAircraftICAOcodeList)):
            pass
            #zUsedAircrafs[k] 
            #solver.Add(solver.Sum( [ xFleetAssignments[k, l] for l in range(len(flightLegsList)) ]  -  sum([sum([ yOnTheGround[k, i , t] for i in range(len(listOfCities)) ]) for t in range(dailyMinutesSpan) ]) )  == zUsedAircrafs[k] )

        ''' --------- objective --------------'''
        objective_terms = []
        for i in range(num_aircrafts):
            for j in range(num_flight_legs):
                objective_terms.append(costs[i][j] * xFleetAssignments[i, j])
                
        
        ''' minimize the costs '''
        solver.Minimize(solver.Sum(objective_terms))
        
        ''' invoke the solver '''
        #status = solver.Solve()
        
        print ("---------- costs with Kerosene -----------")
        '''
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print ('solver status - Optimal = {0} - Feasible = {1} - solver result value = {0}'.format(pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE, status))
            print('Total costs = {0:.2f} in US dollars'.format( solver.Objective().Value() ) )
            for k in range(len(airlineAircraftICAOcodeList)):
                for l in range(len(flightLegsList)):
                    # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                    print ( "---------- {0} -----------------".format(xFleetAssignments[k, l]) )
                    if xFleetAssignments[k, l].solution_value() > 0.5:
                        print('aircraft= {0} assigned to flight leg= {1} - Costs= {2:.2f} in US dollars'.format( k, l, costs[k][l]))
                        print('aircraft= {0} - ICAO code= {1} - assigned to flight leg {2} - Costs= {3:.2f} US dollars for the flight duration'.format( airlineAircraftFullNameList[k], airlineAircraftICAOcodeList[k], flightLegsList[l], costs[k][l] ) )
                        print('aircraft= {0} - ICAO code= {1} - assigned to flight leg {2} - number of seats= {3} for the selected aircraft'.format( airlineAircraftFullNameList[k], airlineAircraftICAOcodeList[k], flightLegsList[l], airlineAircraftNumberOfSeatsList[k] ) )

                        departureAirportICAOcode = str(flightLegsList[l]).split("-")[0]
                        arrivalAirportICAOcode = str(flightLegsList[l]).split("-")[1]
                        durationHours = airlineAircraftRoutesCosts.getFlightLegDurationInHours(airlineAircraftICAOcodeList[k], departureAirportICAOcode, arrivalAirportICAOcode)
                        print('aircraft= {0} - ICAO code= {1} - assigned to flight leg= {2} - duration of flight= {3} Hours for the selected aircraft and the selected flight leg'.format( airlineAircraftFullNameList[k], airlineAircraftICAOcodeList[k], flightLegsList[l], durationHours ) )
                        seatCostDollars = costs[k][l] / airlineAircraftNumberOfSeatsList[k]
                        print('aircraft= {0} - ICAO code= {1} - assigned to flight leg= {2} - seat costs= {3:.2f} in US dollars for the selected aircraft and the selected flight leg'.format( airlineAircraftFullNameList[k], airlineAircraftICAOcodeList[k], flightLegsList[l], seatCostDollars ) )

        '''

        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        
if __name__ == '__main__':
    unittest.main()
                
                