'''
Created on 11 sept. 2021

@author: robert
'''
import time
import unittest

from ortools.linear_solver import pywraplp
import numpy as np

from Home.AirlineRoutes.AirlineAircraftRoutesCostsDatabaseFile import AirlineAircraftRoutesCosts



class TestMethods(unittest.TestCase):
#============================================
    def test_one(self):
    
        t0 = time.clock()
        
        # Create the MIP solver with the SCIP backend.
        solver = pywraplp.Solver.CreateSolver('SCIP')
        
        airlineAircraftRoutesCosts = AirlineAircraftRoutesCosts()
        retOne = airlineAircraftRoutesCosts.read()
        self.assertTrue( retOne )
        
        costs = [
                [90, 80, 75, 70],
                [35, 85, 55, 65],
                [125, 95, 90, 95],
                [45, 110, 95, 115],
                [50, 100, 90, 100],
            ]
        num_aircrafts = len(costs)
        num_flight_legs = len(costs[0])
        
        # x[i, j] is an array of 0-1 variables, which will be 1
        # if worker i is assigned to task j.
        x = {}
        for i in range(num_aircrafts):
            for j in range(num_flight_legs):
                x[i, j] = solver.IntVar(0, 1, '')
                
                
        # Each worker is assigned to at most 1 task.
        for i in range(num_aircrafts):
            solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= 1)
        
        # Each task is assigned to exactly one worker.
        for j in range(num_flight_legs):
            solver.Add(solver.Sum([x[i, j] for i in range(num_aircrafts)]) == 1)

        objective_terms = []
        for i in range(num_aircrafts):
            for j in range(num_flight_legs):
                objective_terms.append(costs[i][j] * x[i, j])
                
                
        ''' minimize the costs '''
        solver.Minimize(solver.Sum(objective_terms))
        
        ''' invoke the solver '''
        status = solver.Solve()
        
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print('Total cost = ', solver.Objective().Value(), '\n')
            for i in range(num_aircrafts):
                for j in range(num_flight_legs):
                    # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                    if x[i, j].solution_value() > 0.5:
                        print('aircraft %d assigned to flight leg %d.  Cost = %d' %  (i, j, costs[i][j]))


        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        
        
if __name__ == '__main__':
    unittest.main()