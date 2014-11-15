import os

# File of constants to be used in every other part of the program

# If you do not have an existing path or file, one will be provided for you
# There is no need to make your own folders before the program runs

# Where your folder containing all the html pages needed to build a database will reside
PATH_TO_DATA = 'data'

#Your csv file
DATABASE_FILE_LOC = os.path.join('database', 'db.csv')

# How close to present day your program tries to grab crimes.
# Note that currently this program will only grab crimes for a date once
# The closer to present, the riskier your decision. You are running the
# risk that crimes have not been posted yet
# A value of 1 is equivalent to saying "grab everything up to and including yesterday"

DAYS_BACK = 14

# This is my key. You'll need to get your own at
# console.developers.google.com ;-). Make sure you enable the Geocoding API
GOOGLE_API_KEY = 'AIzaSyAD8Qj2Sz4XLzM1xFAJEnWtE3_vc9NGQuw'
