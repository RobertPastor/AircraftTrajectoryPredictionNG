'''
Created on Feb 5, 2015

@author: Robert PASTOR
'''
import time

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.Environment.RunWaysDatabaseFile import RunWayDataBase
from Home.Environment.AirportDatabaseFile import AirportsDatabase

from Home.Guidance.GroundRunLegFile import GroundRunLeg
from Home.Guidance.DescentGlideSlopeFile import DescentGlideSlope

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

Knots2MetersPerSecond = 0.514444444
 
if __name__ == '__main__':

    t0 = time.clock()
    print ( "time start= ", t0 )
    
    print ( '================ get aircraft =================' )
    aircraftIcaoCode = 'A320'
    atmosphere = Atmosphere()
    earth = Earth()
    
    acBd = BadaAircraftDatabase()
    assert acBd.read()
        
    if ( acBd.aircraftExists(aircraftIcaoCode) 
            and acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftIcaoCode))):
            
        aircraft = BadaAircraft(aircraftIcaoCode, 
                                  acBd.getAircraftPerformanceFile(aircraftIcaoCode),
                                  atmosphere,
                                  earth)
        aircraft.dump()
    else:
        raise ValueError(': aircraft not found= ' + aircraftIcaoCode)



    print ( '====================  find the run-ways ==================== '+ time.strftime("%c") )
    runWaysDb = RunWayDataBase()
    assert (runWaysDb.read())

    arrivalAirportICAOcode = 'LFPO'
    arrivalRunway =  runWaysDb.getFilteredRunWays(airportICAOcode = arrivalAirportICAOcode, 
                           TakeOffLanding='Landing', 
                           aircraftWakeTurbulence=aircraft.getWakeTurbulenceCategory())
    
    
    print ( '==================== read Airports Database ==================== '+ time.strftime("%c") )
    airportsDB = AirportsDatabase()
    assert (airportsDB.read())
    
    print ( '========== departure is LONDON ================' )
    departureAirport = airportsDB.getAirportFromICAOCode('EGLL')
    assert not(departureAirport is None)
        
    print ( '========== ' + str(arrivalRunway) + ' =================' )
    airportIcaoCode = arrivalRunway.getAirportICAOcode()
    arrivalAirport = airportsDB.getAirportFromICAOCode(airportIcaoCode)
    print ( 'arrival airport= {0}'.format(arrivalAirport) )

    aircraft.setArrivalAirportElevationMeters(arrivalAirport.fieldElevationAboveSeaLevelMeters)

    print ( '=========== add final turn, descent and ground run ===================' )
    arrivalGroundRun = GroundRunLeg( runway   = arrivalRunway,
                                         aircraft = aircraft,
                                         airport  = arrivalAirport )
    touchDownWayPoint = arrivalGroundRun.computeTouchDownWayPoint()
    print ( touchDownWayPoint )
        
    print ( '===================== final 3 degrees descending glide slope ================' )
    dummyDescentGlideSlope = DescentGlideSlope( runway   = arrivalRunway,
                                               aircraft = aircraft,
                                               arrivalAirport = arrivalAirport,
                                               descentGlideSlopeDegrees = 3.0)
    dummyDescentGlideSlope.buildSimulatedGlideSlope()
    firstGlideSlopeWayPoint = dummyDescentGlideSlope.getVertex(v=0).getWeight()
    
    print ( '=============== init aircraft state vector =================' )
    
    casKnots = 107.0
    casMetersPerSecond = casKnots * Knots2MetersPerSecond
    tasMetersPerSecond = atmosphere.cas2tas(casMetersPerSecond, 950.0, speed_units='m/s', altitude_units='m')
    
    elapsedTimeSeconds = 0.0
    aircraft.initStateVector(elapsedTimeSeconds = elapsedTimeSeconds ,
                          trueAirSpeedMetersSecond = tasMetersPerSecond , 
                          altitudeMeanSeaLevelMeters = firstGlideSlopeWayPoint.getAltitudeMeanSeaLevelMeters(),
                          deltaDistanceFlownMeters = 0.0)

    aircraft.setApproachConfiguration(0.0)
    aircraftMassKilograms = 49000.0
    aircraft.setAircraftMassKilograms(aircraftMassKilograms)
    
    print ( '===================== final 3 degrees descending glide slope ================' )
    descentGlideSlope = DescentGlideSlope( runway   = arrivalRunway,
                                               aircraft = aircraft,
                                               arrivalAirport = arrivalAirport,
                                               descentGlideSlopeDegrees = 3.0)

    descentGlideSlope.buildGlideSlope(elapsedTimeSeconds=0.0, 
                                      initialWayPoint=firstGlideSlopeWayPoint, 
                                      flownDistanceMeters = 300000.0, 
                                      distanceStillToFlyMeters=10000.0)
    print ( '================= create output files =========================' )

    descentGlideSlope.createXlsxOutputFile()
    descentGlideSlope.createKmlOutputFile()
    aircraft.createStateVectorOutputFile()
    
    print ( '===================== end of simulation ================' )

        

        