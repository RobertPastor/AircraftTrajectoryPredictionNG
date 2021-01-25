# -*- coding: UTF-8 -*-
'''
Created on 29 december 2014

@author: PASTOR Robert
'''
import time

from Home.Environment.Atmosphere import Atmosphere
from Home.Environment.Earth import Earth

if __name__ == '__main__':

    print ( '==================== Main start ==================== '+ time.strftime("%c") )

    t0 = time.clock()
    print ( "time start= ", t0 )
    atmosphere = Atmosphere()
    earth = Earth()
    