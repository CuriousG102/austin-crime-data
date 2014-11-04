import os
import datetime
import download
from database import Database
import process

def main():
    update()

def update():
    range_ = getUpdateRange()
    download.grabDateRange(range_, 'data')
    DATABASE = Database(os.path.join(os.getcwd(), 'database', 'db.csv'))
    updateDatabase(range_, DATABASE)
    DATABASE.close()

def getUpdateRange():
    PATH_TO_DATA = os.path.join(os.getcwd(), 'data', 'AVIATION')
    ONE_DAY = datetime.timedelta(days = 1) 	
    mostRecentDate = datetime.date.min
    for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
        for f in filenames:
            if not f.startswith('.'):	    
                DATE_FORMAT = "%Y-%m-%d" 
                date = datetime.datetime.strptime(f, DATE_FORMAT).date()
                if mostRecentDate < date:
                    mostRecentDate = date
     
    present = datetime.date.today() - ONE_DAY 
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
            process.process(os.path.join('data', area, str(begin)), 
                            database)
            begin += ONE_DAY

if __name__ == '__main__': main()
