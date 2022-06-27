# -*- coding: UTF-8 -*-
'''
Created on 13 decembre 2014

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


A great circle of a sphere, also known as an ortho-drome or Riemannian circle,
it is the intersection of the sphere and a plane which passes through the center point of the sphere. 
 
 This partial case of a circle of a sphere is opposed to a small circle, 
 the intersection of the sphere and a plane which does not pass through the center.
  Any diameter of any great circle coincides with a diameter of the sphere, 
  and therefore all great circles have the same circumference as each other, 
  and have the same center as the sphere. 
  
  A great circle is the largest circle that can be drawn on any given sphere. 
  Every circle in Euclidean 3-space is a great circle of exactly one sphere.

For any two points on the surface of a sphere there is a unique great circle through the two points. 
An exception is a pair of antipodal points, for which there are infinitely many great circles. 

The minor arc of a great circle between two points is the shortest surface-path between them. 
In this sense the minor arc is analogous to "straight lines" in spherical geometry. 

The length of the minor arc of a great circle is taken as the distance 
between two points on a surface of a sphere in Riemannian geometry. 

The great circles are the geodesics of the sphere.

'''

import math
import logging

from Home.Guidance.WayPointFile import WayPoint
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft
from Home.Guidance.GraphFile import Graph

from Home.Environment.Constants import EarthMeanRadiusMeters 
from Home.Environment.Constants import Meter2Feet 
from Home.Environment.Constants import Meter2NauticalMiles 


