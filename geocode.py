import datetime

from geopy.geocoders import GoogleV3

import settings

def main():
    DATABASE = Database(settings.DATABASE_FILE_LOC)
    geocodeRecentFirst(DATABASE, settings.GOOGLE_API_KEY)
    DATABASE.close()

def geocodeRecentFirst(db, api_key_):
    """
       Geocodes the database it is passed until you're out of queries with
       the api key passed or your database is all geocoded.
    """

    geocoder = GoogleV3(api_key = api_key_)
    
    crimes = db.getAllCrimes().sort(key = sortkey)

    crimeIndex = 0
    outOfQueries = False
    attempts = 0

    while(crimeIndex < len(crimes) and not(outOfQueries) and attempts < 4):
        crime = crimes[crimeIndex]
        if crime['Geocoded'] != '1':
            try:
                crimeQuery = crime['Offense Location Address']
                crimeLocInfo = geocoder.geocode(query = crimeQuery)
                crime['Formatted Address'] = str(crimeLocInfo.address)
                crime['Latitude'] = str(crimeLocInfo.latitude)
                crime['Longitude'] = str(crimeLocInfo.longitude)
                crime['Raw Data'] = str(crimeLocInfo.raw)
                crime['Geocoded'] = '1'
                crimeIndex += 1
                attempts = 0
                db.modify(crime, crime['id'])
                print('Success Crime ID:', crime['id'])
            except geopy.exc.GeocoderQueryError:
                print('Crime ID:', crime['id'], 
                      'FAIL', 'with GeocoderQueryError')
                crimeIndex += 1
                attempts = 0
            except geopy.exc.GeocoderQuotaExceeded:
                print('Out of queries. We\'re done for today')
                outOfQueries = True
            except geopy.exc.GeocoderTimedOut:
                print('Geocode request for crime id', crime['id'],
                      'timed out at', datetime.datetime.now())
                attempts += 1
            except:
                raise
        else:
            crimeIndex += 1

def sortKey(crime):
    offenseTimeString = crime['Offense Date/Time']
    offenseTimeFormat = '%a, %b-%d-%Y %H:%M'
    offenseTime = datetime.datetime.strptime(offenseTimeString,
                                             offenseTimeFormat)
    return offenseTime
