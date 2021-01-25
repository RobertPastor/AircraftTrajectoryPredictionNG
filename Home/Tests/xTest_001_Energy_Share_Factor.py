'''
Created on Jan 30, 2015

@author: Robert PASTOR
'''

import math

Feet2Meter = 0.3048 # 1 feet = 0.3048 meter
Meter2Feet = 3.2808399 

''' Energy Share Factor '''
def computeESF(mach):
    
    ESF1 = 1.0 + ((1.4*287.05287*(-0.0065)*mach*mach)/(2.0*9.80665)) 
    ESF2 = math.pow((1.0 + ((1.4-1.0)/2.0)*mach*mach), (-1.0/(1.4-1.0)))
    ESF3 = math.pow((1.0 + ((1.4-1.0)/2.0)*mach*mach) , (1.4/(1.4-1.0))) - 1.0
    ESF = ESF1 + ESF2 * ESF3
    ESF = math.pow(ESF, -1.0)
    return ESF


if __name__ == '__main__':

    print ( '=========== main start ==================' )
    mach = 0.6
    print ( 'mach= {0} ESF= {1}'.format(mach, computeESF(mach)) )

