'''
Created on 4 sept. 2021

@author: robert
WayPoints specific to the airline routes

'''
import os
import pandas as pd


class AirlineWayPointsDatabase(object):
    WayPointsDict = {}
    ColumnNames = []
    className = ''
    sheetName = ""
    
    def __init__(self):
        self.className = self.__class__.__name__
        
        self.FileName = 'AirlineWayPoints.xls'  
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FileName)
        print ( self.className + ': file path= {0}'.format(self.FilePath) )

        self.WayPointsDict = {}
        self.ColumnNames = ["Name", "latitude", "longitude"]
        self.sheetName = "WayPoints"


    def insertWayPoint(self, wayPointName, Latitude, Longitude):
        
        assert isinstance(wayPointName, (str)) and len(wayPointName)>0
        assert isinstance(Latitude, (str)) and len(Latitude)>0
        assert isinstance(Longitude, (str)) and len(Longitude)>0
        
        wayPoint = {}
        wayPoint[self.ColumnNames[0]] = wayPointName
        wayPoint[self.ColumnNames[1]] = Latitude
        wayPoint[self.ColumnNames[2]] = Longitude
        
        df = pd.DataFrame(wayPoint, index=[0])
        
        if os.path.exists(self.FilePath):
            df_source = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName))
            if df_source is not None:
                df = df_source.append(df)
                
        df.to_excel(excel_writer=self.FilePath, sheet_name="WayPoints", index = False, columns=self.ColumnNames)
        

        

