'''
Created on 1 sept. 2021

@author: robert
'''
import time
import unittest

from Home.AirlineRoutes.AirlineRoutesAirportsReader import AirlineRoutesAirportsDataBase
from Home.Environment.AirportDatabaseFile import AirportsDatabase

from Home.Guidance.WayPointFile import Airport


class TestMethods(unittest.TestCase):
#============================================
    def test_one(self):
    
        t0 = time.clock()
        print ( '================ test one =================' )
        
        routesAirports = AirlineRoutesAirportsDataBase()
        ret = routesAirports.read()
        self.assertTrue (ret)
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
        
        if ret:
            print ("--> airline routes read correctly ")
            routesAirports.dump()
            
            airportsDb = AirportsDatabase()
            self.assertTrue (airportsDb.read())
            
            country = 'United States'
            for airport in airportsDb.getAirportsFromCountry( Country = country):
                airportName = str(airport.getName())
                self.assertTrue ( isinstance(airport, Airport)  )
                print ( airport.getICAOcode() )
            
        
        
if __name__ == '__main__':
    unittest.main()