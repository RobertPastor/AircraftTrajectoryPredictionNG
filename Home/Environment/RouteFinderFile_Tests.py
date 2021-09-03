'''
Created on 2 sept. 2021

@author: robert
'''

import time
import unittest

from Home.Environment.RouteFinderFile import RouteFinder
from Home.Environment.WayPointsDatabaseFile import WayPointsDatabase

class Test_Main(unittest.TestCase):

    def test_one(self):
        
        print ( "=========== Route Finder start  =========== " + time.strftime("%c") )
        wayPointsDb = WayPointsDatabase()
        assert ( wayPointsDb.read() )
    
        print ( "=========== Route Finder start  =========== " + time.strftime("%c") )
    
        routeFinder = RouteFinder()
        if routeFinder.isConnected():
            print ( 'route finder is connected' )
            
            print ( "=========== Route Finder start  =========== " + time.strftime("%c") )
            Adep = 'KATL'
            Ades = 'PHNL'
            RFL = 'FL360'
            
            if routeFinder.findRoute(Adep, Ades, RFL):
                routeList = routeFinder.getRouteAsList()
                print ( routeList )
                 
                routeFinder.insertWayPointsInDatabase(wayPointsDb)
    
        
        print ( "=========== Route Finder start  =========== " + time.strftime("%c") )
        
        
    def test_two(self):
        print ( "=========== Route Finder start  =========== " + time.strftime("%c") )
    
    
#============================================
if __name__ == '__main__':
    unittest.main()
        
    
    