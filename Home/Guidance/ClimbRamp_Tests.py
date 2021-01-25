'''
Created on 23 déc. 2020

@author: robert
'''
import unittest
import time


from Home.Guidance.GroundRunLegFile import GroundRunLeg

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Environment.AirportDatabaseFile import AirportsDatabase
from Home.Environment.AirportDatabaseFile import Airport

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth
from Home.Environment.RunWaysDatabaseFile import  RunWayDataBase
from Home.Environment.RunWayFile import RunWay

from Home.Guidance.ClimbRampFile import ClimbRamp


class Test_ClimbRamp(unittest.TestCase):

    def test_ClimbRamp(self):
        
        atmosphere = Atmosphere()
        earth = Earth()
        
        print ( '==================== Three Degrees climb slope ==================== '+ time.strftime("%c") )
        acBd = BadaAircraftDatabase()
        aircraftICAOcode = 'A320'
        aircraft = None
        if acBd.read():
            if ( acBd.aircraftExists(aircraftICAOcode) 
                 and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                
                print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
    
                aircraft = BadaAircraft(
                                    ICAOcode = aircraftICAOcode,
                                    aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                    badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                    atmosphere = atmosphere,
                                    earth = earth)
                assert ( isinstance(aircraft, BadaAircraft ))
                aircraft.dump()
        
        assert not(aircraft is None)
        
        print ( '==================== get Charles de Gaulle airport ==================== '+ time.strftime("%c") )
        airportsDB = AirportsDatabase()
        assert(airportsDB.read())
        
        CharlesDeGaulle = airportsDB.getAirportFromICAOCode('LFPG')
        assert ( isinstance(CharlesDeGaulle, Airport))
        
        print ( CharlesDeGaulle )
        
        aircraft.setTargetCruiseFlightLevel(RequestedFlightLevel = 390, 
                                            departureAirportAltitudeMSLmeters = CharlesDeGaulle.getAltitudeMeanSeaLevelMeters())
    
     
        
        print ( '==================== Three Degrees climb slope==================== '+ time.strftime("%c") )
        runWaysDatabase = RunWayDataBase()
        if runWaysDatabase.read():
            print ( 'runways DB correctly read' )
        
        runway = runWaysDatabase.getFilteredRunWays('LFPG')
        print ( runway )
        assert ( isinstance(runway, RunWay))
            
        print ( '==================== Ground Run ==================== '+ time.strftime("%c") )
        groundRun = GroundRunLeg(runway=runway, 
                                 aircraft=aircraft,
                                 airport=CharlesDeGaulle)
        
        groundRun.buildDepartureGroundRun(deltaTimeSeconds = 0.1,
                                    elapsedTimeSeconds = 0.0,
                                    distanceStillToFlyMeters = 100000.0,
                                    distanceToLastFixMeters = 100000.0)
        print ( '==================== Three Degrees climb slope==================== '+ time.strftime("%c") )
    
        initialVertex = groundRun.getVertex(groundRun.getNumberOfVertices()-1)
        initialWayPoint = initialVertex.getWeight()
    
        climbRamp = ClimbRamp(initialWayPoint = initialWayPoint,
                               runway=runway, 
                               aircraft=aircraft, 
                               departureAirport=CharlesDeGaulle)
        
        climbRamp.buildClimbRamp(deltaTimeSeconds = 0.1,
                           elapsedTimeSeconds = 0.0, 
                           distanceStillToFlyMeters = 100000.0, 
                           distanceToLastFixMeters = 100000.0,
                           climbRampLengthNautics = 5.0 )
        
        groundRun.addGraph(climbRamp)
        
        groundRun.createKmlOutputFile()
        print ( "=========== ThreeDegreesGlideSlope end =========== " + time.strftime("%c") )
    

if __name__ == '__main__':
    unittest.main()