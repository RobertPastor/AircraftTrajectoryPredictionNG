# -*- coding: UTF-8 -*-

'''
Created on 9 December 2014

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

@note: manages both
 initial climb ramp at 8.0 degrees (parameter)
 orientation = true heading of the provided run-way
 length = 5 nautical miles
 start point has field elevation above mean sea level

'''
import logging
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft
from Home.Environment.RunWaysDatabaseFile import RunWay
from Home.Guidance.WayPointFile import WayPoint, Airport
from Home.Guidance.GraphFile import Graph
from Home.Environment.Constants import NauticalMiles2Meter


class ClimbRamp(Graph):
    
    className = ''
    initialWayPoint = None
    runway = None
    aircraft = None
    takeOffPoint = None
    departureAirport = None
    
    def __init__(self,
                 initialWayPoint = None,
                 runway = None, 
                 aircraft = None, 
                 departureAirport = None):
        
        ''' base class init '''
        Graph.__init__(self)

        self.className = self.__class__.__name__
        
        assert isinstance(initialWayPoint, WayPoint)
        self.initialWayPoint = initialWayPoint
        
        assert isinstance(runway , RunWay) and (not(runway is None))
        self.runway = runway

        assert not(departureAirport is None)
        assert isinstance(departureAirport, Airport)
        self.departureAirport = departureAirport
        
        assert isinstance(aircraft, BadaAircraft)
        self.aircraft = aircraft
        ''' everything is OKay to start '''

        
    def buildClimbRamp(self,
                       deltaTimeSeconds,
                       elapsedTimeSeconds, 
                       distanceStillToFlyMeters, 
                       distanceToLastFixMeters,
                       climbRampLengthNautics = 5.0 ):
        
        ''' from the run-way , we get the orientation or run-way true heading in degrees '''
        runWayOrientationDegrees = self.runway.getTrueHeadingDegrees()     
        logging.info ( self.className + ': run-way orientation degrees= ' + str(runWayOrientationDegrees) + ' degrees' )
                
        ''' climb ramp length in meters '''
        ClimbSlopeLengthMeters = climbRampLengthNautics * NauticalMiles2Meter

        '''============== initial index for the climb ramp graph ============='''
        index = 0
        
        '''========================'''
        ''' initial conditions '''
        '''========================'''
        cumulatedLegDistanceMeters = 0.0
        elapsedTimeSeconds = elapsedTimeSeconds
        altitudeMeanSeaLevelMeters = self.departureAirport.getFieldElevationAboveSeaLevelMeters()

        '''========================'''        
        ''' loop on the climb ramp '''
        '''========================'''
        endOfSimulation = False
        while ( (endOfSimulation == False) and (cumulatedLegDistanceMeters <= ClimbSlopeLengthMeters)):
            
            ''' initial index '''
            if index == 0:
                intermediateWayPoint = self.initialWayPoint
                
            ''' aircraft fly '''
            endOfSimulation, deltaDistanceMeters , altitudeMeanSeaLevelMeters = self.aircraft.fly(
                                                                    elapsedTimeSeconds = elapsedTimeSeconds,
                                                                    deltaTimeSeconds = deltaTimeSeconds , 
                                                                    distanceStillToFlyMeters = distanceStillToFlyMeters,
                                                                    currentPosition =  intermediateWayPoint,
                                                                    distanceToLastFixMeters = distanceToLastFixMeters)
            ''' distance flown '''
            cumulatedLegDistanceMeters += deltaDistanceMeters
            distanceStillToFlyMeters -= deltaDistanceMeters
#             ''' if altitude above ground > 50 feet => move from take-off to initial climb '''
#             if ((altitudeMeanSeaLevelMeters - self.departureAirport.getFieldElevationAboveSeaLevelMeters())*Meter2Feet > 50.0):
#                 self.aircraft.setClimbConfiguration(elapsedTimeSeconds)
            
            ''' name the next way-point '''
            Name = ''
            if index == 0:
                Name = 'climb-ramp-pt-{0}-{1:.2f}-meters'.format(index, cumulatedLegDistanceMeters)
            #bearingDegrees = math.fmod ( runWayOrientationDegrees + 180.0 , 360.0 ) + 180.0
            bearingDegrees = runWayOrientationDegrees
            newIntermediateWayPoint = intermediateWayPoint.getWayPointAtDistanceBearing(Name = Name, 
                                                                                  DistanceMeters = deltaDistanceMeters, 
                                                                                  BearingDegrees = bearingDegrees)
            newIntermediateWayPoint.setAltitudeMeanSeaLevelMeters(altitudeMeanSeaLevelMeters)

            ''' update aircraft state vector '''
            elapsedTimeSeconds += deltaTimeSeconds
            newIntermediateWayPoint.setElapsedTimeSeconds(elapsedTimeSeconds)     
            
            ''' build Climb Ramp the core of the route '''
            self.addVertex(newIntermediateWayPoint)
            
            ''' replace the intermediate point '''
            intermediateWayPoint = newIntermediateWayPoint
            index += 1
            
        ''' set name of the last point '''
        Name = 'climb-ramp-pt-{0}-{1:.2f}-meters'.format(index, cumulatedLegDistanceMeters)
        newIntermediateWayPoint.setName(Name = Name)
 
 
