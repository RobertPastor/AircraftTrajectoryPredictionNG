'''
Created on 11 sept. 2021

There are several constraints for the job shop problem:

No task for a job can be started until the previous task for that job is completed.
A machine can only work on one task at a time.
A task, once started, must run to completion.

@author: robert
'''
import time
import unittest

import numpy as np

import collections
from ortools.sat.python import cp_model

from Home.AirlineCosts.AirlineAircraftRoutesCostsDatabaseFile import AirlineAircraftRoutesCosts
from Home.AirlineRoutes.AirlineRoutesAirportsReader import AirlineRoutesAirportsDataBase

from Home.AirlineFleet.AirlineFleetReader import AirlineFleetDataBase
from Home.AirlineFleet.AirlineFleetReader import AirlineAircraft

from Home.AirlineTurnAroundTimes.AirlineTurnTimesFile import AirlineTurnAroundTimesDatabase

kerosene_kilo_to_US_gallons = 0.33
US_gallon_to_US_dollars = 3.25
        
class TestMethods(unittest.TestCase):
#============================================

    def computeMaxOfFlightLegDurationHours(self, flightLegDepartureArrivalAirports , airlineAircraftICAOcodeList, airlineAircraftRoutesCosts): 
        ''' compute max of duration for all aircrafts '''
        maxDurationHours = 0.0
        
        departureAirportICAOcode = str(flightLegDepartureArrivalAirports).split("-")[0]
        arrivalAirportICAOcode = str(flightLegDepartureArrivalAirports).split("-")[1]
                    
        for i in range(len(airlineAircraftICAOcodeList)):
            aircraftICAOcode = airlineAircraftICAOcodeList[i]
                    
            durationHours = airlineAircraftRoutesCosts.getFlightLegDurationInHours(aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode)

            if ( durationHours > maxDurationHours):
                maxDurationHours = durationHours
            
        print ( "Flight Leg = {0} - max Duration = {1} Hours".format( flightLegDepartureArrivalAirports , maxDurationHours))
        return maxDurationHours
    
    
    def test_two(self):
    
        t0 = time.clock()
        
        print ("-----------airline fleet aircrafts---------")
        
        airlineFleet = AirlineFleetDataBase()
        ret = airlineFleet.read()
        self.assertTrue( ret == True )
        ret = airlineFleet.extendDatabase()
        self.assertTrue( ret == True )
        
        print ("-----------airline fleet aircrafts with ICAO codes---------")

        airlineAircraftFullNameList = []
        airlineAircraftICAOcodeList = []
        airlineAircraftNumberOfSeatsList = []
        airlineAircraftInstancesList = []
        for airlineAircraft in airlineFleet.getAirlineAircrafts():
            self.assertTrue( isinstance( airlineAircraft , AirlineAircraft ) )
            if ( airlineAircraft.hasICAOcode() ):
                print ( airlineAircraft.getAircraftFullName() , "--->>>---" , airlineAircraft.getAircraftICAOcode() )
                
                aircraftICAOcode = airlineAircraft.getAircraftICAOcode()
                nbAircraftsAvailable = airlineFleet.getAircraftNumberOfInstances( aircraftICAOcode )
                for j in range(nbAircraftsAvailable):
                    ''' as there are once more than 99 aircrafts from the same type -> need to pad with 00 zeros '''
                    acInstance =  '{0}-{1}'.format( aircraftICAOcode , str(j).zfill(3)) 
                    print ( acInstance )
                    airlineAircraftInstancesList.append( acInstance )
                    airlineAircraftFullNameList.append( airlineAircraft.getAircraftFullName() )
                    airlineAircraftICAOcodeList.append( airlineAircraft.getAircraftICAOcode() )
                    airlineAircraftNumberOfSeatsList.append( airlineAircraft.getMaximumNumberOfPassengers())

        print ( "length of airline aircraft list = {0}".format( len ( airlineAircraftICAOcodeList ) ) )
        for acIndex in range(len(airlineAircraftInstancesList)):
            print ( "index= {0} - aircraft= {1}".format( acIndex, airlineAircraftInstancesList[acIndex] ) )
        
        print ("------------- airline routes reader --------------")
        airlineRoutesAirports = AirlineRoutesAirportsDataBase()
        ret = airlineRoutesAirports.read()
        self.assertTrue( ret == True )
        
        print ("------------- airline routes airports OR flight legs --------------")
        airlineFlightLegsList = []
        for route in airlineRoutesAirports.getRoutes():
            print (route)
            airlineFlightLegsList.append( route.getFlightLegAsString() )

        print ( "length of airline flight legs list = {0}".format( len ( airlineFlightLegsList ) ) )
        
        print ("-----------airline routes costs---------")

        airlineAircraftRoutesCosts = AirlineAircraftRoutesCosts()
        airlineCosts_np_array = airlineAircraftRoutesCosts.read()
        #print ( airlineCosts_np_array )
        self.assertTrue( airlineCosts_np_array is not None )

        print ("-----------flight leg duration ---------")

        turnAroundDurationHours = 0.5
        flightLegFrequency = {}
        flightLegDurationHours = {}

        for d in range(len(airlineFlightLegsList)):
            flightLegStr = airlineFlightLegsList[d]
            #print ( flightLegStr )
            flightLegDurationHours[d] = self.computeMaxOfFlightLegDurationHours(flightLegStr , airlineAircraftICAOcodeList, airlineAircraftRoutesCosts)
            flightLegFrequency[d] =  int ( 20. / ( flightLegDurationHours[d] + turnAroundDurationHours ) )
            print ( "flight leg = {0} - max flight leg duration in hours {1} - frequency for 20 hours = {2}".format( flightLegStr , flightLegDurationHours[d] , flightLegFrequency[d]) )

        print ("-------- turn around times --------")
        airlineTurnAroundTimesDatabase = AirlineTurnAroundTimesDatabase()

        print ("------- assignments ------")
        #aircraft Boeing 717-200 - ICAO code B712-000 - assigned to flight leg PANC-KATL
        #aircraft Boeing 737-800 - ICAO code B738-003 - assigned to flight leg KATL-KBOS
        #aircraft Airbus A319 - ICAO code A319-000 - assigned to flight leg KSEA-KJFK 
        #aircraft Airbus A319 - ICAO code A319-001 - assigned to flight leg KSFO-KIAD - Cost = 25518.89 US dollars for the flight duration
        #aircraft Airbus A320 - ICAO code A320-000 - assigned to flight leg KIAD-KSFO - Cost = 28759.83 US dollars for the flight duration
        #aircraft Airbus A320 - ICAO code A320-001 - assigned to flight leg KBOS-KATL - Cost = 13274.23 US dollars for the flight duration
        #aircraft Airbus A320 - ICAO code A320-002 - assigned to flight leg KLAX-KATL - Cost = 24464.15 US dollars for the flight duration

        #jobs_data = [  # task = (machine_id, processing_time).
        # #   [(0, 3), (1, 2), (2, 2)],  # Job0
        # #   [(0, 2), (2, 1), (1, 4)],  # Job1
        #    [(1, 4), (2, 3)]  # Job2
        #]
        jobs_data = []
        for acIndex in range(len(airlineAircraftInstancesList)):
            
            aircraftICAOcode = str(airlineAircraftInstancesList[acIndex]).split("-")[0]
            print ( "index= {0} - aircraft= {1} - ICAO code= {2}".format( acIndex, airlineAircraftInstancesList[acIndex] , aircraftICAOcode) )

            if ( aircraftICAOcode == "B712"):
                job = []
                flightLeg = "PANC-KATL"
                departureAirportICAOcode = str(flightLeg).split("-")[0]
                arrivalAirportICAOcode = str(flightLeg).split("-")[1]

                flightLedDurationMinutes = airlineAircraftRoutesCosts.getFlightLegDurationInMinutes(aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode)
                job.append( ( acIndex , int(flightLedDurationMinutes) ) )
                job.append( ( acIndex , int ( airlineTurnAroundTimesDatabase.getTurnAroundTimeInHours(aircraftICAOcode, departureAirportICAOcode) * 60.)) )
                
                flightLeg = "KATL-PANC"
                departureAirportICAOcode = str(flightLeg).split("-")[0]
                arrivalAirportICAOcode = str(flightLeg).split("-")[1]
                
                flightLedDurationMinutes = airlineAircraftRoutesCosts.getFlightLegDurationInMinutes(aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode)
                job.append( ( acIndex , int(flightLedDurationMinutes)) )
                print ( job )
                jobs_data.append(job)
                
            if ( aircraftICAOcode == "B738" ):
                job = []
                flightLeg = "KATL-KBOS"
                departureAirportICAOcode = str(flightLeg).split("-")[0]
                arrivalAirportICAOcode = str(flightLeg).split("-")[1]
                
                flightLedDurationMinutes = airlineAircraftRoutesCosts.getFlightLegDurationInMinutes(aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode)
                job.append( ( acIndex , int ( flightLedDurationMinutes) ) )
                job.append( ( acIndex , int ( airlineTurnAroundTimesDatabase.getTurnAroundTimeInHours(aircraftICAOcode, departureAirportICAOcode) * 60.)) )
                flightLeg = "KBOS-KATL"
                departureAirportICAOcode = str(flightLeg).split("-")[0]
                arrivalAirportICAOcode = str(flightLeg).split("-")[1]
                
                flightLedDurationMinutes = airlineAircraftRoutesCosts.getFlightLegDurationInMinutes(aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode)
                job.append( ( acIndex , int ( flightLedDurationMinutes) ) )
                print ( job )
                jobs_data.append(job)
                
            if ( aircraftICAOcode == "A319" ):
                flightLeg = "KSEA-KJFK"
                departureAirportICAOcode = str(flightLeg).split("-")[0]
                arrivalAirportICAOcode = str(flightLeg).split("-")[1]
                job = []
                flightLedDurationMinutes = airlineAircraftRoutesCosts.getFlightLegDurationInMinutes(aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode)
                job.append( ( acIndex , int ( flightLedDurationMinutes) ) )
                job.append( ( acIndex , int ( airlineTurnAroundTimesDatabase.getTurnAroundTimeInHours(aircraftICAOcode, departureAirportICAOcode) * 60.)) )
                flightLeg = "KJFK-KSEA"
                departureAirportICAOcode = str(flightLeg).split("-")[0]
                arrivalAirportICAOcode = str(flightLeg).split("-")[1]
                
                flightLedDurationMinutes = airlineAircraftRoutesCosts.getFlightLegDurationInMinutes(aircraftICAOcode, departureAirportICAOcode, arrivalAirportICAOcode)
                job.append( ( acIndex , int ( flightLedDurationMinutes) ) )
                print ( job )
                jobs_data.append(job)
 
                
        print (jobs_data)
        
        print ( " ------------- aircraft ICAO code -------------")
        for airlineAircraft in airlineFleet.getAirlineAircrafts():
            self.assertTrue( isinstance( airlineAircraft , AirlineAircraft ) )
            if ( airlineAircraft.hasICAOcode() ):
                print ( airlineAircraft.getAircraftFullName() , "--->>>---" , airlineAircraft.getAircraftICAOcode() )
                
                aircraftICAOcode = airlineAircraft.getAircraftICAOcode()
                

        machines_count = 1 + max(task[0] for job in jobs_data for task in job)
        all_machines = range(machines_count)
        print ( "machine count = {0}".format ( machines_count ))
        # Computes horizon dynamically as the sum of all durations.
        horizon = sum(task[1] for job in jobs_data for task in job)

        # Create the model.
        model = cp_model.CpModel()
    
        # Named tuple to store information about created variables.
        task_type = collections.namedtuple('task_type', 'start end interval')
        # Named tuple to manipulate solution information.
        assigned_task_type = collections.namedtuple('assigned_task_type',
                                                    'start job index duration')
    
        # Creates job intervals and add to the corresponding machine lists.
        all_tasks = {}
        machine_to_intervals = collections.defaultdict(list)

        for job_id, job in enumerate(jobs_data):
            print ("job= {0}".format(job))
            for task_id, task in enumerate(job):
                machine = task[0]
                duration = task[1]
                suffix = '_%i_%i' % (job_id, task_id)
                start_var = model.NewIntVar(0, horizon, 'start' + suffix)
                end_var = model.NewIntVar(0, horizon, 'end' + suffix)
                interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                    'interval' + suffix)
                all_tasks[job_id, task_id] = task_type(start=start_var,
                                                       end=end_var,
                                                       interval=interval_var)
                machine_to_intervals[machine].append(interval_var)

        '''  Create and add disjunctive constraints. '''
        for machine in all_machines:
            model.AddNoOverlap(machine_to_intervals[machine])
    
        ''' Precedences inside a job. '''
        for job_id, job in enumerate(jobs_data):
            for task_id in range(len(job) - 1):
                model.Add(all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end)
    
        # Makespan objective.
        obj_var = model.NewIntVar(0, horizon, 'makespan')
        model.AddMaxEquality(obj_var, [
            all_tasks[job_id, len(job) - 1].end
            for job_id, job in enumerate(jobs_data)
        ])
        model.Minimize(obj_var)

        # Creates the solver and solve.
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
    
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print('Solution:')
            # Create one list of assigned tasks per machine.
            assigned_jobs = collections.defaultdict(list)
            for job_id, job in enumerate(jobs_data):
                for task_id, task in enumerate(job):
                    machine = task[0]
                    assigned_jobs[machine].append(
                        assigned_task_type(start=solver.Value(
                            all_tasks[job_id, task_id].start),
                                           job=job_id,
                                           index=task_id,
                                           duration=task[1]))

            # Create per machine output lines.
            output = ''
            for machine in all_machines:
                # Sort by starting time.
                assigned_jobs[machine].sort()
                sol_line_tasks = 'Machine ' + str(machine) + ': '
                sol_line = '           '
    
                for assigned_task in assigned_jobs[machine]:
                    name = 'job_%i_task_%i' % (assigned_task.job,
                                               assigned_task.index)
                    # Add spaces to output to align columns.
                    sol_line_tasks += '%-15s' % name
    
                    start = assigned_task.start
                    duration = assigned_task.duration
                    sol_tmp = '[%i,%i]' % (start, start + duration)
                    # Add spaces to output to align columns.
                    sol_line += '%-15s' % sol_tmp
    
                sol_line += '\n'
                sol_line_tasks += '\n'
                output += sol_line_tasks
                output += sol_line
    
            # Finally print the solution found.
            print(f'Optimal Schedule Length: {solver.ObjectiveValue()}')
            print(output)
        else:
            print('No solution found.')

           
    
        # Statistics.
        print('\nStatistics')
        print('  - conflicts: %i' % solver.NumConflicts())
        print('  - branches : %i' % solver.NumBranches())
        print('  - wall time: %f s' % solver.WallTime())

        
        print ("------------- end --------------")

        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        
if __name__ == '__main__':
    unittest.main()
    