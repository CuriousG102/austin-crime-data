import os
import ctypes
from collections import deque
import time
import re

from bs4 import BeautifulSoup

from database import Database
import settings

def main():
    PATH_TO_DATA = settings.PATH_TO_DATA 
    DATABASE = Database(settings.DATABASE_FILE_LOC)

    for dirpath, dirnames, filenames in os.walk(PATH_TO_DATA):
        for f in filenames:
            fName = os.path.join(dirpath, f)
            if not is_hidden(fName):
                process(fName, DATABASE)

    DATABASE.close()

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

def process(fName, database):
    startTime = time.time()
    with open(fName) as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        if not soup.find_all(text = 
        re.compile('You may have selected mutually exclusive criteria')):
            tables = soup.find_all(name = 'table', recursive = False)
            table = tables[0]
            crime = getFirstCrimeData(table) # Ridiculously ugly edge case:
                                             # The first crime on each page is
                                             # listed differently.
            database.add(crime)
            for i in range(1, len(tables), 2):
                table = tables[i]
                crime = getData(table)
                database.add(crime)
    
    timeTaken = time.time() - startTime
    print("Processed " + fName + " in " + str(timeTaken))

def getFirstCrimeData(table):
    crime = {}
    
    position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 0), ('td', 1)]
    crime['Report Number'] = getInfo(traverseToTag(position, table)).strip()
    position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 0), ('td', 3)]
    crime['Report Date/Time'] = getInfo(traverseToTag(position, table)).strip() 
    position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 2), ('td', 1)]
    crime['Offense Date/Time'] = getInfo(traverseToTag(position, 
                                                       table)).strip()
    position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 4), ('td', 1)]
    offenses = traverseToTag(position, table)
    offenseList = ''
    for offense in offenses.find_all(name = 'table', recursive = False):
        offenseList += getInfo(traverseToTag([('tr', 0), ('td', 0)],
                                              offense)).strip() + "|||"
    crime['Offense(s)'] = offenseList
    position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 6), ('td', 1)]
    crime['Offense Location Address'] = str(getInfo(traverseToTag(position, 
                                                              table))).strip()
    position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 7), ('td', 1)]
    crime['Offense Location Census Tract'] = str(traverseToTag(position, table).find_all(text = True)[1][2:]).strip()
    position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 7), ('td', 1)]
    crime['Offense Location District'] = str(traverseToTag(position, table).find_all(text = True)[3][2:]).strip()
    position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 7), ('td', 1)]
    crime['Offense Location Area Command'] = str(traverseToTag(position, table).find_all(text = True)[5][2:]).strip()

    position = [('tr', 0), ('td', 0), ('table', 0), ('tr', 9), ('td', 1)]
    crime['Investigator Assigned'] = getInfo(traverseToTag(position, 
                                                           table)).strip()
   
    return crime 


def getData(table): # ugly hack-ish code. IF you have a more elegant
                    # solution, please go for it and put this thing out
                    # of its misery. (Big O must still be same or lower)
    crime = {}
    
    position = [('tr', 0), ('td', 1)]
    crime['Report Number'] = getInfo(traverseToTag(position, table)).strip()
    position = [('tr', 0), ('td', 3)]
    crime['Report Date/Time'] = getInfo(traverseToTag(position, table)).strip()
    position = [('tr', 2), ('td', 1)]
    crime['Offense Date/Time'] = getInfo(traverseToTag(position, 
                                                       table)).strip()

    position = [('tr', 4), ('td', 1)]
    offenses = traverseToTag(position, table)
    offenseList = ''
    for offense in offenses.find_all(name = 'table', recursive = False):
        offenseList += getInfo(traverseToTag([('tr', 0), ('td', 0)],
                                              offense)).strip() + "|||"
    crime['Offense(s)'] = offenseList
    position = [('tr', 6), ('td', 1)]
    crime['Offense Location Address'] = str(getInfo(traverseToTag(position, 
                                                              table))).strip()
    position = [('tr', 7), ('td', 1)]
    crime['Offense Location Census Tract'] = str(traverseToTag(position, table).find_all(text = True)[1][2:]).strip()
    position = [('tr', 7), ('td', 1)]
    crime['Offense Location District'] = str(traverseToTag(position, table).find_all(text = True)[3][2:]).strip()
    position = [('tr', 7), ('td', 1)]
    crime['Offense Location Area Command'] = str(traverseToTag(position, table).find_all(text = True)[5][2:]).strip()

    position = [('tr', 9), ('td', 1)]
    crime['Investigator Assigned'] = getInfo(traverseToTag(position, 
                                                           table)).strip()
   
    return crime

def getTag(tagToSearch, tagToFind, num):
	return tagToSearch.find_all(name = tagToFind, recursive = False)[num]

def traverseToTag(tagList, rootTag):
	return traverseToTagb(deque(tagList), rootTag)

def traverseToTagb(tagList, rootTag):
	if len(tagList) <= 0:
		return rootTag
	
	item = tagList.popleft()

	tagToFind = item[0]
	numTag = item[1]

	return traverseToTagb(tagList, getTag(rootTag, tagToFind, numTag))

def getInfo(tag):
	return str(tag.find_all(text = True)[0])

if __name__ == '__main__':
    main()
