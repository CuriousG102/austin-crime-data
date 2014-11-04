import os
import datetime

import download
from database import Database
import process
import settings

def main():
    update()

def update():
    range_ = getUpdateRange()
    download.grabDateRange(range_, settings.PATH_TO_DATA)
    DATABASE = Database(settings.DATABASE_FILE_LOC)
    updateDatabase(range_, DATABASE)
    DATABASE.close()

def getUpdateRange():
    PATH_TO_DATA = os.path.join(settings.PATH_TO_DATA, 'AVIATION')
    ONE_DAY = datetime.timedelta(days = 1) 	
    mostRecentDate = datetime.date.min
    for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
        for f in filenames:
            if not f.startswith('.'):	    
                DATE_FORMAT = "%Y-%m-%d" 
                date = datetime.datetime.strptime(f, DATE_FORMAT).date()
                if mostRecentDate < date:
                    mostRecentDate = date
     
    present = datetime.date.today() - datetime.timedelta(days = settings.DAYS_BACK) 
    past = mostRecentDate + ONE_DAY
    
    return [past, present]

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
