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

from Home.Guidance.GroundRunLegFile import GroundRunLeg
from Home.Guidance.ClimbRampFile import ClimbRamp

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

if __name__ == '__main__':

    t0 = time.clock()
    print ( "time start= ", t0 )
    atmosphere = Atmosphere()
    earth = Earth()
    
    print ( '==================== Run-Ways Testing ==================== '+ time.strftime("%c") )
    
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
            
    print ( '==================== read Airports Database ==================== '+ time.strftime("%c") )
    airportsDB = AirportsDatabase()
    airport = airportsDB.getAirportFromICAOCode('LFPG')
    
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
        
        print ( '==========================' )
        print ( runway )
        airportIcaoCode = runway.getAirportICAOcode()
        airport = airportsDB.getAirportFromICAOCode(airportIcaoCode)
        
        print ( '==========================' )
        print ( airport )
        
        print ( '====================  ground run ==================== '+ time.strftime("%c") )

        groundRun = GroundRunLeg(runway=runway, 
                             aircraft=aircraft,
                             airport=airport)
        groundRun.buildDepartureGroundRun()
        initialWayPoint = groundRun.getLastVertex().getWeight()
        
        climbRamp = ClimbRamp(initialWayPoint=initialWayPoint,
                              runway=runway, 
                              aircraft=aircraft, 
                              departureAirport=airport)
        climbRamp.buildClimbRamp()
        groundRun.addGraph(climbRamp)
        groundRun.createKmlOutputFile()
 
        