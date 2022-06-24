'''
Created on 23 mai 2015

@author: PASTOR Robert

        Written By:
                Robert PASTOR 
                @Email: < robert [--DOT--] pastor0691 (--AT--) orange [--DOT--] fr >

        http://trajectoire-predict.monsite-orange.fr/ 
        Copyright 2015 Robert PASTOR 

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
        

this class is responsible for reading the synonym file
The SYNONYM file provided by BADA contains the set of aircraft ICAO code and the prefix to fetch its OPF (Performance file)
this class is aware of the synonym file structure

'''
import os
import logging
BADA_381_DATA_FILES = 'Bada381DataFiles'

class BadaSynonymAircraft(object):
    ''' 
    this class stores the data provided in the synonym file for one aircraft 
    '''
    def __init__(self, 
                 aircraftICAOcode , 
                 aircraftFullName ,
                 OPFfilePrefix ,
                 useSynonym):
        
        self.className = self.__class__.__name__
        self.aircraftICAOcode = aircraftICAOcode
        self.aircraftFullName = aircraftFullName
        self.OPFfilePrefix = OPFfilePrefix
        self.useSynonym = useSynonym

    def getICAOcode(self):
        return self.aircraftICAOcode
    
    def getAircraftFullName(self):
        return self.aircraftFullName
    
    def getAircraftOPFfilePrefix(self):
        return self.OPFfilePrefix
    

class BadaAircraftDatabase(object):
    ''' this class is responsible for reading the synonym file '''
    
    def __init__(self):
        self.className = self.__class__.__name__
        
        self.OPFfileExtension = '.OPF'
        self.BadaSynonymFilePath = 'SYNONYM.NEW'
        
        self.FilesFolder = os.path.dirname(__file__)
            
        logging.info ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.BadaSynonymFilePath = (self.FilesFolder + os.path.sep + self.BadaSynonymFilePath)
        logging.info ( self.className + ': file path= {0}'.format(self.BadaSynonymFilePath) )

        self.aircraftFilesFolder = BADA_381_DATA_FILES
        self.aircraftFilesFolder = (os.path.dirname(__file__) + os.path.sep   + self.aircraftFilesFolder)
               
        self.aircraftDict = {}

    def exists(self):
        return os.path.exists(self.BadaSynonymFilePath) and os.path.isfile(self.BadaSynonymFilePath)
        
    def getSynonymFilePath(self):
        return self.BadaSynonymFilePath
    
    def read(self):
        logging.info ( "{0} - : opening file= ".format( self.className , self.BadaSynonymFilePath ) )
        try:
            f = open(self.BadaSynonymFilePath, "r")
            for line in f:
                line = line.strip()
                useSynonym = False
                if str(line).startswith('CD'):
                    #logging.info self.className + ' line= {0}'.format(line)
                    itemIndex = 0
                    aircraftFullName = ''
                    aircraftICAOcode = ''
                    for item in str(line).split():
                        ''' second item 0..1..2 is the aircraft ICAO code '''
                        if itemIndex == 1:
                            if str(item).strip() == '-':
                                #logging.info self.className +' : has main OPF file'
                                useSynonym = False
                            elif str(item).strip() == '*':
                                #logging.info self.className +' : use synonym OPF file'
                                useSynonym = True

                        if itemIndex == 2:
                            ''' second item is the ICAO code '''
                            aircraftICAOcode = str(item).strip()
                            #logging.info self.className + ': aircraft ICAO code= {0}'.format(aircraftICAOcode)
                            
                        if (item.endswith('_')):
                            break
                        
                        elif itemIndex > 3:
                            aircraftFullName += ' ' + item
                            
                        elif itemIndex > 2:
                            aircraftFullName += item
                        
                        itemIndex += 1
                    OPFfilePrefix = str(str(line).split()[-3])
                    #logging.info self.className + ': OPF file prefix= {0}'.format(OPFfilePrefix)
                    ''' situation after the item finishing with two underscores __ '''
                    if aircraftICAOcode in self.aircraftDict:
                        logging.info ( self.className + ': aircraft ICAO code already in Database' )
                    else:
                        self.aircraftDict[aircraftICAOcode] = BadaSynonymAircraft(aircraftICAOcode = aircraftICAOcode,
                                                                        aircraftFullName = aircraftFullName,
                                                                        OPFfilePrefix = OPFfilePrefix,
                                                                        useSynonym = useSynonym)         
            f.close()
            logging.info ( self.className + ': number of aircrafts in db= {0}'.format(len(self.aircraftDict)) )
            return True
        except Exception as e:
            raise ValueError(self.className + ': error= {0} while reading= {1} '.format(e, self.BadaSynonymFilePath))
        return False    


    def aircraftExists(self, aircraftICAOcode):
        aircraftICAOcode = str(aircraftICAOcode).upper()
        logging.info ( self.className + ': aircraft= {0} exists= {1}'.format(aircraftICAOcode, aircraftICAOcode in self.aircraftDict ) )
        return aircraftICAOcode in self.aircraftDict


    def getAircraftFullName(self, aircraftICAOcode):
        aircraftICAOcode = str(aircraftICAOcode).upper()
        if aircraftICAOcode in self.aircraftDict:
            ac = self.aircraftDict[aircraftICAOcode]
            return ac.getAircraftFullName()
        else:
            return ''


    def getAircraftPerformanceFile(self, aircraftICAOcode):
        aircraftICAOcode = str(aircraftICAOcode).upper()
        if aircraftICAOcode in self.aircraftDict:
            
            ac = self.aircraftDict[aircraftICAOcode]
            OPFfilePrefix = ac.getAircraftOPFfilePrefix()
            
            filePath = os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + BADA_381_DATA_FILES + os.path.sep + OPFfilePrefix + self.OPFfileExtension
            return filePath
        
        return ''
        
        
    def aircraftPerformanceFileExists(self, aircraftICAOcode):
        ''' checks that the performance file OPF exists in its specific folder '''
        aircraftICAOcode = str(aircraftICAOcode).upper()
        if aircraftICAOcode in self.aircraftDict:
            logging.info ( self.className + ': aircraft= {0} - found in database'.format(aircraftICAOcode) )
            ac = self.aircraftDict[aircraftICAOcode]
            OPFfilePrefix = ac.getAircraftOPFfilePrefix()

            filePath = os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + BADA_381_DATA_FILES + os.path.sep + OPFfilePrefix + self.OPFfileExtension
            logging.info ( self.className + ': aircraft= {0} - OPF file= {1} - exists= {2}'.format(aircraftICAOcode,
                                                                                          filePath,
                                                                                          os.path.exists(filePath)) )
            return os.path.exists(filePath) and os.path.isfile(filePath)
        else:
            logging.warning ( self.className + ': aircraft= {0} - NOT found in database'.format(aircraftICAOcode) )
        return False


    def dump(self):
        for key, value in self.aircraftDict.items():
            logging.info ( key )
            logging.info ( self.getAircraftFullName(key) )


    def getAircraftICAOcodes(self):
        for key, value in self.aircraftDict.items():
            yield key