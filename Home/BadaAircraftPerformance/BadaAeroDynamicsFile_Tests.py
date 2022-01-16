
''' Robert PASTOR '''
from calendar import January
''' 9th January 2022 '''


import unittest
from Home.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

from Home.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance
from Home.BadaAircraftPerformance.BadaAeroDynamicsFile import AeroDynamics

class Test_Class(unittest.TestCase):

    def test_Class_One(self):
            
        print ( '================ test one ====================' )
        acBd = BadaAircraftDatabase()
        assert acBd.read()
        
        atmosphere = Atmosphere()
        earth = Earth()
        
        aircraftICAOcode = 'A320'
        if ( acBd.aircraftExists(aircraftICAOcode) and
             acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
            
            print ( acBd.getAircraftFullName(aircraftICAOcode) )
            
            aircraftPerformance = AircraftPerformance(acBd.getAircraftPerformanceFile(aircraftICAOcode))
            aeroDynamics = AeroDynamics(aircraftPerformance, atmosphere, earth)
            
            print ( aeroDynamics )
            for phase in ['CR', 'IC', 'TO', 'AP', 'LD']:
                print ( 'phase= {0} - Vstall CAS= {1} knots'.format(phase, aeroDynamics.getVstallKcas(phase)) )
                
            for phase in ['CR', 'IC', 'TO', 'AP', 'LD']:
                print ( 'phase= {0} - Drag Coeff= {1}'.format(phase, aeroDynamics.getDragCoeff(phase)) )

            print ( 'Wing Area Surface={0} Square-meters'.format(aeroDynamics.getWingAreaSurfaceSquareMeters()) )
        
        
    def test_Class_Two(self):
            
        print ( '================ test Two ====================' )
        acBd = BadaAircraftDatabase()
        assert acBd.read()
        
        atmosphere = Atmosphere()
        earth = Earth()
        
        aircraftICAOcode = 'A320'
        if ( acBd.aircraftExists(aircraftICAOcode) and
             acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
            
            print ( acBd.getAircraftFullName(aircraftICAOcode) )
            
            aircraftPerformance = AircraftPerformance(acBd.getAircraftPerformanceFile(aircraftICAOcode))
            aeroDynamics = AeroDynamics(aircraftPerformance, atmosphere, earth)
            
            print ( aeroDynamics )
            phase = 'XX'
            try:
                print ( aeroDynamics.getDragCoeff(phase) )
            except Exception as e: 
                print ( 'test two = {0}'.format(e) )
                self.assertTrue(isinstance(e, AssertionError))
            
            
if __name__ == '__main__':
    unittest.main()