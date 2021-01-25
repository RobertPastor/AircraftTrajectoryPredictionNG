'''
Created on 9 February 2015

@author: PASTOR Robert
'''

Pound2Kilogram = 0.45359237

from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from Home.Guidance.FlightPathFile import FlightPath

#============================================
if __name__ == '__main__':
    
    print ( "=========== Flight Plan start  =========== " )
    acBd = BadaAircraftDatabase()
    assert acBd.read()

    strRoute = 'ADEP/LFBO-TOU-ALIVA-TOU37-FISTO-LMG-PD01-PD02-AMB-AMB01-AMB02-PD03-PD04-OLW11-OLW83-ADES/LFPO'
    acDict = {}
    acList =               ['B722' , 'B737' , 'B744' , 'B752', 'B762', 'B772', 'DC10', 'A319']
    targetCruiseLevel    = [ 330   ,  290   ,  270   ,  340  ,  350  ,  340  ,  320  ,  350  ]
    minWeightLbs =         [123240 , 108100 , 544800 , 146780, 250250 , 385100 , 316860 , 111600 ]
    maxWeightLbs = []
    
    index = 0
    for aircraftIcaoCode in acList:
        print ( aircraftIcaoCode )
        print ( 'aircraft= {0} exists= {1}'.format(aircraftIcaoCode, acBd.aircraftExists(aircraftIcaoCode)) )
        if acBd.aircraftExists(aircraftIcaoCode):
            print ( 'aircraft= {0} performance file exists= {1}'.format(aircraftIcaoCode, acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftIcaoCode))) )
        print ( 'aircraft= {0} - target cruise level= {1}'.format(aircraftIcaoCode, targetCruiseLevel[index]) )
        
        flightPath = FlightPath(route = strRoute, 
                                aircraftIcaoCode = aircraftIcaoCode,
                                RequestedFlightLevel = targetCruiseLevel[index], 
                                cruiseMach = 'use-default', 
                                takeOffMassKilograms = minWeightLbs[index] * Pound2Kilogram)
            
        flightPath.computeFlight()
        index += 1
