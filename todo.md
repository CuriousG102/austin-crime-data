##Download
- [x] write script to automatically download most recent pages that aren't already in data/
- [ ] add capacity to download utpd pdf

##Database
- [ ] Change code in add and modify so that add simply calls modify and there is no duplicated logic
- [ ] There is a glitch in APD's site that occasionally duplicates a crime report. Write a script to go through Google Fusion Table and deduplicate (for first round of data). Write another to go through the csv table and deduplicate (for updates and future use).

##Process
- [X] fix id bug
- [ ] write code to process the first crime on each page
- [ ] create mySql database class
- [ ] add capacity to process utpd pdf for crimes

##Display
- [ ] generate abstract plan for data display on a static image (that can eventually be scaled to an interactive)
- [ ] generate abstract plan for using OpenStreetMaps, javascript slippy maps, to display crimes. May be drupal specific.

##Update
- [ ] Broke cross-platform compatibility checking for hidden files. If a windows directory has a hidden file the program will fail. Needs fix.

##Other Tasks
- [ ] create unit tests
