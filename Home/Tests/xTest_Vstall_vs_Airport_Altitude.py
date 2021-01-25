# -*- coding: UTF-8 -*-

'''
Created on 29 decembre 2014

@author: PASTOR Robert
'''

import time
import unittest

from Home.aerocalc.airspeed import cas2tas, default_temp_units

from Home.Environment.Atmosphere import  Atmosphere
from Home.Environment.Earth import Earth

from Home.Environment.AirportDatabaseFile import  AirportsDatabase

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

class Test_Vstall(unittest.TestCase):

    def test_Vstall(self):
        
        
        t0 = time.clock()
        print ( "time start= ", t0 )
        
        atmosphere = Atmosphere()
        earth = Earth()
        print ( '==================== Stall Speed according to airport field elevation ==================== '+ time.strftime("%c") )
        acBd = BadaAircraftDatabase()
        aircraftICAOcode = 'B743'
        if acBd.read():
            if ( acBd.aircraftExists(aircraftICAOcode) 
                 and acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftICAOcode))):
                
                print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
                aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                        aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                        badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                        atmosphere = atmosphere,
                                        earth = earth)
                aircraft.dump()
                
        print ( '==================== Airport database ==================== '+ time.strftime("%c") )
        airportsDB = AirportsDatabase()
        assert airportsDB.read()
        for airport in airportsDB.getAirports():
            print ( '============' + airport.getName() + ' ============' )
            #print airport
            aircraft = BadaAircraft(ICAOcode =  aircraftICAOcode, 
                                        aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                        badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                        atmosphere = atmosphere,
                                        earth = earth)
            print ( 'airport field elevation= {0:.2f} meters'.format( airport.getFieldElevationAboveSeaLevelMeters()) )
            CAS = aircraft.computeStallSpeedCasKnots()
            print ( 'V stall Calibrated AirSpeed= {0:.2f} knots'.format(CAS)  )
            TAS = cas2tas(cas = CAS , 
                  altitude = airport.getFieldElevationAboveSeaLevelMeters(),
                  temp = 'std',
                  speed_units = 'kt',
                  alt_units = 'm',
                  temp_units=default_temp_units,
                  )
            print ( 'V stall True AirSpeed= {0:.2f} knots'.format(TAS)  )

    

    #============================================
if __name__ == '__main__':
    unittest.main()

    