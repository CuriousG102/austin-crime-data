import datetime

import geopy

from database import Database
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

    geocoder = geopy.geocoders.GoogleV3(api_key = api_key_)
    
    crimes = db.getAllCrimes()
    crimes.sort(key = sortKey, reverse = True)

    crimeIndex = 0
    outOfQueries = False
    attempts = -1

    while(crimeIndex < len(crimes) and not(outOfQueries) and attempts < settings.ACCEPTABLE_GEOCODE_TIME_OUTS):
        crime = crimes[crimeIndex]
        if not('Geocoded' in crime) or crime['Geocoded'] != '1':
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
                db.modify(crime, int(crime['id']))
                print('Success Crime ID:', crime['id'])
            except geopy.exc.GeocoderQueryError:
                print('Crime ID:', crime['id'], 
                      'FAIL', 'with GeocoderQueryError')
                crimeIndex += 1
                attempts += 1
            except geopy.exc.GeocoderQuotaExceeded:
                print('Out of queries. We\'re done for today')
                outOfQueries = True
            except geopy.exc.GeocoderTimedOut:
                print('Geocode request for crime id', crime['id'],
                      'timed out at', datetime.datetime.now())
                attempts += 1
            except geopy.exc.AttributeError:
                print('Geocode request for crime id', crime['id'],
                      'failed with AttributeError. Moving to next crime.')
                attempts += 1
                crimeIndex += 1
            except:
                raise
        else:
            crimeIndex += 1
    if (not attempts < settings.ACCEPTABLE_GEOCODE_TIME_OUTS):
        print("The geocoder suffered more than your allowed settings.ACCEPTABLE_GEOCODE_TIME_OUTS: ", 
                settings.ACCEPTABLE_GEOCODE_TIME_OUTS, " and so it has been shut down.")

def sortKey(crime):
    offenseTimeString = crime['Offense Date/Time']
    offenseTimeFormat = '%a, %b-%d-%Y %H:%M'
    offenseTime = datetime.datetime.strptime(offenseTimeString,
                                             offenseTimeFormat)
    return offenseTime

if __name__ == '__main__': main()
