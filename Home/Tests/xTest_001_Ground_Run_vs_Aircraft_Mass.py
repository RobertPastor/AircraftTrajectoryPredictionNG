'''
Created on January 12, 2015

@author: Robert PASTOR

verify that ground run length varies with aircraft mass

'''

import unittest


from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Guidance.GroundRunLegFile import GroundRunLeg

from Home.Environment.RunWaysDatabaseFile import RunWayDataBase
from Home.Environment.AirportDatabaseFile import AirportsDatabase



class Test_Ground_Run_versus_Aircraft_Mass(unittest.TestCase):

    def test_One(self):
        
        
        print ( '=========== main start ==================' )
        aircraftICAOcode = 'A320'
    
        atmosphere = Atmosphere()
        assert (not(atmosphere is None))
        
        earth = Earth()
        assert (not(earth is None))
    
        acBd = BadaAircraftDatabase()
        assert acBd.read()
            
        if ( acBd.aircraftExists(aircraftICAOcode) and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                
                aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                        aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                    badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                    atmosphere = atmosphere,
                                    earth = earth)
                aircraft.dump()
        else:
            raise ValueError(': aircraft not found= ' + aircraftICAOcode)
    
        assert not(aircraft is None)
        
        print ( '================ load airports =================' )
        airportsDB = AirportsDatabase()
        assert (airportsDB.read())
        
        adepIcaoCode = 'LFML'
    
        departureAirport = airportsDB.getAirportFromICAOCode(adepIcaoCode)
        print ( ': departure airport= ' + str(departureAirport) )
        assert not (departureAirport is None)
        
        print ( '================ load runways =================' )
    
        runWaysDatabase = RunWayDataBase()
        assert (runWaysDatabase.read())
    
        print ( '====================  take off run-way ==================== ' )
        departureRunway = runWaysDatabase.getFilteredRunWays(adepIcaoCode)
        print ( '=========== minimum and maximum aircraft mass ==================' )
    
        minMassKg = aircraft.getMinimumMassKilograms()
        print ( 'aircraft minimum mass: ' + str(minMassKg) + ' kilograms' )
        
        maxMassKg = aircraft.getMaximumMassKilograms()
        print ( 'aircraft maximum mass: ' + str(maxMassKg) + ' kilograms' )
    
        deltaMass = maxMassKg - minMassKg
        massKg = 39000.0
        while (massKg < maxMassKg):
            
            massKg += 1000.0
            print ( '==================== set aircraft reference mass ==================== ' )
            aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                    aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                    badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                    atmosphere = atmosphere,
                                    earth = earth)
            
            aircraft.setTargetCruiseFlightLevel(310, departureAirport.getFieldElevationAboveSeaLevelMeters())
            
            print ( '==================== aircraft reference mass ==================== ' )
            print ( 'aircraft reference mass= ' + str(massKg) + ' Kilograms' )
            
            aircraft.setAircraftMassKilograms(massKg)
            print ( '==================== begin of ground run ==================== ' )
            groundRunLeg = GroundRunLeg(runway = departureRunway, 
                                         aircraft = aircraft,
                                         airport = departureAirport)
            
            groundRunLeg.buildDepartureGroundRun(deltaTimeSeconds = 0.1,
                                                 elapsedTimeSeconds = 0.0, 
                                                 distanceStillToFlyMeters = 500000.0,
                                                 distanceToLastFixMeters  = 500000.0)
            
            groundRunLeg.computeLengthMeters()
            #groundRunLeg.createXlsxOutputFile()
            
            print ( '==================== end of ground run ==================== ' )
            initialWayPoint = groundRunLeg.getLastVertex().getWeight()
                
            print ( '==================== dump aircraft speed profile ==================== ' )
            aircraft.createStateVectorOutputFile(aircraftICAOcode+"-Mass-" + str(massKg))
            print ( '=========== main end ==================' )
    
    

        

if __name__ == '__main__':
    unittest.main()
    