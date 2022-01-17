'''
Created on 5 sept. 2021

@author: robert

compute a simulated routes for one aircraft type

'''

import time
import unittest

from Home.AirlineRoutes.AirlineRoutes import AirlineRoutes
from Home.AirlineCosts.AirlineAircraftRoutesCostsDatabaseFile import AirlineAircraftRoutesCost
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
    
 
        
    def test_three(self):
        pass
        t0 = time.clock()

        print ( '================ test three =================' )

        airlineRoutes = AirlineRoutes()
        route = airlineRoutes.getRoute("PANC","KATL")
        self.assertTrue( isinstance(route , Route) )
        
        print ( route.getRouteAsString() )
        
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
        
        airlineFleet = AirlineFleetDataBase()
        retOne = airlineFleet.read()
        
        retTwo = airlineFleet.extendDatabase()
        
        acBd = BadaAircraftDatabase()
        retThree = acBd.read()
        
        atmosphere = Atmosphere()
        earth = Earth()
        
        if retOne and retTwo and retThree:
            
            aircraftICAOcode = "B712"
                    
            if ( acBd.aircraftExists(aircraftICAOcode) 
                and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                            
                print (" ---------------- " , str(aircraftICAOcode).upper() , " -----------------")
                print ( 'FOUND -> aircraft full name = {0} -- aircraft ICAO code = {1}'.format( aircraftICAOcode , aircraftICAOcode  ) )
                print (" ---------------- " , str(aircraftICAOcode).upper() , " -----------------")

                acBada = BadaAircraft(ICAOcode = aircraftICAOcode , 
                                              aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode), 
                                              badaPerformanceFilePath =  acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                      atmosphere = atmosphere, earth = earth)
                            
                acPerformance = AircraftPerformance(acBd.getAircraftPerformanceFile(aircraftICAOcode))

                if ( ((acBada is None) == False) and ( isinstance( acBada, BadaAircraft ) ) and ((acPerformance is None) == False) ):
                                
                    print ( "Landing length meters = {0}".format(acBada.getLandingLengthMeters()) )
                    print ( "Take-off length meters = {0}".format(acBada.getTakeOffLengthMeters()) )      
                    print ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                    print ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   
                                
                    flightPath = FlightPath(route = route.getRouteAsString(), 
                                                    aircraftICAOcode = aircraftICAOcode,
                                                    RequestedFlightLevel = acPerformance.getMaxOpAltitudeFeet()/100., 
                                                    cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                                    takeOffMassKilograms = acPerformance.getMaximumMassKilograms())
                                
                    print ("=========== Flight Plan compute  =========== " + time.strftime("%c"))
                                
                    t0 = time.clock()
                    print ('time zero= ' + str(t0))
                    lengthNauticalMiles = flightPath.computeLengthNauticalMiles()
                    print ('flight path length= {0:.2f} nautics '.format(lengthNauticalMiles))
                                
                                    
                    try:
                        flightPath.computeFlight(deltaTimeSeconds = 1.0)
                        print ('simulation duration= ' + str(time.clock()-t0) + ' seconds')
                                        
                        takeOffMassKilograms = acBada.getMaximumMassKilograms()
                        print ( "TakeOff Mass (kilograms) = {0}".format( ( takeOffMassKilograms ) ) )
        
                        finalMassKilograms = flightPath.getAircraftCurrentMassKilograms()
                        print ( "Final Mass (kilograms) = {0}".format( ( finalMassKilograms ) ) )
                                        
                        flightDurationSeconds = flightPath.getFlightDurationSeconds()
                        print ( "Flight Duration (seconds) = {0}".format( ( flightDurationSeconds ) ) )
     
                                
                                    
                    except Exception as e:
                        print ("-----------> flight was aborted = {0}".format(e))
                                
                    print ("=========== Flight Plan create output files  =========== " + time.strftime("%c"))
                    flightPath.createFlightOutputFiles()
                    print ("=========== Flight Plan end  =========== " + time.strftime("%c"))

                    
                    
            print ("it is finished")
                
        
if __name__ == '__main__':
    unittest.main()