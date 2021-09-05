'''
Created on 5 sept. 2021

@author: robert

strRoute = 'ADEP/LFBM/27-SAU-VELIN-LMG-BEBIX-GUERE-LARON-KUKOR-MOU-'
    strRoute += 'PIBAT-DJL-RESPO-DANAR-POGOL-OBORN-LUPEN-SUL-'
    strRoute += 'ESULI-TEDGO-ETAGO-IBAGA-RATIP-PIBAD-SOMKO-'
    strRoute += 'ADES/EDDP/26R'
    
'''

import time
import unittest
from Home.Guidance.RouteFile import Route

#============================================
class Tests(unittest.TestCase):

    def test_One(self):
        pass
        t0 = time.clock()
        print ( '================ test one =================' )

        route = Route( _departureAirportICAOcode="KATL", _departureRunWay="", _listOfWayPointNames= ["VUZ"] , _arrivalAirportICAOcode = "KLAX", _arrivalRunWay="")
        
        print ( route.getRouteAsString() )
    
    

if __name__ == '__main__':
    unittest.main()