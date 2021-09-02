# AircraftTrajectoryPredictionNG
Port of the Aircraft Trajectory Prediction from Python 2. to Python 3.7
of 
https://github.com/RobertPastor/AircraftTrajectoryPredictor/

# required packages
numpy
xlsxwriter
xlrd

# Unit testing

There are 64 unit tests. In the Eclipse IDE, click on the project and perform right click Run Python Unit-tests

# Regression

Unfortunately, I did not have time yet to check all the results.
Hence there might regressions since the code needed some changes to adapt for Python 7.

# Further Enhancements

Implement a "french gabarit" ie a manhattan of constraints along the planned path. Constraints are speed constraints, level constraints to achieve a speed, a level, etc. before, after, on, a geo POINT.

Manage a set of Abaquus for the continuous descending phase.
Need a strategy here to decide to descent slowly from a big distance to the convergence point, or descent quickly.
Strategies are based upon : fuel consumption, time in the air opposed to crew salaries, delay in the arrival that will constraint the company to pay for passenger missing their correspondence...

# process

Please provide a pull request for any improvement. As soon as a Unit test is there with Asserts, this is OK.