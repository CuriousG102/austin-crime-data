austin-crime-data
=================

A suite of tools written in python to download, process, and display crime data posted by the Austin Police Department. Push requests are welcome and will be pulled if they are well written!

The ultimate goal of this project is to have a solution which can easily be put on different server environments. This solution would be able to pull down crime data in the middle of the night (when taxing computational resources is not problematic),
put it in a database, and display that data in a meaningful and dynamic way to users.

Download:
There is a module (download.py) with functions designed to download pages from APD's website. These pages can be processed for their data and stored in a database immediately using functions and classes from process.py and database.py or saved for later.

Database:
There is a solution for sending crime data to a csv file (for easy statistical analysis by reporters in excel) and I will soon write one for sending crime data to a MySQL database (for use on website).

Display:
This is my major to-do item right now. The likely solution will be to use html and javascript to allow users to view this data on a page in an interactive map. OpenStreetMap's data is likely to be utilized in combination with some existing javascript solution.
