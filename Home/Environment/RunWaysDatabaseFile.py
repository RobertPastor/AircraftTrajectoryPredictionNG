'''
Created on 8 avr. 2015

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

@note: Read an XLS file containing the runways

'''

import os
from xlrd import open_workbook
from Home.Environment.RunWayFile import RunWay


fieldNames = ['id' , 'airport_ref', 'airport_ident' , 'length_ft' , 'width_ft' ,
              'surface' , 'lighted', 'closed', 
              'le_ident' , 'le_latitude_deg' , 'le_longitude_deg' , 
              'le_elevation_ft', 'le_heading_degT', 'le_displaced_threshold_ft' ,
              'he_ident' , 'he_latitude_deg' , 'he_longitude_deg' , 
              'he_elevation_ft' , 'he_heading_degT', 'he_displaced_threshold_ft' ]


    
    
class RunWayDataBase(object):
    FilePath = ''
    #runWaysDb = {}
    
    def __init__(self):
        self.className = self.__class__.__name__

        self.FilePath = "RunWays.xls"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FilePath)
        print ( self.className + ': file path= {0}'.format(self.FilePath) )

        #self.runWaysDb = {}
        
    def getInternalRunWays(self, rowValues):
        '''
        in one row there might be TWO run-ways
        '''
        #print ( 'id content= {0}'.format( rowValues[self.ColumnNames['id']] ) )
        #print ( type ( rowValues[self.ColumnNames['id']] ) )
        id_content = str( int ( rowValues[self.ColumnNames['id']] ) )
        if len(id_content.strip())> 0:
                
            runwayDict = {}
            for column in self.ColumnNames:
                if column == 'id':
                    runwayDict[column] = int(rowValues[self.ColumnNames[column]])
                        
                elif column in ['le_latitude_deg', 'le_longitude_deg', 'le_heading_degT', 
                                    'he_latitude_deg', 'he_longitude_deg', 'he_heading_degT' ,
                                    'length_ft']:
                    ''' float values '''
                    if len(str(rowValues[self.ColumnNames[column]]).strip())>0:
                        runwayDict[column] = float(rowValues[self.ColumnNames[column]])
                    
                elif column in ['le_ident', 'he_ident']:
                    strRunwayName = str(rowValues[self.ColumnNames[column]]).strip().split('.')[0]
                    runwayDict[column] = strRunwayName
                    if str(strRunwayName).isdigit() and int(strRunwayName) < 10 and len(strRunwayName)==1:
                        runwayDict[column] = '0' + strRunwayName
                        
                else:
                    # string fields
                    runwayDict[column] = str(rowValues[self.ColumnNames[column]]).strip()
            ''' we have transformed the row values into a Dictionary => now create the run-ways '''
            keyOne = ''
            keyTwo = ''
            runwayOne = None
            runwayTwo = None
            if (len(str(rowValues[self.ColumnNames['le_ident']]).strip()) > 0 and
                    len(str(rowValues[self.ColumnNames['airport_ident']]).strip()) > 0 and
                    len(str(rowValues[self.ColumnNames['length_ft']]).strip()) > 0 and
                    len(str(rowValues[self.ColumnNames['le_heading_degT']]).strip()) > 0 and
                    len(str(rowValues[self.ColumnNames['le_latitude_deg']]).strip()) > 0 and
                    len(str(rowValues[self.ColumnNames['le_longitude_deg']]).strip()) > 0 ):
                    
                runwayOne = RunWay(Name                =   runwayDict['le_ident'],
                                    airportICAOcode     =   runwayDict['airport_ident'],
                                    LengthFeet          =   runwayDict['length_ft'],
                                    TrueHeadingDegrees  =   runwayDict['le_heading_degT'],
                                    LatitudeDegrees     =   runwayDict['le_latitude_deg'],
                                    LongitudeDegrees    =   runwayDict['le_longitude_deg'])
                    
                keyOne = runwayDict['le_ident']

                    
            if (len(str(rowValues[self.ColumnNames['he_ident']]).strip()) > 0 and
                    len(str(rowValues[self.ColumnNames['airport_ident']]).strip()) > 0 and
                    len(str(rowValues[self.ColumnNames['length_ft']]).strip()) > 0 and
                    len(str(rowValues[self.ColumnNames['he_heading_degT']]).strip()) > 0 and
                    len(str(rowValues[self.ColumnNames['he_latitude_deg']]).strip()) > 0 and
                    len(str(rowValues[self.ColumnNames['he_longitude_deg']]).strip()) > 0 ):
                    
                runwayTwo = RunWay(Name                =   runwayDict['he_ident'],
                                    airportICAOcode     =   runwayDict['airport_ident'],
                                    LengthFeet          =   runwayDict['length_ft'],
                                    TrueHeadingDegrees  =   runwayDict['he_heading_degT'],
                                    LatitudeDegrees     =   runwayDict['he_latitude_deg'],
                                    LongitudeDegrees    =   runwayDict['he_longitude_deg'])
                                    
                keyTwo = runwayDict['he_ident']

        runwayDict = {}
        if len(keyOne)>0 and not(runwayOne is None):
            runwayDict[keyOne] = runwayOne
        if len(keyTwo)>0 and not(runwayTwo is None):
            runwayDict[keyTwo] = runwayTwo
        return runwayDict
    
    
    def getAirportRunways(self, airportICAOcode, runwayLengthFeet = 0.0):
        return None
        
    def hasRunWays(self, airportICAOcode):
        assert not(self.sheet is None)
        assert (isinstance(airportICAOcode, str)) and len(airportICAOcode)>0
        
        for row in range(self.sheet.nrows): 
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if (rowValues[self.ColumnNames['airport_ident']] == airportICAOcode):
                return True
        return False
 
    def getRunWaysAsDict(self, airportICAOcode):
        assert not(self.sheet is None)
        assert (isinstance(airportICAOcode, str)) and len(airportICAOcode)>0
        
        runwaysDict = {}
        for row in range(self.sheet.nrows): 
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if (rowValues[self.ColumnNames['airport_ident']] == airportICAOcode):
                runwaysDict.update(self.getInternalRunWays(rowValues))
        
        return runwaysDict        

    def getRunWays(self, airportICAOcode):
        assert not(self.sheet is None)
        assert (isinstance(airportICAOcode, str)) and len(airportICAOcode)>0
        
        runwaysDict = self.getRunWaysAsDict(airportICAOcode)
        
        for runway in runwaysDict.values():
            yield runway
            
        
    def findAirportRunWays(self, airportICAOcode , runwayLengthFeet = 0.0):
        ''' returns a dictionnary with runways '''
        ''' assert there is only one sheet '''
        assert not(self.sheet is None)
        assert (isinstance(airportICAOcode, str)) and len(airportICAOcode)>0
        #print self.className + ': find runways for airport= {0}'.format(airportICAOcode)
        runwaysDict = {}
        for row in range(self.sheet.nrows): 
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if runwayLengthFeet > 0.0:
                if (rowValues[self.ColumnNames['airport_ident']] == airportICAOcode) and (rowValues[self.ColumnNames['length_ft']] > runwayLengthFeet):
                    runwaysDict.update(self.getInternalRunWays(rowValues))

            else:
                if (rowValues[self.ColumnNames['airport_ident']] == airportICAOcode):
                    runwaysDict.update(self.getInternalRunWays(rowValues))
        return runwaysDict
        
        
    def read(self):
        ''' this method does not read the whole file - only the headers '''
        print (self.FilePath)
        assert len(self.FilePath)>0 and os.path.isfile(self.FilePath) 
        book = open_workbook(self.FilePath, formatting_info=True)
        ''' assert there is only one sheet '''
        self.sheet = book.sheet_by_index(0)
        for row in range(self.sheet.nrows): 
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if row == 0:
                self.ColumnNames = {}
                index = 0
                for column in rowValues:
                    if column not in fieldNames:
                        print ( self.className + ': ERROR - expected runway column name= {0} not in field names'.format(column) )
                        return False
                    else:
                        self.ColumnNames[column] = index
                    index += 1
                break
        
        return True
    
    
    def __str__(self):
        print ( self.className + ':RunWay DataBase= {0}'.format(self.FilePath) )
        
        
    def getFilteredRunWays(self, airportICAOcode, runwayName = ''):
        assert not(airportICAOcode is None) 
        assert isinstance(airportICAOcode, (str)) 
        assert (len(airportICAOcode)>0)
        #print self.className + ': query for airport= {0} and runway= {1}'.format(airportICAOcode, runwayName)
        assert not(self.sheet is None)
        runwaysDict = {}
        for row in range(self.sheet.nrows): 
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if (rowValues[self.ColumnNames['airport_ident']] == airportICAOcode):
                runwaysDict.update(self.getInternalRunWays(rowValues))
        if runwayName in runwaysDict:
            return runwaysDict[runwayName]
        else:
            ''' return arbitrary chosen first run-way '''
            return runwaysDict.get(list (runwaysDict)[0])
        
        
    def __getitem__(self, key):
        if key in self.runWaysDb.keys():
            return self.runWaysDb[key]
        else:
            return None
            
    
