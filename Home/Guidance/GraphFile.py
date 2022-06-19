# -*- coding: UTF-8 -*-
'''
Created on Mar 18, 2015

@author: Robert PASTOR

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

'''

from datetime import datetime

from Home.Guidance.WayPointFile import WayPoint, Airport

from Home.OutputFiles.KmlOutput import KmlOutput
from Home.OutputFiles.GroundTrackOutput import GroundTrackOutput

class Vertex(object):
    
    def __init__(self, vertex):
        self.className = self.__class__.__name__
        self._vertex = vertex
        
    def getWeight(self):
        return self._vertex
    
    def __str__(self):
        return self.className + ': vertex= {0}'.format(str(self._vertex))


class Edge(object):
    _tail = None
    _head = None
    distanceTailHeadMeters = 0.0
    bearingTailHeadDegrees = 0.0
    
    def __init__(self, tail, head):
        self._tail = tail
        self._head = head
    
    def getTail(self):
        return self._tail
    
    
    def getHead(self):
        return self._head


    def getDistanceTailHeadMeters(self):
        if ( isinstance(self._tail, (WayPoint, Airport)) and isinstance(self._head, (WayPoint , Airport)) ):
            self.distanceTailHeadMeters = self._tail.getDistanceMetersTo(self._head)

        return self.distanceTailHeadMeters


    def getBearingTailHeadDegrees(self):
        if ( isinstance(self._tail, (WayPoint , Airport)) and isinstance(self._head, (WayPoint , Airport)) ):
            self.bearingTailHeadDegrees = self._tail.getBearingDegreesTo(self._head)

        return self.bearingTailHeadDegrees


