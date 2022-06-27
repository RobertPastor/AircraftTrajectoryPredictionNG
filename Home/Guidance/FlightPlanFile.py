# -*- coding: UTF-8 -*-

'''
Created on 25 janvier 2015

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

@note: typical flight plan 

    strRoute = 'ADEP/LFBO-TOU-ALIVA-TOU37-FISTO-LMG-PD01-PD02-AMB-AMB01-AMB02-PD03-PD04-OLW11-OLW83-ADES/LFPO'

purpose : build a fix list from a route expressed as a sequence of names

@ TODO: it should be possible to insert in the flight plan
1) a lat-long expressed point such as N88-55-66W001-02-03
2) a condition such as before a given fix , a speed condition is reached (below 10.000 feet speed is lower to 250knots)

'''
import math
import logging

from Home.Environment.WayPointsDatabaseFile import WayPointsDatabase
from Home.Environment.AirportDatabaseFile import AirportsDatabase

from Home.Environment.RunWaysDatabaseFile import RunWayDataBase
from Home.Environment.RunWayFile import RunWay

from Home.Guidance.WayPointFile import WayPoint, Airport

from Home.Guidance.ConstraintsFile import analyseConstraint
from Home.Environment.Constants import Meter2NauticalMiles


class FixList(object):
    
    className = ""
    ''' ordered list of fixes '''
    fixList = []
    constraintsList = []
    
    strRoute = ""
    departureAirportICAOcode = ""
    arrivalAirportICAOcode = ""
    departureRunwayName = ""
    arrivalRunwayName = ""
    
    
    def __init__(self, strRoute):
        self.className = self.__class__.__name__
        self.fixList = []
        
        self.departureAirportIcaoCode = ""
        self.arrivalAirportICAOcode = ""
        
        self.departureRunwayName = ""
        self.arrivalRunwayName = ""
        
        assert isinstance(strRoute, (str))
        logging.info ( "{0} - route= {1}".format( self.className , strRoute) )
        self.strRoute = strRoute
        
    def __str__(self):
        return self.className + ' fix list= ' + str(self.fixList)
    
    
    def getDepartureAirportICAOcode(self):
        return self.departureAirportICAOcode
    
    def getArrivalAirportICAOcode(self):
        return self.arrivalAirportICAOcode
    
    def getDepartureRunwayName(self):
        return self.departureRunwayName
    
    def getArrivalRunwayName(self):
        return self.arrivalRunwayName
    
    def getFix(self):
        for fix in self.fixList:
            yield fix
            

    def createFixList(self):

        #logging.info self.className + ': ================ get Fix List ================='
        self.fixList = []
        index = 0
        for fix in self.strRoute.split('-'):
            fix = str(fix).strip()
            ''' first item is the Departure Airport '''
            if str(fix).startswith('ADEP'):
                ''' fix is the departure airport '''
                if index == 0:
                    ''' ADEP is the first fix of the route '''
                    if len(str(fix).split('/')) >= 2:
                        self.departureAirportICAOcode = str(fix).split('/')[1]
                        logging.info (self.className + ': departure airport= {0}'.format( self.departureAirportICAOcode))
    
                    self.departureRunwayName = ''
                    if len(str(fix).split('/')) >= 3:
                        self.departureRunwayName = str(fix).split('/')[2]
                        
                else:
                    raise ValueError (self.className + ': ADEP must be the first fix in the route!!!')

                
            elif  str(fix).startswith('ADES'):
                ''' check if Destination Airport is last item of the list '''
                if index == (len(self.strRoute.split('-'))-1):
                    ''' ADES is the last fix of the route '''
                    if len(str(fix).split('/')) >= 2:
                        self.arrivalAirportICAOcode = str(fix).split('/')[1]
                        logging.info (self.className + ': arrival airport= {0}'.format( self.arrivalAirportICAOcode))

                    self.arrivalRunwayName = ''
                    if len(str(fix).split('/')) >= 3:
                        self.arrivalRunwayName = str(fix).split('/')[2]
                    
                    
                else:
                    raise ValueError (self.classeName + ': ADES must be the last fix of the route!!!' )

            else:
                ''' do not take the 1st one (ADEP) and the last one (ADES) '''
                constraintFound, levelConstraint, speedConstraint = analyseConstraint(index, fix)
                #logging.info self.className + ': constraint found= {0}'.format(constraintFound)
                if constraintFound == True:
                    constraint = {}
                    constraint['fixIndex'] = index
                    constraint['level'] = levelConstraint
                    constraint['speed'] = speedConstraint
                    self.constraintsList.append(constraint)
                    print ( self.constraintsList )
                else:
                    self.fixList.append(fix)


            index += 1             


    def deleteFix(self, thisFix):
        if thisFix in self.fixList:
            self.fixList.remove(thisFix)
            
    def indexIsTheLast(self, index):
        return index == len(self.fixList)-1
    
    def nextFixHasConstraint(self, fixIndex):
        answer = False
        for constraint in self.constraintsList:
            if constraint["fixIndex"] == fixIndex:
                logging.warn ( self.className + "----------> there is a constraint associated with the fix = {0} ".format(self.fixList[fixIndex]))
                answer = True
                #raise ValueError("---------- there is a constraint associated with this fix -------")
        return answer
    
    def nextConstraintIsLevel(self, fixIndex):
        answer = False
        for constraint in self.constraintsList:
            if constraint["fixIndex"] == fixIndex and (( constraint["level"] is None ) == False ):
                logging.warn ( self.className + "----------> there is a Level constraint associated with the fix = {0} ".format(self.fixList[fixIndex]))
                answer = True
                #raise ValueError("---------- there is a constraint associated with this fix -------")
        return answer
    
    def getNextLevelConstraintasFlightLevel(self, fixIndex):
        flightLevel = 0.0
        for constraint in self.constraintsList:
            if constraint["fixIndex"] == fixIndex and (( constraint["level"] is None ) == False ):
                logging.warn ( self.className + "----------> there is a Level constraint associated with the fix = {0} ".format(self.fixList[fixIndex]))
                levelConstraint = constraint['level']
                flightLevel = levelConstraint.getLevelConstraintAsFLightLevel()
                #raise ValueError("---------- there is a constraint associated with this fix -------")
        return flightLevel
    

