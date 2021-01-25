'''
Created on Jan 15, 2015

@author: Robert PASTOR

=========================== not working ==========================
'''

from Home.aerocalc.airspeed import tas2cas, cas2tas

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

if __name__ == '__main__':
    
    atmosphere = Atmosphere()

    print ( '=========== main start ==================' )
    for tas in range(0,100,1):
        cas1 = tas2cas(tas = tas , altitude = 100.0, temp='std', speed_units = 'm/s', alt_units='m')
        cas2 = atmosphere.tas2cas(tas, altitudeMeters = 100.0, speed_units = 'm/s', altitude_units = 'm')
        print ( tas, cas1, cas2 )
    
    print ( '=========== main start ==================' )

    for altitude in range(0, 10000, 100):
        cas = 100.0 # 100 m/s
        tas1 = cas2tas(cas = cas, altitude = altitude, temp='std', speed_units = 'm/s', alt_units='m')
        tas2 = atmosphere.cas2tas(cas = cas, altitudeMeters = altitude, speed_units = 'm/s', altitude_units = 'm')
        print ( 'altitude= {0} meters ... cas= {1} m/s constant ... tas1= {2} m/s ... tas2= {3} m/s'.format(altitude, cas, tas1, tas2) )
    
    print ( '=========== main start ==================' )

    earth = Earth()
    acBd = BadaAircraftDatabase()
    assert acBd.read()
    aircraftIcaoCode = 'B742'
    if ( acBd.aircraftExists(aircraftIcaoCode) 
        and acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftIcaoCode))):
        aircraft = BadaAircraft(aircraftIcaoCode, 
                                  acBd.getAircraftPerformanceFile(aircraftIcaoCode),
                                  atmosphere,
                                  earth)
        aircraft.dump()
    else:
        raise ValueError(': aircraft not found= ' + aircraftIcaoCode)
    massKilograms = 356000
    aircraft.setAircraftMassKilograms(massKilograms)
    KCAS = 182.0 # knots
    for alt in range(0,40000,1000):
        tas = cas2tas(cas = KCAS, altitude=alt, temp='std', speed_units = 'kt', alt_units='ft')
        print ( 'alt= {0} feet ... cas= {1} knots ... tas= {2} knots'.format(alt, KCAS, tas) )
    