import time
import unittest

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth
from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft
from Home.Environment.AirportDatabaseFile import  AirportsDatabase
from Home.Environment.WayPointsDatabaseFile import WayPointsDatabase
from Home.Environment.RunWaysDatabaseFile import RunWayDataBase

from Home.Guidance.DescentGlideSlopeFile import DescentGlideSlope
from Home.Guidance.GroundRunLegFile import GroundRunLeg

from Home.Guidance.GreatCircleRouteFile import GreatCircleRoute

#============================================
class Test_Class(unittest.TestCase):

    def test_One(self):  
        
        atmosphere = Atmosphere()
        earth = Earth()
        
        print ( '==================== Aircraft ==================== '+ time.strftime("%c") )
        acBd = BadaAircraftDatabase()
        aircraftICAOcode = 'A320'
        if acBd.read():
            if ( acBd.aircraftExists(aircraftICAOcode) 
                 and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                
                print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
                aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                            aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                            badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                            atmosphere = atmosphere,
                                            earth = earth)
                print ( aircraft )
                assert not(aircraft is None)
            
        print ( '==================== departure airport ==================== '+ time.strftime("%c") )
        
        airportsDB = AirportsDatabase()
        assert (airportsDB.read())
        
        CharlesDeGaulle = airportsDB.getAirportFromICAOCode('LFPG')
        print ( CharlesDeGaulle )
        
        print ( '==================== arrival airport ==================== '+ time.strftime("%c") )

        MarseilleMarignane = airportsDB.getAirportFromICAOCode('LFML')
        print ( MarseilleMarignane )
            
        print ( '==================== Great Circle ==================== '+ time.strftime("%c") )
    
        aircraft.setCurrentAltitudeSeaLevelMeters( 
                                         elapsedTimeSeconds = 0.0 , 
                                         altitudeMeanSeaLevelMeters = 0.0,
                                         lastAltitudeMeanSeaLevelMeters = 0.0,
                                         targetCruiseAltitudeMslMeters = 10000.0)
        
        aircraft.initStateVector( 
                        elapsedTimeSeconds = 0.0,
                        trueAirSpeedMetersSecond = 70.0,
                        airportFieldElevationAboveSeaLevelMeters = 152.0)
        
        aircraft.setTargetCruiseFlightLevel(RequestedFlightLevel = 310, 
                                   departureAirportAltitudeMSLmeters = 152.0)
        
        print ( '==================== runways database ==================== '+ time.strftime("%c") )
        
        runWaysDatabase = RunWayDataBase()
        assert runWaysDatabase.read()
        arrivalRunway = runWaysDatabase.getFilteredRunWays(airportICAOcode = 'LFML', runwayName = '31R')
        print ( arrivalRunway )

        print ( '==================== Compute touch down ==================== '+ time.strftime("%c") )

        arrivalGroundRun = GroundRunLeg( runway   = arrivalRunway,
                                         aircraft = aircraft,
                                         airport  = MarseilleMarignane )
        
        touchDownWayPoint = arrivalGroundRun.computeTouchDownWayPoint()
        aircraft.setArrivalRunwayTouchDownWayPoint(touchDownWayPoint)

        print ( "=========== simulated descent glide slope  =========== " + time.strftime("%c") )
 
        threeDegreesGlideSlope = DescentGlideSlope(runway = arrivalRunway, 
                                                   aircraft = aircraft, 
                                                   arrivalAirport = MarseilleMarignane )
        
        threeDegreesGlideSlope.buildSimulatedGlideSlope(descentGlideSlopeSizeNautics = 5.0)
        approachWayPoint = threeDegreesGlideSlope.getLastVertex().getWeight()
        
        aircraft.setTargetApproachWayPoint(approachWayPoint)
        
        print ( '==================== Great Circle ==================== '+ time.strftime("%c") )

        greatCircle = GreatCircleRoute(initialWayPoint = CharlesDeGaulle, 
                                           finalWayPoint = approachWayPoint,
                                           aircraft = aircraft)
        
        distanceStillToFlyMeters = CharlesDeGaulle.getDistanceMetersTo(approachWayPoint)
        greatCircle.computeGreatCircle(deltaTimeSeconds = 1.0,
                           elapsedTimeSeconds = 0.0,
                           distanceStillToFlyMeters = distanceStillToFlyMeters,
                           distanceToLastFixMeters = distanceStillToFlyMeters)
        print ( 'main great circle length= ' + str(greatCircle.computeLengthMeters()) + ' meters' )
                        
        greatCircle.createKmlOutputFile(False, aircraftICAOcode, CharlesDeGaulle.getName(), MarseilleMarignane.getName())
        greatCircle.createXlsxOutputFile(False, aircraftICAOcode, CharlesDeGaulle.getName(), MarseilleMarignane.getName())
        

    def test_Two(self):  
    
        t0 = time.clock()
        print ( " ========== Great Circle ======= time start= ", t0 )
        atmosphere = Atmosphere()
        earth = Earth()
        
        print ( '==================== Great Circle ==================== '+ time.strftime("%c") )
        acBd = BadaAircraftDatabase()
        aircraftICAOcode = 'A320'
        if acBd.read():
            if ( acBd.aircraftExists(aircraftICAOcode) 
                 and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                
                print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
                aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                            aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                            badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                            atmosphere = atmosphere,
                                            earth = earth)
                print ( aircraft )
        
        else:
            
            print ( '====================  airport database ==================== '+ time.strftime("%c") )
            airportsDB = AirportsDatabase()
            assert not(airportsDB is None)
            
            wayPointsDb = WayPointsDatabase()
            assert (wayPointsDb.read())
        
            initialWayPoint = wayPointsDb.getWayPoint('TOU')
            finalWayPoint = wayPointsDb.getWayPoint('ALIVA') 
            print ( initialWayPoint.getBearingDegreesTo(finalWayPoint) )
            print ( finalWayPoint.getBearingDegreesTo(initialWayPoint) )
            
            ''' departure ground run => initial speed is null '''
            trueAirSpeedMetersSecond = 70.0
            elapsedTimeSeconds = 0.0
    
            aircraft.setCurrentAltitudeSeaLevelMeters( 
                                             elapsedTimeSeconds = 0.0 , 
                                             altitudeMeanSeaLevelMeters = 0.0,
                                             lastAltitudeMeanSeaLevelMeters = 0.0,
                                             targetCruiseAltitudeMslMeters = 10000.0)
                   
            aircraft.initStateVector( 
                            elapsedTimeSeconds = 0.0,
                            trueAirSpeedMetersSecond = 70.0,
                            airportFieldElevationAboveSeaLevelMeters = 152.0)
            
            aircraft.setTargetCruiseFlightLevel(RequestedFlightLevel = 310, 
                                       departureAirportAltitudeMSLmeters = 152.0)
            
            print ( "=========== simulated descent glide slope  =========== " + time.strftime("%c") )
            MarseilleMarignane = airportsDB.getAirportFromICAOCode('LFML')
            
            print ( '==================== runways database ==================== '+ time.strftime("%c") )
            runWaysDatabase = RunWayDataBase()
            assert runWaysDatabase.read()
            runway = runWaysDatabase.getFilteredRunWays(airportICAOcode = 'LFML', runwayName = '')
    
            arrivalGroundRun = GroundRunLeg( runway   = runway,
                                             aircraft = aircraft,
                                             airport  = MarseilleMarignane )
            
            touchDownWayPoint = arrivalGroundRun.computeTouchDownWayPoint()
            aircraft.setArrivalRunwayTouchDownWayPoint(touchDownWayPoint)
    
            threeDegreesGlideSlope = DescentGlideSlope(runway = runway, 
                                                       aircraft = aircraft, 
                                                       arrivalAirport = MarseilleMarignane )
            threeDegreesGlideSlope.buildSimulatedGlideSlope(descentGlideSlopeSizeNautics = 5.0)
            approachWayPoint = threeDegreesGlideSlope.getLastVertex().getWeight()
            
            aircraft.setTargetApproachWayPoint(approachWayPoint)
            
            ''' =================================='''
            greatCircle = GreatCircleRoute(initialWayPoint = initialWayPoint, 
                                            finalWayPoint = finalWayPoint,
                                            aircraft = aircraft)
            
            distanceStillToFlyMeters = initialWayPoint.getDistanceMetersTo(approachWayPoint)
    
            greatCircle.computeGreatCircle( 
                               deltaTimeSeconds = 0.1,
                               elapsedTimeSeconds = 0.0,
                               distanceStillToFlyMeters = distanceStillToFlyMeters,
                               distanceToLastFixMeters = distanceStillToFlyMeters)
            
            print ( 'main great circle length= ' + str(greatCircle.computeLengthMeters()) + ' meters' )
    
            greatCircle.createKmlOutputFile(False, aircraftICAOcode, "Great-Circle", MarseilleMarignane.getName())
            greatCircle.createXlsxOutputFile(False, aircraftICAOcode, "Great-Circle", MarseilleMarignane.getName())
        
        
if __name__ == '__main__':
    unittest.main()