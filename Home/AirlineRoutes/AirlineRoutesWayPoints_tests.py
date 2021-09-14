'''
Created on 4 sept. 2021

@author: robert
'''

import time
import unittest

from Home.AirlineRoutes.AirlineWayPointsDatabase import AirlineWayPointsDatabase
from Home.AirlineRoutes.AirlineRoutes import AirlineRoutes
from Home.Guidance.RouteFile import Route


class TestMethods(unittest.TestCase):
#============================================
    def test_one(self):
        pass
    
        t0 = time.clock()
        print ( '================ test one =================' )
        wayPointsDB = AirlineWayPointsDatabase()
        
        airlineRoutes = AirlineRoutes()
        airlineRoutes.createRoutesFiles()
        
        for wayPoint in airlineRoutes.getExtendedWayPointsList():
            
            print ( wayPoint )
            wayPointsDB.insertWayPoint(wayPointName=wayPoint["Name"], Latitude=wayPoint["latitude"], Longitude=wayPoint["longitude"])
        
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
        
        wayPointsDB.dropDuplicates()
        
        t2 = time.clock()
        print ( 'duration= {0} seconds'.format(t2-t1) )
        
    
    
if __name__ == '__main__':
    unittest.main()