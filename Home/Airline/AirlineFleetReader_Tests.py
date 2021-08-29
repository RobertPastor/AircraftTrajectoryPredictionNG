'''
Created on 29 août 2021

@author: robert
'''

import time
import unittest
from Home.Airline.AirlineFleetReader import AirlineFleetDataBase
from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

class TestMethods(unittest.TestCase):
#============================================
    def test_one(self):
    
        t0 = time.clock()
        print ( '================ test one =================' )
        airlineFleet = AirlineFleetDataBase()
        print ( 'file= {0} - exists= {1}'.format(airlineFleet.FilePath , airlineFleet.exists()) )
        
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
        print ( '=================================' )
        readReturn = airlineFleet.read()
        if readReturn:
            print ( 'Airline fleet read correctly = {0}'.format( readReturn ) )
            print ( '=================================' )
            airlineFleet.dump()
        
        
    def test_two(self):
        
        t0 = time.clock()
        print ( '=============== test two ==================' )
        bdAc = BadaAircraftDatabase()
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        ret = bdAc.read()
        #if ret:
            #bdAc.dump()
            #for acIcaoCode in bdAc.getAircraftICAOcodes():
            #    print ( acIcaoCode )
            #    print ( 'aircraft ICAO code = {0} - aircraft full name = {1}'.format( acIcaoCode , bdAc.getAircraftFullName( acIcaoCode ) ) )
        
        
    def test_three(self):
        
        print ( '=============== test three ==================' )

        airlineFleet = AirlineFleetDataBase()
        retOne = airlineFleet.read()
        
        acBd = BadaAircraftDatabase()
        retTwo = acBd.read()
        
        atmosphere = Atmosphere()
        earth = Earth()
        
        allResults = []
        
        if retOne and retTwo:
            for acType in airlineFleet.getAircraftFullNames():
                print ( str(acType).upper() )
                print (" ---------------- " , str(acType).upper() , " -----------------")

                for aircraftICAOcode in acBd.getAircraftICAOcodes():
                    if ( str(acType).upper() == acBd.getAircraftFullName( aircraftICAOcode )):
                        print ( 'aircraft full name = {0} -- aircraft ICAO code = {1}'.format( acType , aircraftICAOcode  ) )
                        
                        if ( acBd.aircraftExists(aircraftICAOcode) 
                             and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                        
                            ac = BadaAircraft(ICAOcode = aircraftICAOcode , 
                                              aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode), 
                                              badaPerformanceFilePath =  acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                      atmosphere = atmosphere, earth = earth)
                            print ( ac.getLandingLengthMeters() )
                            print ( ac.getTakeOffLengthMeters() )
                            results = {}
                            results["aircraft ICAO code"] = aircraftICAOcode
                            results["aircraft Full Name"] = str(acType).upper()
                            results["Landing Length"] = str(ac.getLandingLengthMeters())
                            results["TakeOff Length"] = str(ac.getTakeOffLengthMeters())
                            allResults.append(results)
                
        print (" ---------------- final results -----------------")
        for result in allResults:
            for key , value in result.items():
                print ( key , value )
        
if __name__ == '__main__':
    unittest.main()