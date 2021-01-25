# -*- coding: UTF-8 -*-
'''
Created on 28 déc. 2014

@author: PASTOR Robert
'''
import time

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Environment.AirportDatabaseFile import AirportsDatabase

Meter2Feet = 3.2808399 # one meter approx == 3 feet (3 feet 3 inches)


if __name__ == '__main__':

    t0 = time.clock()
    print ( "time start= ", t0 )
    
    atmosphere = Atmosphere()
    earth = Earth()

    print ( '==================== Fuel Flow Testing ==================== '+ time.strftime("%c") )
    
    print ( '==================== BadaAircraftDatabase ==================== '+ time.strftime("%c"))
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
                                    earth =earth)
            aircraft.dump()
            
    print ( '==================== read Airports Database ==================== '+ time.strftime("%c") )
    airportsDB = AirportsDatabase()
    airport = airportsDB.getAirportFromICAOCode('LFPG')

            
    print ( '==================== fuel flow testing  ==================== '+ time.strftime("%c") )
    
    elapsedTimeSeconds = 0.0
    
    for index in range(0,100):
        print ( '==================== fuel flow testing  ==================== '+ time.strftime("%c") )

        deltaTimeSeconds = 1.0
        elapsedTimeSeconds += deltaTimeSeconds

        print ( 'elapsed time= ' + str(elapsedTimeSeconds) + ' fuel flow kilograms= ' + str(aircraft.getAircraftMassKilograms()) )
        aircraft.updateAircraftMassKilograms(elapsedTimeSeconds, 
                                            deltaTimeSeconds, 
                                            airport.getFieldElevationAboveSeaLevelMeters()* Meter2Feet)

    
    print ( '==================== fuel flow testing  ==================== '+ time.strftime("%c") )


