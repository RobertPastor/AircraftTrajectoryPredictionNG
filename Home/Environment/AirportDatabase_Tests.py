'''
Created on 1 juin 2015

@author: PASTOR Robert

'''
import time
import unittest

from Home.Environment.AirportDatabaseFile import AirportsDatabase
from Home.OutputFiles.KmlOutput import KmlOutput
from Home.Guidance.WayPointFile import Airport

class Test_Main(unittest.TestCase):

    def test_create_Country_Airports_KML(self):
        
        print ( '============ create country specific airports KML file =============' )

        airportsDb = AirportsDatabase()
        self.assertTrue (airportsDb.read())
        country = 'France'
        
        CountryList = ['France', 'Japan', 'United Kingdom', 
                       'Germany', 'Spain', 'United States', 'Canada', 'Italy', 'Spain', 'United Kingdom']

        for country in CountryList:
            fileName =  country + '_Airports.kml'
            kmlOutputFile = KmlOutput(fileName=fileName)
    
            for airport in airportsDb.getAirportsFromCountry( Country = country):
                airportName = str(airport.getName())
                kmlOutputFile.write(name = airportName, 
                                    LongitudeDegrees = airport.getLongitudeDegrees(),
                                    LatitudeDegrees = airport.getLatitudeDegrees(),
                                    AltitudeAboveSeaLevelMeters = airport.getAltitudeMeanSeaLevelMeters())
            kmlOutputFile.close()


    def test_get_countries(self):
        
        print ( '============ test get countries =============' )
        airportsDb = AirportsDatabase()
        self.assertTrue (airportsDb.read())
        
        for country in airportsDb.getCountries():
            print ( 'test get country= ' + country )
        
        
    def test_main(self):
    
        t0 = time.clock()
        print ( ' ========== AirportsDatabase testing ======= ' )
        airportsDb = AirportsDatabase()
        ret = airportsDb.read()
        self.assertTrue (ret)
        t1 = time.clock()
        print ( t1-t0 )
        
        print ( ' ========== AirportsDatabase testing ======= ' )
    
        airportsDb.dumpCountry(Country="France")
        print ( "number of airports= ", airportsDb.getNumberOfAirports() )
        
        print ( ' ========== AirportsDatabase testing ======= ' )
    
        for ap in ['Orly', 'paris', 'toulouse', 'marseille' , 'roissy', 'blagnac' , 'provence' , 'de gaulle']:
            print ( "ICAO Code of= ", ap, " ICAO code= ", airportsDb.getICAOCode(ap) )
        
        t2 = time.clock()
        print ( t2-t1 ) 
        print ( ' ========== AirportsDatabase testing ======= ' )
        CharlesDeGaulleRoissy = airportsDb.getAirportFromICAOCode('LFPG')
        print ( CharlesDeGaulleRoissy )
        
        print ( ' ========== AirportsDatabase testing ======= ' )
        MarseilleMarignane = airportsDb.getAirportFromICAOCode('LFML')
        print ( MarseilleMarignane )
        
        print ( ' ========== AirportsDatabase testing ======= ' )
        Lisbonne = airportsDb.getAirportFromICAOCode('LPPT')
        print ( Lisbonne )
            
        print ( ' ========== AirportsDatabase testing ======= ' )
        JohnFKennedy = airportsDb.getAirportFromICAOCode('KJFK')
        self.assertTrue( isinstance( JohnFKennedy, Airport))
        print ( JohnFKennedy )
        
        print ( ' ========== AirportsDatabase testing ======= ') 
        LosAngeles = airportsDb.getAirportFromICAOCode('KLAX')
        print ( LosAngeles )
        
        self.assertTrue(True)
        
if __name__ == '__main__':
    unittest.main()