"""Get all of the unique categories of crime that are in the database and print them. This was necessitated by the presence of 'sensitive' crimes in the database. A consequence of how accurate Google's geocoding APIs are is that crimes like "family violence" are being plotted directly on top of homes in neighborhoods. While this data shouldn't be hidden, I am considering making it slightly harder for someone to use the map to discover, say, exactly which of their neighbors have family issues, or who has had to call the police because their stalker filed a restraining order."""

import settings
from database import Database

def main():
    DB = Database(settings.DATABASE_FILE_LOC)
    categories = getUniqueCategories(DB)
    categoriesList = []

    while len(categories) != 0:
        categoriesList.append(categories.pop())

    categoriesList.sort()
    
    for category in categoriesList:
        print(category)

def getUniqueCategories(DB):
    uniqueCategories = set()

    for i in range(len(DB)):
        crime = DB.getID(i)
        categories = crime['Offense(s)'].split('|||')
        for category in categories:
            uniqueCategories.add(category)

    return uniqueCategories

if __name__ == '__main__': main()
