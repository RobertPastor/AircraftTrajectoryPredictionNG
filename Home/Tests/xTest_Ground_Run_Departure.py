# -*- coding: UTF-8 -*-
'''
Created on 4 Janvier 2015

@author: PASTOR Robert
'''
import time

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.Environment.AirportDatabaseFile import AirportsDatabase
from Home.Environment.RunWaysDatabaseFile import RunWayDataBase

from Home.Guidance.GroundRunLegFile import GroundRunLeg

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

if __name__ == '__main__':

    t0 = time.clock()
    print ( "time start= ", t0 )
    atmosphere = Atmosphere()
    earth = Earth()
    
    print ( '==================== Main test departure Ground Run Leg ==================== '+ time.strftime("%c") )
    acBd = BadaAircraftDatabase()
    aircraftICAOcode = 'A320'
    if acBd.read():
        if ( acBd.aircraftExists(aircraftICAOcode) 
             and acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftICAOcode))):
            
            print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
            aircraft = BadaAircraft(aircraftICAOcode, 
                                    acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                    atmosphere,
                                    earth)
            aircraft.dump()
            
    print ( '==================== Get Departure Airport ==================== '+ time.strftime("%c") )
    airportsDB = AirportsDatabase()
    assert airportsDB.read()

    print ( '====================  find the run-ways ==================== '+ time.strftime("%c") )
    runWaysDB = RunWayDataBase()
    if runWaysDB.read():
        print ( 'runways DB correctly read' )
    else:
        raise ValueError ('runways not read correctly')
    
    print ( '====================  find the run-ways ==================== '+ time.strftime("%c") )
    for runway in runWaysDB.getRunWays():
        
        print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
        aircraft = BadaAircraft(aircraftICAOcode, 
                                    acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                    atmosphere,
                                    earth)
        
        print ( '====================  run-way ==================== ' )
        print ( runway )
        
        airportIcaoCode = runway.getAirportICAOcode()
        departureAirport = airportsDB.getAirportFromICAOCode(airportIcaoCode)
        
        print ( '====================== departure airport =================' )
        print ( departureAirport )
        
        print ( '====================  ground run ==================== ' )
        groundRun = GroundRunLeg(runway = runway, 
                             aircraft = aircraft,
                             airport = departureAirport)
        groundRun.buildDepartureGroundRun(elapsedTimeSeconds = 0.0 , distanceStillToFlyMeters = 600000.0)    
        groundRun.createKmlOutputFile()

    