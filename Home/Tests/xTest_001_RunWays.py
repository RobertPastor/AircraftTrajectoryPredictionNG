'''
Created on Dec 22, 2014

@author: Robert PASTOR

for each existing runways, the test program creates 
1) a climb ramp
2) a descent glide slope

based upon the runway data.
'''


import time

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.Environment.RunWaysDatabaseFile import RunWayDataBase
from Home.Environment.AirportDatabaseFile import AirportsDatabase

from Home.Guidance.ClimbRampFile import ClimbRamp
from Home.Guidance.DescentGlideSlopeFile import DescentGlideSlope

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

if __name__ == '__main__':

    t0 = time.clock()
    print ( "time start= ", t0 )
    
    atmosphere = Atmosphere()
    earth = Earth()
    
    print ( '==================== Run-Ways Testing ==================== ' )
    
    acBd = BadaAircraftDatabase()
    aircraftICAOcode = 'A320'
    assert acBd.read()
    assert acBd.aircraftExists(aircraftICAOcode)
    if acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftICAOcode)):
            
        print ( '==================== aircraft found  ==================== ' )
        acA320 = BadaAircraft(aircraftICAOcode, 
                              acBd.getAircraftPerformanceFile(aircraftICAOcode),
                              atmosphere,
                              earth)
        acA320.dump()
            
    print ( '==================== read Airports Database ==================== ' )
    airportsDb = AirportsDatabase()
    assert (airportsDb.read())
    
    print ( '====================  find the run-ways ==================== ' )
    runWaysDB = RunWayDataBase()
    if runWaysDB.read(): 
        print ( 'runways DB correctly read' )
    else:
        raise ValueError ('runways not read correctly')
    
    print ( '====================  find the run-ways ==================== ' )
    for arrivalRunway in runWaysDB.getRunWays():
        
        print ( '====================  run-way ==================== ' )
        print ( arrivalRunway )
        
        airportIcaoCode = arrivalRunway.getAirportICAOcode()
        airport = airportsDb.getAirportFromICAOCode(airportIcaoCode)
        print ( '====================  airport ==================== ' )

        print ( airport )

        climbRamp = ClimbRamp(runway = arrivalRunway, 
                              aircraft = acA320,
                              departureAirport = airport)
        climbRamp.buildClimbRamp()
        climbRamp.createXlsxOutputFile()
        
        descentSlope = DescentGlideSlope(runway = arrivalRunway, 
                                         aircraft = acA320, 
                                         arrivalAirport = airport)
        descentSlope.buildGlideSlope()
        descentSlope.createXlsxOutputFile()
        