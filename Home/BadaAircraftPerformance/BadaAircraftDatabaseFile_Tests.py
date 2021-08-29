'''
Created on 29 août 2021

@author: robert
'''

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase

import time
import unittest


class TestMethods(unittest.TestCase):
#============================================
    def test_one(self):
    
        t0 = time.clock()
        print ( '=================================' )
        acBd = BadaAircraftDatabase()
        print ( 'file= {0} - exists= {1}'.format(acBd.getSynonymFilePath(), acBd.exists()) )
        
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
        
        print ( '=================================' )
        readReturn = acBd.read()
        print ( 'file= {0} - read= {1}'.format(acBd.getSynonymFilePath(), readReturn ) )
        
        t2 = time.clock() 
        print ( 'duration= {0} seconds'.format(t2-t1) )
        print ( '=================================' )
    
        print ( acBd.getAircraftFullName('A320') )
        
        print ( '=================================' )
        print ( 'aircraft= {0} - exists= {1}'.format('A320', acBd.aircraftPerformanceFileExists('A320')) )
        
        print ( '=================================' )
        print ( acBd.getAircraftPerformanceFile('A320') )
        
        for acICAOcode in ['A10', 'b737', 'A320', 'B747', 'F50', 'B741', 'B742', 'B743', 'A319', 'CL73']:
            print ( "=================================" )
            print ( "aircraft= ", acICAOcode )
            print ( "=================================" )
            print ( 'aircraft= {0} exists= {1}'.format(acICAOcode, acBd.aircraftExists(acICAOcode)) )
            if acBd.aircraftExists(acICAOcode):
                print ( 'aircraft= {0} performance file= {1}'.format(acICAOcode, acBd.getAircraftPerformanceFile(acICAOcode)) )
                print ( 'aircraft= {0} full name= {1}'.format(acICAOcode, acBd.getAircraftFullName(acICAOcode)) )
                print  ( acBd.getAircraftPerformanceFile(acICAOcode) )
                        
                        
        assert (True)
        
    def test_two(self):
    
        t0 = time.clock()
        print ( '=================================' )
        acBd = BadaAircraftDatabase()
        print ( 'file= {0} - exists= {1}'.format(acBd.getSynonymFilePath(), acBd.exists()) )
        
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )
        
        print ( '=================================' )
        readReturn = acBd.read()
        print ( 'file= {0} - read= {1}'.format(acBd.getSynonymFilePath(), readReturn ) )
        
        t2 = time.clock() 
        print ( 'duration= {0} seconds'.format(t2-t1) )
        print ( '=================================' )

    

if __name__ == '__main__':
    unittest.main()
    