'''
Created on 21 déc. 2020

@author: rober
'''

import time
import unittest

from Home.Environment.AirportDatabaseFile import AirportsDatabase
from Home.Environment.RunWaysDatabaseFile import RunWayDataBase

from Home.OutputFiles.KmlOutput import KmlOutput
from Home.Guidance.GeographicalPointFile import GeographicalPoint

class Test_Main(unittest.TestCase):

    def test_main_one(self):
    
        print ( '====================run-ways====================' )
        t0 = time.clock()
    
        runWaysDatabase = RunWayDataBase()
        if runWaysDatabase.read():
            print ( 'runways DB correctly read' )
        
        t1 = time.clock()
        print ( 'time spent= {0:.2f} seconds'.format(t1-t0) )
        
        print ( '====================run-ways====================' )
    
        print ( runWaysDatabase.findAirportRunWays('LFPG') )
        t2 = time.clock()
        print ('time spent= {0:.2f} seconds'.format(t2-t1) )
        
    
        print ( '====================run-ways get filtered run ways====================' )
        print ( runWaysDatabase.getFilteredRunWays('LFML') )
        
        print ( '====================run-ways get filtered run ways====================' )
        print ( runWaysDatabase.getFilteredRunWays('LFBO') )
        
        print ( '====================run-ways get filtered run ways====================' )
        print ( runWaysDatabase.findAirportRunWays('LFBO') )
        
        
        print ( '====================run-ways get filtered run ways====================' )
        runway = runWaysDatabase.getFilteredRunWays('EGLL') 
        print ( runway )
        
        print ( '====================run-ways get filtered run ways====================' )
        #print 'number of runways: ' + str(len(runWaysDatabase.getRunWays('LFPG')))
        runway = runWaysDatabase.getFilteredRunWays(airportICAOcode = 'LFPG', runwayName  = '27L')
        print ( runway )
        
        print ( '====================run-ways get filtered run ways====================' )
        runway = runWaysDatabase.getFilteredRunWays(airportICAOcode = 'KJFK', runwayName  = '31L')
        print ( runway )
        
        print ( '====================run-ways get filtered run ways====================' )
    
        runway = runWaysDatabase.getFilteredRunWays(airportICAOcode = 'KLAX', runwayName  = '06L')
        print ( runway )
        
        for ICAOcode in ['LFPG', 'LFPO', 'LFBO', 'LFML', 'LFST', 'KJFK', 'SBGL', 'LFBD']:
            
            print ( '====================run-ways get filtered run ways====================' )
    
            tStart = time.clock()
            print ( runWaysDatabase.findAirportRunWays(ICAOcode) )
            tEnd = time.clock()
            print ( 'icao= {0} - duration= {1:.2f} seconds'.format(ICAOcode, (tEnd-tStart)) )
    #     print '====================run-ways===================='
    #     for runway in runWaysDatabase.getRunWays():
    #         print runway.getAirportICAOcode() + '-' + runway.getName()
            
        print ( '====================run-ways====================' )
    #     for runway in runWaysDatabase.getRunWays():
    #         print runway
    
        print ( '====================run-ways get filtered run ways====================' )
    
        print ( runWaysDatabase.findAirportRunWays('LPPT') )
    
    
    def test_main_two(self):
        
        print ( '====================run-ways test two ====================' )

        runWaysDatabase = RunWayDataBase()
        self.assertTrue( runWaysDatabase.read() )
            
        airportICAOcode = 'LPPT'
        self.assertTrue ( runWaysDatabase.hasRunWays(airportICAOcode) )
        
    def test_main_three(self):
        
        print ( '====================run-ways test three ====================' )

        runWaysDatabase = RunWayDataBase()
        self.assertTrue( runWaysDatabase.read() )
        
        airportICAOcode = 'LFPG'
        for runway in runWaysDatabase.getRunWaysAsDict(airportICAOcode) :
            print ( runway )

    def test_main_four(self):

        print ( '==================== run-ways test four ====================' )
    
        runWaysDatabase = RunWayDataBase()
        self.assertTrue( runWaysDatabase.read() )
        
        airportICAOcode = 'LFPG'
        for runway in runWaysDatabase.getRunWays(airportICAOcode) :
            print ( runway )
            
    def test_main_five(self):
        
        print ( '==================== run-ways test five ====================' )

        airportsDb = AirportsDatabase()
        self.assertTrue (airportsDb.read())
        
        CharlesDeGaulleRoissy = airportsDb.getAirportFromICAOCode('LFPG')
        print ( CharlesDeGaulleRoissy )
        
        runWaysDatabase = RunWayDataBase()
        self.assertTrue( runWaysDatabase.read() )
        
        airportICAOcode = 'LFPG'
        runwayName = "08L"
        runway = runWaysDatabase.getFilteredRunWays(airportICAOcode = airportICAOcode, runwayName  = runwayName)
        print ( runway )
        
        fileName = airportICAOcode + "-" + runwayName
        kmlOutputFile = KmlOutput(fileName=fileName)
        
        kmlOutputFile.write(name = fileName, 
            LongitudeDegrees = runway.getLongitudeDegrees(),
            LatitudeDegrees = runway.getLatitudeDegrees(),
            AltitudeAboveSeaLevelMeters = CharlesDeGaulleRoissy.getAltitudeMeanSeaLevelMeters())


        latitudeDegrees , longitudeDegrees = runway.getGeoPointAtDistanceHeading(runway.getLengthMeters(), runway.getTrueHeadingDegrees())
        
        name = airportICAOcode + "-" + runwayName + "-" + "Runway-End"
        kmlOutputFile.write(name = name, 
            LongitudeDegrees = longitudeDegrees,
            LatitudeDegrees = latitudeDegrees,
            AltitudeAboveSeaLevelMeters = CharlesDeGaulleRoissy.getAltitudeMeanSeaLevelMeters())
        
        ''' GreatCircleRoute: final way-point= turn-pt-189-229.70-degrees - latitude= 48.93 degrees - longitude= 2.75 degrees - altitudeMSL= 500.49 meters '''
        routeLatitudeDegrees = 48.93
        routeLongitudeDegrees = 2.75
        routeGeographicalPoint = GeographicalPoint(routeLatitudeDegrees, routeLongitudeDegrees, CharlesDeGaulleRoissy.getAltitudeMeanSeaLevelMeters())
        
        kmlOutputFile.write(name = "Route-Point", 
            LongitudeDegrees = routeLongitudeDegrees,
            LatitudeDegrees = routeLatitudeDegrees,
            AltitudeAboveSeaLevelMeters = CharlesDeGaulleRoissy.getAltitudeMeanSeaLevelMeters())
        
        shortestDistanceMeters = runway.computeShortestDistanceToRunway(routeGeographicalPoint)
        print ( "Shortest distance = {0} meters".format( shortestDistanceMeters ) )
        
        kmlOutputFile.close()

        
    
if __name__ == '__main__':
    unittest.main()