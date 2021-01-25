# -*- coding: UTF-8 -*-
'''
Created on 11 february 2015

@author: PASTOR Robert

demonstrate that turn radius is increasing with True Air Speed
extract from A320 Airbus instructor manual

The RADIUS OF TURN of the trajectory is a function of TAS and BANK.
TAS [kt] RADIUS (15° Φ) [NM] RADIUS (25° Φ) [NM]
150             1.2                 0.7
180             1.8                 1.0
210             2.4                 1.4
250             3.4                 2.0
300             4.9                 2.8
480             12.5                 7.2

'''

from Home.Environment.Earth import Earth
from Home.Environment.Atmosphere import Atmosphere

from Home.Environment.AirportDatabaseFile import AirportsDatabase

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Guidance.TurnLegFile import TurnLeg


Meter2Feet = 3.2808 # one meter equals 3.28 feet
Knots2MetersPerSecond = 0.514444444

if __name__ == '__main__':
    
    
    airportsDb = AirportsDatabase()
    assert airportsDb.read()
    departureAirport = airportsDb.getAirportFromICAOCode('LFPO')
    arrivalAirport = airportsDb.getAirportFromICAOCode('LFBO')
    
    atmosphere = Atmosphere()
    earth = Earth()
    
    acBd = BadaAircraftDatabase()
    assert acBd.read()
    aircraftIcaoCode = 'A320'
    if ( acBd.aircraftExists(aircraftIcaoCode) 
        and acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftIcaoCode))):
        
        tasKnots = 480.0
        print ( '--------------- tas= {0:.2f} knots ----------------------'.format(tasKnots) )
        aircraft = BadaAircraft(aircraftIcaoCode, 
                                      acBd.getAircraftPerformanceFile(aircraftIcaoCode),
                                      atmosphere,
                                      earth)
        aircraft.dump()
    
        takeOffMassKilograms = 64000.0
        aircraft.setAircraftMassKilograms(takeOffMassKilograms)
            
        RequestedFlightLevel = 310.0
        fieldElevationAboveSeaLevelMeters = 150.0
        aircraft.setTargetCruiseFlightLevel(RequestedFlightLevel, fieldElevationAboveSeaLevelMeters)
        tasMetersPerSecond = tasKnots * Knots2MetersPerSecond
        aircraft.initStateVector(elapsedTimeSeconds = 0.0, 
                                     trueAirSpeedMetersSecond = tasMetersPerSecond, 
                                     altitudeMeanSeaLevelMeters = 3000.0 * Meter2Feet, 
                                     deltaDistanceFlownMeters = 0.0)
        aircraft.setCruiseConfiguration(elapsedTimeSeconds = 0.0)
            
        turnLeg =  TurnLeg(  initialWayPoint  = departureAirport,
                                finalWayPoint    = arrivalAirport,
                                initialHeadingDegrees = 215.0,
                                finalHeadingDegrees = 180.0,
                                aircraft = aircraft,
                                reverse = False)
        
        distanceStillToFlyMeters = 700000.0
        turnLeg.buildTurnLeg(elapsedTimeSeconds = 0.0, distanceStillToFlyMeters = distanceStillToFlyMeters)
        turnLeg.createKmlOutputFile()
        turnLeg.createXlsxOutputFile()
