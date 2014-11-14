##Download
- [x] write script to automatically download most recent pages that aren't already in data/
- [ ] add capacity to download utpd pdf

##Database
- [ ] Change code in add and modify so that add simply calls modify and there is no duplicated logic

##Process
- [X] fix id bug
- [X] write code to process the first crime on each page
- [ ] create mySql database class
- [ ] add capacity to process utpd pdf for crimes

##Display
- [ ] generate abstract plan for data display on a static image (that can eventually be scaled to an interactive)
- [ ] generate abstract plan for using OpenStreetMaps, javascript slippy maps, to display crimes. May be drupal specific.

##Update
- [x] Broke cross-platform compatibility checking for hidden files. If a windows directory has a hidden file the program will fail. Needs fix.

##Other Tasks
- [ ] create unit tests

##Geocode
- [ ] write code to get lat long for as many locations as possible every day, starting with the most recent days and working back

##Webpage
- [ ] write code for people to filter crimes by different criteria
- [ ] do not display and do not provide option to display certain crimes like domestic disputes

