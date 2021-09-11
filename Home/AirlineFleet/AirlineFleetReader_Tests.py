'''
Created on 29 août 2021

@author: robert
'''

import time
import unittest

from Home.AirlineFleet.AirlineFleetReader import AirlineAircraft
from Home.AirlineFleet.AirlineFleetReader import AirlineFleetDataBase
from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth


class TestMethods(unittest.TestCase):
#============================================
    '''def test_one(self):
    
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
    '''    
        
    ''' def test_two(self):
        
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
    '''   
        
    def test_three(self):
        
        print ( '=============== test three ==================' )

        airlineFleet = AirlineFleetDataBase()
        retOne = airlineFleet.read()
        
        if retOne:
            retTwo = airlineFleet.extendDatabase()
            if retTwo:
                
                airlineFleet.createExtendedDatabaseXls()
                
                print (" ---------------- final results -----------------")
                print ( "aircraft Full Name;aircraft ICAO code;Landing Length (meters);TakeOff Length @MTOW (meters);nb Aircrafts In Service;Total Passengers;Costs Flying Hours Dollars")
                for ac in airlineFleet.getAirlineAircrafts():
                    if (len(ac.getAircraftICAOcode())>0):
                        print ( "{0} ; {1} ; {2} ; {3} ; {4} ; {5} ; {6}".format( ac.getAircraftFullName() , 
                                                                              ac.getAircraftICAOcode() ,
                                                                              ac.getLandingLengthMeters() ,
                                                                              ac.getTakeOffMTOWLengthMeters() ,
                                                                              ac.getNumberOfAircraftInstances() ,
                                                                              ac.getMaximumNumberOfPassengers() ,
                                                                              ac.getCostsFlyingPerHoursDollars() ) )
                    
                


if __name__ == '__main__':
    unittest.main()