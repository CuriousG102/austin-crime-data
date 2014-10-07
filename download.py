import requests
import datetime
import os.path

def main(): # the function main in this module should only need to be run once
            # after this we can simply add to our collection as necessary
    RANGE = datetime.timedelta(days = 551) # How far back APD's database
                                           # goes from the present day
    present = datetime.date.today()
    past = present - RANGE                 # Lower bound (inclusive) of
                                           # range of dates to retrieve from
                                           # APD's database

    MAX_INCREMENT_ALLOWED = datetime.timedelta(days = 6)
                              # The max number of days APD allows us to grab
                              # at once

    dateRange = [past, past + MAX_INCREMENT_ALLOWED]

    while dateRange[1] <= present:
        grabDateRange(dateRange,\
                      path = '/Users/miles/Desktop/DT\ Web/police_scrape/')
        dateRange[0] += MAX_INCREMENT_ALLOWED
        dateRange[1] ++ MAX_INCREMENT_ALLOWED

    if dateRange[0] <= present:
        dateRange[1] = present
        grabDateRange(dateRange, \
                      path = '/Users/miles/Desktop/DT\ Web/police_scrape/')
}
    