class FlightPlan(FixList):
    
    className = ''
    
    wayPointsDict = {}
    #constraintsList = []
    
    departureAirportIcaoCode = ''
    departureAirport = None
    arrivalAirportIcaoCode = ''
    arrivalAirport = None
    
    def __init__(self, strRoute):
        
        self.className = self.__class__.__name__
        
        FixList.__init__(self, strRoute)
        
        self.wayPointsDict = {}
        
        # call to build the fix list
        self.buildFixList()
         

    def getArrivalAirport(self):
        assert ( not(self.arrivalAirport is None) and isinstance(self.arrivalAirport, Airport))
        return self.arrivalAirport
    
    
    def getDepartureAirport(self):
        assert ( not(self.departureAirport is None) and isinstance(self.departureAirport, Airport))
        return self.departureAirport


    def buildFixList(self):
        '''
        from the route build a fix list and from the fix list build a way point list
        '''
        self.wayPointsDict = {}
        wayPointsDb = WayPointsDatabase()
        assert (wayPointsDb.read())
        
        airportsDb = AirportsDatabase()
        assert airportsDb.read()
        
        runwaysDb = RunWayDataBase()
        assert runwaysDb.read()
        
        self.createFixList()
        for fix in self.getFix():
            wayPoint = wayPointsDb.getWayPoint(fix)
            if not(wayPoint is None) and isinstance(wayPoint, WayPoint):
                #logging.info wayPoint
                self.wayPointsDict[fix] = wayPoint
            else:
                self.deleteFix(fix)
        
        
        self.arrivalRunway =  runwaysDb.getFilteredRunWays(airportICAOcode = self.arrivalAirportICAOcode, runwayName = self.arrivalRunwayName)
        assert ( not (self.arrivalRunway is None) and isinstance(self.arrivalRunway, RunWay ))
        
        self.arrivalAirport = airportsDb.getAirportFromICAOCode(ICAOcode = self.arrivalAirportICAOcode)
        assert ( not (self.arrivalAirport is None) and isinstance( self.arrivalAirport, Airport))
                                
        self.departureRunway = runwaysDb.getFilteredRunWays(airportICAOcode = self.departureAirportICAOcode, runwayName = self.departureRunwayName)
        assert ( not (self.departureRunway is None) and isinstance(self.departureRunway, RunWay ))

        self.departureAirport = airportsDb.getAirportFromICAOCode(ICAOcode = self.departureAirportICAOcode)
        assert ( not (self.departureAirport is None) and isinstance( self.departureAirport, Airport))

        #logging.info self.className + ': fix list= ' + str(self.fixList)
        assert (self.allAnglesLessThan90degrees(minIntervalNautics = 10.0))
       
        
    def insert(self, position, wayPoint):
        ''' 
        insert a waypoint is the list and add the way-point to the flight plan dictionary 
        '''
        assert (isinstance(wayPoint, WayPoint))

        if position == 'begin':
            self.fixList.insert(0, wayPoint.getName())
        elif position == 'end':
            self.fixList.insert(len(self.fixList), wayPoint.getName())
        else:
            if isinstance(position, int):
                self.fixList.insert(position, wayPoint.getName())

        # need to ensure that the same name does not appear twice in the list
        self.wayPointsDict[wayPoint.getName()] = wayPoint


    def getFirstWayPoint(self):
        ''' 
        if fix list is empty , need at least an arrival airport 
        '''
        if len(self.fixList) > 0:
            firstFix = self.fixList[0]
            return self.wayPointsDict[firstFix]
        else:
            ''' fix list is empty => need a departure airport at least '''
            assert not(self.departureAirport is None) and isinstance( self.departureAirport, Airport)
            return self.departureAirport
      
      
    def getLastWayPoint(self):
        ''' if fix list is empty, return arrival airport '''
        if len(self.fixList) > 0:
            lastFix = self.fixList[-1]
            return self.wayPointsDict[lastFix]
        else:
            assert (not(self.arrivalAirport is None)) and isinstance(self.arrivalAirport , Airport)
            return self.arrivalAirport
        
        
    def isOverFlight(self):
        return (self.departureAirport is None) and (self.arrivalAirport is None)
    
    
    def isDomestic(self):
        return not(self.departureAirport is None) and not(self.arrivalAirport is None)
    
    
    def isInBound(self):
        return (self.departureAirport is None) and not(self.arrivalAirport is None)
        
        
    def isOutBound(self):
        return not(self.departureAirport is None) and (self.arrivalAirport is None)
    

    def checkAnglesGreaterTo(self, 
                             firstWayPoint, 
                             secondWayPoint, 
                             thirdWayPoint, 
                             maxAngleDifferenceDegrees = 45.0):
        
        logging.info (self.className + ': {0} - {1} - {2}'.format(firstWayPoint.getName(), secondWayPoint.getName(), thirdWayPoint.getName()) )
        firstAngleDegrees = firstWayPoint.getBearingDegreesTo(secondWayPoint)
        secondAngleDegrees = secondWayPoint.getBearingDegreesTo(thirdWayPoint)
                
        assert (firstAngleDegrees >= 0.0) and (secondAngleDegrees >= 0.0)
        
        logging.info ( self.className + ': first angle= {0:.2f} degrees and second angle= {1:.2f} degrees'.format(firstAngleDegrees, secondAngleDegrees) )
        firstAngleRadians = math.radians(firstAngleDegrees)
        secondAngleRadians = math.radians(secondAngleDegrees)

        angleDifferenceDegrees = math.degrees(math.atan2(math.sin(secondAngleRadians-firstAngleRadians), math.cos(secondAngleRadians-firstAngleRadians))) 
        logging.info (self.className + ': difference= {0:.2f} degrees'.format(angleDifferenceDegrees) )
        
        if abs(angleDifferenceDegrees) > maxAngleDifferenceDegrees:
            logging.info ( self.className + ': WARNING - angle difference=  {0:.2f} greater to {1:.2f} degrees'.format(angleDifferenceDegrees, maxAngleDifferenceDegrees) )
            return False
        
        firstIntervalDistanceNm = firstWayPoint.getDistanceMetersTo(secondWayPoint) * Meter2NauticalMiles
        secondIntervalDistanceNm = secondWayPoint.getDistanceMetersTo(thirdWayPoint) * Meter2NauticalMiles
        if (firstIntervalDistanceNm < 20.0):
            logging.info ( self.className + ': WARNING - distance between {0} and {1} less than 20 Nm = {2:.2f}'.format(firstWayPoint.getName(), secondWayPoint.getName(), firstIntervalDistanceNm) )
        if (secondIntervalDistanceNm < 20.0):
            logging.info ( self.className + ': WARNING - distance between {0} and {1} less than 20 Nm = {2:.2f}'.format(secondWayPoint.getName(), thirdWayPoint.getName(), secondIntervalDistanceNm) )

        return True


    def isDistanceLessThan(self, 
                           firstIndex, 
                           secondIndex, 
                           minIntervalNautics = 10.0):
        '''
        check distance between two index in the fix list 
        '''
        assert (len(self.fixList) > 0) 
        assert  (firstIndex >= 0) and (firstIndex < len(self.fixList))
        assert  (secondIndex >= 0) and (secondIndex < len(self.fixList))
        assert (firstIndex != secondIndex)
        
        firstWayPoint = self.wayPointsDict[self.fixList[firstIndex]]
        secondWayPoint = self.wayPointsDict[self.fixList[secondIndex]]
        IntervalDistanceNm = firstWayPoint.getDistanceMetersTo(secondWayPoint) * Meter2NauticalMiles
        if IntervalDistanceNm < minIntervalNautics:
            logging.info ( self.className + ': WARNING - distance between {0} and {1} less than 10 Nm = {2:.2f}'.format(firstWayPoint.getName(), secondWayPoint.getName(), IntervalDistanceNm) )
            return True
        return False


    def allAnglesLessThan90degrees(self, minIntervalNautics = 10.0):
        ''' returns True if all contiguous angles lower to 90 degrees '''
        ''' suppress point not compliant with the distance interval rules '''
        
        ''' Note: need 3 way-points to build 2 contiguous angles '''
        oneFixSuppressed = True
        while oneFixSuppressed:
            index = 0
            oneFixSuppressed = False
            for fix in self.fixList:
                logging.info ( self.className + ': fix= {0}'.format(fix) )
                
                if index == 1 and not(self.departureAirport is None):
                    firstWayPoint = self.departureAirport
                    logging.info ( firstWayPoint )
                    secondWayPoint = self.wayPointsDict[self.fixList[index-1]]
                    logging.info ( secondWayPoint )
                    thirdWayPoint = self.wayPointsDict[self.fixList[index]]
                    logging.info ( thirdWayPoint )
                    if (self.isDistanceLessThan(firstIndex = index-1, 
                                             secondIndex = index, 
                                             minIntervalNautics = minIntervalNautics) == True):
                        ''' suppress the point from the fix list '''
                        logging.info ( self.className + ': fix suppressed= {0}'.format(self.fixList[index]) )
                        self.fixList.pop(index)
                        oneFixSuppressed = True
                        
                    if oneFixSuppressed:
                        logging.info ( self.className + ': start the whole loop again from the very beginning ' )
                        break
                    else:
                        self.checkAnglesGreaterTo(firstWayPoint, 
                                              secondWayPoint, 
                                              thirdWayPoint,
                                              maxAngleDifferenceDegrees = 30.0)
    
                if index >= 2:
                    
                    firstWayPoint = self.wayPointsDict[self.fixList[index-2]]
                    logging.info ( firstWayPoint )
                    secondWayPoint = self.wayPointsDict[self.fixList[index-1]]
                    logging.info ( secondWayPoint )
                    if (self.isDistanceLessThan(firstIndex = index - 2, 
                                             secondIndex = index - 1, 
                                             minIntervalNautics = minIntervalNautics) == True):
                        ''' suppress the point from the fix list '''
                        logging.info ( self.className + ': fix suppressed= {0}'.format(self.fixList[index-1]) )
                        self.fixList.pop(index-1)
                        oneFixSuppressed = True
                        
                    thirdWayPoint = self.wayPointsDict[self.fixList[index]]
                    logging.info ( thirdWayPoint )
                    if (self.isDistanceLessThan(firstIndex = index - 1, 
                                             secondIndex = index, 
                                             minIntervalNautics = minIntervalNautics) == True) and not (self.indexIsTheLast(index)):
                        ''' suppress the point from the fix list '''
                        logging.info ( self.className + ': fix suppressed= {0}'.format(self.fixList[index]) )
                        self.fixList.pop(index)
                        oneFixSuppressed = True
                    
                    if oneFixSuppressed:
                        logging.info ( self.className + ': start the whole loop again from the very beginning ' )
                        break
                    else:
                        self.checkAnglesGreaterTo(firstWayPoint, 
                                              secondWayPoint, 
                                              thirdWayPoint,
                                              maxAngleDifferenceDegrees = 30.0)
    
                logging.info ( self.className + '============ index = {0} ==========='.format(index) )
                index += 1
        return True
    
    
    def computeLengthNauticalMiles(self):
        return self.computeLengthMeters() * Meter2NauticalMiles
    
    
    def computeLengthMeters(self):
        '''
        returns a float corresponding to the length of the route in Meters 
        if there is a arrival airport , distance from last fix to arrival airport is added
        '''
        lengthMeters = 0.0
        index = 0
        for fix in self.fixList:
            #logging.info fix
            if not(self.departureAirport is None) and isinstance(self.departureAirport, Airport ): 
                if index == 0:
                    lengthMeters += self.departureAirport.getDistanceMetersTo(self.wayPointsDict[fix])
                    previousWayPoint = self.wayPointsDict[fix]

                else:
                    lengthMeters += previousWayPoint.getDistanceMetersTo(self.wayPointsDict[fix])
                    previousWayPoint = self.wayPointsDict[fix]

            else:
                ''' no departure airport '''
                if index == 0:
                    previousWayPoint = self.wayPointsDict[fix]
                else:
                    lengthMeters += previousWayPoint.getDistanceMetersTo(self.wayPointsDict[fix]) 
                    previousWayPoint = self.wayPointsDict[fix]

            index += 1
            
        ''' add distance from last fix to arrival airport if applicable '''
        if not(self.arrivalAirport is None) and isinstance(self.arrivalAirport, Airport):
            #logging.info self.className + ': last fix= ' + self.fixList[-1]
            if len(self.wayPointsDict) > 0:
                lengthMeters += self.wayPointsDict[self.fixList[-1]].getDistanceMetersTo(self.arrivalAirport)
            else:
                raise self.className + " - wayPoints Dictionary is empty !!!"
                if (not(self.departureAirport is None) and isinstance( self.departureAirport, Airport )):
                    lengthMeters += self.departureAirport.getDistanceMetersTo(self.arrivalAirport)
            
        return lengthMeters 

  
    def computeDistanceToLastFixMeters(self, currentPosition, fixListIndex):
        '''
        compute length to fly from the provided index in the fix list
        '''
        lengthMeters = 0.0
        if fixListIndex == len(self.fixList):
            return 0.0

        assert (len(self.fixList) > 0) 
        assert (fixListIndex >= 0) 
        assert (fixListIndex < len(self.fixList))
        assert (len(self.wayPointsDict) > 0)
        if len(self.fixList) == 1:
            return 0.0

        for index in range(fixListIndex, len(self.fixList)):
            #logging.info index
            if index == fixListIndex:
                firstWayPoint = currentPosition
            else:
                firstWayPoint = self.wayPointsDict[self.fixList[index]]
            #logging.info firstWayPoint
            if index + 1 < len(self.fixList):
                secondWayPoint = self.wayPointsDict[self.fixList[index+1]]
                #logging.info secondWayPoint
                lengthMeters += firstWayPoint.getDistanceMetersTo(secondWayPoint)
                #logging.info self.className + ': first wayPoint= {0} - second wayPoint= {1}'.format(firstWayPoint, secondWayPoint)
        
        ''' do not count distance from last fix to arrival airport '''
#         if not(self.arrivalAirport is None):
#             lengthMeters += self.wayPointsDict[self.fixList[-1]].getDistanceMetersTo(self.arrivalAirport)

        return lengthMeters
    
    
