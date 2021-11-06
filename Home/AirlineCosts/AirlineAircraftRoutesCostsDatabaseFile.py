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

kerosene_kilo_to_US_gallons = 0.33
US_gallon_to_US_dollars = 3.25

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
        self.costsHeaders.append( "Aircraft full name" )
        self.costsHeaders.append( "Aircraft ICAO code" )
        self.costsHeaders.append( "Departure Airport"  )
        self.costsHeaders.append( "Departure Airport ICAO code" )
        self.costsHeaders.append( "Arrival Airport" )
        self.costsHeaders.append( "Arrival Airport ICAO code" )
        
        self.costsHeaders.append( "Flight duration (seconds)" )
        self.costsHeaders.append( "Flight Duration (Decimal Hours)" )

        self.costsHeaders.append( "Operational costs (US dollars)" )
        
        self.costsHeaders.append( "take-off Mass (Kilograms)" )
        self.costsHeaders.append( "Fuel Consumption Mass (Kilograms)" )
        self.costsHeaders.append( "Fuel costs (US dollars)" )
        self.costsHeaders.append( "Operational plus fuel costs (US dollars)" )

    
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
            
            ''' loop though all the routes '''
            assert( isinstance(route,Route) == True)
            
            print ( route.getRouteAsString() )
            
            for airlineAircraft in airlineFleet.getAirlineAircrafts():
                ''' loop through all the aircrafts with an ICAO code ''' 
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
            ''' flight duration hours '''
            costDict[self.costsHeaders[index]] = "{0:.2f}".format( cost.getflightDurationSeconds() / 3600.0 )

            index = index + 1    
            ''' total operational costs '''
            operationalCostsUSdollars = ( cost.getflightDurationSeconds() / 3600.0 ) *  cost.getAirlineAircraft().getCostsFlyingPerHoursDollars()
            costDict[self.costsHeaders[index]] = "{0:.2f}".format( operationalCostsUSdollars )
                
            index = index + 1    
            costDict[self.costsHeaders[index]] = "{0:.2f}".format( cost.getTakeOffMassKilograms() )
                
            index = index + 1    
            costDict[self.costsHeaders[index]] = "{0:.2f}".format( cost.getFuelConsumptionKilograms() )
            
            index = index +1
            ''' fuel kerosene costs '''
            fuelCostsUSdollars =  ( cost.getFuelConsumptionKilograms() * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars )
            costDict[self.costsHeaders[index]] = "{0:.2f}".format( fuelCostsUSdollars )

            index = index +1
            ''' total costs = operational + kerosene costs '''
            operationalPlusFuelCostsUSdollars = operationalCostsUSdollars + ( cost.getFuelConsumptionKilograms() * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars )
            costDict[self.costsHeaders[index]] = "{0:.2f}".format( operationalPlusFuelCostsUSdollars )
            
            costs.append(costDict)
            print ( costDict )
                
                
        if ( len ( self.airlineAircraftRoutesCosts ) > 0):
            df = pd.DataFrame(costs)
            df.to_excel(excel_writer=self.FilePath, sheet_name=self.sheetName, index = False, columns=self.costsHeaders)
            print ("write to Excel file done")
            return True
        
        return False
    
    
    def read(self):
        ''' returns a numpy array '''
        print ( self.FilePath )
        if os.path.exists(self.FilePath):
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName, names=self.costsHeaders))
            #for row in df:
                #pass
                #print ( row )
            #print ( "data frame shape = {0}".format(df.shape) )
            #temp = ""
            '''for index in range(len(df)):
                temp += df[self.costsHeaders[0]].iloc[index] 
                temp += " - " + df[self.costsHeaders[1]].iloc[index] 
                temp += " - " + df[self.costsHeaders[2]].iloc[index]
                temp += " - " + df[self.costsHeaders[3]].iloc[index]
                temp += " - " + df[self.costsHeaders[4]].iloc[index]
                temp += " - " + df[self.costsHeaders[5]].iloc[index]
                temp += " - " + str ( df[self.costsHeaders[6]].iloc[index] )
                temp += " - " + str ( df[self.costsHeaders[7]].iloc[index] )
                temp += "\n" '''
            #print ( temp )
            #print  ( df.shape[0] > 0 )
            return df.to_numpy()
        else:
            return None
        
    def getFlightLegOperationalPlusFuelCostsDollars(self, aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode):
        operationalPlusFuelCostsDollars = 0.0
        
        if os.path.exists(self.FilePath):
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName, names=self.costsHeaders))
            np_array = df.to_numpy()
            for row in np_array:
                #print ( "--- numpy array row = {0}".format(row) )
                
                if ( row[1] == aircraftICAOcode and \
                     row[3] == departureAirportICAOcode and \
                     row[5] == arrivalAirportICAOcode):
                    operationalPlusFuelCostsDollars = row[12]
        
        return operationalPlusFuelCostsDollars
    
    def getFlightLegDurationInHours(self, aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode ):
        #print (aircraftICAOcode , departureAirportICAOcode , arrivalAirportICAOcode)
        
        durationHours = 0.0

        if os.path.exists(self.FilePath):
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName, names=self.costsHeaders))
            np_array = df.to_numpy()
            for row in np_array:
                #print ( "--- numpy array row = {0}".format(row) )
                
                if ( row[1] == aircraftICAOcode and \
                     row[3] == departureAirportICAOcode and \
                     row[5] == arrivalAirportICAOcode):
                    durationHours = row[7]
        
        return durationHours
                

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
    
    def getflightDurationHours(self):
        return self.flightDurationSeconds / 3600.0
    
    def getTakeOffMassKilograms(self):
        return self.takeOffMassKilograms
    
    def getFuelConsumptionKilograms(self):
        return self.takeOffMassKilograms - self.finalMassKilograms
    