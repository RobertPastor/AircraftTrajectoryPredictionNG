'''
Created on 1 janv. 2021

@author: robert
'''
import unittest
from Home.Environment.WayPointsDatabaseFile import WayPointsDatabase

class Test_Main(unittest.TestCase):

    def test_main(self):
    
        print ( '==================== Way-Points ====================' )
        wayPointsDb = WayPointsDatabase()
        self.assertTrue( wayPointsDb.read() , 'way points DB correctly read')
            
        TOU = wayPointsDb.getWayPoint('tou')
        print ( TOU )
        
        TouLatDegrees = TOU.getLatitudeDegrees()
        print ( 'TOU latitude= {0} degrees'.format(TouLatDegrees) )
        print ( '==================== Way-Points ====================' )
        for wayPoint in wayPointsDb.getWayPoints():
            pass
            #print ( wayPoint )
        print ( '==================== Way-Points ====================' )
        NOT_EXISTING = wayPointsDb.getWayPoint('doesnotexist')
        print ( NOT_EXISTING )
        
        print ( 'number of wayPoints= {0}'.format(wayPointsDb.getNumberOfWayPoints()) )
        
        ret = wayPointsDb.insertWayPoint('VALEK', "N31°40'58.50" + '"', "N31°40'58.50" + '"')
        if wayPointsDb.hasWayPoint('VALEK'):
            self.assertFalse(ret, 'insertion not done')
        else:
            self.assertTrue(ret, 'insertion correct')
    
        print ( 'number of wayPoints= {0}'.format(wayPointsDb.getNumberOfWayPoints()) )
    
    def test_duplicates(self):
        print ("---------- test duplicates -----------")
        
        wayPointsDb = WayPointsDatabase()
        self.assertTrue( wayPointsDb.read() , 'way points DB correctly read')

        wayPointsSet = set()
        for wayPoint in wayPointsDb.getWayPoints():
            if not (wayPoint.getName() in wayPointsSet ):
                wayPointsSet.add( wayPoint.getName() )
            else:
                print ( "{0} - {1}".format(wayPoint.getName(), (wayPoint.getName() in wayPointsSet) ) )
                print( "--------{0}".format( wayPoint.getName() ) )
        
        print ( 'number of wayPoints= {0}'.format(wayPointsDb.getNumberOfWayPoints()) )
        print ( 'number of wayPoints= {0}'.format( len (wayPointsSet) ) )


        
    
if __name__ == '__main__':
    unittest.main()