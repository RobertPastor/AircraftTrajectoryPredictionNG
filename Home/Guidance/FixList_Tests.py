'''
Created on 25 déc. 2020

@author: robert
'''


import unittest

from Home.Guidance.FlightPlanFile import FixList

class Test_FixList(unittest.TestCase):

    def test_one(self):
        
        strRoute = 'ADEP/SBGL/10-ALDEIA-NIKDO-MACAE-GIKPO-MABSI-VITORIA-GIDOD-'
        strRoute += 'ISILA-POSGA-SEGURO-BIDEV-NAXOV-IRUMI-ESLIB-MEDIT-RUBEN-KIBEG-'
        strRoute += 'AMBET-VUKSU-NORONHA-UTRAM-MEDAL-NAMBI-RAKUD-IRAVU-MOGNI-ONOBI-CABRAL-'
        strRoute += 'IPERA-ISOKA-LIMAL-UDATI-ODEGI-LOMAS-CANARIA-VASTO-SULAM-DIMSA-ATLUX-'
        strRoute += 'SUNID-AKUDA-OBOLO-PESAS-EKRIS-LUSEM-LULUT-BORDEAUX-COGNAC-ADABI-BOKNO-'
        strRoute += 'DEVRO-VANAD-KOVAK-ADES/LFPG/08L'
        
        fixList = FixList(strRoute)
        fixList.createFixList()
        
        for fix in fixList.getFix():
            print (fix)
            
        print ( "departure Airport ICAO code = {0}".format( fixList.getDepartureAirportICAOcode()) )
        print ( "departure Runway Name = {0}".format( fixList.getDepartureRunwayName() ) )
        
        print ( "arrival Airport ICAO code = {0}".format( fixList.getArrivalAirportICAOcode() ) )
        print ( "arrival runway name = {0}".format( fixList.getArrivalRunwayName() ) )
        
        assert ( fixList.getDepartureAirportICAOcode() == "SBGL" )
        assert ( fixList.getArrivalAirportICAOcode() == "LFPG" )
        
        assert ( fixList.getDepartureRunwayName() == "10" )
        assert ( fixList.getArrivalRunwayName() == "08L" )

    def test_two(self):
        
        strRoute = 'ADEP/SBGL/10-ALDEIA-NIKDO-MACAE-GIKPO-MABSI-VITORIA-GIDOD-'
        strRoute += 'ISILA-POSGA-SEGURO-BIDEV-NAXOV-IRUMI-ESLIB-MEDIT-RUBEN-KIBEG-'
        strRoute += 'AMBET-VUKSU-NORONHA-UTRAM-MEDAL-NAMBI-RAKUD-IRAVU-MOGNI-ONOBI-CABRAL-F280-'
        strRoute += 'IPERA-ISOKA-LIMAL-UDATI-ODEGI-LOMAS-CANARIA-VASTO-SULAM-DIMSA-ATLUX-'
        strRoute += 'SUNID-AKUDA-OBOLO-PESAS-EKRIS-LUSEM-LULUT-BORDEAUX-COGNAC-ADABI-BOKNO-'
        strRoute += 'DEVRO-VANAD-KOVAK-ADES/LFPG/08L'
        
        fixList = FixList(strRoute)
        fixList.createFixList()
        
        for fix in fixList.getFix():
            print (fix)
            
        print ( "departure Airport ICAO code = {0}".format( fixList.getDepartureAirportICAOcode()) )
        print ( "departure Runway Name = {0}".format( fixList.getDepartureRunwayName() ) )
        
        print ( "arrival Airport ICAO code = {0}".format( fixList.getArrivalAirportICAOcode() ) )
        print ( "arrival runway name = {0}".format( fixList.getArrivalRunwayName() ) )
        
        assert ( fixList.getDepartureAirportICAOcode() == "SBGL" )
        assert ( fixList.getArrivalAirportICAOcode() == "LFPG" )
        
        assert ( fixList.getDepartureRunwayName() == "10" )
        assert ( fixList.getArrivalRunwayName() == "08L" )

        
if __name__ == '__main__':
    unittest.main()
        