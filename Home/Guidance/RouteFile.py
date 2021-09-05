'''
Created on 5 sept. 2021

@author: robert

this class manages a route 
a route is defined by
1) a departure airport
2) a departure runway - if missing a default runway will be used
3) an ordered list of wayPoints - these are names only - latitude and longitude are defined in a separate database
4) an arrival airport
5) an arrival runway - if missing a default runway will be used


strRoute = 'ADEP/LFBM/27-SAU-VELIN-LMG-BEBIX-GUERE-LARON-KUKOR-MOU-'
    strRoute += 'PIBAT-DJL-RESPO-DANAR-POGOL-OBORN-LUPEN-SUL-'
    strRoute += 'ESULI-TEDGO-ETAGO-IBAGA-RATIP-PIBAD-SOMKO-'
    strRoute += 'ADES/EDDP/26R'

'''


class Route(object):
    
    departureAirportICAOcode = ""
    departureRunWay = ""
    listOfWayPointNames = []
    arrivalAirportICAOcode = ""
    arrivalRunWay = ""
    
    
    
    def __init__(self, _departureAirportICAOcode, _departureRunWay, _listOfWayPointNames, _arrivalAirportICAOcode, _arrivalRunWay):
        
        print ( type(_departureAirportICAOcode) )
        assert ( type(_departureAirportICAOcode)  == str )
        assert ( len(_departureAirportICAOcode) >= 3)
        self.departureAirportICAOcode = _departureAirportICAOcode
        
        if ( _departureRunWay != None ):
            assert ( type(_departureRunWay)  == str )
            self.departureRunWay = _departureRunWay
        else:
            self.departureRunWay = ""
        
        assert ( type(_listOfWayPointNames) == list )
        ''' at least one way point in the list '''
        assert ( len(_listOfWayPointNames ) > 0) 
        self.listOfWayPointNames = _listOfWayPointNames
        
        assert ( type(_arrivalAirportICAOcode)  == str )
        assert ( len(_arrivalAirportICAOcode) >= 3)

        self.arrivalAirportICAOcode = _arrivalAirportICAOcode
        
        if ( _arrivalRunWay != None ):
            assert ( type(_arrivalRunWay) == str )
            self.arrivalRunWay = _arrivalRunWay
        else:
            self.arrivalRunWay = ""
        
        
    def getRouteAsString(self):
        strRoute = "ADEP/" + self.departureAirportICAOcode 
        if ( len ( self.departureRunWay ) > 0):
            strRoute += "/" + self.departureRunWay
            
        strRoute += "-"
        for wayPoint in self.listOfWayPointNames:
            strRoute += str(wayPoint).strip()
            strRoute += "-"
        
        strRoute += "ADES/" + self.arrivalAirportICAOcode
        if ( len ( self.arrivalRunWay ) > 0):
            strRoute += "/" + self.arrivalRunWay 
            
        return strRoute