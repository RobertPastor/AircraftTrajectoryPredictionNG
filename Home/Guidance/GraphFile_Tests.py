
import time
import unittest
from Home.Environment.AirportDatabaseFile import AirportsDatabase
from Home.Guidance.GraphFile import Graph, Edge, Vertex

class Test_Graph(unittest.TestCase):

    def test_main_one(self):    
        g1 = Graph()
        print ( 'empty graph= ' , g1 )
        v1 = Vertex('Robert')
        g1.addVertex(v1)
        print ( g1 )
        print ( 'number of vertices: {0}'.format(g1.getNumberOfVertices()) )
        print ( g1.getLastVertex().getWeight() )
        print ( g1.getVertex(0).getWeight() )
        
    def test_main_two(self):    
        g1 = Graph()
        v1 = Vertex('Robert')
        v2 = Vertex('Francois')
        g1.addVertex(v1)
        g1.addVertex(v2)
        print ( 'number of vertices: {0}'.format(g1.getNumberOfVertices()) )
        print ( 'number of edges: {0}'.format(g1.getNumberOfEdges()) )
        print ( g1.getLastVertex().getWeight() )
        
    def test_main_three(self):    

        g2 = Graph()
        v3 = Vertex('Marie')
        g2.addVertex(v3)
        
        g1 = Graph()
        v1 = Vertex('Robert')
        v2 = Vertex('Francois')
        g1.addVertex(v1)
        g1.addVertex(v2)
        
        g1.addGraph(g2)
        print ( g1 )
        for vertex in g1.getVertices():
            print ( vertex )
        print ( "=================" )
        for edge in g1.getEdges():
            print ( edge.getTail(), edge.getHead() )

    def test_main_four(self):    

        print ( " ========== AirportsDatabase testing ======= time start= " )
        airportsDb = AirportsDatabase()
        assert (airportsDb.read())
        airportsDb.dumpCountry(Country="France")
        print ( "number of airports= ", airportsDb.getNumberOfAirports() )
        for ap in ['Orly', 'paris', 'toulouse', 'marseille' , 'roissy', 'blagnac' , 'provence' , 'de gaulle']:
            print ( "ICAO Code of= ", ap, " ICAO code= ", airportsDb.getICAOCode(ap) )
        
        t1 = time.clock()
        print ( " ========== AirportsDatabase testing ======= time start= ", t1 )
        CharlesDeGaulleRoissy = airportsDb.getAirportFromICAOCode('LFPG')
        print ( CharlesDeGaulleRoissy )
        MarseilleMarignane = airportsDb.getAirportFromICAOCode('LFML')
        print ( MarseilleMarignane )
        
        g0 = Graph()
        for icao in [ 'LFPO', 'LFMY', 'LFAT', 'LFGJ']:
            airport = airportsDb.getAirportFromICAOCode(icao)
            g0.addVertex(airport)
            
        print ( '================ g0 ================='  )
        for node in g0.getVertices():
            print ( node )
        
        g1 = Graph()
        for icao in [ 'LFKC', 'LFBO' , 'LFKB']:
            airport = airportsDb.getAirportFromICAOCode(icao)
            g1.addVertex(airport)     
            
        print ( '================ g1 ================='  )
        for node in g1.getVertices():
            print ( node )
            
        print ( ' ============== g0.add_graph(g1) ===============' )
        g0.addGraph(g1)
        for node in g0.getVertices():
            print ( node )
            
        print ( ' ============== g0.create XLS file ===============' )
    
        g0.createXlsxOutputFile(False, "Dummy-Aircraft", "Dummy-Adep", "Dummy-Ades")
        g0.createKmlOutputFile(False, "Dummy-Aircraft", "Dummy-Adep", "Dummy-Ades")
    
    def test_main_five(self):    

        airportsDb = AirportsDatabase()
        assert (airportsDb.read())
        
        print ( ' ============== g3 performance ===============' )
        t0 = time.clock()
        g3 = Graph()
        index = 0
        for airport in airportsDb.getAirports():
            print ( airport )
            g3.addVertex(airport)
            index += 1
        t1 = time.clock()
        print ( 'number of airports= {0} - duration= {1} seconds'.format(index, t1-t0) )
     
        airport = airportsDb.getAirportFromICAOCode('LFPG')
        t2= time.clock()
        g4 = Graph()
        for i in range (0,10000):
            g4.addVertex(airport)
        t3 = time.clock()
        print ( 'number of addVertex = {0} - duration= {1:.8f} seconds'.format(i , t3-t2) )
    
if __name__ == '__main__':
    unittest.main()