'''
Created on 31 déc. 2020

@author: robert

'''

import time
import unittest

from Home.Guidance.FlightPathFile import FlightPath



'''
LFPG             0      0   N49°00'35.09" E002°32'52.15" PARIS CHARLES DE GAULLE
NURMO            9     50   N49°49'33.99" E002°45'18.99" NURMO
PERON           32      6   N49°54'45.00" E002°50'23.99" PERON --
SULEX           32      6   N50°00'00.00" E002°55'31.99" SULEX --
CMB     112.6   32     16   N50°13'41.00" E003°09'05.00" CAMBRAI --
VEKIN           24     12   N50°24'14.99" E003°16'29.99" VEKIN --
ADUTO           26      7   N50°30'53.99" E003°21'42.00" ADUTO --
FERDI           23     26   N50°54'45.00" E003°38'12.99" FERDI --
HELEN           24     21   N51°14'06.99" E003°52'11.00" HELEN --
VICOT           24     16   N51°28'54.00" E004°03'01.99" VICOT  --
STD     386     25     17   N51°44'28.99" E004°14'36.99" STAD --
EKROS           25     33   N52°14'13.99" E004°37'10.00" EKROS --
PAM     117.8   71     18   N52°20'04.99" E005°05'32.00" PAMPUS --
NYKER          111     17   N52°13'49.00" E005°31'44.00" NYKER --
ELPAT          112     17   N52°07'38.99" E005°57'03.99" ELPAT --
ARNEM          112      5   N52°05'46.99" E006°04'36.00" ARNEM --
SONEB          100     26   N52°01'24.99" E006°45'51.00" SONEB --
OLDOD          105     10   N51°58'52.00" E007°02'00.99" OLDOD --
SUVOX          106      3   N51°58'08.99" E007°06'29.00" SUVOX --
OSN     114.3   73     46   N52°12'00.00" E008°17'08.00" OSNABRUECK -- 
MOBSA           88      6   N52°12'22.99" E008°26'57.99" MOBSA --
ROBEG           88     30   N52°14'00.99" E009°16'11.00" ROBEG --
DLE     115.2   89     23   N52°15'01.00" E009°53'01.00" LEINE --
HLZ     117.3   80     34   N52°21'48.00" E010°47'43.00" HEHLINGEN
BATEL           47     16   N52°32'49.00" E011°05'59.00" BATEL
EDDT            91     80   N52°33'34.87" E013°17'15.76" BERLIN-TEGEL
'''



class Test_Route(unittest.TestCase):


    def test_route(self):
    
        print ( "=========== Flight Plan start  =========== "  )
        
        #strRoute = 'ADEP/LFPG/26R-LAIGLE-ROLEN-PEPON-KURIS-TERPO-ERIGA-INBAB-ATLEN-DEVAR-ASTURIAS-KUVAN-BISMU-BARKO-FATIMA-ADES/LPPT/03'
        
        strRoute = "ADEP/LFPG/08R"
        strRoute += "-NURMO-PERON-SULEX-CMB-VEKIN-ADUTO-FERDI-HELEN-VICOT-STD-EKROS-PAM"
        strRoute += "-NYKER-ELPAT-ARNEM-SONEB-OLDOD-SUVOX-OSN-MOBSA-ROBEG-DLE-HLZ-BATEL"
        strRoute += "-ADES/EDDT/26R"

        flightPath = FlightPath(route = strRoute, 
                                aircraftICAOcode = 'A320',
                                RequestedFlightLevel = 330, 
                                cruiseMach = 0.82, 
                                takeOffMassKilograms = 68000.0)
        '''
        RFL:    FL 310 => 31000 feet
        Cruise Speed    Mach 0.78                                    
        Take Off Weight    62000 kgs    
        '''
        print ( "=========== Flight Plan compute  =========== " + time.strftime("%c") )
        
        t0 = time.clock()
        print ( 'time zero= ' + str(t0) )
        lengthNauticalMiles = flightPath.computeLengthNauticalMiles()
        print ( 'flight path length= {0:.2f} nautics '.format(lengthNauticalMiles) )
        flightPath.computeFlight(deltaTimeSeconds = 1.0)
        print ( 'simulation duration= ' + str(time.clock()-t0) + ' seconds' )
        
        print ( "=========== Flight Plan create output files  =========== " + time.strftime("%c") )
        flightPath.createFlightOutputFiles()
        print ( "=========== Flight Plan end  =========== " + time.strftime("%c") )


if __name__ == '__main__':
    unittest.main()