class GreatCircleRoute(Graph):
    
    className = ''
    initialWayPoint = None
    finalWayPoint = None
    climbRampAngleDegrees = 0.0
    
    def __init__(self, 
                 initialWayPoint,   
                 finalWayPoint, 
                 aircraft):
                
        ''' init base class '''
        Graph.__init__(self)
        self.className = self.__class__.__name__
        self.climbRampAngleDegrees = 8.0
                
        assert (isinstance(initialWayPoint, WayPoint)) and (isinstance(finalWayPoint, WayPoint))
        
        self.initialWayPoint = initialWayPoint
        self.finalWayPoint = finalWayPoint
        
        assert (isinstance(aircraft, BadaAircraft))
        self.aircraft = aircraft
        
        ''' sanity checks '''
        ptlon1 = initialWayPoint.getLongitudeDegrees()
        assert (ptlon1 >= -180.) and (ptlon1 <= 180.)
        
        ''' sanity checks '''
        ptlat1 = initialWayPoint.getLatitudeDegrees()
        assert (ptlat1 >= -90.0) and (ptlat1 <= 90.)
        
        ''' sanity checks '''
        ptlon2 = finalWayPoint.getLongitudeDegrees()
        assert  (ptlon2 >= -180.) and (ptlon2 <= 180.)
        
        ''' sanity checks '''
        ptlat2 = finalWayPoint.getLatitudeDegrees()
        assert (ptlat2 >= -90.0) and (ptlat2 <= 90.)

        self.ptlon1_radians = math.radians(ptlon1)
        self.ptlat1_radians = math.radians(ptlat1)
        self.ptlon2_radians = math.radians(ptlon2)
        self.ptlat2_radians = math.radians(ptlat2)


    def computeGreatCircle(self, 
                           deltaTimeSeconds,
                           elapsedTimeSeconds,
                           distanceStillToFlyMeters,
                           distanceToLastFixMeters):
        ''' internally modified '''
        initialDeltaTimeSeconds = deltaTimeSeconds
        '''
        build the great circle
        '''
        distance_radians = 2 * math.asin(math.sqrt(math.pow((math.sin((self.ptlat1_radians-self.ptlat2_radians)/2)),2) + math.cos(self.ptlat1_radians) * math.cos(self.ptlat2_radians)*math.pow((math.sin((self.ptlon1_radians-self.ptlon2_radians)/2)),2)))
        ''' 6371.009 represents the mean radius of the earth'''
        ''' shortest path distance'''
        distanceMeters = EarthMeanRadiusMeters * distance_radians
        #logging.info self.className + ': computeGreatCircle shortest path distance= ' + str(distanceMeters) + ' meters'

        ''' init the loop index '''
        index = 0
        elapsedTimeSeconds = elapsedTimeSeconds
        
        #logging.info self.className + ': initial True Air Speed= ' + str(trueAirSpeedMetersSecond) + ' meters/second'
        overflownDistanceMeters = 0.0
        ''' loop over the over-flown distance '''
        endOfSimulation = False
        while ( (endOfSimulation == False) and (overflownDistanceMeters <  distanceMeters)):
            
            ''' initialization of the loop '''
            if index == 0:
                logging.info ( self.className + ': initial way-point= {0}'.format(self.initialWayPoint) )
                intermediateWayPoint = self.initialWayPoint
            
            #if self.aircraft.isCruiseSpeedReached():
            #    ''' speed up the computation => step = 10 seconds '''
            #    deltaTimeSeconds = 10.0
            #else:
            #    deltaTimeSeconds = initialDeltaTimeSeconds
                
            ''' fly => increase in true air speed '''
            endOfSimulation, deltaDistanceMeters , altitudeMeanSeaLevelMeters = self.aircraft.fly(
                                                                    elapsedTimeSeconds = elapsedTimeSeconds,
                                                                    deltaTimeSeconds = deltaTimeSeconds, 
                                                                    distanceStillToFlyMeters = distanceStillToFlyMeters,
                                                                    currentPosition = intermediateWayPoint,
                                                                    distanceToLastFixMeters = distanceToLastFixMeters)
            #logging.info self.className + ': True AirSpeed= ' + str(trueAirSpeedMetersSecond) + ' meters/second'

            ''' cumulated  over-flown distance '''
            overflownDistanceMeters += deltaDistanceMeters
            distanceStillToFlyMeters -= deltaDistanceMeters
            distanceToLastFixMeters -= deltaDistanceMeters
            fprime = overflownDistanceMeters / distanceMeters
            
            #logging.info self.className + ': altitude= ' + str(altitudeMeanSeaLevelMeters) + ' meters'

            ''' fprime is expressed as a fraction along the route from point 1 to point 2 '''
            A = math.sin((1-fprime)*distance_radians) / math.sin(distance_radians)
            B = math.sin(fprime*distance_radians) / math.sin(distance_radians)
                
            x = A * math.cos(self.ptlat1_radians) * math.cos(self.ptlon1_radians) + B * math.cos(self.ptlat2_radians) * math.cos(self.ptlon2_radians)
            y = A * math.cos(self.ptlat1_radians) * math.sin(self.ptlon1_radians) +  B * math.cos(self.ptlat2_radians) * math.sin(self.ptlon2_radians)
            z = A * math.sin(self.ptlat1_radians) + B * math.sin(self.ptlat2_radians)

            newLatitudeRadians = math.atan2(z, math.sqrt(math.pow(x,2)+math.pow(y,2)))
            newLongitudeRadians = math.atan2(y,x)
                
            newlat_degrees = math.degrees(newLatitudeRadians)
            newlon_degrees = math.degrees(newLongitudeRadians)
                
            #name = 'gc-pt-{0}-{1:.2f}-Nm'.format(index, overflownDistanceMeters*Meter2NauticalMiles)
            name = ''
            ''' new way point is built with an altitude  '''
            newWayPoint = WayPoint(Name = name,
                                   LatitudeDegrees = newlat_degrees,
                                   LongitudeDegrees = newlon_degrees,
                                   AltitudeMeanSeaLevelMeters = altitudeMeanSeaLevelMeters)
            
            ''' update new point '''
            elapsedTimeSeconds += deltaTimeSeconds            
            newWayPoint.setElapsedTimeSeconds(elapsedTimeSeconds)

            ''' build the route '''
            self.addVertex(newWayPoint)
            ''' set new intermediate way-point '''
            intermediateWayPoint = newWayPoint
            ''' increment index needed when adding vertex '''
            index += 1
        
        ''' rename the final way point '''
        intermediateWayPoint.setName(self.finalWayPoint.getName())
#         minutes, seconds = divmod(elapsedTimeSeconds, 60)
#         strMsg = ': passing way-point: {0} ... altitude= {1:.2f} feet ... distance= {2:.2f} nautics ... elapsed time= {3:.2f} sec ... elapsed time= {4} min {5} sec'.format(
#                                                     self.finalWayPoint.getName(), 
#                                                     altitudeMeanSeaLevelMeters * Meter2Feet,
#                                                     self.computeLengthMeters()* Meter2NauticalMiles,
#                                                     elapsedTimeSeconds, int(minutes), int(seconds))
#         logging.info self.className + strMsg                                               
        logging.info ( self.className + ': final way-point= {0}'.format(intermediateWayPoint) )
        return endOfSimulation
       


        
