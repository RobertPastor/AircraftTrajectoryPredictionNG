'''
Created on 1 sept. 2021

@author: robert
'''
import os

from xlrd import open_workbook

HeaderNames = ["Departure Airport", "Departure Airport ICAO Code", "Arrival Airport", "Arrival Airport ICAO Code"]

class AirlineRoute(object):
    
    departureAirportICAOcode = ""
    arrivalAirportICAOcode = ""
    
    def __init__(self, _departureAirportICAOcode , _arrivalAirportICAOcode):
        self.className = self.__class__.__name__
        self.departureAirportICAOcode = _departureAirportICAOcode
        self.arrivalAirportICAOcode = _arrivalAirportICAOcode
        
        
    def setRoute(self, route):
        assert ( type(route) is dict )
        assert ( "Departure Airport ICAO Code" in route.keys())
        assert ( "Arrival Airport ICAO Code" in route.keys())
        self.departureAirportICAOcode =  route["Departure Airport ICAO Code"]
        self.arrivalAirportICAOcode =  route["Arrival Airport ICAO Code"]
        
        
    def getDepartureAirportICAOcode(self):
        return self.departureAirportICAOcode
    
    def getArrivalAirportICAOcode(self):
        return self.arrivalAirportICAOcode
    

class AirlineRoutesAirportsDataBase(object):
    FilePath = ''
    RoutesAirports = []

    def __init__(self):
        self.className = self.__class__.__name__

        self.FilePath = "AirlineRoutesAirportsDepartureArrival.xls"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FilePath)
        print ( self.className + ': file path= {0}'.format(self.FilePath) )
        
        
    def exists(self):
        return os.path.exists(self.FilePath) 
    
    
    def read(self):
        ''' this method reads the whole dataset file - not only the headers '''
        print (self.FilePath)
        assert len(self.FilePath)>0 and os.path.isfile(self.FilePath) 
        
        book = open_workbook(self.FilePath, formatting_info=True)
        ''' assert there is only one sheet '''
        self.sheet = book.sheet_by_index(0)
        print ( 'Sheet contains - number of rows = {0}'.format(self.sheet.nrows))
        for row in range(self.sheet.nrows):
            print ( '--> row --> {0}'.format(row) )
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if row == 0:
                self.ColumnNames = {}
                index = 0
                for column in rowValues:
                    if column not in HeaderNames:
                        print ( self.className + ': ERROR - expected Routes Airports column name= {0} not in Header names'.format(column) )
                        return False
                    else:
                        self.ColumnNames[column] = index
                    index += 1

            else:
                #print ( str(row) )
                index = 0
                route = {}
                for cell in rowValues:
                    
                    if len(str(cell))>0:
                        print ( str(cell) )
                        route[HeaderNames[index]] = str(cell)
                        
                    index = index + 1
                self.RoutesAirports.append(route)
        
        return True
    
    
    def dump(self):
        for route in self.RoutesAirports:
            print ( route )
    
    
    def getDepartureArrivalAirportICAOcode(self):
        for route in self.RoutesAirports:
            yield route[HeaderNames[1]] , route[HeaderNames[3]]
            
            
    def getRoutes(self):
        for route in self.RoutesAirports:
            airlineRoute = AirlineRoute()
            airlineRoute.setRoute(route)
            yield airlineRoute
    
    
    def getDepartureAirportsICAOcode(self):
        for route in self.RoutesAirports:
            airportICAOcode = route[HeaderNames[1]]
            yield airportICAOcode
                

    def getArrivalAirportsICAOcode(self):
        for route in self.RoutesAirports:
            airportICAOcode = route[HeaderNames[3]]
            yield airportICAOcode