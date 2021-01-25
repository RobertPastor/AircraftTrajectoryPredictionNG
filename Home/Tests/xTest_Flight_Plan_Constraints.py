# -*- coding: UTF-8 -*-

'''
Created on 14 sept. 2015

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

import unittest
from Home.Guidance.FlightPlanFile import FlightPlan
from Home.Guidance.WayPointFile import Airport

class Test_Flight_Plan(unittest.TestCase):

    def test_main_one(self):
         
        print ( "=========== Flight Plan start  =========== "  )
        
        strRoute = 'ADEP/LFBO-TOU-ALIVA-TOU37-FISTO-LMG-PD01-PD02-AMB-AMB01-AMB02-PD03-PD04-OLW11-OLW83-ADES/LFPO'
        flightPlan = FlightPlan(strRoute)
    
        self.assertFalse(flightPlan.isOverFlight())
        self.assertTrue (flightPlan.isDomestic())
        self.assertFalse(flightPlan.isInBound())
        self.assertFalse(flightPlan.isOutBound())
        print ( 'all angles < 90.0 degrees= ' + str(flightPlan.allAnglesLessThan90degrees()) )
        print ( 'flight path length= ' + str(flightPlan.computeLengthNauticalMiles()) + ' nautical miles' )
    
    
    #     fixListIndex = 0
    #     print 'length from index={0} - length= {1} meters'.format(fixListIndex, 
    #                                                               flightPlan.computeDistanceToLastFixMeters(fixListIndex = 0))
    #     print "=========== Flight Plan start  =========== " 
    # 
    #     fixListIndex = 1
    #     print 'length from index={0} - length= {1} meters'.format(fixListIndex, 
    #                                                               flightPlan.computeStillToFlyMeters(fixListIndex = 0))
    
    def test_main_two(self):
        
        print ( "=========== Flight Plan start  =========== "  )

        strRoute = 'ADEP/LFBO-TOU-ALIVA-TOU37-FISTO-LMG-PD01-PD02-AMB-AMB01-AMB02-PD03-PD04-OLW11-OLW83-ADES/LFPO'
        flightPlan = FlightPlan(strRoute)
        
        self.assertTrue ( isinstance( flightPlan.getDepartureAirport(), Airport) )
        self.assertTrue ( isinstance( flightPlan.getArrivalAirport() , Airport) )
                          
                          
    def test_main_three(self):

        print ( "=========== Flight Plan start  =========== "  )
        
        strRoute = 'TOU-ALIVA-TOU37-FISTO-LMG-PD01-PD02-AMB-AMB01-AMB02-PD03-PD04-OLW11-OLW83-ADES/LFPO'
        flightPlan = FlightPlan(strRoute)
    
        print ( 'is over flight= ' + str(flightPlan.isOverFlight()) )
        print ( 'is domestic= ' + str(flightPlan.isDomestic()))
        print ( 'is in Bound= ' + str(flightPlan.isInBound()))
        print ( 'is out Bound= ' + str(flightPlan.isOutBound()))
        print ( 'all angles < 90.0 degrees= ' + str(flightPlan.allAnglesLessThan90degrees()))
        print ( 'flight path length= ' + str(flightPlan.computeLengthNauticalMiles()) + ' nautical miles')
    
    def test_main_four(self):

        print ( "=========== Flight Plan start  =========== " )
        
        strRoute = 'ADEP/LFBO-TOU-ALIVA-TOU37-FISTO-LMG-PD01-PD02-AMB-AMB01-AMB02-PD03-PD04-OLW11-OLW83'
        flightPlan = FlightPlan(strRoute)
    
        print ('is over flight= ' + str(flightPlan.isOverFlight()))
        print ('is domestic= ' + str(flightPlan.isDomestic()))
        print ('is in Bound= ' + str(flightPlan.isInBound()))
        print ('is out Bound= ' + str(flightPlan.isOutBound()))
        print ('all angles < 90.0 degrees= ' + str(flightPlan.allAnglesLessThan90degrees()))
        print ('flight path length= ' + str(flightPlan.computeLengthNauticalMiles()) + ' nautical miles')
    
    def test_main_five(self):

        print ( "=========== Flight Plan start  =========== "  )
        
        strRoute = 'TOU-ALIVA-TOU37-FISTO-LMG-PD01-PD02-AMB-AMB01-AMB02-PD03-PD04-OLW11-OLW83'
        flightPlan = FlightPlan(strRoute)
    
        print ('is over flight= ' + str(flightPlan.isOverFlight()))
        print ('is domestic= ' + str(flightPlan.isDomestic()))
        print ('is in Bound= ' + str(flightPlan.isInBound()))
        print ('is out Bound= ' + str(flightPlan.isOutBound()))
        print ('all angles < 90.0 degrees= ' + str(flightPlan.allAnglesLessThan90degrees()))
        print ('flight path length= ' + str(flightPlan.computeLengthNauticalMiles()) + ' nautical miles')
        
    def test_main_six(self):
        
        print ( "=========== Flight Plan start  =========== "  )

        strRoute = 'ADEP/SBGL-ALDEIA-NIKDO-MACAE-GIKPO-MABSI-VITORIA-GIDOD-'
        strRoute += 'ISILA-POSGA-SEGURO-BIDEV-NAXOV-IRUMI-ESLIB-MEDIT-RUBEN-KIBEG-'
        strRoute += 'AMBET-VUKSU-NORONHA-UTRAM-MEDAL-NAMBI-RAKUD-IRAVU-MOGNI-ONOBI-CABRAL-'
        strRoute += 'IPERA-ISOKA-LIMAL-UDATI-ODEGI-LOMAS-CANARIA-VASTO-SULAM-DIMSA-ATLUX-'
        strRoute += 'SUNID-AKUDA-OBOLO-PESAS-EKRIS-LUSEM-LULUT-BORDEAUX-COGNAC-ADABI-BOKNO-'
        strRoute += 'DEVRO-VANAD-KOVAK-ADES/LFPG'

    
        flightPlan = FlightPlan(strRoute)
    
        print ('is over flight= ' + str(flightPlan.isOverFlight()))
        print ('is domestic= ' + str(flightPlan.isDomestic()))
        print ('is in Bound= ' + str(flightPlan.isInBound()))
        print ('is out Bound= ' + str(flightPlan.isOutBound()))
        print ('all angles < 90.0 degrees= ' + str(flightPlan.allAnglesLessThan90degrees()))
        print ('flight path length= ' + str(flightPlan.computeLengthNauticalMiles()) + ' nautical miles')
        
    def test_main_seven(self):

        print ( "=========== Flight Plan start  =========== " )
        
        strRoute = 'ADEP/SBGL-ALDEIA-NIKDO-MACAE'
        flightPlan = FlightPlan(strRoute)
        
        print ( 'flight path length= ' + str(flightPlan.computeLengthNauticalMiles()) + ' nautical miles' )

    def test_main_eight(self):

        print ( "=========== Flight Plan start  =========== " )
    
        strRoute = 'ADEP/LFBM/27-'
        strRoute += 'SAU-VELIN-LMG-BEBIX-GUERE-LARON-KUKOR-MOU-'
        strRoute += 'PIBAT-DJL-RESPO-DANAR-POGOL-OBORN-LUPEN-SUL-'
        strRoute += 'ESULI-TEDGO-ETAGO-IBAGA-RATIP-PIBAD-SOMKO-'
        strRoute += 'ADES/EDDP/26R'
        flightPlan = FlightPlan(strRoute)
        
        print ( 'flight path length= ' + str(flightPlan.computeLengthNauticalMiles()) + ' nautical miles' )
    
    def test_main_nine(self):
        
        print ( "=========== Test Speed and Level constraints  =========== " )
        
        ''' N suivi de 4 chiffres pour la vitesse propre (TAS) en n�uds (exemple : N0450), '''
        strRoute = 'ADEP/LFBO-TOU-ALIVA-N0450-FISTO-LMG-PD01-PD02-AMB-AMB01-AMB02-PD03-PD04-OLW11-OLW83-ADES/LFPO'
        flightPlan = FlightPlan(strRoute)
        print ( flightPlan )
        
    def test_main_ten(self):

        print ( "=========== Test Speed and Level constraints  =========== "  )

        ''' M suivi de 3 chiffres pour une vitesse exprimée en nombre de Mach (exemple : M078). '''
        strRoute = 'ADEP/LFBO-TOU-ALIVA-FISTO-LMG-M078-PD02-AMB-AMB01-AMB02-PD03-PD04-OLW11-OLW83-ADES/LFPO'
        flightPlan = FlightPlan(strRoute)
        print ( flightPlan )
        
    def test_main_eleven(self):
        
        print ( "=========== Test Speed and Level constraints  =========== "  )

        ''' F suivi de 3 chiffres : niveau de vol (exemple : F080) '''
        strRoute = 'ADEP/LFBO-TOU-ALIVA-N0250F080-FISTO-LMG-PD01-PD02-AMB-AMB01-AMB02-PD03-PD04-OLW11-OLW83-ADES/LFPO'
        flightPlan = FlightPlan(strRoute)
        print ( flightPlan )
        
        ''' A suivi de 3 chiffres : altitude en centaines de pieds (exemple : A100 pour 10 000 ft), '''

    def test_main_twelve(self):
        
        print ( "=========== Test Speed and Level constraints  =========== " )

        ''' F suivi de 3 chiffres : niveau de vol (exemple : F080) '''
        strRoute = 'ADEP/LFBO-TOU-ALIVA-N0250F280-FISTO-LMG-MEDAL-OLW11-OLW83-ADES/LFPO'
        flightPlan = FlightPlan(strRoute)
        print ( flightPlan )
        
        ''' A suivi de 3 chiffres : altitude en centaines de pieds (exemple : A100 pour 10 000 ft), '''
        
    def test_main_thirteen(self):
        
        print ( "=========== Test Speed and Level constraints  =========== " )

        ''' F suivi de 3 chiffres : niveau de vol (exemple : F080) '''
        strRoute = 'ADEP/LFBO-TOU-ALIVA-M082A100-FISTO-LMG-MEDAL-OLW11-OLW83-ADES/LFPO'
        flightPlan = FlightPlan(strRoute)
        print ( flightPlan )
        
        ''' A suivi de 3 chiffres : altitude en centaines de pieds (exemple : A100 pour 10 000 ft), '''
    
if __name__ == '__main__':
    unittest.main()
