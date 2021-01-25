'''
Created on January 20, 2015

@author: Robert PASTOR

demonstrate that Vertical Phase changes according to aircraft CAS speed

'''
import time
import math

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft
from Home.Environment.AirportDatabaseFile import AirportsDatabase
from Home.Environment.RunWaysDatabaseFile import RunWayDataBase

from Home.Guidance.GroundRunLegFile import GroundRunLeg
from Home.Guidance.DescentGlideSlopeFile import DescentGlideSlope

Feet2Meter = 0.3048 # 1 feet = 0.3048 meter
Meter2Feet = 3.2808399 

if __name__ == '__main__':

    print ( '=========== main start ==================' )
    aircraftIcaoCode = 'A320'
    
    atmosphere = Atmosphere()
    assert (not(atmosphere is None))
    
    earth = Earth()
    assert (not(earth is None))

    acBd = BadaAircraftDatabase()
    assert acBd.read()
    
    print ( '==================== load airports ==================== '+ time.strftime("%c") )
    airportsDB = AirportsDatabase()
    assert airportsDB.read()
    
    departureAirport = airportsDB.getAirportFromICAOCode('LFPG')
    assert not(departureAirport is None)
    print ( departureAirport )
    
    arrivalAirportIcaoCode = 'LFML'
    arrivalAirport = airportsDB.getAirportFromICAOCode(arrivalAirportIcaoCode)
    assert not(arrivalAirport is None)
    print ( arrivalAirport )
    
    runwaysDb = RunWayDataBase()
    assert runwaysDb.read()
    
    arrivalRunway =  runwaysDb.getFilteredRunWays(arrivalAirportIcaoCode, 'Landing')
    
    if ( acBd.aircraftExists(aircraftIcaoCode) 
        and acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftIcaoCode))):
        aircraft = BadaAircraft(aircraftIcaoCode, 
                                  acBd.getAircraftPerformanceFile(aircraftIcaoCode),
                                  atmosphere,
                                  earth)
        aircraft.dump()
    assert not(aircraft is None)

    elapsedTimeSeconds = 0.0
    deltaTimeSeconds = 1.0
    
    aircraft.initStateVector(elapsedTimeSeconds = 0.0, 
                               trueAirSpeedMetersSecond = 0.0, 
                               altitudeMeanSeaLevelMeters = 0.0)
    
    aircraft.setTargetCruiseFlightLevel(RequestedFlightLevel = 310.0 , 
                                        departureAirportAltitudeMSLmeters = 0.0)
    aircraft.setAircraftMassKilograms(aircraftMassKilograms = 64000.0)
    aircraft.setTargetCruiseMach(cruiseMach = 0.8)
    
    tas = aircraft.getCurrentTrueAirSpeedMetersSecond()
    previousAltitudeMSLmeters = 0.0
    t0 = time.clock()
    print ( 'simulation start= {0} seconds'.format(t0) )
    print ( '=========== simulation start ==================' )
    endOfSimulation = False
    currentPosition = departureAirport
    
    arrivalGroundRun = GroundRunLeg( runway   = arrivalRunway,
                                    aircraft = aircraft,
                                    airport  = arrivalAirport )
    touchDownWayPoint = arrivalGroundRun.computeTouchDownWayPoint()
    print ( touchDownWayPoint )

    print ( '===================== final 3 degrees descending glide slope ================' )
    descentGlideSlope = DescentGlideSlope( runway   = arrivalRunway,
                                               aircraft = aircraft,
                                               arrivalAirport = arrivalAirport,
                                               descentGlideSlopeDegrees = 3.0)
    ''' if there is a fix nearer to 5 nautics of the touch-down then limit size of simulated glide slope '''
    descentGlideSlopeSizeNautics = 5.0

    descentGlideSlope.buildSimulatedGlideSlope(descentGlideSlopeSizeNautics)
    firstGlideSlopeWayPoint = descentGlideSlope.getVertex(v=0).getWeight()
    aircraft.setTargetApproachWayPoint(firstGlideSlopeWayPoint)
    aircraft.setArrivalRunwayTouchDownWayPoint(touchDownWayPoint)
    
    distanceStillToFlyMeters = departureAirport.getDistanceMetersTo(arrivalAirport)
    print ( 'distance still To Fly Meters= {0:.2f} meters'.format(distanceStillToFlyMeters) )
    
    index = 0
    while (endOfSimulation == False and not(aircraft.isLanding())):
        endOfSimulation, deltaDistanceMeters, altitudeMeters = aircraft.fly(elapsedTimeSeconds, 
                                                           deltaTimeSeconds, 
                                                           distanceStillToFlyMeters,
                                                           currentPosition)
        distanceStillToFlyMeters = distanceStillToFlyMeters - deltaDistanceMeters
        RateOfClimbDescentFeetMinute = ((altitudeMeters - previousAltitudeMSLmeters) * Meter2Feet) / (deltaTimeSeconds / 60.0) 
        previousAltitudeMSLmeters = altitudeMeters
        #if math.fmod(elapsedTimeSecond)
        #print 'rate of climb / descent= {0} feet/minute'.format(RateOfClimbDescentFeetMinute)
        #print 'altitude= {0} feet'.format(altitudeMeters * Meter2Feet)
        elapsedTimeSeconds += deltaTimeSeconds
        bearingDegrees = currentPosition.getBearingDegreesTo(firstGlideSlopeWayPoint)
        newWayPoint = currentPosition.getWayPointAtDistanceBearing(Name='pt-{0}'.format(index), 
                                                                       DistanceMeters= deltaDistanceMeters, 
                                                                       BearingDegrees = bearingDegrees)
        newWayPoint.setAltitudeAboveSeaLevelMeters(altitudeMeters)
        distanceStillToFlyMeters = newWayPoint.getDistanceMetersTo(arrivalAirport)
        currentPosition = newWayPoint
        index = index + 1
        
    print ( '=========== create State Vector output file ==================' )
    print ( 'simulation end - duration= {0} seconds'.format(time.clock()-t0))
    aircraft.createStateVectorOutputFile()
    print ( '=========== simulation end ==================')
