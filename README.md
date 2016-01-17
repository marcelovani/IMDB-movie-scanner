# IMDB-movie-scanner
====================
Python script that scans local folders and updates meta data and cover photos. It can
send the film info to a CMS using an End point.

Requires IMDBPY
https://github.com/alberanid/imdbpy

Installation
============
- Download IMDBPY inside a folder called imdbpy. It's advisable to place this folder as a sibbling of IMDB-movie-scanner
- Go inside the folder and run: sudo ./setup.py [folder]
  The parameter folder defines where to scan your movies from

- Go inside IMDB Movie Scanner folder and run: sudo ./setup.py install
The installation will create a file called config.ini which you can edit and customize your options

Usage
========
Go inside IMDB-movie-scanner folder and run: ./scan.py -f [folder] -o [new/all]
  Parameters:
    -f: Optional folder, if not provided, it will use the folder in config.ini
    -o: new -> will only scan new films. It knows its new if there is not a Summary.txt file on the folder
        all -> will scan all films
