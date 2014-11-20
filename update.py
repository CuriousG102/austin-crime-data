import os
import datetime
import ctypes
import sys

import download
from database import Database
import process
import settings
import geocode

def main():
    update()

def update():
    range_ = getUpdateRange()
    download.grabDateRange(range_, settings.PATH_TO_DATA)
    DATABASE = Database(settings.DATABASE_FILE_LOC)
    updateDatabase(range_, DATABASE)
    try:
        geocode.geocodeRecentFirst(DATABASE, settings.GOOGLE_API_KEY)
    except:
        print("Geocode Error:", sys.exc_info()[0])
        DATABASE.close()
        print("Database saved: No loss of data suffered.")
    DATABASE.close()

def getUpdateRange():
    PATH_TO_DATA = os.path.join(settings.PATH_TO_DATA, 'AVIATION')
    ONE_DAY = datetime.timedelta(days = 1) 	
    mostRecentDate = datetime.date.min
    for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
        for f in filenames:
            fPath = os.path.join(dirpath, f)
            if not is_hidden(fPath):
                DATE_FORMAT = "%Y-%m-%d" 
                date = datetime.datetime.strptime(f, DATE_FORMAT).date()
                if mostRecentDate < date:
                    mostRecentDate = date
         
    present = datetime.date.today() - datetime.timedelta(days = settings.DAYS_BACK) 
    past = mostRecentDate + ONE_DAY
    
    return [past, present]

# http://stackoverflow.com/questions/284115/cross-platform-hidden-file-detection
def is_hidden(filepath):
    name = os.path.basename(os.path.abspath(filepath))
    return name.startswith('.') or has_hidden_attribute(filepath)

# http://stackoverflow.com/questions/284115/cross-platform-hidden-file-detection
def has_hidden_attribute(filepath):
    try:
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    
    return result



def updateDatabase(range_, database):
    ONE_DAY = datetime.timedelta(days = 1) 
    AREAS = ['AVIATION', 'CENTRAL EAST', 'CENTRAL WEST', 'DOWNTOWN',
             'NORTH CENTRAL', 'NORTH EAST', 'NORTH WEST', 'OUT OF AREA',
             'SOUTH CENTRAL', 'SOUTH EAST', 'SOUTH WEST']
 
    
    for area in AREAS:
        begin = range_[0]
        end = range_[1]
        while begin <= end:
            process.process(os.path.join(settings.PATH_TO_DATA, area, str(begin)), 
                            database)
            begin += ONE_DAY

if __name__ == '__main__': main()
