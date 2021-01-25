'''
Created on January 20, 2015

@author: Robert PASTOR

demonstrate that Vertical Phase changes according to aircraft CAS speed

'''
import time

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

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

    if ( acBd.aircraftExists(aircraftIcaoCode) 
        and acBd.aircraftPerformanceFileExists(aircraftIcaoCode)):
        aircraft = BadaAircraft(aircraftIcaoCode, 
                                  acBd.getAircraftPerformanceFile(aircraftIcaoCode),
                                  atmosphere,
                                  earth)
        aircraft.dump()
    else:
        raise ValueError(': aircraft not found= ' + aircraftIcaoCode)
    assert not(aircraft is None)

    latitudeDegrees = 45.0
    distanceStillToFlyMeters = 500000.0
    
    elapsedTimeSeconds = 0.0
    deltaTimeSeconds = 1.0
    
    aircraft.initStateVector(elapsedTimeSeconds = 0.0, 
                               trueAirSpeedMetersSecond = 0.0, 
                               altitudeMeanSeaLevelMeters = 0.0)
    aircraft.setArrivalAirportElevationMeters(0.0)
    
    aircraft.setTargetCruiseFlightLevel(RequestedFlightLevel = 310.0 , 
                                        departureAirportAltitudeMSLmeters = 0.0)
    aircraft.setAircraftMassKilograms(massKilograms = 64000.0)
    aircraft.setTargetCruiseMach(cruiseMach = 0.8)
    
    tas = aircraft.getCurrentTrueAirSpeedMetersSecond()
    previousAltitudeMSLmeters = 0.0
    t0 = time.clock()
    print ( 'simulation start= {0} seconds'.format(t0) )
    print ( '=========== simulation start ==================' )
    endOfSimulation = False
    while ( (endOfSimulation == False) and not(aircraft.isLandingConfiguration())):
        endOfSimulation, deltaDistanceMeters, altitudeMeters = aircraft.fly(elapsedTimeSeconds, 
                                                           deltaTimeSeconds, 
                                                           latitudeDegrees, 
                                                           distanceStillToFlyMeters)
        distanceStillToFlyMeters = distanceStillToFlyMeters - deltaDistanceMeters
        RateOfClimbDescentFeetMinute = ((altitudeMeters - previousAltitudeMSLmeters) * Meter2Feet) / (deltaTimeSeconds / 60.0) 
        previousAltitudeMSLmeters = altitudeMeters
        #if math.fmod(elapsedTimeSecond)
        #print 'rate of climb / descent= {0} feet/minute'.format(RateOfClimbDescentFeetMinute)
        #print 'altitude= {0} feet'.format(altitudeMeters * Meter2Feet)
        elapsedTimeSeconds += deltaTimeSeconds
        
    print ( '=========== create State Vector output file ==================')
    print ( 'simulation end - duration= {0} seconds'.format(time.clock()-t0) )
    aircraft.createStateVectorOutputFile()
    print ( '=========== simulation end ==================' )
