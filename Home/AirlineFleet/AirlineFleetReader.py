'''
Created on 29 août 2021

@author: robert
'''

import os

from xlrd import open_workbook
import pandas as pd

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth


''' in service means number of available aircrafts '''
HeaderNames = ['Aircraft' , 'In service', 'Orders' , 'Passengers Delta One', 'Passengers First Class', 'Passengers Premium Select' ,
               'Passengers Delta Confort Plus' , 'Passengers Main Cabin' , 'Passengers Total' , 'Costs per flying hours dollars', 'Refs', 'Notes']


class AirlineAircraft(object):
    
    aircraftFullName = ""
    aircraftICAOcode = ""
    numberOfAircraftsInService = int(0.0)
    maximumOfPassengers = int(0.0)
    costsFlyingPerHoursDollars = 0.0
    
    landingLengthMeters = 0.0
    takeOffMTOWLengthMeters = 0.0
    
    def __init__(self, acFullName, nbInService, maxPassengers, CostsFlyingHoursDollars):
        self.aircraftICAOcode = ""
        self.aircraftFullName = acFullName
        self.numberOfAircraftsInService = nbInService
        self.maximumOfPassengers = maxPassengers
        self.costsFlyingPerHoursDollars = CostsFlyingHoursDollars
        self.landingLengthMeters = 0.0
        self.takeOffMTOWLengthMeters = 0.0
        
    def __str__(self):
        return "{0}-{1}".format(self.aircraftFullName, self.aircraftICAOcode)
        
    def hasICAOcode(self):
        return ( len ( self.aircraftICAOcode ) > 0 )
        
    def getAircraftFullName(self):
        return self.aircraftFullName
    
    def getNumberOfAircraftInstances(self):
        return self.numberOfAircraftsInService
    
    def getMaximumNumberOfPassengers(self):
        return self.maximumOfPassengers
    
    def getCostsFlyingPerHoursDollars(self):
        return self.costsFlyingPerHoursDollars
    
    ''' added as an extension from other databases '''
    def setAircraftICAOcode(self, acICAOcode):
        self.aircraftICAOcode = acICAOcode
    
    def getAircraftICAOcode(self):
        return self.aircraftICAOcode
    
    def setLandingLengthMeters(self, lengthMeters):
        self.landingLengthMeters = lengthMeters
    
    def setTakeOffMTOWLengthMeters(self, lenghtMeters):
        self.takeOffMTOWLengthMeters = lenghtMeters
    
    def getLandingLengthMeters(self):
        return self.landingLengthMeters
    
    def getTakeOffMTOWLengthMeters(self):
        return self.takeOffMTOWLengthMeters