class Graph(object):
    _vertex = []
    _edge = []
    lengthMeters = 0.0
    
    def __init__(self):
        self.className = self.__class__.__name__

        self._vertex = []
        self._edge = []
        self.lengthMeters = 0.0


    def __str__(self):
        return self.className + ': number of vertices= {0}'.format(len(self._vertex))


    def addGraph(self, otherGraph):
        ''' add the vertices of a another graph to self '''
        assert isinstance(otherGraph, Graph)
        for vertex in otherGraph._vertex:
            ''' add the vertex '''
            self.addVertex( vertex.getWeight() )
        
        
    def addVertex(self, *args):
        if len(args) == 1:
            weight = args[0]
            self._vertex.append(Vertex(weight))
            ''' add edge here '''
            numberOfVertices = len(self._vertex)
            if numberOfVertices > 1:
                tail = self._vertex[numberOfVertices-2].getWeight()
                head = self._vertex[numberOfVertices-1].getWeight()
                self.addEdge(Edge(tail, head))
            
        else:
            assert (isinstance(args[0], int))
            index = args[0]
            if (index >= 0) and (index <=  len(self._vertex)):
                weight = args[1]
                self._vertex.insert(index, Vertex(weight))
                ''' need to re build the list of Edges '''
                ''' remove edge with index -1 '''
                if index == 0:
                    self._edge.pop(0)
                else:
                    self._edge.pop(index-1)
                ''' need to rebuild two edges '''
                tail1 = self._vertex[index-1].getWeight()
                head1 = self._vertex[index].getWeight()
                self.insertEdge(index, Edge(tail1, head1))
                
                tail2 = self._vertex[index].getWeight()
                head2 = self._vertex[index+1].getWeight()
                self.insertEdge(index+1, Edge(tail2, head2))
            else:
                raise ValueError(self.className + ': insert index= {0] not in the limits 0..len'.format(index, len(self._vertex)))

        
    def getVertex(self, v):
        """
        (Graph, int) -> Vertex
        Returns the specified vertex of this graph.
        """
        assert isinstance(v, int)
        if v < 0 or v >= len(self._vertex):
            raise ValueError(self.className + ': getVertex: vertex index out of bounds!!!')
        return self._vertex[v]
    
        
    def getLastVertex(self):
        numberOfVertices = len(self._vertex)
        if numberOfVertices > 0:
            return self._vertex[numberOfVertices-1]
        return None
    
    
    def insertEdge(self, index, baseEdge):
        assert(isinstance(index, int))
        if (index >= 0) and (index <= len(self._edge)):
            if (isinstance(baseEdge, Edge)):
                ''' modify the list '''
                self._edge.insert(index, baseEdge)
                ''' update the graph length '''
                self.lengthMeters += baseEdge.getDistanceTailHeadMeters()
            else:
                raise ValueError('Graph: insert edge - edge must be of class BaseEdge !!!')

        else:
            raise ValueError('Graph: getVertex: vertex index out of bounds!!!')
    
    
    def addEdge(self, baseEdge):
        '''print 'Graph: add edge'''
        if (isinstance(baseEdge, Edge)):
            self._edge.append(baseEdge)
            ''' update the graph length '''
            self.lengthMeters += baseEdge.getDistanceTailHeadMeters()
        else:
            raise ValueError('Graph: add edge - edge must be of class BaseEdge !!!')
    
    
    def getLastEdge(self):
        numberOfEdges = len(self._edge)
        if  numberOfEdges > 0:
            return self._edge[numberOfEdges-1]
        return None


    def getEdge(self, w):
        '''
        (Graph, int) -> Edge
        '''
        assert isinstance(w, int)
        if w < 0 or w > len(self._edge):
            raise ValueError('Graph: getEdge: edge index out of bounds!!!')
        return self._edge[w]
    
    
    def getNumberOfVertices(self):
        """
        (Graph) -> int
        Returns the number of vertices in this graph.
        """
        return len(self._vertex)


    def getNumberOfEdges(self):
        """
        (Graph) -> int
        Returns the number of edges in this graph.
        """
        return len(self._edge)
    
     
    def getVertices(self):
        for vertex in self._vertex:
            yield vertex


    def getEdges(self):
        ''' returns an iterator on the edges '''
        for edge in self._edge:
            yield edge
    
    
    def createKmlOutputFile(self, abortedFlight, aircraftICAOcode, AdepICAOcode, AdesICAOcde):
        assert ( type(abortedFlight) == bool )
        if self.getNumberOfVertices() > 1:
            ''' need at least two vertices '''
            tail = self.getVertex(0)
            head = self.getVertex(self.getNumberOfVertices()-1)
            assert isinstance(tail.getWeight(), WayPoint)
            assert isinstance(head.getWeight(), WayPoint)
            tailWayPoint = tail.getWeight()
            headWayPoint = head.getWeight()
            
            strFileName = ""
            if abortedFlight:
                strFileName = "ABORTED-"
            strFileName += str(aircraftICAOcode) + "-" + AdepICAOcode + "-" + AdesICAOcde
            strFileName += "-" + tailWayPoint.getName()+'-'+headWayPoint.getName()
            ''' replace '''
            strFileName = str(strFileName).replace(' ', '-')
            strFileName += '-{0}.kml'.format(datetime.now().strftime("%d-%b-%Y-%Hh%Mm%S"))
            
            kmlOutputFile = KmlOutput(strFileName)
            for vertex in self.getVertices():
                wayPoint = vertex.getWeight()
                kmlOutputFile.write(wayPoint.getName(),
                                    wayPoint.getLongitudeDegrees(),
                                    wayPoint.getLatitudeDegrees(), 
                                    wayPoint.getAltitudeMeanSeaLevelMeters())
            kmlOutputFile.close()
    
    
    def createXlsxOutputFile(self, abortedFlight, aircraftICAOcode, AdepICAOcode, AdesICAOcode):
        assert (type(abortedFlight) == bool )
        
        if self.getNumberOfVertices() > 1:
            ''' need at least two vertices '''
            tail = self.getVertex(0)
            head = self.getLastVertex()
            assert isinstance(tail.getWeight(), WayPoint)
            assert isinstance(head.getWeight(), WayPoint)
            tailWayPoint = tail.getWeight()
            headWayPoint = head.getWeight()
            
            strFileName = ""
            if abortedFlight:
                strFileName = "ABORTED-"
            strFileName += str(aircraftICAOcode) + "-" + AdepICAOcode +  "-" + AdesICAOcode
            strFileName += "-" + tailWayPoint.getName()+'-'+headWayPoint.getName()
            strFileName = str(strFileName).replace(' ', '-')
            strFileName += '-{0}.xlsx'.format(datetime.now().strftime("%d-%b-%Y-%Hh%Mm%S"))
            
            groundTrackOutput = GroundTrackOutput(strFileName)
            groundTrackOutput.writeHeaders()
            ''' compute cumulated distance in Meters '''
            cumulatedDistanceMeters = 0.0
            ''' loop '''
            index = 0
            for vertex in self.getVertices():
                ''' build an edge having two consecutive vertices as tail and head '''
                edge = None
                if index > 0:
                    edge = Edge(self.getVertex(index-1).getWeight(), self.getVertex(index).getWeight())
                    
                deltaDistanceMeters = 0.0
                courseAngleDegrees = 0.0
                if not (edge is None):
                    deltaDistanceMeters = edge.getDistanceTailHeadMeters()
                    courseAngleDegrees = edge.getBearingTailHeadDegrees()
                    
                cumulatedDistanceMeters += deltaDistanceMeters
                wayPoint = vertex.getWeight()
                groundTrackOutput.write(wayPoint.getElapsedTimeSeconds(),
                                 wayPoint.getName(),
                                 
                                 wayPoint.getLongitudeDegrees(),
                                 wayPoint.getLatitudeDegrees(),
                                 
                                 wayPoint.getAltitudeMeanSeaLevelMeters(),
                                 deltaDistanceMeters,
                                 cumulatedDistanceMeters,
                                 courseAngleDegrees)
                index += 1
            groundTrackOutput.close()
            
            
    def getLengthMeters(self):
        return self.lengthMeters
            
            
    def computeLengthMeters(self):
        self.lengthMeters = 0.0
        ''' assert that there only one way to visit this graph '''
        for edge in self.getEdges():
            self.lengthMeters +=  edge.getDistanceTailHeadMeters()
        return self.lengthMeters

    

    