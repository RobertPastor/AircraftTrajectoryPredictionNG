'''
Created on 29 août 2021

@author: robert
'''

import os

from xlrd import open_workbook

HeaderNames = ['Aircraft' , 'In service', 'Orders' , 'Passengers Delta One', 'Passengers First Class', 'Passengers Premium Select' ,
               'Passengers Delta Confort Plus' , 'Passengers Main Cabin' , 'Total' , 'Refs', 'Notes']


class AirlineFleetDataBase(object):
    FilePath = ''
    FleetAircraftTypes = []
    
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
        print ( 'Sheet contains - number of rows = {0}'.format(self.sheet.nrows))
        for row in range(self.sheet.nrows):
            print ( '--> row --> {0}'.format(row) )
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
                for cell in rowValues:
                    if index == 0:
                        if len(str(cell))>0:
                            print ( cell )
                            self.FleetAircraftTypes.append(str(cell))
                        index = index + 1
                    else:
                        index = index + 1
        
        return True
    
    
    def dump(self):
        if len(self.FleetAircraftTypes)>0:
            for aircraftType in self.FleetAircraftTypes:
                print ( 'fleet aircraft type -> {0}'.format( aircraftType ))
                
    def getAircraftFullNames(self):
        for aircraftType in self.FleetAircraftTypes:
            yield aircraftType