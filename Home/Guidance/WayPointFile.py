'''
Created on 13 juil. 2014

@author: PASTOR Robert

        Written By:
                Robert PASTOR 
                @Email: < robert [--DOT--] pastor0691 (--AT--) orange [--DOT--] fr >

        @http://trajectoire-predict.monsite-orange.fr/ 
        @copyright: Copyright 2015 Robert PASTOR 

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 3 of the License, or
        (at your option) any later version.
 
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
 
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
        
'''

from Home.Guidance.Haversine import points2distanceMeters, points2bearingDegrees, LatitudeLongitudeAtDistanceBearing
from Home.Environment.RunWaysDatabaseFile import RunWayDataBase
from Home.Guidance.GeographicalPointFile import GeographicalPoint

import time
import math
import unittest


def to_positive_angle(angleDegrees):
    angleDegrees = math.fmod(angleDegrees, 360);
    if (angleDegrees < 0): 
        angleDegrees += 360;
    return angleDegrees;



class WayPoint(GeographicalPoint):
    className = ''
    Name = ''
    
    isTopOfDescent = False
    isOverFlown = False
    isFlyBy = True
    elapsedTimeSeconds = 0.0
    
    def __init__(self, Name='', 
                 LatitudeDegrees = 0.0, 
                 LongitudeDegrees = 0.0,
                 AltitudeMeanSeaLevelMeters = 0.0):
        
        self.className = self.__class__.__name__
        self.Name = Name
        GeographicalPoint.__init__(self, LatitudeDegrees, LongitudeDegrees, AltitudeMeanSeaLevelMeters)
        
        self.isTopOfDescent = False
        self.isOverFlown = False
        self.isFlyBy = True
        
    def __str__(self):
        return  "{0} = {1} - latitude= {2:.2f} degrees - longitude= {3:.2f} degrees".format(self.className, self.Name, self.LatitudeDegrees, self.LongitudeDegrees)
    
    def setElapsedTimeSeconds(self, elapsedTimeSeconds):
        self.elapsedTimeSeconds = elapsedTimeSeconds
        
    def getElapsedTimeSeconds(self):
        return self.elapsedTimeSeconds
    
    
    def getName(self):
        return self.Name
    
    def setName(self, Name):
        self.Name = Name
    

    
    def getDistanceMetersTo(self, nextWayPoint):
        if isinstance(nextWayPoint, WayPoint)==True:
            return points2distanceMeters([self.LatitudeDegrees,self.LongitudeDegrees],
                                         [nextWayPoint.LatitudeDegrees, nextWayPoint.LongitudeDegrees])
        return 0.0
    
    def getBearingDegreesTo(self, nextWayPoint):
        if isinstance(nextWayPoint, WayPoint)==True:
            return to_positive_angle(points2bearingDegrees([self.LatitudeDegrees,self.LongitudeDegrees],
                                         [nextWayPoint.LatitudeDegrees, nextWayPoint.LongitudeDegrees]))
        return 0.0
    
    def getWayPointAtDistanceBearing(self, Name='', DistanceMeters=0.0, BearingDegrees=0.0):
        '''
        returns the latitude and longitude of a point along a great circle
        located along a radial at a distance from "self"
        '''
        assert (not(DistanceMeters is None) and isinstance(DistanceMeters, float))
        assert (not(BearingDegrees is None) and isinstance(BearingDegrees, float))
        
        latitudeDegrees , longitudeDegrees = LatitudeLongitudeAtDistanceBearing([self.LatitudeDegrees,self.LongitudeDegrees], DistanceMeters, BearingDegrees)
#         if len(Name)==0:
#             Name = "Way-Point-At-Distance-Bearing-{0}".format(self.Name)
        return WayPoint(Name , latitudeDegrees, longitudeDegrees )
        
    def getWayPointAtDistanceHeading(self, Name='', DistanceMeters=0.0, HeadingDegrees=0.0):
        '''
        returns the lat long of a point along a great circle
        located along a radial at a distance from "self"
        '''
        assert (not(DistanceMeters is None) and isinstance(DistanceMeters, float))
        assert (not(HeadingDegrees is None) and isinstance(HeadingDegrees, float))

        ''' convert heading into bearing '''
        BearingDegrees = math.fmod ( HeadingDegrees + 180.0 , 360.0 ) - 180.0

        latitudeDegrees , longitudeDegrees = LatitudeLongitudeAtDistanceBearing([self.LatitudeDegrees,self.LongitudeDegrees], DistanceMeters, BearingDegrees)
        if len(Name)==0:
            Name = "Way-Point-At-Distance-Heading-{0}".format(self.Name)
        
        return WayPoint(Name, latitudeDegrees, longitudeDegrees)    
    
    def dump(self):
        print ( "WayPoint Name= ", self.Name, " Lat-deg= ",self.LatitudeDegrees, " Long-deg= ",self.LongitudeDegrees, " flight-level= ", self.AltitudeMeanSeaLevelMeters, " meters" )
        if isinstance(self, Airport):
            print ( "way point is an airport" )
        if self.isTopOfDescent==True:
            print ( "way Point is Top Of Descent !!! " )


