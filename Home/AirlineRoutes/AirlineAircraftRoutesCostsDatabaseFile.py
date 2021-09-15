'''
Created on 12 sept. 2021

@author: robert

compute for each aircraft of the fleet and each route
1) flying duration
2) mass of fuel used during the flight
'''

import time
import os

import pandas as pd

from Home.AirlineRoutes.AirlineRoutes import AirlineRoutes
from Home.Guidance.RouteFile import Route
from Home.AirlineFleet.AirlineFleetReader import AirlineFleetDataBase
from Home.AirlineFleet.AirlineFleetReader import AirlineAircraft

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.Guidance.FlightPathFile import FlightPath
from Home.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance

from Home.Environment.AirportDatabaseFile import AirportsDatabase
from Home.Guidance.WayPointFile import Airport

class AirlineAircraftRoutesCosts(object):
    
    airlineAircraftRoutesCosts = []
    costsHeaders = []

    def __init__(self):
        pass
        self.airlineAircraftRoutesCosts = []
        self.className = self.__class__.__name__
        
        self.FileName = "AirlineAircraftRoutesCosts.xls" 
        self.FilesFolder = os.path.dirname(__file__)
        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FileName)

        self.sheetName = "costs"
        
        self.costsHeaders = []
        self.costsHeaders.append( "aircraft full name" )
        self.costsHeaders.append( "aircraft ICAO code" )
        self.costsHeaders.append( "departure Airport"  )
        self.costsHeaders.append( "departure Airport ICAO code" )
        self.costsHeaders.append( "arrival Airport" )
        self.costsHeaders.append( "arrival Airport ICAO code" )
        self.costsHeaders.append( "flight duration (seconds)" )
        
        self.costsHeaders.append( "total operational costs (dollars)" )
        
        self.costsHeaders.append( "take-off Mass (Kilograms)" )
        self.costsHeaders.append( "Fuel Consumption Mass (Kilograms)" )

    
    def build(self):
        pass
    
        airlineFleet = AirlineFleetDataBase()
        retOne = airlineFleet.read()
        assert(retOne == True)

        retTwo = airlineFleet.extendDatabase()
        assert(retTwo == True)
        
        acBd = BadaAircraftDatabase()
        retThree = acBd.read()
        assert (retThree == True)

        atmosphere = Atmosphere()
        earth = Earth()

        print ( '================ test start =================' )

        airlineRoutes = AirlineRoutes()
        for route in airlineRoutes.getRoutes():
            
            assert( isinstance(route,Route) == True)
            
            print ( route.getRouteAsString() )
            
            for airlineAircraft in airlineFleet.getAirlineAircrafts():
                
                if ( airlineAircraft.hasICAOcode() ):
                    
                    aircraftICAOcode = airlineAircraft.getAircraftICAOcode()
                    print ( "___________________" + aircraftICAOcode + "___________________")
                    
                    if ( acBd.aircraftExists(aircraftICAOcode) 
                         and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                        
                        print ( "___________________" + aircraftICAOcode + "______Exists !!!_____________")

                        acBada = BadaAircraft(ICAOcode = aircraftICAOcode , 
                                              aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode), 
                                              badaPerformanceFilePath =  acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                      atmosphere = atmosphere, earth = earth)

                        acPerformance = AircraftPerformance(acBd.getAircraftPerformanceFile(aircraftICAOcode))

                        if ( ((acBada is None) == False) and ( isinstance( acBada  , BadaAircraft )  ) and ((acPerformance is None) == False) ):
                            
                            print ( "Landing length meters = {0}".format(acBada.getLandingLengthMeters()) )
                            print ( "Take-off length meters = {0}".format(acBada.getTakeOffLengthMeters()) )      
                            print ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                            print ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   
                            print ( "Max Operational Mach Number = {0}".format(acPerformance.getMaxOpMachNumber() ) )   
                                
                            ''' compute the route '''
                            flightPath = FlightPath(route = route.getRouteAsString(), 
                                                    aircraftICAOcode = aircraftICAOcode,
                                                    RequestedFlightLevel = acPerformance.getMaxOpAltitudeFeet() / 100., 
                                                    cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                                    takeOffMassKilograms = acPerformance.getMaximumMassKilograms())
                                
                            print ("=========== Flight Plan compute  =========== " + time.strftime("%c"))
                                
                            t0 = time.clock()
                            print ('time zero= ' + str(t0))
                            #lengthNauticalMiles = flightPath.computeLengthNauticalMiles()
                            #print ('flight path length= {0:.2f} nautics '.format(lengthNauticalMiles))
                            
                            try:
                                flightPath.computeFlight(deltaTimeSeconds = 1.0)
                                print ('simulation duration= ' + str(time.clock()-t0) + ' seconds')
                                    
                                takeOffMassKilograms = acBada.getMaximumMassKilograms()
                                print ( "TakeOff Mass (kilograms) = {0}".format( ( takeOffMassKilograms ) ) )
    
                                finalMassKilograms = flightPath.getAircraftCurrentMassKilograms()
                                print ( "Final Mass (kilograms) = {0}".format( ( finalMassKilograms ) ) )
                                    
                                flightDurationSeconds = flightPath.getFlightDurationSeconds()
                                print ( "Flight Duration (seconds) = {0}".format( ( flightDurationSeconds ) ) )
 
                                airlineAircraftRoutesCost = AirlineAircraftRoutesCost(airlineAircraft, acBada , route, flightDurationSeconds , takeOffMassKilograms, finalMassKilograms)
                                self.airlineAircraftRoutesCosts.append(airlineAircraftRoutesCost)
                                    
                            except Exception as e:
                                print ("-----------> flight was aborted = {0}".format(e))
                                    
                else:
                    print("---------------------------")
                    print("--------- no ICAO code for = {}".format( airlineAircraft.getAircraftFullName() ) )
                    

        ''' check if list is empty '''
        if ( len ( self.airlineAircraftRoutesCosts ) > 0):
            return True
        
        print ( "list of airlineAircraftRoutesCosts is empty.....")
        return False
    
                                    
    def createCostsResultsFile(self):
        pass
    
        airportsDb = AirportsDatabase()
        assert ( airportsDb.read() == True)
        
        print ( self.className + ': file path= {0}'.format(self.FilePath) ) 
            
        if os.path.exists(self.FilePath):
            os.remove(self.FilePath)
            
        
        costs = []
        
        for cost in self.airlineAircraftRoutesCosts:
            assert ( isinstance( cost , AirlineAircraftRoutesCost ) )
            
            costDict = {}
            index = 0
            costDict[self.costsHeaders[index]] = cost.getAircraftFullName()
            index = index + 1
            costDict[self.costsHeaders[index]] = str(cost.getAircraftICAOcode())
                
            airport = airportsDb.getAirportFromICAOCode(cost.getRoute().getDepartureAirportICAOcode())
            assert ( isinstance( airport, Airport) )
            index = index + 1
            costDict[self.costsHeaders[index]] = airport.getName()
            
            index = index + 1
            costDict[self.costsHeaders[index]] = str(cost.getRoute().getDepartureAirportICAOcode())
                
            airport = airportsDb.getAirportFromICAOCode(cost.getRoute().getArrivalAirportICAOcode())
            assert ( isinstance( airport, Airport) )
            
            index = index + 1
            costDict[self.costsHeaders[index]] = airport.getName()

            index = index + 1
            costDict[self.costsHeaders[index]] = str(cost.getRoute().getArrivalAirportICAOcode())

            index = index + 1    
            costDict[self.costsHeaders[index]] = "{0:.2f}".format( cost.getflightDurationSeconds() )
            
            index = index + 1    
            costDict[self.costsHeaders[index]] = "{0:.2f}".format( ( cost.getflightDurationSeconds() / 3600.0 ) *  cost.getAirlineAircraft().getCostsFlyingPerHoursDollars() )
                
            index = index + 1    
            costDict[self.costsHeaders[index]] = "{0:.2f}".format( cost.getTakeOffMassKilograms() )
                
            index = index + 1    
            costDict[self.costsHeaders[index]] = "{0:.2f}".format( cost.getFuelConsumptionKilograms() )
            
            costs.append(costDict)
            print ( costDict )
                
                
        if ( len ( self.airlineAircraftRoutesCosts ) > 0):
            df = pd.DataFrame(costs)
            df.to_excel(excel_writer=self.FilePath, sheet_name=self.sheetName, index = False, columns=self.costsHeaders)
            print ("write to Excel file done")
            return True
        
        return False
    
    
    def read(self):
        print ( self.FilePath )
        if os.path.exists(self.FilePath):
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName, names=self.costsHeaders))
            return  ( df.shape[0] > 0 )
        else:
            return 0


