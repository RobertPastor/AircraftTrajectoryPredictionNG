'''
Created on 3 janv. 2021

@author: robert
'''

import os
import xlrd
import unittest

from Home.Environment.Constants import Meter2NauticalMiles
from Home.Environment.AirportDatabaseFile import AirportsDatabase
from Home.Guidance.WayPointFile import WayPoint
from Home.OutputFiles.KmlOutput import KmlOutput
from Home.Environment.Earth import EarthRadiusMeters

class WorldCitiesDatabase(object):
    
    rows = []
    headers = []
    geoPoints = []

    def __init__(self):
        self.className = self.__class__.__name__
        
        self.FileName = 'worldcities.xls'
        self.FilesFolder = os.path.dirname(__file__)
        
        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder + os.path.sep + self.FileName)
        print ( self.className + ': file path= {0}'.format(self.FilePath) )

    def read(self):
        
        workbook = xlrd.open_workbook(self.FilePath)
        worksheet = workbook.sheet_by_index(0)
        
        self.rows = []
        for i, row in enumerate(range(worksheet.nrows)):
            
            r = []
            for j, col in enumerate(range(worksheet.ncols)):
                r.append(worksheet.cell_value(i, j))
            if (i == 0):
                self.headers = r
            else:
                self.rows.append(r)
                self.geoPoints.append(WayPoint(r[1],r[2],r[3]))
        
        print ( "{0} - read {1} rows".format( self.className, len(self.rows) ) )
        print ( self.headers )  # Print column headings
        print ( self.rows[0] ) # Print first data row sample
        return ( len(self.rows) > 0)
        
    def getCities(self):
        for geoPoint in self.geoPoints:
            yield geoPoint
                
        
class Test_Main(unittest.TestCase):

    def test_main(self):
        
        worldCitiesDatabase = WorldCitiesDatabase()
        self.assertTrue( worldCitiesDatabase.read() )
        
        airportsDb = AirportsDatabase()
        self.assertTrue (airportsDb.read())
        
        CharlesDeGaulleRoissy = airportsDb.getAirportFromICAOCode('LFPG')
        print ( CharlesDeGaulleRoissy )
        
        BerlinTegel = airportsDb.getAirportFromICAOCode('EDDT')
        print ( BerlinTegel )
        
        distanceMeters = CharlesDeGaulleRoissy.getDistanceMetersTo(BerlinTegel)
        print ( "distance from CDG to Berlin Tegel = {0:.2f} meters - {1:.2f} nautics".format( distanceMeters , distanceMeters*Meter2NauticalMiles) )
        
        NumberOfPoints = int( (distanceMeters * Meter2NauticalMiles) / 10.)
        print ( "Number of points = {0}".format( NumberOfPoints ) )
        
        kmlOutputFile = KmlOutput(fileName="CDG-Berlin-Tegel")
        kmlOutputFile.write(name = CharlesDeGaulleRoissy.getName(), 
                                    LongitudeDegrees = CharlesDeGaulleRoissy.getLongitudeDegrees(),
                                    LatitudeDegrees = CharlesDeGaulleRoissy.getLatitudeDegrees(),
                                    AltitudeAboveSeaLevelMeters = CharlesDeGaulleRoissy.getAltitudeMeanSeaLevelMeters())
        
        kmlOutputFile.write(name = BerlinTegel.getName(), 
                                    LongitudeDegrees = BerlinTegel.getLongitudeDegrees(),
                                    LatitudeDegrees = BerlinTegel.getLatitudeDegrees(),
                                    AltitudeAboveSeaLevelMeters = BerlinTegel.getAltitudeMeanSeaLevelMeters())

        nearestCities = []
        for wayPoint in worldCitiesDatabase.getCities():
            distanceMetersToDeparture = CharlesDeGaulleRoissy.getDistanceMetersTo(wayPoint)
            distanceMetersToArrival = BerlinTegel.getDistanceMetersTo(wayPoint)
            if ( distanceMetersToDeparture + distanceMetersToArrival ) < ( distanceMeters + ( (10.0 * distanceMeters) / 100. )):
                nearestCities.append({ "wayPoint" : wayPoint , "distanceMeters": distanceMetersToDeparture + distanceMetersToArrival })
        
        ''' re ordering '''
        nearestCities.sort(key=lambda x: x["distanceMeters"], reverse=False)
        
        count = 0
        for city in nearestCities:
            count = count + 1
            if (count < NumberOfPoints ):
                kmlOutputFile.write( name = city["wayPoint"].getName(),
                                     LongitudeDegrees = city["wayPoint"].getLongitudeDegrees(),
                                    LatitudeDegrees = city["wayPoint"].getLatitudeDegrees(),
                                    AltitudeAboveSeaLevelMeters = 0.0)


        kmlOutputFile.close()
            
            

if __name__ == '__main__':
    unittest.main()
