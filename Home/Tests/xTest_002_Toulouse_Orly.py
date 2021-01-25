'''
Created on Dec 19, 2014

@author: Robert PASTOR
'''

import math
import time

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth
from Home.Environment.AirportDatabaseFile import AirportsDatabase
from Home.Environment.RunWaysDatabaseFile import RunWayDataBase

from Home.Guidance.ClimbRampFile import ClimbRamp
from Home.Guidance.DescentGlideSlopeFile import DescentGlideSlope
from Home.Guidance.GreatCircleRouteFile import GreatCircleRoute
from Home.Guidance.TurnLegFile import TurnLeg

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

Knots2MetersPerSecond = 0.514444444


if __name__ == '__main__':

    t0 = time.clock()
    print ( "time start= ", t0 )
    
    atmosphere = Atmosphere()
    earth = Earth()
    
    print ( '==================== Turn Leg ==================== '+ time.strftime("%c") )
    acBd = BadaAircraftDatabase()
    aircraftICAOcode = 'B743'
    if acBd.read():
        if ( acBd.aircraftExists(aircraftICAOcode) 
             and acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftICAOcode))):
            
            print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
            aircraft = BadaAircraft(aircraftICAOcode, 
                                    acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                    atmosphere,
                                    earth)
            aircraft.dump()
    
    print ( '==================== Turn Leg ==================== '+ time.strftime("%c") )
    print ( 'ac max altitude Mean Sea Level Max TakeOff Weight feet= ' + str(aircraft.getMaxAltitudeMslMtowFeet()) + ' feet')
        
    print ( '==================== Read Airport Database ==================== '+ time.strftime("%c"))
    airportsDB = AirportsDatabase()
    
    print ( '==================== Get Departure Airport ==================== '+ time.strftime("%c") )
    departureAirportIcaoCode = 'LFBO'
    departureAirport = airportsDB.getAirportFromICAOCode(departureAirportIcaoCode)
    print ( departureAirport )
    
    print ( '==================== Get Arrival Airport ==================== '+ time.strftime("%c") )
    arrivalAirportIcaoCode = 'LFPO'
    arrivalAirport = airportsDB.getAirportFromICAOCode(arrivalAirportIcaoCode)
    print ( arrivalAirport )
    
    print ( '====================  find the run-ways ==================== '+ time.strftime("%c") )
    runWaysDatabase = RunWayDataBase()
    if runWaysDatabase.read():
        print ( 'runways DB correctly read' )
        
    print ( '====================  take off run-way ==================== '+ time.strftime("%c") )
    departureRunway = runWaysDatabase.getFilteredRunWays(departureAirportIcaoCode, 'TakeOff', aircraft.WakeTurbulenceCategory)
    print ( departureRunway )
    
    print ('====================  arrival run-way ==================== '+ time.strftime("%c"))
    arrivalRunway = runWaysDatabase.getFilteredRunWays(arrivalAirportIcaoCode, 'Landing', aircraft.WakeTurbulenceCategory)
    print ( arrivalRunway )
  
    print ( "=========== Three Degrees Descent GlideSlope constructor  =========== " + time.strftime("%c"))
    
    threeDegreesDescentGlideSlope = DescentGlideSlope(arrivalRunway, aircraft, arrivalAirport )
    threeDegreesDescentGlideSlope.buildGlideSlope()
    
    finalVertex = threeDegreesDescentGlideSlope.getVertex(threeDegreesDescentGlideSlope.getNumberOfVertices()-1) 
    finalArrivalDescentSlopeWayPoint = finalVertex.getWeight()
    print ( finalArrivalDescentSlopeWayPoint )
    
    initialVertex = threeDegreesDescentGlideSlope.getVertex(0)
    initialArrivalDescentSlopeWayPoint = initialVertex.getWeight()
    
    print ("=========== initial Arrival Descent Slope Way Point  =========== " + time.strftime("%c"))
    print ('altitude of initial arrival Descent Slope Way Point= ' + str(initialArrivalDescentSlopeWayPoint.getAltitudeMeanSeaLevelMeters()) + ' meters')
    
    print ("=========== initial Arrival Descent Slope Way Point  =========== " + time.strftime("%c"))
    print ( initialArrivalDescentSlopeWayPoint )
        
    print ( '==================== Three Degrees climb slope==================== '+ time.strftime("%c"))
    climbSlope = ClimbRamp(runway=departureRunway, 
                            aircraft=aircraft, 
                            departureAirport=departureAirport)
    climbSlope.buildClimbRamp()
    
    print ( '==================== Initial WayPoint - end of Climb Ramp ==================== '+ time.strftime("%c") )
    initialVertex = climbSlope.getVertex(climbSlope.getNumberOfVertices()-1)
    endOfClimbRampWayPoint = initialVertex.getWeight()
    print ( endOfClimbRampWayPoint )
        
    print ( '==================== Initial Heading = end of Climb Ramp ==================== '+ time.strftime("%c") )
    lastClimbSlopeEdge = climbSlope.getEdge(climbSlope.getNumberOfEdges()-1)
    lastClimbSlopeLeg = lastClimbSlopeEdge.getWeight()
    print ('end of climb ramp orientation= ' + str(lastClimbSlopeLeg.getBearingTailHeadDegrees()) + ' degrees')
    
    print ( ' ================== great circle =============== ' )
    
    greatCircle = GreatCircleRoute(departureAirport, arrivalAirport)
    greatCircle.computeGreatCircle()
    print ( 'great circle length= ' + str(greatCircle.computeLengthMeters()) + ' meters')
    
    initialEdge = greatCircle.getEdge(0)
    initialLeg = initialEdge.getWeight()
    print ( 'initial leg bearing= ' + str(initialLeg.getBearingTailHeadDegrees()) + ' degrees' )
    
    print ( ' ================== Take-Off V Stall Speed  =============== ' )
    takeOffVStallSpeedMetersSecond = aircraft.computeStallSpeedCasKnots(
                                                                         aircraftConfiguration='Take-Off', 
                                                                         airport=departureAirport)*Knots2MetersPerSecond
    print ( 'take-off Vstall Kcas= ' + str(takeOffVStallSpeedMetersSecond) + ' meters per second' )

    print ( ' ================== Departure Turn Leg  =============== ' )

    departureTurnLeg = TurnLeg(initialWayPoint=endOfClimbRampWayPoint,
                      finalWayPoint=finalArrivalDescentSlopeWayPoint,
                     initialHeadingDegrees=lastClimbSlopeLeg.getBearingTailHeadDegrees(), 
                     finalHeadingDegrees=initialLeg.getBearingTailHeadDegrees(), 
                     trueAirSpeedMetersSecond=takeOffVStallSpeedMetersSecond,
                     altitudeAboveSeaLevelMeters=endOfClimbRampWayPoint.getAltitudeMeanSeaLevelMeters(),
                     reverse=False)
    
    departureTurnLeg.buildTurnLeg()
    
    print ( ' =========== add Turn Leg to the Departure Climb Slope ============== ' )
    climbSlope.addGraph(departureTurnLeg)
    #climbSlope.createKmlOutputFile()
    
    lastVertex = climbSlope.getVertex(climbSlope.getNumberOfVertices()-1)
    lastWayPoint = lastVertex.getWeight()
    
    lastEdge = climbSlope.getEdge(climbSlope.getNumberOfEdges()-1)
    lastLeg = lastEdge.getWeight()
    print ( 'final heading= ' + str(lastLeg.getBearingTailHeadDegrees()) + ' degrees' )
    
    ''' last leg is down -wards '''
    finalHeadingDegrees = math.fmod ( lastLeg.getBearingTailHeadDegrees() + 180.0 , 360.0 )
    print ( 'final heading - corrected= ' + str(finalHeadingDegrees) + ' degrees '  )

    print ( ' ================== Landing V Stall Speed  =============== ' )
    landingVStallSpeedMetersSecond = aircraft.computeStallSpeedCasKnots(
                                                                         aircraftConfiguration='Landing', 
                                                                         airport=departureAirport)*Knots2MetersPerSecond
    print ( 'take-off Vstall Kcas= ' + str(takeOffVStallSpeedMetersSecond) + ' meters per second' )


    print ( ' ================== arrival turn leg  =============== ' )

    arrivalTurnLeg = TurnLeg(initialWayPoint=initialArrivalDescentSlopeWayPoint,
                         finalWayPoint=lastWayPoint,
                         initialHeadingDegrees=arrivalRunway.getTrueHeadingDegrees(),
                         finalHeadingDegrees=finalHeadingDegrees,
                         trueAirSpeedMetersSecond=landingVStallSpeedMetersSecond,
                     altitudeAboveSeaLevelMeters=initialArrivalDescentSlopeWayPoint.getAltitudeMeanSeaLevelMeters(),
                     reverse=True)
    
    arrivalTurnLeg.buildTurnLeg()
    threeDegreesDescentGlideSlope.addGraph(arrivalTurnLeg)
    
    print ( ' ================== great circle =============== ' )
    t1 = time.clock()
    print ( "time end= ",t1 ,"duration= {0:3.10f} seconds".format(t1-t0) )

    climbSlopeLastVertex = climbSlope.getVertex(climbSlope.getNumberOfVertices()-1)
    climbSlopeLastWayPoint = climbSlopeLastVertex.getWeight()
    print ( climbSlopeLastWayPoint )
    
    arrivalTurnLegFirstVertex = arrivalTurnLeg.getVertex(0)
    arrivalTurnLegFirstWayPoint = arrivalTurnLegFirstVertex.getWeight()
    
    finalGreatCircle = GreatCircleRoute(climbSlopeLastWayPoint, arrivalTurnLegFirstWayPoint)
    finalGreatCircle.computeGreatCircle()
    print ( 'great circle length= ' + str(greatCircle.computeLengthMeters()) + ' meters' )
    
    print ( ' ============= buildClimbRamp the final graph =================')
    climbSlope.addGraph(finalGreatCircle)
    climbSlope.addGraph(threeDegreesDescentGlideSlope)
    print ( 'route length= ' + str(climbSlope.computeLengthMeters()) + ' meters')
    climbSlope.createKmlOutputFile()
    
    t1 = time.clock()
    print ( "time end= ",t1 ,"duration= {0:3.10f} seconds".format(t1-t0) )
