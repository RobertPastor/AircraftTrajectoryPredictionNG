'''
Created on 23 déc. 2020

@author: robert
'''
import time
import unittest

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Environment.RunWaysDatabaseFile import RunWayDataBase
from Home.Environment.AirportDatabaseFile import AirportsDatabase

from Home.Guidance.DescentGlideSlopeFile import DescentGlideSlope

from Home.Guidance.WayPointFile import WayPoint, Airport

#============================================
class Test_DescentGlideSlope(unittest.TestCase):

    def test_DescentGlideSlope_One(self):
    
        atmosphere = Atmosphere()
        earth = Earth()
        print ( '==================== three degrees Descent Slope Start  ==================== '+ time.strftime("%c") )
    
        acBd = BadaAircraftDatabase()
        aircraftICAOcode = 'A320'
        aircraft = None
        if acBd.read():
            if ( acBd.aircraftExists(aircraftICAOcode) 
                 and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                
                print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
    
                aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                        aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                        badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                        atmosphere = atmosphere,
                                        earth = earth)
                aircraft.dump()
     
        assert not (aircraft is None)
        print ( '==================== runways database ==================== '+ time.strftime("%c") )
        runWaysDatabase = RunWayDataBase()
        assert runWaysDatabase.read()
        
        runway = runWaysDatabase.getFilteredRunWays(airportICAOcode = 'LFML', runwayName = '31R')
        print ( runway )
      
        print ( "=========== airports  =========== " + time.strftime("%c") )
        airportsDB = AirportsDatabase()
        assert (airportsDB.read())
        
        MarseilleMarignane = airportsDB.getAirportFromICAOCode('LFML')
        print ( MarseilleMarignane )
        
        print ( "=========== descent glide slope  =========== " + time.strftime("%c") )
        threeDegreesGlideSlope = DescentGlideSlope(runway = runway, 
                                                   aircraft = aircraft, 
                                                   arrivalAirport = MarseilleMarignane )
        
        
        print ( "=========== DescentGlideSlope build the glide slope  =========== " + time.strftime("%c") )
    #     threeDegreesGlideSlope.buildGlideSlope(deltaTimeSeconds = 0.1,
    #                         elapsedTimeSeconds = 0.0, 
    #                         initialWayPoint = None, 
    #                         flownDistanceMeters = 0.0, 
    #                         distanceStillToFlyMeters = 100000.0,
    #                         distanceToLastFixMeters = 100000.0)
    
        threeDegreesGlideSlope.buildSimulatedGlideSlope(descentGlideSlopeSizeNautics = 5.0)
        
        print ( "=========== DescentGlideSlope  =========== " + time.strftime("%c") )
        for node in threeDegreesGlideSlope.getVertices():
            print ( node )
        
        print ( "=========== DescentGlideSlope length =========== " + time.strftime("%c") )
        print ( "get number of vertices= {0}".format( threeDegreesGlideSlope.getNumberOfVertices() ) )
        print ( "get number of edges= {0}".format ( threeDegreesGlideSlope.getNumberOfEdges() ) )
        print ( 'Glide Slope overall length= {0} meters'.format( threeDegreesGlideSlope.computeLengthMeters() ) )
        
        threeDegreesGlideSlope.createKmlOutputFile(False, aircraftICAOcode, "Descent-Glide-Scope" + "-{0}".format(runway.getName()), MarseilleMarignane.getName())
        threeDegreesGlideSlope.createXlsxOutputFile(False, aircraftICAOcode, "Descent-Glide-Scope" + "-{0}".format(runway.getName()), MarseilleMarignane.getName())
        print ( '==================== three degrees Descent Slope End  ==================== '+ time.strftime("%c") )


    def test_DescentGlideSlope_Two(self):
    
        atmosphere = Atmosphere()
        earth = Earth()
        print ( '==================== three degrees Descent Slope Start  ==================== '+ time.strftime("%c") )
    
        acBd = BadaAircraftDatabase()
        aircraftICAOcode = 'A320'
        aircraft = None
        if acBd.read():
            if ( acBd.aircraftExists(aircraftICAOcode) 
                 and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                
                print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
    
                aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                        aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                        badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                        atmosphere = atmosphere,
                                        earth = earth)
                aircraft.dump()
     
        assert not (aircraft is None)
        print ( '==================== runways database ==================== '+ time.strftime("%c") )
        runWaysDatabase = RunWayDataBase()
        assert runWaysDatabase.read()
        
        runway = runWaysDatabase.getFilteredRunWays(airportICAOcode = 'LFPG', runwayName = '08L')
        print ( runway )
        
        print ( "=========== airports  =========== " + time.strftime("%c") )
        airportsDB = AirportsDatabase()
        assert (airportsDB.read())
        
        CharlesDeGaulle = airportsDB.getAirportFromICAOCode('LFPG')
        print ( CharlesDeGaulle )

        
        print ( "=========== descent glide slope  =========== " + time.strftime("%c") )
        threeDegreesGlideSlope = DescentGlideSlope(runway = runway, 
                                                   aircraft = aircraft, 
                                                   arrivalAirport = CharlesDeGaulle )
        

        threeDegreesGlideSlope.buildSimulatedGlideSlope(descentGlideSlopeSizeNautics = 5.0)
        
        print ( "=========== DescentGlideSlope  =========== " + time.strftime("%c") )
        for node in threeDegreesGlideSlope.getVertices():
            print ( node )
        
        print ( "=========== DescentGlideSlope length =========== " + time.strftime("%c") )
        print ( "get number of vertices= {0}".format( threeDegreesGlideSlope.getNumberOfVertices() ) )
        print ( "get number of edges= {0}".format ( threeDegreesGlideSlope.getNumberOfEdges() ) )
        print ( 'Glide Slope overall length= {0} meters'.format( threeDegreesGlideSlope.computeLengthMeters() ) )
        
        threeDegreesGlideSlope.createKmlOutputFile(False, aircraftICAOcode, "Descent-Glide-Scope" + "-{0}".format(runway.getName()), CharlesDeGaulle.getName())
        threeDegreesGlideSlope.createXlsxOutputFile(False, aircraftICAOcode, "Descent-Glide-Scope" + "-{0}".format(runway.getName()), CharlesDeGaulle.getName())
        print ( '==================== three degrees Descent Slope End  ==================== '+ time.strftime("%c") )



if __name__ == '__main__':
    unittest.main()
    