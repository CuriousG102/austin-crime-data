austin-crime-data
=================

A suite of tools written in python to download, process, and display crime data posted by the Austin Police Department. Pull requests are welcome and will be pulled if they are well written! See todo.md for tasks that I have identified. Contact me at mileshutson@utexas.edu for more information.

The ultimate goal of this project is to have a solution which can easily be put on different server environments. This solution would be able to pull down crime data in the middle of the night (when taxing computational resources is not problematic),
put it in a database, and display that data in a meaningful and dynamic way to users.

##Download:
There is a module (download.py) with functions designed to download pages from APD's website. These pages can be processed for their data and stored in a database immediately using functions and classes from process.py and database.py or saved for later.

##Database:
There is a solution for sending crime data to a csv file (for easy statistical analysis by reporters in excel and fusion tables) and I will soon write one for sending crime data to a MySQL database (for use on website). The highest priority on this project right now is using the google fusion tables api to automatically upload crimes with well formatted date/time information and latitude and longitudes, so that this is not a manual task. This will be done using Google's geocoding API, which allows plenty (2,500) of server-side API requests per day.

##Display:
This is my major to-do item right now. Currently, information is uploaded into a Google Fusion Table. Here, it can be geocoded and displayed on a map. Google Fusion Tables often lots of flexibility in return for very little time and programming, so there are more immediate priorities than its replacement. Eventually, I hope to replace much of Fusion Table's functionality with Open Street Maps. This will be a gradual replacement, but is necessary because of the limited ability to expand outside of functionality built into Fusion Tables. It is also gradual by necessity: Fusion Tables is the only service allowing unlimited Geocoding API requests each day. Replicating the work that it does (it hides the latitude and longitude it assigns to addresses from me) will take about 200 days for the entirety of the database using Google's server-side geocoding API ( [~466,000 entries + ~850 additional per day]/[2,500 API requests per day] )
