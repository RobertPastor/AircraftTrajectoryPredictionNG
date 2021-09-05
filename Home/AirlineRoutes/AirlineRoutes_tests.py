'''
Created on 5 sept. 2021

@author: robert

compute a simulated routes for one aircraft type

'''

import time
import unittest

from Home.AirlineRoutes.AirlineRoutes import AirlineRoutes
from Home.Guidance.RouteFile import Route
from Home.AirlineFleet.AirlineFleetReader import AirlineFleetDataBase

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.Guidance.FlightPathFile import FlightPath

from Home.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance

class TestMethods(unittest.TestCase):
#============================================
    def test_one(self):
        pass
    
        t0 = time.clock()
        print ( '================ test one =================' )
        
        airlineRoutes = AirlineRoutes()
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        airlineRoutes.createRoutesFiles()
        
        t2 = time.clock()
        print ( 'duration= {0} seconds'.format(t2-t1) )
        

    def test_two(self):
        pass
        t0 = time.clock()

        print ( '================ test two =================' )

        airlineRoutes = AirlineRoutes()
        route = airlineRoutes.getRoute("KATL","KLAX")
        self.assertTrue( isinstance(route , Route) )
        
        print ( route.getRouteAsString() )
        
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
        

    def test_three(self):
        pass
        t0 = time.clock()

        print ( '================ test three =================' )

        airlineRoutes = AirlineRoutes()
        route = airlineRoutes.getRoute("KATL","KLAX")
        self.assertTrue( isinstance(route , Route) )
        
        print ( route.getRouteAsString() )
        
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
        
        airlineFleet = AirlineFleetDataBase()
        retOne = airlineFleet.read()
        
        acBd = BadaAircraftDatabase()
        retTwo = acBd.read()
        
        atmosphere = Atmosphere()
        earth = Earth()
        
        if retOne and retTwo:
            for acType in airlineFleet.getAircraftFullNames():
                print ( str(acType).upper() )
                print (" ---------------- " , str(acType).upper() , " -----------------")

                for aircraftICAOcode in acBd.getAircraftICAOcodes():
                    if ( str(acType).upper() == acBd.getAircraftFullName( aircraftICAOcode )):
                        
                        if ( acBd.aircraftExists(aircraftICAOcode) 
                             and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                            
                            print (" ---------------- " , str(acType).upper() , " -----------------")
                            print ( 'FOUND -> aircraft full name = {0} -- aircraft ICAO code = {1}'.format( acType , aircraftICAOcode  ) )
                            print (" ---------------- " , str(acType).upper() , " -----------------")

                            ac = BadaAircraft(ICAOcode = aircraftICAOcode , 
                                              aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode), 
                                              badaPerformanceFilePath =  acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                      atmosphere = atmosphere, earth = earth)
                            
                            acPerformance = AircraftPerformance(acBd.getAircraftPerformanceFile(aircraftICAOcode))

                            if ( ((ac is None) == False) and ((acPerformance is None) == False) ):
                                print ( "Landing length meters = {0}".format(ac.getLandingLengthMeters()) )
                                print ( "Take-off length meters = {0}".format(ac.getTakeOffLengthMeters()) )      
                                print ( "Max TakeOff Weight kilograms = {0}".format(ac.getMaximumMassKilograms() ) )   
                                print ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   
                                
                                flightPath = FlightPath(route = route.getRouteAsString(), 
                                                    aircraftICAOcode = aircraftICAOcode,
                                                    RequestedFlightLevel = acPerformance.getMaxOpAltitudeFeet()/100., 
                                                    cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                                    takeOffMassKilograms = ac.getMaximumMassKilograms())
                                '''
                                RFL:    FL 310 => 31000 feet
                                Cruise Speed    Mach 0.78                                    
                                Take Off Weight    62000 kgs    
                                '''
                                print ("=========== Flight Plan compute  =========== " + time.strftime("%c"))
                                
                                t0 = time.clock()
                                print ('time zero= ' + str(t0))
                                lengthNauticalMiles = flightPath.computeLengthNauticalMiles()
                                print ('flight path length= {0:.2f} nautics '.format(lengthNauticalMiles))
                                flightPath.computeFlight(deltaTimeSeconds = 1.0)
                                print ('simulation duration= ' + str(time.clock()-t0) + ' seconds')
                                
                                print ("=========== Flight Plan create output files  =========== " + time.strftime("%c"))
                                flightPath.createFlightOutputFiles()
                                print ("=========== Flight Plan end  =========== " + time.strftime("%c"))

        
        
if __name__ == '__main__':
    unittest.main()