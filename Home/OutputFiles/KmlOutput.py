# -*- coding: UTF-8 -*-

'''
@since: Created on 26 aout 2014

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

create a KML output file that is readable in Google Earth
'''
import os
import xml.dom.minidom

class KmlOutput():
    
    fileName = ""
    kmlDoc = None
    documentElement = None
    
    def __init__(self, fileName):
        
        self.className = self.__class__.__name__

        self.fileName = str(fileName).replace('/', '-')
        if ( not ( str(self.fileName).endswith(".kml") )):
            self.fileName = self.fileName + ".kml"
        #sanity check : filename shall not contain "/"
        assert (not ('/' in self.fileName))
        
        # This constructs the KML document
        self.kmlDoc = xml.dom.minidom.Document()
        kmlElement = self.kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
        kmlElement.setAttribute('xmlns', 'http://earth.google.com/kml/2.2')
        kmlElement = self.kmlDoc.appendChild(kmlElement)
        self.documentElement = self.kmlDoc.createElement('Document')
        self.documentElement = kmlElement.appendChild(self.documentElement)
        
        
    def write(self, 
              name,
              LongitudeDegrees, 
              LatitudeDegrees, 
              AltitudeAboveSeaLevelMeters):
        
        assert isinstance(name, (str))
        assert isinstance(LongitudeDegrees, float)
        assert isinstance(LatitudeDegrees, float)
        assert isinstance(AltitudeAboveSeaLevelMeters, float)
        
        placemarkElement = self.kmlDoc.createElement('Placemark')
        
        nameElement = self.kmlDoc.createElement('name')
        nameElement.appendChild(self.kmlDoc.createTextNode(name))
        placemarkElement.appendChild(nameElement)
        
        pointElement = self.kmlDoc.createElement('Point')
        placemarkElement.appendChild(pointElement)
        
        extrudeElement = self.kmlDoc.createElement('extrude')
        extrudeElement.appendChild(self.kmlDoc.createTextNode("1"))
        pointElement.appendChild(extrudeElement)
        
        ''' 16th June 2022 - altitude above Sea Level '''
        altitudeElement = self.kmlDoc.createElement('altitude')
        altitudeElement.appendChild(self.kmlDoc.createTextNode(str(AltitudeAboveSeaLevelMeters)))
        pointElement.appendChild(altitudeElement)

        
        altitudeModeElement = self.kmlDoc.createElement('altitudeMode')
        altitudeModeElement.appendChild(self.kmlDoc.createTextNode("absolute"))
        pointElement.appendChild(altitudeModeElement)
        
        coordinates = str(float(LongitudeDegrees))+","+str(float(LatitudeDegrees))+","+str(AltitudeAboveSeaLevelMeters)
        #coordinates = str(float(LongitudeDegrees))+","+str(float(LatitudeDegrees))
        coorElement = self.kmlDoc.createElement('coordinates')
        coorElement.appendChild(self.kmlDoc.createTextNode(coordinates))
        pointElement.appendChild(coorElement)
        
        self.documentElement.appendChild(placemarkElement)

        
    def close(self):
        ''' always write in the results folder '''
        self.FilesFolder = os.path.dirname(__file__)
        self.FilesFolder =  self.FilesFolder + os.path.sep + '..' + os.path.sep + 'ResultsFiles'
        filePath = (self.FilesFolder + os.path.sep + self.fileName)
        print ( self.className + ': file path= {0}'.format(filePath) )
        kmlFile = open(filePath, 'wb')
        kmlFile.write(self.kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))
        kmlFile.close()

        
#============================================
if __name__ == '__main__':
    
    ''' create an KML file with all the way points '''
    