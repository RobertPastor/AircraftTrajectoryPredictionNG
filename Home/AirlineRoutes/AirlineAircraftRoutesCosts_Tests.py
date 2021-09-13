'''
Created on 12 sept. 2021

@author: robert

compute potential costs for each fleet aircraft for each route

'''
import time
import unittest

from Home.AirlineRoutes.AirlineAircraftRoutesCostsFile import AirlineAircraftRoutesCosts

class TestMethods(unittest.TestCase):
#============================================
    def test_one(self):
        pass
    
        t0 = time.clock()
        print ( '================ test one =================' )
        
        airlineAircraftRoutesCosts = AirlineAircraftRoutesCosts()
        retOne = airlineAircraftRoutesCosts.build()
        self.assertTrue( retOne )
        
        retTwo = airlineAircraftRoutesCosts.createCostsResultsFile()
        self.assertTrue( retTwo )
        
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
        
        

if __name__ == '__main__':
    unittest.main()       