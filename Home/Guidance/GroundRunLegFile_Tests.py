import time
import unittest
import logging

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Environment.RunWaysDatabaseFile import  RunWayDataBase
from Home.Environment.AirportDatabaseFile import AirportsDatabase

from Home.Guidance.GroundRunLegFile import GroundRunLeg

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

#============================================
class Test_Class(unittest.TestCase):

    def test_One(self):
    
        logging.basicConfig(level=logging.INFO)
        
        atmosphere = Atmosphere()
        earth = Earth()
        
        logging.info ( '==================== Ground run ==================== '+ time.strftime("%c") )
        acBd = BadaAircraftDatabase()
        aircraftICAOcode = 'A320'
        if acBd.read():
            logging.info  ("aircraft database read correctly")
            print ( acBd.aircraftExists(aircraftICAOcode)  )
            print ( acBd.getAircraftPerformanceFile(aircraftICAOcode) )
            print ( acBd.aircraftPerformanceFileExists(aircraftICAOcode) )
            if ( acBd.aircraftExists(aircraftICAOcode) 
                 and acBd.aircraftPerformanceFileExists(aircraftICAOcode) ):
                
                logging.info ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
                aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                        aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                        badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                        atmosphere = atmosphere,
                                        earth = earth)
                aircraft.dump()
            else:
                raise ValueError("aircraft not found")
        
        logging.info ( '==================== Ground run ==================== '+ time.strftime("%c") )
        airportsDB = AirportsDatabase()
        assert airportsDB.read()
        
        CharlesDeGaulle = airportsDB.getAirportFromICAOCode('LFPG')
        logging.info ( CharlesDeGaulle )
        
        logging.info ( '==================== Ground run - read runway database ==================== '+ time.strftime("%c") )
        runWaysDatabase = RunWayDataBase()
        assert runWaysDatabase.read() == True
        
        logging.info ( '==================== Ground run ==================== '+ time.strftime("%c") )
        runway = runWaysDatabase.getFilteredRunWays('LFPG', "06L")
        logging.info ( runway )
        
        logging.info ( '==================== departure Ground run ==================== '+ time.strftime("%c") )
        groundRun = GroundRunLeg(runway=runway, 
                                 aircraft=aircraft,
                                 airport=CharlesDeGaulle)
        
        groundRun.buildDepartureGroundRun(deltaTimeSeconds = 0.1,
                                    elapsedTimeSeconds = 0.0,
                                    distanceStillToFlyMeters = 100000.0,
                                    distanceToLastFixMeters = 0.0)
        
        groundRun.createKmlOutputFile(False, aircraftICAOcode, CharlesDeGaulle.getName() , 'LFML')
        groundRun.createXlsxOutputFile(False, aircraftICAOcode, CharlesDeGaulle.getName() , 'LFML')
            
        logging.info ( '==================== Get Arrival Airport ==================== '+ time.strftime("%c") )
        arrivalAirportIcaoCode = 'LFML'
        arrivalAirport = airportsDB.getAirportFromICAOCode(arrivalAirportIcaoCode)
        logging.info ( arrivalAirport )
        
        logging.info ( '====================  arrival run-way ==================== '+ time.strftime("%c") )
        arrivalRunway = runWaysDatabase.getFilteredRunWays(arrivalAirportIcaoCode,
                                                            aircraft.WakeTurbulenceCategory)
        logging.info ( arrivalRunway )
        logging.info ( '==================== arrival Ground run ==================== '+ time.strftime("%c") )
    #     aircraft.setLandingConfiguration(elapsedTimeSeconds = 0.0)
    #     
    #     aircraft.initStateVector(elapsedTimeSeconds = 0.0,
    #                           trueAirSpeedMetersSecond = 101.0 * Knots2MetersPerSecond, 
    #                           airportFieldElevationAboveSeaLevelMeters = arrivalAirport.getFieldElevationAboveSeaLevelMeters())
    # 
    #     groundRun = GroundRunLeg(runway = runway, 
    #                              aircraft = aircraft,
    #                              airport = CharlesDeGaulle)
    #     groundRun.buildArrivalGroundRun(deltaTimeSeconds = 0.1,
    #                               elapsedTimeSeconds = 0.0,
    #                               initialWayPoint)
    #     groundRun.createXlsxOutputFile()
    #     groundRun.createKmlOutputFile()


if __name__ == '__main__':
    unittest.main()
