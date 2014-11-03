import os
import datetime
import download

def main():
    range = getUpdateRange()
    download.grabDateRange(range, 'data')
    database = getDatabase()
    updateDatabase(database)

def getUpdateRange():
	