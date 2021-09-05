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
        self.ColumnNames = ["WayPoint", "Country", "Type", "Latitude", "Longitude" , "Name"]
        self.sheetName = "WayPoints"


    def insertWayPoint(self, wayPointName, Latitude, Longitude):
        
        assert isinstance(wayPointName, (str)) and len(wayPointName)>0
        assert isinstance(Latitude, (str)) and len(Latitude)>0
        assert isinstance(Longitude, (str)) and len(Longitude)>0
        
        wayPoint = {}
        wayPoint[self.ColumnNames[0]] = wayPointName
        wayPoint[self.ColumnNames[1]] = "Unknown"
        wayPoint[self.ColumnNames[2]] = "WayPoint"
        wayPoint[self.ColumnNames[3]] = Latitude
        wayPoint[self.ColumnNames[4]] = Longitude
        wayPoint[self.ColumnNames[5]] = "Unknown Name"
        
        df = pd.DataFrame(wayPoint, index=[0])
        
        if os.path.exists(self.FilePath):
            df_source = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName))
            if df_source is not None:
                df = df_source.append(df)
                
        df.to_excel(excel_writer=self.FilePath, sheet_name="WayPoints", index = False, columns=self.ColumnNames)
        

    def hasDuplicates(self):
        if os.path.exists(self.FilePath):
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName))
            if df is not None:
                df_dupes = df.df.duplicated()
                if ( df_dupes is None ):
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False
    
    
    def getNumberOfRows(self):
        if os.path.exists(self.FilePath):
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName))
            return df.shape[0]
        else:
            return 0
    
    
    def dropDuplicates(self):
        
        if os.path.exists(self.FilePath):
            
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName))
            df = df.drop_duplicates()
            
            os.remove(self.FilePath)
            df.to_excel(excel_writer=self.FilePath, sheet_name="WayPoints", index = False, columns=self.ColumnNames)
            return True
        else:
            return False