class AirlineAircraftRoutesCost(object):
    
    aircraftICAOcode = ""
    airlineAircraft = None
    aircraftBada = None
    route = None
    flightDurationSeconds = 0.0
    takeOffMassKilograms = 0.0
    finalMassKilograms = 0.0

    def __init__(self, _airlineAircraft, acBada, _route, _flightDurationSeconds, _takeOffMassKilograms, _finalMassKilograms):
        pass
        assert ( isinstance( _airlineAircraft, AirlineAircraft) )
        self.airlineAircraft = _airlineAircraft

        self.aircraftICAOcode = self.airlineAircraft.getAircraftICAOcode()
        
        assert ( isinstance( acBada, BadaAircraft) )
        self.aircraftBada = acBada
        
        assert ( isinstance( _route, Route) )
        self.route = _route
        
        #assert ( type(_flightDurationSeconds) == float)
        self.flightDurationSeconds = _flightDurationSeconds
        
        #assert ( type(_takeOffMassKilograms) == float)
        self.takeOffMassKilograms = _takeOffMassKilograms

        #assert ( type(_finalMassKilograms) == float)
        self.finalMassKilograms = _finalMassKilograms
        
    def getAirlineAircraft(self):
        return self.airlineAircraft
        
    def getAircraftFullName(self):
        return self.airlineAircraft.getAircraftFullName()
        
    def getAircraftICAOcode(self):
        return self.aircraftICAOcode
    
    def getRoute(self):
        return self.route
    
    def getflightDurationSeconds(self):
        return self.flightDurationSeconds
    
    def getTakeOffMassKilograms(self):
        return self.takeOffMassKilograms

    
    def getFuelConsumptionKilograms(self):
        return self.takeOffMassKilograms - self.finalMassKilograms
    