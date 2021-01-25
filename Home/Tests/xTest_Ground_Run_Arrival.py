'''
Created on 24 janvier. 2015

@author: PASTOR Robert
'''

import time

from Home.aerocalc.airspeed import cas2tas, default_temp_units

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
    
    print ( '==================== Main test Arrival Ground Run Leg ==================== '+ time.strftime("%c") )
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
    
    arrivalAirportCode = 'LFPO'
    arrivalAirport = airportsDB.getAirportFromICAOCode(arrivalAirportCode)
    print ( arrivalAirport )

    print ( '====================  find the runway ==================== '+ time.strftime("%c") )
    runWaysDB = RunWayDataBase()
    assert runWaysDB.read()
    
    arrivalRunway = runWaysDB.getFilteredRunWays(arrivalAirportCode, 'Landing', aircraft.WakeTurbulenceCategory)
    print ( arrivalRunway )
    
    aircraft.setArrivalAirportElevationMeters(arrivalAirport.getFieldElevationAboveSeaLevelMeters())

    CAS = aircraft.computeLandingStallSpeedCasKnots()
    TAS = cas2tas(cas = CAS , 
                  altitude = arrivalAirport.getFieldElevationAboveSeaLevelMeters(),
                  temp = 'std',
                  speed_units = 'kt',
                  alt_units = 'm',
                  temp_units=default_temp_units,
                  )
    aircraft.initStateVector(elapsedTimeSeconds = 0.0, 
                             trueAirSpeedMetersSecond = TAS, 
                             altitudeMeanSeaLevelMeters = arrivalAirport.getFieldElevationAboveSeaLevelMeters(), 
                             deltaDistanceFlownMeters = 0.0)
    aircraft.setLandingConfiguration(0.0)
    groundRun = GroundRunLeg(runway = arrivalRunway, 
                             aircraft=aircraft,
                             airport=arrivalAirport)
    
    groundRun.buildArrivalGroundRun(0.0)
    groundRun.createXlsxOutputFile()
    groundRun.createKmlOutputFile() 