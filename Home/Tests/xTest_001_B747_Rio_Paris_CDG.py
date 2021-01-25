'''
Created on 6 janvier 2015

@author: PASTOR Robert
'''

import time


from Home.Guidance.FlightPathFile import FlightPath


Meter2Feet = 3.2808 # one meter equals 3.28 feet
Meter2NauticalMiles = 0.000539956803 # One Meter = 0.0005 nautical miles
NauticalMiles2Meter = 1852 

#============================================
if __name__ == '__main__':
    
    print ( "=========== Flight Plan start  =========== "  )
    
    strRoute = 'ADEP/SBGL-ALDEIA-NIKDO-MACAE-GIKPO-MABSI-VITORIA-GIDOD-'
    strRoute += 'ISILA-POSGA-SEGURO-BIDEV-NAXOV-IRUMI-ESLIB-MEDIT-RUBEN-KIBEG-'
    strRoute += 'AMBET-VUKSU-NORONHA-UTRAM-MEDAL-NAMBI-RAKUD-IRAVU-MOGNI-ONOBI-CABRAL-'
    strRoute += 'IPERA-ISOKA-LIMAL-UDATI-ODEGI-LOMAS-CANARIA-VASTO-SULAM-DIMSA-ATLUX-'
    strRoute += 'SUNID-AKUDA-OBOLO-PESAS-EKRIS-LUSEM-LULUT-BORDEAUX-COGNAC-ADABI-BOKNO-'
    strRoute += 'DEVRO-VANAD-KOVAK-ADES/LFPG'
    flightPath = FlightPath(route = strRoute, 
                            aircraftICAOcode = 'B744',
                            RequestedFlightLevel = 390, 
                            cruiseMach = 0.92, 
                            takeOffMassKilograms = 280000.0)
    '''
    RFL:    FL 450 => 45000 feet
    Cruise Speed    => Mach 0.92                                    
    Take Off Weight    396800 kgs    
    '''
    print ( "=========== Flight Plan compute  =========== "  )
    
    t0 = time.clock()
    print ( 'time zero= ' + str(t0) )
    
    lengthNauticalMiles = flightPath.computeLengthNauticalMiles()
    print ( 'flight path length= {0} nautics '.format(lengthNauticalMiles) )
    
    flightPath.computeFlight(deltaTimeSeconds = 1.0)
    print ( 'simulation duration= ' + str(time.clock()-t0) + ' seconds' )
    
    print ( "=========== Flight Plan create output files  =========== " )
    flightPath.createFlightOutputFiles()
    print ( "=========== Flight Plan end  =========== "  )
