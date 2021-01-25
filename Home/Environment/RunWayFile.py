'''
Created on 21 déc. 2020

@author: robert
'''

import math
from Home.Environment.Constants import Feet2Meter
from Home.Environment.Earth import EarthRadiusMeters

from Home.Guidance.GeographicalPointFile import GeographicalPoint


class RunWay(GeographicalPoint):    
    '''
    The Charles De Gaulle airport has 2 configurations, depending on the wind directions.
    However, in both configurations Eastward and Westward of Charles de Gaulle:
    - The Run-ways 08R/26L and 09L/27R (far from the terminal) are mainly used for landings.
    - The Run-ways 08L/26R and 09R/27L (near the terminal) are mainly used for take-offs. 
    
    Id, ICAO,Number, Length Meters, Length Feet, Orientation Degrees
    The run-way true heading is defined as the angle 
      1) expressed in degrees
      2) counted from the geographic NORTH, 
      3) clock-wise 
      4) with the run-way end point as the summit of the angle

    Lat-long are the position of the end of the runway
    1) end - if takeoff runway -  is the location the aircraft starts its ground run
    2) end - if landing runway - is the location where after the touch down and deceleration, the ac reaches the taxi speed
     
    '''
    className = ''
    airportICAOcode = ''
    Name = ''
    LengthFeet = 0.0
    TrueHeadingDegrees = 0.0
    TakeOffLanding = ''

    
    def __init__(self, 
                 Name, 
                 airportICAOcode, 
                 LengthFeet, 
                 TrueHeadingDegrees, 
                 LatitudeDegrees, 
                 LongitudeDegrees):
        
        self.className = self.__class__.__name__

        assert not(Name is None) and isinstance(Name, (str)) 
        assert not(airportICAOcode is None) and isinstance(airportICAOcode, (str))
                    
        assert not (LengthFeet is None) and isinstance(LengthFeet, float) and (LengthFeet>0.0)
            
        assert not (TrueHeadingDegrees is None) and isinstance(TrueHeadingDegrees, float) 
        assert (-360.0 <= TrueHeadingDegrees) and (TrueHeadingDegrees <= 360.0)
                    
        assert not (LatitudeDegrees is None) and (isinstance(LatitudeDegrees, float)) 
        assert (-90.0 <= LatitudeDegrees) and (LatitudeDegrees <= 90.0)
            
        assert not (LongitudeDegrees is None) and (isinstance(LongitudeDegrees, float))
        assert (-180.0 <= LongitudeDegrees) and (LongitudeDegrees <= 180.0)
        
        GeographicalPoint.__init__(self, LatitudeDegrees=LatitudeDegrees, LongitudeDegrees=LongitudeDegrees, AltitudeMeanSeaLevelMeters=EarthRadiusMeters)
            
        self.airportICAOcode = airportICAOcode
        self.Name = Name
        self.LengthFeet = LengthFeet
        self.TrueHeadingDegrees = TrueHeadingDegrees
        
                                    
    def getName(self):
        return self.Name
    
    def getAirportICAOcode(self):
        return self.airportICAOcode
    
    def getLengthMeters(self):
        return self.LengthFeet * Feet2Meter
    
    def getTrueHeadingDegrees(self):
        return self.TrueHeadingDegrees
    
    def getLatitudeDegrees(self):
        return self.LatitudeDegrees
    
    def getLongitudeDegrees(self):
        return self.LongitudeDegrees
    
    def __str__(self):
        strRunWay = self.className
        strRunWay += ': runway= ' + self.Name
        strRunWay += ' airport ICAO code= '     + self.airportICAOcode 
        strRunWay += ' length= {0:.2f} feet'.format(self.LengthFeet) 
        strRunWay += ' true heading= {0:.2f} degrees'.format(self.TrueHeadingDegrees)
        strRunWay += ' latitude= {0:.2f} degrees'.format(self.LatitudeDegrees)
        strRunWay += ' longitude= {0:.2f} degrees'.format(self.LongitudeDegrees)
        return strRunWay
    
    def getEndOfRunWay(self):
        latitudeDegrees , longitudeDegrees = self.getGeoPointAtDistanceHeading(self.getLengthMeters(), self.getTrueHeadingDegrees())
        return GeographicalPoint(latitudeDegrees , longitudeDegrees, EarthRadiusMeters)
    
    def computeShortestDistanceToRunway(self, geographicalPoint):
        ''' https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line '''
        assert not(geographicalPoint is None) and isinstance(geographicalPoint, (GeographicalPoint)) 
        
        #x0, y0, z0 = geographicalPoint.convert2Cartesian()
        #x0 , y0 = geographicalPoint.projectionMillerCylindrical()
        x0 = geographicalPoint.new_x_coord()
        y0 = geographicalPoint.new_y_coord()
        
        ''' these are cartesian coordinates from runway starting point '''
        #x1, y1, z1 = self.convert2Cartesian()
        #x1, y1 = self.projectionMillerCylindrical()
        x1 = self.new_x_coord()
        y1 = self.new_y_coord()
        
        endOfRunway = self.getEndOfRunWay()
        #x2, y2, z2 = endOfRunway.convert2Cartesian()
        #x2 , y2 = endOfRunway.projectionMillerCylindrical()
        x2 = endOfRunway.new_x_coord()
        y2 = endOfRunway.new_y_coord()
        
        ''' Assuming that all three points are in the same Z plane '''
        
        ''' The numerator is twice the area of the triangle with its vertices at the three points, (x0, y0), P1 and P2 '''
        numerator = math.fabs ( ( (x2 - x1) * (y1 - y0)) - ( (x1 - x0) * (y2 - y1) ) )
        ''' The denominator of this expression is the distance between P1 and P2 '''
        denominator = math.sqrt( (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1) )
        return numerator / denominator
        
        
