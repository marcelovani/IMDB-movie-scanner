# IMDB-movie-scanner
Python script that scans local folders and updates meta data and cover photos. It can
send the film info to a CMS using an End point.

Requires IMDBPY
https://github.com/alberanid/imdbpy

Installation
- Download IMDBPY
- Go inside the folder
- run: sudo ./setup.py
- Go inside IMDB Movie Scanner
- run: sudo ./setup.py
- Edit config.ini
  - Set your movies folder

Using it
run: ./scan.py [folder]
  - The parameter folder is optional, if blank, it will use the folder in config.ini

