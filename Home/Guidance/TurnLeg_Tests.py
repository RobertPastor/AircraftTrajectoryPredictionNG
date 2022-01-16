# -*- coding: UTF-8 -*-
'''
Created on 17 December 2014

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


this class computes a turn leg.
the turn radius depends upon the speed of the aircraft
A turn leg connects two great circles, each great circle having a course-heading.

http://www.aerospaceweb.org/question/performance/q0146.shtml

extract from A320 Airbus instructor manual

The RADIUS OF TURN of the trajectory is a function of TAS and BANK.
TAS [kt] RADIUS (15° Φ) [NM] RADIUS (25° Φ) [NM]
150             1.2                 0.7
180             1.8                 1.0
210             2.4                 1.4
250             3.4                 2.0
300             4.9                 2.8
480             12.5                 7.2

'''

import time

import unittest
from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.Environment.RunWaysDatabaseFile import RunWayDataBase
from Home.Environment.WayPointsDatabaseFile import WayPointsDatabase
from Home.Environment.AirportDatabaseFile import AirportsDatabase

from Home.Guidance.DescentGlideSlopeFile import DescentGlideSlope
from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Guidance.GroundRunLegFile import GroundRunLeg

from Home.Guidance.TurnLegFile import TurnLeg


class Test_TurnLeg(unittest.TestCase):

    def test_TurnLeg(self):

        print ( '==================== Turn Leg ==================== '+ time.strftime("%c") )
        atmosphere = Atmosphere()
        earth = Earth()
        
        acBd = BadaAircraftDatabase()
        aircraftICAOcode = 'A320'
        assert acBd.read()
        assert acBd.aircraftExists(aircraftICAOcode) 
        assert acBd.aircraftPerformanceFileExists(aircraftICAOcode)
                
        print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
        aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                atmosphere = atmosphere,
                                earth = earth)
        aircraft.dump()
                
        print ( '==================== Get Airport ==================== '+ time.strftime("%c") )
        airportsDB = AirportsDatabase()
        assert airportsDB.read()
        
        print ( '==================== Get Arrival Airport ==================== '+ time.strftime("%c") )
        AirportICAOcode = "KATL"
        #Lisbonne = airportsDB.getAirportFromICAOCode('LPPT')
        Atlanta = airportsDB.getAirportFromICAOCode(AirportICAOcode)
        print ( Atlanta )
        
        print ( '====================  find the run-ways ==================== '+ time.strftime("%c") )
        runWaysDatabase = RunWayDataBase()
        if runWaysDatabase.read():
            print ( 'runways DB correctly read' )
            
        print ( '====================  take off run-way ==================== '+ time.strftime("%c") )
        arrivalRunway = runWaysDatabase.getFilteredRunWays(airportICAOcode = AirportICAOcode,  runwayName = '')
        print ( arrivalRunway )
        
        print ( '==================== Ground run ==================== '+ time.strftime("%c") )
        groundRun = GroundRunLeg(runway = arrivalRunway, 
                                 aircraft = aircraft,
                                 airport = Atlanta)
        
        touchDownWayPoint = groundRun.computeTouchDownWayPoint()
        print ( touchDownWayPoint )
        groundRun.buildDepartureGroundRun(deltaTimeSeconds = 1.0,
                                          elapsedTimeSeconds = 0.0,
                                          distanceStillToFlyMeters = 0.0,
                                          distanceToLastFixMeters = 0.0)
        print ( '==================== Climb Ramp ==================== '+ time.strftime("%c") )
        
        initialWayPoint = groundRun.getLastVertex().getWeight()
    
        descentGlideSlope = DescentGlideSlope( runway = arrivalRunway,
                                                aircraft = aircraft,
                                                arrivalAirport = Atlanta ,
                                                descentGlideSlopeDegrees = 3.0)
        
        ''' if there is a fix nearer to 5 nautics of the touch-down then limit size of simulated glide slope '''
        descentGlideSlope.buildSimulatedGlideSlope(descentGlideSlopeSizeNautics = 5.0)
        descentGlideSlope.createKmlOutputFile(False, aircraftICAOcode, "TopOfGlideSlope", AirportICAOcode)
        
        firstGlideSlopeWayPoint = descentGlideSlope.getVertex(v=0).getWeight()
    
        print ( '==================== Climb Ramp ==================== '+ time.strftime("%c") )
        initialWayPoint = groundRun.getLastVertex().getWeight()
    
        print ( ' ================== turn leg end =============== ' )
        wayPointsDb = WayPointsDatabase()
        assert (wayPointsDb.read())
        
        PLESS = wayPointsDb.getWayPoint('PLESS')
        BNA = wayPointsDb.getWayPoint('BNA')

        #Exona = wayPointsDb.getWayPoint('EXONA')
        #Rosal = wayPointsDb.getWayPoint('ROSAL')
    
        #print ( Rosal.getBearingDegreesTo(Exona) )
        print ( PLESS.getBearingDegreesTo(BNA) )
        initialHeadingDegrees = arrivalRunway.getTrueHeadingDegrees()
        
        lastTurnLeg = TurnLeg( initialWayPoint = firstGlideSlopeWayPoint, 
                               finalWayPoint = BNA,
                               initialHeadingDegrees = initialHeadingDegrees, 
                               aircraft = aircraft,
                               reverse = True)
        deltaTimeSeconds = 1.0
        radiusOfTurnMeters = lastTurnLeg.buildNewSimulatedArrivalTurnLeg(deltaTimeSeconds = deltaTimeSeconds,
                                                     elapsedTimeSeconds = 0.0,
                                                     distanceStillToFlyMeters = 0.0,
                                                     simulatedAltitudeSeaLevelMeters = firstGlideSlopeWayPoint.getAltitudeMeanSeaLevelMeters(),
                                                     flightPathAngleDegrees = 3.0)
        lastTurnLeg.createKmlOutputFile(False, aircraftICAOcode, str("PLESS"), str("BNA"))
        descentGlideSlope.addGraph(lastTurnLeg)
        #descentGlideSlope.createXlsxOutputFile()
        descentGlideSlope.createKmlOutputFile(False, aircraftICAOcode, str("BNA"), Atlanta.getICAOcode())
        print ("radius of turn in meters = {0}".format(radiusOfTurnMeters))
        
        print ( ' ================== turn leg end =============== ' )

if __name__ == '__main__':
    unittest.main()