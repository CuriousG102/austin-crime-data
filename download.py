import datetime
import os.path
import sys

import requests

import settings
RANGE = datetime.timedelta(days = 551) # How far back APD's database
                                           # goes from the present day


def main(): # the function main in this module should only need to be run once
            # after this we can simply add to our collection as necessary
    present = datetime.date.today() - datetime.timedelta(days = settings.DAYS_BACK)
    past = present - RANGE                 # Lower bound (inclusive) of
                                           # range of dates to retrieve from
                                           # APD's database

    grabDateRange([past, present], 'data/')

def grabDateRange(dateRange, path):
    """Grabs the crime data page for days within this range(inclusive for
       both sides). Grabs data one day at a time. Allowable ranges will have
       a beginning that is 551 days before the present, and an end that is
       either the present - 1 day or earlier. The beginning will be less than the end.
       Writes this data to folders in the
       path provided. These folders mirror the available "areas" specified
       by APD.

       dateRange = [datetime.date, datetime.date]
       path = String"""

    ZERO_DAYS = datetime.timedelta(days = 0)
    ONE_DAY = datetime.timedelta(days = 1)
    AREAS = ['AVIATION', 'CENTRAL EAST', 'CENTRAL WEST', 'DOWNTOWN',
             'NORTH CENTRAL', 'NORTH EAST', 'NORTH WEST', 'OUT OF AREA',
             'SOUTH CENTRAL', 'SOUTH EAST', 'SOUTH WEST']
   
    for area in AREAS:
        begin = dateRange[0] + ZERO_DAYS
        end = dateRange[1]

        if not os.path.exists(os.path.join(path, area)):
            os.makedirs(os.path.join(path, area))

        while begin <= end:
            try:
                page = getPage(begin, area)
                with open(os.path.join(path, area, str(begin)), 'w') as f:
                    f.write(page.text)
                print("Success: " + area + " " + str(begin))
                begin += ONE_DAY
            except:
                print("Failure: " + area + " " + str(begin))
                print("Exception: " + str(sys.exc_info()[0]))
                print("Trying again")

def getPage(date, area):
    try:
        dateString = "{:02d}/{:02d}/{:04d}".format(date.month, date.day, date.year)

        QUERY = {'startdate': dateString, 'numdays': '1', 'address': '',\
                 'rucrext': '', 'tract_num': '', 'zipcode': '', 'zone': '',\
                 'district': area, 'city': '', 'choice': 'criteria',\
                 'Submit': 'Submit'}

        r = requests.post("https://www.austintexas.gov/police/reports/search2.cfm", data = QUERY)

        return r
    except:
        raise

if __name__ == '__main__': main()      