class Airport(WayPoint):
    
    fieldElevationAboveSeaLevelMeters = 0.0
    isDeparture = False
    isArrival = False
    ICAOcode = ''
    Country = ''
    
    def __init__(self, Name="Orly-Paris-Sud", 
                 LatitudeDegrees = 48.726254 , 
                 LongitudeDegrees = 2.365247 ,
                 fieldElevationAboveSeaLevelMeters = 300, 
                 isDeparture = False, 
                 isArrival = False,
                 ICAOcode = '',
                 Country = ''):
        
        WayPoint.__init__(self, Name, LatitudeDegrees, LongitudeDegrees, fieldElevationAboveSeaLevelMeters)
        self.fieldElevationAboveSeaLevelMeters = fieldElevationAboveSeaLevelMeters
        
        assert isinstance(isDeparture, bool) and isinstance(isArrival, bool)
        self.isDeparture = isDeparture
        self.isArrival = isArrival
        
        assert isinstance(ICAOcode, (str)) and len(ICAOcode)>0
        self.ICAOcode = ICAOcode
    
        assert isinstance(Country, (str)) and len(Country)>0
        self.Country = Country
        
    def getICAOcode(self):
        return self.ICAOcode
    
    def __str__(self):
        strMsg = self.className + ': Airport: ' + self.ICAOcode + ' - '
        strMsg += self.Country + ' - ' 
        strMsg += self.Name + ' - lat= {0:.2f} degrees - long= {1:.2f} degrees'.format(self.LatitudeDegrees, self.LongitudeDegrees) 
        strMsg += ' - field elevation= {0:.2f} meters'.format(self.fieldElevationAboveSeaLevelMeters)
        return strMsg
    
    def isArrival(self):
        return self.isArrival
    
    def getFieldElevationAboveSeaLevelMeters(self):
        return self.fieldElevationAboveSeaLevelMeters
    
    
    def hasRunWays(self, runwaysDatabase):
        ''' return true if this airport has at least one run-way in the database '''
        assert isinstance(runwaysDatabase, RunWayDataBase) and not(runwaysDatabase is None)
        return runwaysDatabase.hasRunWays(self.ICAOcode)
    
    def getRunWaysAsDict(self, runwaysDatabase):
        assert isinstance(runwaysDatabase, RunWayDataBase) and not(runwaysDatabase is None)
        return runwaysDatabase.getRunWaysAsDict(self.ICAOcode)
    
    def getRunWays(self, runwaysDatabase):
        assert isinstance(runwaysDatabase, RunWayDataBase) and not(runwaysDatabase is None)
        return runwaysDatabase.getRunWays(self.ICAOcode)
    
    def dump(self):
        WayPoint.dump(self)
        print ( "airport field Elevation above Sea Level Meters=",self.fieldElevationAboveSeaLevelMeters, " meters" )
        print ( 'airport ICAO code= ' + self.ICAOcode )



class Test_WayPoint(unittest.TestCase):

    def test_WayPoint(self):
    
        print ( "=========== WayPoint start  =========== " + time.strftime("%c") )
        London = WayPoint('London-Heathrow', 51.5, 0.0)
        Orly = WayPoint('Orly', 48.726254, 2.365247)
        print ( "distance from London to Orly= ", London.getDistanceMetersTo(Orly), " meters" )
        print ( "bearing from London to Orly= ", London.getBearingDegreesTo(Orly), " degrees" )
        
        #Zurich = WayPoint('Zurich-Kloten', 47.458215, 8.555424)
        Marseille = WayPoint('Marseille-Marignane', 43.438431, 5.214382 )
        Zurich = WayPoint('Zurich-Kloten', 47.458215, 8.555424)
        
        print ( "=========== WayPoint resume  =========== " + time.strftime("%c") )
    
        print ( "distance from Marseille to Zurich= ", Marseille.getDistanceMetersTo(Zurich), " meters" )
        print ( "bearing from Zurich to Marseille = ", Zurich.getBearingDegreesTo(Marseille), " degrees" )
        
        distanceMeters = 321584.699454
        bearingDegrees = Zurich.getBearingDegreesTo(Marseille)
        #bearingDegrees = Marseille.getBearingDegreesTo(Zurich)
        Zurich.dump()
        Marseille.dump()
        TopOfDescent = Zurich.getWayPointAtDistanceBearing('TopOfDescent', distanceMeters, bearingDegrees)
        TopOfDescent.dump()
        
        print ( "=========== WayPoint resume  =========== " + time.strftime("%c") )
        London.dump()
        Orly.dump()
        bearingDegrees = Orly.getBearingDegreesTo(London)
        print ( "bearing from London to Orly= ", London.getBearingDegreesTo(Orly), " degrees" )
    
        TopOfDescent = Orly.getWayPointAtDistanceBearing('TopOfDescent', distanceMeters, bearingDegrees)
        TopOfDescent.dump()
        

    def test_Airport(self):

        print ( "=========== Airport  =========== " + time.strftime("%c") )

        airportICAOcode = 'LFPG'
        CharlesDeGaulle = Airport(Name = 'CharlesDeGaulle',
                                ICAOcode = airportICAOcode,
                                Country = 'France')
        self.assertTrue( not(CharlesDeGaulle is None) )
        
        runWaysDatabase = RunWayDataBase()
        self.assertTrue( runWaysDatabase.read() , 'run ways DB read correctly')
        
        self.assertTrue( CharlesDeGaulle.hasRunWays(runWaysDatabase) )
        print ( 'airport= {0} has run-ways= {1}'.format(CharlesDeGaulle, CharlesDeGaulle.hasRunWays(runWaysDatabase)) )
        
        print ( "=========== Airport run ways ONE =========== " + time.strftime("%c") )

        for runway in CharlesDeGaulle.getRunWaysAsDict(runWaysDatabase):
            print ( runway )
            
        print ( "=========== Airport run ways TWO =========== " + time.strftime("%c") )

        for runway in CharlesDeGaulle.getRunWays(runWaysDatabase):
            print ( runway )


if __name__ == '__main__':
    unittest.main()
    