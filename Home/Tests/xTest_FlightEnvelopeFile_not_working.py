'''
Created on January 12, 2015

@author: Robert PASTOR
==================== not working =========================
'''

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.OutputFiles.XlsxOutputFile import XlsxOutput

Meter2Feet = 3.2808
Knots2MetersPerSecond = 0.514444444



#============================================
if __name__ == '__main__':
    
    FileName = "FlightEnvelope.xlsx"
    print ( "=================== Flight Envelope start======================" )
    
    aircraftIcaoCode = 'A320'
    
    atmosphere = Atmosphere()
    assert not(atmosphere is None)
    
    earth = Earth()
    assert not(earth is None)

    acBd = BadaAircraftDatabase()
    assert acBd.read()
        
    assert acBd.aircraftExists(aircraftIcaoCode) 
    assert acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftIcaoCode))
    
            
    aircraft = BadaAircraft(aircraftIcaoCode, 
                                  acBd.getAircraftPerformanceFile(aircraftIcaoCode),
                                  atmosphere,
                                  earth)
    aircraft.dump()
        
