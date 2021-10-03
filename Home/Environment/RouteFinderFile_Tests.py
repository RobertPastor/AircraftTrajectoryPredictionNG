'''
Created on 2 sept. 2021

@author: robert
'''

import time
import unittest

from Home.Environment.RouteFinderFile import RouteFinder
from Home.Environment.WayPointsDatabaseFile import WayPointsDatabase

Adep = "KATL" #  US Atlanta-Hartsfield Jackson Atlanta Intl
Ades = "KLAX" # US Los Angeles-Los Angeles Intl    

#Adep = "PANC" # US Alaska Anchorage
#Ades = "KATL" #   US Atlanta-Hartsfield Jackson Atlanta Intl

#Adep = "KJFK" # US John F. Kennedy
#Ades = "KSEA" # US Seattle-Seattle Tacoma Intl

#Adep = "KATL" # Atlanta
#Ades = "PHNL" # US Honolulu Intl States 

Adep = "KATL" #  US Atlanta-Hartsfield Jackson Atlanta Intl
Ades = "KMSP" # Minneapolie

Adep = "KBOS"
Ades = "KATL"

Adep = "KIAH"
Ades = "KORD"

Adep = "KIAD"
Ades = "KSFO"

routeDict = {}
routeDict["Adep"] = Adep
routeDict["Ades"] = Ades


class Test_Main(unittest.TestCase):

    def test_one(self):
        
        print ( "=========== Route Finder start  =========== " + time.strftime("%c") )
        wayPointsDb = WayPointsDatabase()
        assert ( wayPointsDb.read() )
        
        print ("Departure = {0} - arrivale = {1}".format(Adep, Ades))
    
        print ( "=========== Route Finder start  =========== " + time.strftime("%c") )
    
        routeFinder = RouteFinder()
        if routeFinder.isConnected():
            print ( 'route finder is connected' )
            
            print ( "=========== Route Finder start  =========== " + time.strftime("%c") )
            #Adep = 'KATL'
            #Ades = 'PHNL'
            
            RFL = 'FL360'
            
            if routeFinder.findRoute(Adep, Ades, RFL):
                routeList = routeFinder.getRouteAsList()
                print ( routeList )
                 
                routeFinder.insertWayPointsInDatabase(wayPointsDb)
      
        print ( "=========== Route Finder start  =========== " + time.strftime("%c") )
        
        

#============================================
if __name__ == '__main__':
    unittest.main()
        
    
    