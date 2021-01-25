'''
Created on 21 déc. 2020

@author: robert
'''

import math

from Home.Guidance.Haversine import  LatitudeLongitudeAtDistanceBearing

from Home.Environment.Earth import EarthRadiusMeters
from Home.Guidance.Haversine import points2distanceMeters

class GeographicalPoint(object):
    className = ""
    LatitudeDegrees = 0.0
    LongitudeDegrees = 0.0
    AltitudeMeanSeaLevelMeters = 0.0
    
    def __init__(self, LatitudeDegrees = 0.0, 
                 LongitudeDegrees = 0.0,
                 AltitudeMeanSeaLevelMeters = 0.0):
        self.className = self.__class__.__name__
        
        if isinstance(LatitudeDegrees, str):
            self.LatitudeDegrees = float(LatitudeDegrees)
        else:
            self.LatitudeDegrees = LatitudeDegrees
        if isinstance(LongitudeDegrees, str):
            self.LongitudeDegrees = float(LongitudeDegrees)
        else:
            self.LongitudeDegrees = LongitudeDegrees
            
        assert self.LatitudeDegrees >= -90.0 and self.LatitudeDegrees <= 90.0
        assert self.LongitudeDegrees >= -180.0 and self.LongitudeDegrees <= 180.0
        
        self.AltitudeMeanSeaLevelMeters = AltitudeMeanSeaLevelMeters
        
    def convert2Cartesian(self):
        pass
        x = ( EarthRadiusMeters+self.AltitudeMeanSeaLevelMeters ) * math.cos(math.radians(self.LatitudeDegrees)) * math.cos(math.radians(self.LongitudeDegrees))
        y = ( EarthRadiusMeters+self.AltitudeMeanSeaLevelMeters ) * math.cos(math.radians(self.LatitudeDegrees)) * math.sin(math.radians(self.LongitudeDegrees))
        z = ( EarthRadiusMeters+self.AltitudeMeanSeaLevelMeters ) * math.sin(math.radians(self.LatitudeDegrees))
        return x , y , z

    def projectionMillerCylindrical(self):
        ''' x = longitude in degrees '''
        x = math.radians(self.LongitudeDegrees)
        y = math.tan( ( math.pi/4.0) +  (2.0/5.0) * math.radians(self.LatitudeDegrees) )
        y = ( (5.0/4.0)* math.log( y ))
        return x , y
        
    def new_y_coord(self):
        """Converts a lat, longitude location to a new transformed longitude
        """
        lat_in_rads = math.radians( self.LatitudeDegrees )
        long_in_rads = math.radians ( self.LongitudeDegrees )
        new_y_rad = 0.5 * math.log( (1 + ( math.sin(long_in_rads) * math.cos(lat_in_rads) ) ) / (1 - ( math.sin(long_in_rads) * math.cos(lat_in_rads) ) ) ) 
        new_y_deg = math.degrees( new_y_rad )
        ''' 360 degrees = 2 PI earthRadius at the equator '''
        new_y_meters = ( ( 2 * math.pi * EarthRadiusMeters ) / 360.0 ) * new_y_deg
        return new_y_meters
 
 
    def new_x_coord(self):
        """Converts a lat, longitude location to a new transformed latitude
        """
        lat_in_rads = math.radians( self.LatitudeDegrees )
        long_in_rads = math.radians ( self.LongitudeDegrees )
        new_x_rad = - ( math.atan ( ( math.tan(lat_in_rads) ) / ( math.cos(long_in_rads) ) ) )
        new_x_deg = math.degrees( new_x_rad )
     
        """this code fixes the arctan problem of mapping only back to 
        -90 < arctan > 90. It does this by checking the position on the world map.
        """
        if self.LongitudeDegrees < -90.0 or self.LongitudeDegrees > 90.0:
            if self.LatitudeDegrees  > 0.0:
                new_x_deg -= 180.0
            elif self.LatitudeDegrees < 0.0:
                new_x_deg += 180.0
        ''' convert angles to meters - 360 degrees = 2 PI earthRadius (mostly true at the equator) '''
        new_x_meters = ( ( 2 * math.pi * EarthRadiusMeters ) / 360.0 ) * new_x_deg
        return new_x_meters
                      

    def getAltitudeMeanSeaLevelMeters(self):
        return self.AltitudeMeanSeaLevelMeters
    
    def setAltitudeMeanSeaLevelMeters(self, levelMeters):
        self.AltitudeMeanSeaLevelMeters = levelMeters
        
    def setAltitudeAboveSeaLevelMeters(self, levelMeters):
        self.AltitudeMeanSeaLevelMeters = levelMeters
        
    def getLatitudeDegrees(self):
        return self.LatitudeDegrees
    
    def getLongitudeDegrees(self):
        return self.LongitudeDegrees
        
    def getGeoPointAtDistanceHeading(self, DistanceMeters=0.0, HeadingDegrees=0.0):
        '''
        returns the lat long of a point along a great circle
        located along a radial at a distance from "self"
        '''
        assert (not(DistanceMeters is None) and isinstance(DistanceMeters, float))
        assert (not(HeadingDegrees is None) and isinstance(HeadingDegrees, float))

        ''' convert heading into bearing '''
        BearingDegrees = math.fmod ( HeadingDegrees + 180.0 , 360.0 ) - 180.0

        latitudeDegrees , longitudeDegrees = LatitudeLongitudeAtDistanceBearing([self.LatitudeDegrees,self.LongitudeDegrees], DistanceMeters, BearingDegrees)
        
        return  latitudeDegrees, longitudeDegrees   


    def computeDistanceMetersTo(self, nextGeoPoint):
        assert ( not(nextGeoPoint is None) and isinstance(nextGeoPoint, GeographicalPoint))
        return points2distanceMeters([self.LatitudeDegrees,self.LongitudeDegrees], [nextGeoPoint.LatitudeDegrees, nextGeoPoint.LongitudeDegrees])
        