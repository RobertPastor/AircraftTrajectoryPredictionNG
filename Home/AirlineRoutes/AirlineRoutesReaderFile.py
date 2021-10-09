'''
Created on 9 oct. 2021

@author: robert

Read all AirlineRoute XLS files starting with AirlineRoute prefix

'''
import os


class AirlineRoutesReader(object):

    def __init__(self):
        
        self.className = self.__class__.__name__
        self.FileNamePrefix = "AirlineRoute"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FilePath)
        print ( self.className + ': file path= {0}'.format(self.FilePath) )