class AirlineFleetDataBase(object):
    FilePath = ''
    
    ''' list of class AirlineAircraft '''
    FleetAircrafts = []
    
    def __init__(self):
        self.className = self.__class__.__name__
        self.FilePath = "AirlineFleet.xls"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FilePath)
        print ( self.className + ': file path= {0}'.format(self.FilePath) )
        
        
    def exists(self):
        return os.path.exists(self.FilePath) 


    def read(self):
        ''' this method reads the whole file - not only the headers '''
        print (self.FilePath)
        assert len(self.FilePath)>0 and os.path.isfile(self.FilePath) 
        book = open_workbook(self.FilePath, formatting_info=True)
        ''' assert there is only one sheet '''
        self.sheet = book.sheet_by_index(0)
        #print ( 'Sheet contains - number of rows = {0}'.format(self.sheet.nrows))
        for row in range(self.sheet.nrows):
            #print ( '--> row --> {0}'.format(row) )
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if row == 0:
                self.ColumnNames = {}
                index = 0
                for column in rowValues:
                    if column not in HeaderNames:
                        print ( self.className + ': ERROR - expected Fleet column name= {0} not in Header names'.format(column) )
                        return False
                    else:
                        self.ColumnNames[column] = index
                    index += 1

            else:
                #print ( str(row) )
                index = 0
                aircraftFullName = ""
                nbAvailableAircrafts = 0
                nbMaxPassengers = 0
                costsFlyingDollars = 0
                for cell in rowValues:
                    if index == 0:
                        if len(str(cell))>0:
                            #print ( cell )
                            aircraftFullName = str(cell).strip()
                        index = index + 1
                    else:
                        if (HeaderNames[index] == "In service"):
                            if len (str(cell).strip()) > 0 :
                                #print ( str(cell).strip() )
                                #print ( type ( str(cell).strip() ) )
                                nbAvailableAircrafts = float(str(cell).strip())
                                nbAvailableAircrafts = int ( nbAvailableAircrafts )
                            
                        if (HeaderNames[index] == "Passengers Total"):
                            if len (str(cell).strip()) > 0 :
                                #print ( str(cell).strip() )
                                nbMaxPassengers = float(str(cell).strip())
                                nbMaxPassengers = int ( nbMaxPassengers )

                        if (HeaderNames[index] == "Costs per flying hours dollars"):
                            if len (str(cell).strip()) > 0 :
                                #print ( cell )
                                assert ( type (str(cell).strip() == float ))
                                costsFlyingDollars = float( str(cell).strip() )
                            
                        index = index + 1
                        
                ''' one ac per row '''
                airlineAircraft = AirlineAircraft( aircraftFullName, nbAvailableAircrafts, nbMaxPassengers, costsFlyingDollars)
                self.FleetAircrafts.append( airlineAircraft )
                
        return True
    
    
    def removeAircrafts(self, listOfFullNames):
        index = 0
        ''' use a copy '''
        for airlineAircraft in list ( self.FleetAircrafts ):
            print ( airlineAircraft.getAircraftFullName() )
            for acFullName in listOfFullNames:
                if acFullName == airlineAircraft.getAircraftFullName():
                    print ( "aircraft found -> {0}".format( acFullName ) )

                    self.FleetAircrafts.pop(index)
                    break
                    
            index = index + 1
    
    
    def extendDatabase(self):
        
        acBd = BadaAircraftDatabase()
        retTwo = acBd.read()
        
        atmosphere = Atmosphere()
        earth = Earth()
        
        if retTwo:
            ''' search for aircraft in the BAD database '''
            for airlineAircraft in self.FleetAircrafts:
                
                assert( isinstance( airlineAircraft, AirlineAircraft ) )
                
                acType = airlineAircraft.getAircraftFullName()
                #print ( str(acType).upper() )
                #print (" ---------------- " , str(acType).upper() , " -----------------")

                for aircraftICAOcode in acBd.getAircraftICAOcodes():
                    ''' check if ac full name found in BADA database '''
                    if ( str(acType).upper() == acBd.getAircraftFullName( aircraftICAOcode )):
                        
                        if ( acBd.aircraftExists(aircraftICAOcode) 
                             and acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
                            
                            print (self.className + " ---------------- " , str(acType).upper() , " -----------------")
                            print (self.className + ' FOUND -> aircraft full name = {0} -- aircraft ICAO code = {1}'.format( acType , aircraftICAOcode  ) )
                            print (self.className + " ---------------- " , str(acType).upper() , " -----------------")

                            ac = BadaAircraft(ICAOcode = aircraftICAOcode , 
                                              aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode), 
                                              badaPerformanceFilePath =  acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                      atmosphere = atmosphere, earth = earth)
                            if (ac is None) == False:
                                print (self.className +  "Landing length meters = {0}".format(ac.getLandingLengthMeters()) )
                                print (self.className +  "Take-off length meters = {0}".format(ac.getTakeOffLengthMeters()) )
                                airlineAircraft.setAircraftICAOcode(aircraftICAOcode)
                                airlineAircraft.setLandingLengthMeters(ac.getLandingLengthMeters())
                                airlineAircraft.setTakeOffMTOWLengthMeters(ac.getTakeOffLengthMeters())
                                
                        else:
                            print (self.className + " ---------------- " , str(acType).upper() , " -----------------")
                            print (self.className + ' NOT FOUND -> aircraft full name = {0} -- aircraft ICAO code = {1}'.format( acType , aircraftICAOcode  ) )
                            print (self.className + " ---------------- " , str(acType).upper() , " -----------------")
                     
                    
            return True
        else:
            return False
        
        
    def createExtendedDatabaseXls(self):
        
        headers = ["aircraft Full Name" , "aircraft ICAO code" , "Landing Length (meters)", "TakeOff Length @MTOW (meters)", "nb Aircrafts In Service", "Total Passengers", "Costs Flying Hours Dollars"]
        
        listAcExtended = []
        for ac in self.FleetAircrafts:
            acDict = {}
            if (len(ac.getAircraftICAOcode())>0):
                acDict[headers[0]] = ac.getAircraftFullName()
                acDict[headers[1]] = ac.getAircraftICAOcode()
                acDict[headers[2]] = ac.getLandingLengthMeters()
                acDict[headers[3]] = ac.getTakeOffMTOWLengthMeters()
                acDict[headers[4]] = ac.getNumberOfAircraftInstances()
                acDict[headers[5]] = ac.getMaximumNumberOfPassengers()
                acDict[headers[6]] = ac.getCostsFlyingPerHoursDollars()
                listAcExtended.append(acDict)
            
        df = pd.DataFrame(listAcExtended)
        fileName =  "AirlineFleetExtendedData.xls" 
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        filePath = os.path.abspath(self.FilesFolder+ os.path.sep + fileName)
        print ( self.className + ': file path= {0}'.format(self.FilePath) ) 
        df.to_excel(excel_writer=filePath, sheet_name="Aircrafts", index = False, columns=headers)

    
    def dump(self):
        for aircraft in self.FleetAircraftTypes:
            print ( 'fleet aircraft type -> {0}'.format( aircraft ))
                
    def getAirlineAircrafts(self):
        for airlineAircraft in self.FleetAircrafts:
            assert( isinstance( airlineAircraft, AirlineAircraft ) )
            yield airlineAircraft
            
    def getAircraftNumberOfInstances(self, aircraftICAOcode):
        nbAvailable = 0
        for airlineAircraft in self.FleetAircrafts:
            assert( isinstance( airlineAircraft, AirlineAircraft ) )
            if ( airlineAircraft.getAircraftICAOcode() == aircraftICAOcode ):
                nbAvailable = airlineAircraft.getNumberOfAircraftInstances()
                
        return nbAvailable
    
        