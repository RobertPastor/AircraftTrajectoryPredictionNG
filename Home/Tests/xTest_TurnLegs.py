'''
Created on Dec 22, 2014

@author: Robert PASTOR
'''

import time

from Home.Environment.RunWaysDatabaseFile import RunWayDataBase
from Home.Environment.AirportDatabaseFile import AirportsDatabase

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.Guidance.ClimbRampFile import ClimbRamp

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Guidance.GreatCircleRouteFile import GreatCircleRoute
from Home.Guidance.TurnLegFile import TurnLeg


Knots2MetersPerSecond = 0.514444444

if __name__ == '__main__':

    t0 = time.clock()
    print ( "time start= ", t0 )
    atmosphere = Atmosphere()
    earth = Earth()
    
    print ( '==================== Turn Legs Testing ==================== '+ time.strftime("%c") )
    acBd = BadaAircraftDatabase()
    aircraftICAOcode = 'A320'
    if acBd.read():
        if ( acBd.aircraftExists(aircraftICAOcode) 
             and acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftICAOcode))):
            
            print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
            aircraft = BadaAircraft(aircraftICAOcode, 
                                    acBd.getAircraftPerformanceFile(aircraftICAOcode), 
                                    atmosphere,
                                    earth)
            aircraft.dump()
            
            print ( 'target altitude= ' + str(aircraft.getMaxAltitudeMslMtowFeet()) + ' feet' )
            print ( 'target speed= ' + str(aircraft.getMaxOpSpeedCasKnots()) + ' knots' )
        else:
            raise ValueError ('aircraft not found')
    else:
        raise ValueError ('error while reading the aircraft database')
            
    print ( '==================== Read Airports Database ==================== '+ time.strftime("%c") )
    airportsDB = AirportsDatabase()
    
    print ( '====================  Read the run-ways ==================== '+ time.strftime("%c") )
    runWaysDB = RunWayDataBase()
    if runWaysDB.read():
        print ( 'runways DB correctly read' )
    else:
        raise ValueError ('run-ways not read correctly')
    
    print ( '====================  find the run-ways ==================== '+ time.strftime("%c") )
    for runway in runWaysDB.getRunWays():
        
        print ( '========== ' + str(runway) + ' =================' )
        airportIcaoCode = runway.getAirportICAOcode()
        departureAirport = airportsDB.getAirportFromICAOCode(airportIcaoCode)
        if departureAirport is None:
            raise ValueError ('departure airport not found')
        
        print ( '====================  departure airport ==================== '+ time.strftime("%c") )
        print ( departureAirport )

        print ( '====================  Climb Ramp ==================== '+ time.strftime("%c") )
        climbRamp = ClimbRamp(runway=runway, 
                              aircraft=aircraft, 
                              departureAirport=departureAirport)
        climbRamp.buildClimbRamp()
        
        print ( '==================== Initial WayPoint - end of Climb Ramp ==================== '+ time.strftime("%c") )
        initialVertex = climbRamp.getVertex(climbRamp.getNumberOfVertices()-1)
        endOfClimbRampWayPoint = initialVertex.getWeight()
        print ( endOfClimbRampWayPoint )
          
        print ( '==================== Initial Heading = end of Climb Ramp ==================== '+ time.strftime("%c") )
        lastClimbRampEdge = climbRamp.getEdge(climbRamp.getNumberOfEdges()-1)
        lastClimbRampLeg = lastClimbRampEdge.getWeight()
        print ( 'end of climb ramp orientation= ' + str(lastClimbRampLeg.getBearingTailHeadDegrees()) + ' degrees' )
        
        print ( ' ================== Arrival Airport =============== ' )
        LondonHeathrow = airportsDB.getAirportFromICAOCode('EGLL')
        if LondonHeathrow is None:
            raise ValueError('London-Heathrow not found')
        
        print ( LondonHeathrow )
            
        print ( ' ================== temporary great circle =============== ' )
        greatCircle = GreatCircleRoute(endOfClimbRampWayPoint, LondonHeathrow)
        greatCircle.computeGreatCircle()
        print ( 'great circle length= ' + str(greatCircle.computeLengthMeters()) + ' meters' )
    
        '======== get the first edge => defines the target heading after the turn leg ====== '
        initialGreatCircleEdge = greatCircle.getEdge(0)
        initialGreatCircleLeg = initialGreatCircleEdge.getWeight()
        print ( 'initial leg bearing= ' + str(initialGreatCircleLeg.getBearingTailHeadDegrees()) + ' degrees' )
                                
        print ( ' ================== Departure Turn Leg  =============== ' )
        departureTurnLeg = TurnLeg(
                                   initialWayPoint=endOfClimbRampWayPoint,
                                   finalWayPoint=LondonHeathrow,
                                   initialHeadingDegrees=lastClimbRampLeg.getBearingTailHeadDegrees(),
                                   finalHeadingDegrees=initialGreatCircleLeg.getBearingTailHeadDegrees(),
                                   aircraft=aircraft,
                                   aircraftConfiguration='take-off',
                                   reverse=False)
        departureTurnLeg.buildTurnLeg()
    
        print ( ' =========== add Turn Leg to the Departure Climb Slope ============== ' )
        climbRamp.addGraph(departureTurnLeg)
        
        print ( ' ================== last point of climb ramp + turn leg =============== ' )
        lastVertex = climbRamp.getVertex(climbRamp.getNumberOfVertices()-1)
        endOfCurrentRouteWayPoint = lastVertex.getWeight()
        print ( endOfCurrentRouteWayPoint )

        print ( ' ================== temporary great circle =============== ' )

        secondGreatCircle = GreatCircleRoute(endOfCurrentRouteWayPoint, LondonHeathrow)
        secondGreatCircle.computeGreatCircle()
        print ( 'great circle length= ' + str(greatCircle.computeLengthMeters()) + ' meters' )
        
        print ( ' =========== add Turn Leg to the Departure Climb Slope ============== ' )
        climbRamp.addGraph(secondGreatCircle)
        climbRamp.createKmlOutputFile()