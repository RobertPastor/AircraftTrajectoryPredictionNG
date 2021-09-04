'''
Created on 4 sept. 2021

@author: robert

This class manages the ordered list of wayPoints of one route
'''
import os
import time
import unittest
import pandas as pd


class AirlineRoutes(object):
    
    FilesFolder = ""
    FileName = ""
    FilePath = ""
    ColumnNames = [ "order" , "wayPoint"]
    
    def __init__(self):
        self.className = self.__class__.__name__

        route_KATL_PHNL = [{'Name': 'BNA', 'latitude': 'N36°08\'13.05"', 'longitude': 'W086°41\'05.17"'}, {'Name': 'PLESS', 'latitude': 'N37°48\'34.48"', 'longitude': 'W088°57\'47.48"'}, {'Name': 'STL', 'latitude': 'N38°51\'38.48"', 'longitude': 'W090°28\'56.52"'}, {'Name': 'TWAIN', 'latitude': 'N39°40\'20.55"', 'longitude': 'W091°26\'35.13"'}, {'Name': 'COLIE', 'latitude': 'N40°16\'50.12"', 'longitude': 'W092°11\'01.93"'}, {'Name': 'SKBOZ', 'latitude': 'N40°34\'52.20"', 'longitude': 'W092°33\'26.15"'}, {'Name': 'CHASY', 'latitude': 'N40°41\'38.25"', 'longitude': 'W092°41\'55.11"'}, {'Name': 'JAVAS', 'latitude': 'N40°45\'56.25"', 'longitude': 'W092°47\'19.80"'}, {'Name': 'DSM', 'latitude': 'N41°26\'15.44"', 'longitude': 'W093°38\'54.80"'}, {'Name': 'EYHUX', 'latitude': 'N42°26\'08.02"', 'longitude': 'W095°01\'09.77"'}, {'Name': 'FSD', 'latitude': 'N43°38\'58.16"', 'longitude': 'W096°46\'52.05"'}, {'Name': 'ABR', 'latitude': 'N45°25\'02.47"', 'longitude': 'W098°22\'07.39"'}, {'Name': 'MUNEF', 'latitude': 'N45°41\'21.22"', 'longitude': 'W098°49\'04.75"'}, {'Name': 'IRIWY', 'latitude': 'N46°03\'11.72"', 'longitude': 'W099°25\'52.63"'}, {'Name': 'WISEK', 'latitude': 'N46°22\'49.35"', 'longitude': 'W099°59\'38.99"'}, {'Name': 'MOFIT', 'latitude': 'N46°33\'01.37"', 'longitude': 'W100°17\'28.81"'}, {'Name': 'BIS', 'latitude': 'N46°45\'42.34"', 'longitude': 'W100°39\'55.46"'}, {'Name': 'FIKAG', 'latitude': 'N46°55\'20.20"', 'longitude': 'W100°43\'48.91"'}, {'Name': 'WILTN', 'latitude': 'N47°04\'58.09"', 'longitude': 'W100°47\'43.84"'}, {'Name': 'WASHR', 'latitude': 'N47°18\'26.68"', 'longitude': 'W100°53\'15.50"'}, {'Name': 'TERTL', 'latitude': 'N47°34\'16.39"', 'longitude': 'W100°59\'47.62"'}, {'Name': 'HIDEL', 'latitude': 'N48°01\'45.05"', 'longitude': 'W101°11\'19.40"'}, {'Name': 'PABIC', 'latitude': 'N48°03\'07.54"', 'longitude': 'W101°11\'54.34"'}, {'Name': 'MOT', 'latitude': 'N48°15\'37.20"', 'longitude': 'W101°17\'13.44"'}, {'Name': 'VLN', 'latitude': 'N50°40\'01.22"', 'longitude': 'W104°53\'22.96"'}, {'Name': 'SEFFY', 'latitude': 'N51°23\'24.47"', 'longitude': 'W107°08\'15.94"'}, {'Name': 'FUDGY', 'latitude': 'N52°13\'07.50"', 'longitude': 'W110°00\'00.00"'}, {'Name': 'OMROD', 'latitude': 'N53°00\'20.11"', 'longitude': 'W113°05\'35.92"'}, {'Name': 'YEG', 'latitude': 'N53°11\'08.09"', 'longitude': 'W113°52\'00.62"'}, {'Name': 'WYLDE', 'latitude': 'N53°36\'52.20"', 'longitude': 'W114°53\'38.40"'}, {'Name': 'YQU', 'latitude': 'N55°10\'27.15"', 'longitude': 'W119°01\'48.74"'}, {'Name': 'ELTEX', 'latitude': 'N56°53\'57.14"', 'longitude': 'W125°00\'00.00"'}, {'Name': 'KEVPO', 'latitude': 'N58°01\'36.32"', 'longitude': 'W130°00\'00.00"'}, {'Name': 'MITOM', 'latitude': 'N58°19\'14.70"', 'longitude': 'W131°32\'02.90"'}, {'Name': 'DEEJA', 'latitude': 'N58°54\'08.00"', 'longitude': 'W135°00\'00.00"'}, {'Name': 'YAK', 'latitude': 'N59°30\'38.98"', 'longitude': 'W139°38\'53.27"'}, {'Name': 'MDO', 'latitude': 'N59°25\'18.49"', 'longitude': 'W146°21\'00.05"'}, {'Name': 'WUXAN', 'latitude': 'N59°53\'00.00"', 'longitude': 'W149°00\'00.00"'}, {'Name': 'HOM', 'latitude': 'N59°42\'33.94"', 'longitude': 'W151°27\'23.75"'}, {'Name': 'ELDOH', 'latitude': 'N59°36\'35.01"', 'longitude': 'W152°03\'58.25"'}, {'Name': 'AUGEY', 'latitude': 'N59°28\'10.96"', 'longitude': 'W152°53\'19.40"'}, {'Name': 'BATTY', 'latitude': 'N59°03\'56.60"', 'longitude': 'W155°04\'41.86"'}, {'Name': 'OSKOE', 'latitude': 'N58°47\'13.64"', 'longitude': 'W156°27\'22.24"'}, {'Name': 'AKN', 'latitude': 'N58°43\'28.96"', 'longitude': 'W156°45\'08.44"'}, {'Name': 'EXIPE', 'latitude': 'N58°43\'36.42"', 'longitude': 'W157°04\'19.23"'}, {'Name': 'DAJOB', 'latitude': 'N58°43\'42.72"', 'longitude': 'W157°40\'37.69"'}, {'Name': 'EHM', 'latitude': 'N58°39\'24.42"', 'longitude': 'W162°04\'17.16"'}, {'Name': 'SPY', 'latitude': 'N57°09\'25.19"', 'longitude': 'W170°13\'58.77"'}, {'Name': 'CREMR', 'latitude': 'N56°54\'51.20"', 'longitude': 'W173°52\'08.20"'}, {'Name': 'PIPPA', 'latitude': 'N56°43\'02.00"', 'longitude': 'W176°18\'26.00"'}, {'Name': 'ONEIL', 'latitude': 'N54°12\'08.80"', 'longitude': 'E172°40\'50.90"'}, {'Name': 'NYMPH', 'latitude': 'N53°24\'31.60"', 'longitude': 'E168°14\'23.40"'}, {'Name': 'NUZAN', 'latitude': 'N51°39\'27.50"', 'longitude': 'E163°38\'41.80"'}, {'Name': 'NRKEY', 'latitude': 'N50°12\'25.00"', 'longitude': 'E160°22\'39.00"'}, {'Name': 'NIPPI', 'latitude': 'N49°42\'38.40"', 'longitude': 'E159°20\'48.30"'}, {'Name': 'NOGAL', 'latitude': 'N46°13\'00.00"', 'longitude': 'E153°00\'12.01"'}, {'Name': 'NUBDA', 'latitude': 'N42°23\'27.78"', 'longitude': 'E147°28\'32.74"'}, {'Name': 'NANNO', 'latitude': 'N41°54\'57.90"', 'longitude': 'E146°51\'33.04"'}, {'Name': 'NODAN', 'latitude': 'N40°25\'10.29"', 'longitude': 'E144°59\'45.93"'}, {'Name': 'NANAC', 'latitude': 'N38°54\'22.70"', 'longitude': 'E143°13\'40.77"'}, {'Name': 'KAGIS', 'latitude': 'N35°49\'12.89"', 'longitude': 'E142°33\'48.50"'}, {'Name': 'ONASU', 'latitude': 'N34°44\'22.87"', 'longitude': 'E140°40\'44.32"'}, {'Name': 'MOE', 'latitude': 'N34°04\'15.75"', 'longitude': 'E139°33\'40.64"'}, {'Name': 'KARTA', 'latitude': 'N33°11\'35.56"', 'longitude': 'E138°58\'20.63"'}, {'Name': 'YOSHI', 'latitude': 'N33°10\'14.59"', 'longitude': 'E138°57\'26.94"'}, {'Name': 'MAPDO', 'latitude': 'N32°36\'48.78"', 'longitude': 'E138°38\'43.10"'}, {'Name': 'TAXON', 'latitude': 'N30°00\'13.67"', 'longitude': 'E137°14\'19.81"'}, {'Name': 'ASEDA', 'latitude': 'N25°00\'15.62"', 'longitude': 'E139°09\'31.73"'}, {'Name': 'MONPI', 'latitude': 'N21°00\'00.00"', 'longitude': 'E140°36\'00.00"'}, {'Name': 'RICHH', 'latitude': 'N17°11\'49.00"', 'longitude': 'E142°49\'12.00"'}, {'Name': 'REEDE', 'latitude': 'N14°57\'00.00"', 'longitude': 'E143°59\'00.00"'}, {'Name': 'UNZ', 'latitude': 'N13°27\'16.40"', 'longitude': 'E144°43\'59.90"'}, {'Name': 'JUNIE', 'latitude': 'N11°32\'50.64"', 'longitude': 'E147°06\'28.51"'}, {'Name': 'GUNSS', 'latitude': 'N10°43\'54.00"', 'longitude': 'E148°03\'54.00"'}, {'Name': 'TKK', 'latitude': 'N07°27\'25.00"', 'longitude': 'E151°50\'25.00"'}, {'Name': 'BIRUQ', 'latitude': 'N07°01\'23.32"', 'longitude': 'E157°42\'03.29"'}, {'Name': 'PNI', 'latitude': 'N06°58\'56.00"', 'longitude': 'E158°12\'07.00"'}, {'Name': 'HAVNU', 'latitude': 'N07°04\'31.07"', 'longitude': 'E158°41\'44.61"'}, {'Name': 'LOOIS', 'latitude': 'N08°12\'06.00"', 'longitude': 'E164°44\'54.00"'}, {'Name': 'NDJ', 'latitude': 'N08°43\'15.00"', 'longitude': 'E167°43\'39.00"'}, {'Name': 'CURCH', 'latitude': 'N08°17\'35.00"', 'longitude': 'E168°39\'08.00"'}, {'Name': 'MAJ', 'latitude': 'N07°04\'00.00"', 'longitude': 'E171°16\'42.00"'}, {'Name': 'MAZZA', 'latitude': 'N11°42\'32.00"', 'longitude': 'W180°00\'00.00"'}, {'Name': 'MANRE', 'latitude': 'N15°55\'50.00"', 'longitude': 'W171°33\'23.00"'}, {'Name': 'MCFLY', 'latitude': 'N19°39\'29.00"', 'longitude': 'W162°41\'58.00"'}, {'Name': 'CHOKO', 'latitude': 'N20°22\'38.44"', 'longitude': 'W160°52\'59.15"'}]

        route_KJFK_KSEA = [{'Name': 'SAX', 'latitude': 'N41°04\'03.15"', 'longitude': 'W074°32\'17.92"'}, {'Name': 'COATE', 'latitude': 'N41°08\'10.42"', 'longitude': 'W074°41\'42.60"'}, {'Name': 'LAAYK', 'latitude': 'N41°28\'32.64"', 'longitude': 'W075°28\'57.31"'}, {'Name': 'YYOST', 'latitude': 'N41°34\'57.78"', 'longitude': 'W075°51\'21.05"'}, {'Name': 'DGRAF', 'latitude': 'N41°41\'10.52"', 'longitude': 'W076°13\'21.15"'}, {'Name': 'MTCAF', 'latitude': 'N41°46\'11.34"', 'longitude': 'W076°31\'20.58"'}, {'Name': 'REBBL', 'latitude': 'N41°52\'57.63"', 'longitude': 'W076°55\'58.06"'}, {'Name': 'REXXY', 'latitude': 'N42°00\'39.83"', 'longitude': 'W077°24\'34.97"'}, {'Name': 'HERBA', 'latitude': 'N42°14\'35.29"', 'longitude': 'W078°16\'27.84"'}, {'Name': 'RAAKK', 'latitude': 'N42°23\'59.00"', 'longitude': 'W078°54\'39.00"'}, {'Name': 'FARGN', 'latitude': 'N42°36\'42.19"', 'longitude': 'W079°47\'18.42"'}, {'Name': 'ICHOL', 'latitude': 'N42°38\'31.46"', 'longitude': 'W080°30\'13.99"'}, {'Name': 'JAAJA', 'latitude': 'N42°40\'00.00"', 'longitude': 'W081°16\'00.00"'}, {'Name': 'TWIGS', 'latitude': 'N42°48\'34.10"', 'longitude': 'W082°33\'10.30"'}, {'Name': 'BERYS', 'latitude': 'N42°54\'33.97"', 'longitude': 'W083°17\'59.75"'}, {'Name': 'FNT', 'latitude': 'N42°58\'00.38"', 'longitude': 'W083°44\'49.08"'}, {'Name': 'MONEE', 'latitude': 'N43°14\'25.80"', 'longitude': 'W084°27\'50.95"'}, {'Name': 'GRB', 'latitude': 'N44°33\'18.57"', 'longitude': 'W088°11\'41.48"'}, {'Name': 'TWINZ', 'latitude': 'N45°02\'55.67"', 'longitude': 'W092°17\'21.64"'}, {'Name': 'GEP', 'latitude': 'N45°08\'44.46"', 'longitude': 'W093°22\'23.45"'}, {'Name': 'ABR', 'latitude': 'N45°25\'02.47"', 'longitude': 'W098°22\'07.39"'}, {'Name': 'MLS', 'latitude': 'N46°22\'56.00"', 'longitude': 'W105°57\'12.72"'}, {'Name': 'ISAME', 'latitude': 'N46°25\'43.25"', 'longitude': 'W106°11\'05.39"'}, {'Name': 'ESTRO', 'latitude': 'N46°57\'09.42"', 'longitude': 'W109°00\'37.65"'}, {'Name': 'LWT', 'latitude': 'N47°03\'10.69"', 'longitude': 'W109°36\'22.20"'}, {'Name': 'MLP', 'latitude': 'N47°27\'24.85"', 'longitude': 'W115°38\'45.76"'}]

        route_PANC_KATL = [{'Name': 'YESKA', 'latitude': 'N61°00\'00.78"', 'longitude': 'W149°20\'01.84"'}, {'Name': 'REMBY', 'latitude': 'N60°40\'00.00"', 'longitude': 'W146°00\'00.00"'}, {'Name': 'COHIL', 'latitude': 'N60°06\'31.00"', 'longitude': 'W139°00\'00.00"'}, {'Name': 'GOROV', 'latitude': 'N59°18\'21.10"', 'longitude': 'W133°00\'02.80"'}, {'Name': 'OMLOK', 'latitude': 'N58°46\'45.59"', 'longitude': 'W130°00\'00.00"'}, {'Name': 'BINGA', 'latitude': 'N57°42\'07.09"', 'longitude': 'W125°00\'00.00"'}, {'Name': 'LEPET', 'latitude': 'N56°25\'35.90"', 'longitude': 'W120°16\'15.72"'}, {'Name': 'NUBEG', 'latitude': 'N54°16\'51.69"', 'longitude': 'W113°59\'03.32"'}, {'Name': 'YWV', 'latitude': 'N52°58\'53.00"', 'longitude': 'W110°49\'59.79"'}, {'Name': 'VLN', 'latitude': 'N50°40\'01.22"', 'longitude': 'W104°53\'22.96"'}, {'Name': 'MOT', 'latitude': 'N48°15\'37.20"', 'longitude': 'W101°17\'13.44"'}, {'Name': 'PABIC', 'latitude': 'N48°03\'07.54"', 'longitude': 'W101°11\'54.34"'}, {'Name': 'HIDEL', 'latitude': 'N48°01\'45.05"', 'longitude': 'W101°11\'19.40"'}, {'Name': 'TERTL', 'latitude': 'N47°34\'16.39"', 'longitude': 'W100°59\'47.62"'}, {'Name': 'WASHR', 'latitude': 'N47°18\'26.68"', 'longitude': 'W100°53\'15.50"'}, {'Name': 'WILTN', 'latitude': 'N47°04\'58.09"', 'longitude': 'W100°47\'43.84"'}, {'Name': 'FIKAG', 'latitude': 'N46°55\'20.20"', 'longitude': 'W100°43\'48.91"'}, {'Name': 'BIS', 'latitude': 'N46°45\'42.34"', 'longitude': 'W100°39\'55.46"'}, {'Name': 'MOFIT', 'latitude': 'N46°33\'01.37"', 'longitude': 'W100°17\'28.81"'}, {'Name': 'WISEK', 'latitude': 'N46°22\'49.35"', 'longitude': 'W099°59\'38.99"'}, {'Name': 'IRIWY', 'latitude': 'N46°03\'11.72"', 'longitude': 'W099°25\'52.63"'}, {'Name': 'MUNEF', 'latitude': 'N45°41\'21.22"', 'longitude': 'W098°49\'04.75"'}, {'Name': 'ABR', 'latitude': 'N45°25\'02.47"', 'longitude': 'W098°22\'07.39"'}, {'Name': 'FSD', 'latitude': 'N43°38\'58.16"', 'longitude': 'W096°46\'52.05"'}, {'Name': 'EYHUX', 'latitude': 'N42°26\'08.02"', 'longitude': 'W095°01\'09.77"'}, {'Name': 'DSM', 'latitude': 'N41°26\'15.44"', 'longitude': 'W093°38\'54.80"'}, {'Name': 'JAVAS', 'latitude': 'N40°45\'56.25"', 'longitude': 'W092°47\'19.80"'}, {'Name': 'CHASY', 'latitude': 'N40°41\'38.25"', 'longitude': 'W092°41\'55.11"'}, {'Name': 'SKBOZ', 'latitude': 'N40°34\'52.20"', 'longitude': 'W092°33\'26.15"'}, {'Name': 'COLIE', 'latitude': 'N40°16\'50.12"', 'longitude': 'W092°11\'01.93"'}, {'Name': 'TWAIN', 'latitude': 'N39°40\'20.55"', 'longitude': 'W091°26\'35.13"'}, {'Name': 'STL', 'latitude': 'N38°51\'38.48"', 'longitude': 'W090°28\'56.52"'}, {'Name': 'PLESS', 'latitude': 'N37°48\'34.48"', 'longitude': 'W088°57\'47.48"'}, {'Name': 'BNA', 'latitude': 'N36°08\'13.05"', 'longitude': 'W086°41\'05.17"'}]

        route_KATL_KLAX = [{'Name': 'VUZ', 'latitude': 'N33°40\'12.47"', 'longitude': 'W086°53\'59.41"'}, {'Name': 'YAALL', 'latitude': 'N33°47\'36.30"', 'longitude': 'W087°28\'51.23"'}, {'Name': 'XESSS', 'latitude': 'N34°18\'50.62"', 'longitude': 'W090°07\'02.78"'}, {'Name': 'CARIN', 'latitude': 'N34°27\'14.98"', 'longitude': 'W090°53\'13.05"'}, {'Name': 'ARIGY', 'latitude': 'N34°32\'07.71"', 'longitude': 'W091°20\'49.90"'}, {'Name': 'LIT', 'latitude': 'N34°40\'39.62"', 'longitude': 'W092°10\'49.90"'}, {'Name': 'KOMMA', 'latitude': 'N35°00\'52.67"', 'longitude': 'W094°40\'39.39"'}, {'Name': 'KLUBB', 'latitude': 'N35°07\'13.30"', 'longitude': 'W095°28\'00.29"'}, {'Name': 'DWINE', 'latitude': 'N35°12\'29.02"', 'longitude': 'W096°12\'58.54"'}, {'Name': 'IRW', 'latitude': 'N35°21\'30.94"', 'longitude': 'W097°36\'33.21"'}, {'Name': 'CRUSR', 'latitude': 'N35°20\'07.49"', 'longitude': 'W098°51\'58.39"'}, {'Name': 'PNH', 'latitude': 'N35°14\'06.22"', 'longitude': 'W101°41\'56.51"'}, {'Name': 'TCC', 'latitude': 'N35°10\'55.94"', 'longitude': 'W103°35\'54.89"'}, {'Name': 'ABQ', 'latitude': 'N35°02\'37.66"', 'longitude': 'W106°48\'58.72"'}, {'Name': 'ZUN', 'latitude': 'N34°57\'56.71"', 'longitude': 'W109°09\'16.23"'}, {'Name': 'PYRIT', 'latitude': 'N34°52\'10.39"', 'longitude': 'W110°30\'41.16"'}, {'Name': 'DRK', 'latitude': 'N34°42\'09.19"', 'longitude': 'W112°28\'49.24"'}, {'Name': 'HIPPI', 'latitude': 'N34°33\'44.24"', 'longitude': 'W113°38\'21.73"'}, {'Name': 'CADEZ', 'latitude': 'N34°12\'23.63"', 'longitude': 'W115°20\'34.34"'}, {'Name': 'TNP', 'latitude': 'N34°06\'44.04"', 'longitude': 'W115°46\'11.65"'}]

        self.routes = []
        self.routes.append ( { "Adep" : "KATL" , "Ades": "PHNL" , "route": route_KATL_PHNL })
        self.routes.append ( { "Adep" : "KJFK" , "Ades": "KSEA" , "route": route_KJFK_KSEA})
        self.routes.append ( { "Adep" : "PANC" , "Ades": "KATL" , "route": route_PANC_KATL})
        self.routes.append ( { "Adep" : "KATL" , "Ades": "KLAX" , "route": route_KATL_KLAX})

    
    def createRoutesFiles(self):
        
        for route in self.routes:
            
            self.FileName = "Airline-Route-" + route["Adep"] + '-' + route["Ades"] + ".xls" 
            self.FilesFolder = os.path.dirname(__file__)

            print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
            self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FileName)
            print ( self.className + ': file path= {0}'.format(self.FilePath) ) 
            
            if os.path.exists(self.FilePath):
                os.remove(self.FilePath)
            
            orderedWayPoints = []
            routeWithWayPoints = route["route"]
            index = 1
            for wayPoint in routeWithWayPoints:
                orderedWayPoint = {}
                orderedWayPoint[self.ColumnNames[0]] = str(index)
                orderedWayPoint[self.ColumnNames[1]] = wayPoint["Name"]
                orderedWayPoints.append(orderedWayPoint)
                index = index + 1
                
            df = pd.DataFrame(orderedWayPoints)
            df.to_excel(excel_writer=self.FilePath, sheet_name="WayPoints", index = False, columns=self.ColumnNames)

    
    
class TestMethods(unittest.TestCase):
#============================================
    def test_one(self):
        pass
    
        t0 = time.clock()
        print ( '================ test one =================' )
        
        airlineRoutes = AirlineRoutes()
        t1 = time.clock()
        print ( 'duration= {0} seconds'.format(t1-t0) )

        airlineRoutes.createRoutesFiles()
        
        print ( '================ test one =================' )

        t2 = time.clock()
        print ( 'duration= {0} seconds'.format(t2-t1) )
        
if __name__ == '__main__':
    unittest.main()