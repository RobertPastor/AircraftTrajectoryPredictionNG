'''
Created on 1 sept. 2021

@author: robert
'''
import time
import unittest

from Home.AirlineRoutes.AirlineRoutesAirportsReader import AirlineRoutesAirportsDataBase
from Home.AirlineRoutes.AirlineRoutesAirportsReader import AirlineRoute
from Home.Environment.AirportDatabaseFile import AirportsDatabase

from Home.Guidance.WayPointFile import Airport
from Home.Environment.Constants import Meter2NauticalMiles

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
            print ("------- airports database read correctly --------")
            
            for departureAirportICAOcode in routesAirports.getDepartureAirportsICAOcode():       
                country = 'United States'
                for airport in airportsDb.getAirportsFromCountry( Country = country):
                    #airportName = str(airport.getName())
                    self.assertTrue ( isinstance(airport, Airport)  )
                    if ( departureAirportICAOcode == airport.getICAOcode() ):
                        print ( "--> found -> {0} --> name = {1}".format( airport.getICAOcode() , airport.getName()) )        

            for arrivalAirportICAOcode in routesAirports.getArrivalAirportsICAOcode():
                country = 'United States'
                for airport in airportsDb.getAirportsFromCountry( Country = country):
                    #airportName = str(airport.getName())
                    self.assertTrue ( isinstance(airport, Airport)  )
                    if ( arrivalAirportICAOcode == airport.getICAOcode() ):
                        print ( "--> found -> {0} --> name = {1}".format( airport.getICAOcode() , airport.getName()) )
            
            
            for route in routesAirports.getRoutes():
                print ( route )
                self.assertTrue( isinstance( route, AirlineRoute ) )
                departureAirport = airportsDb.getAirportFromICAOCode(route.getDepartureAirportICAOcode())
                print ( departureAirport )
                arrivalAirport = airportsDb.getAirportFromICAOCode(route.getArrivalAirportICAOcode())
                print ( arrivalAirport )
                
                distanceMeters = departureAirport.getDistanceMetersTo(arrivalAirport)
                print ( "distance from {0} - to {1} - dist = {2} meters".format(departureAirport.getICAOcode() , arrivalAirport.getICAOcode() , distanceMeters))
                print ( "distance from {0} - to {1} - dist = {2} nautical miles".format(departureAirport.getICAOcode() , arrivalAirport.getICAOcode() , distanceMeters*Meter2NauticalMiles))
        
        
    def test_two(self):
    
        t0 = time.clock()
        print ( '================ test one =================' )
        
        airlineRoutesAirportsDataBase = AirlineRoutesAirportsDataBase()
        ret = airlineRoutesAirportsDataBase.read()
        self.assertTrue (ret)
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
        
        if ret:
            print ("--> airline routes read correctly ")
        
        print ("------------- airline routes airports OR flight legs --------------")
        for route in airlineRoutesAirportsDataBase.getRoutes():
            print (route)


        
if __name__ == '__main__':
    unittest.main()