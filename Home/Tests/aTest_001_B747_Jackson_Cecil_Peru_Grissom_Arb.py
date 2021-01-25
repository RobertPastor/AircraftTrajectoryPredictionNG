'''
Created on 6 janvier 2015

@author: PASTOR Robert

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

'''

import time


from Home.Guidance.FlightPathFile import FlightPath


Meter2Feet = 3.2808 # one meter equals 3.28 feet
Meter2NauticalMiles = 0.000539956803 # One Meter = 0.0005 nautical miles
NauticalMiles2Meter = 1852 

#============================================
if __name__ == '__main__':
    
    print ( "=========== Flight Plan start  =========== "  )
    
    strRoute = 'ADEP/KVQQ/36R-MONIA-AYS-WUXTE-AMG-AHN-VXV-GHATS-RYANS-IIU-HEALS-STREP-HOUSE-MOUTH-ICUCO-ROSES-VHP-ZIPPY-EDMEW-HUBOP-PASEW-OKK-ADES/KGUS/05'
    
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
