# IMDB-movie-scanner
====================
Python script that scans local folders and updates meta data and cover photos. It can
send the film info to a CMS using an End point.

* It will only scan one movie per folder, which means, you need to create a folder for each movie.

Requires IMDBPY

Installation
============
- Download IMDBPY inside a folder called imdbpy. It's advisable to place this folder as a sibbling of IMDB-movie-scanner
  ```
  $ git clone https://github.com/alberanid/imdbpy
  ```
- Go inside the folder and run the install
  ``` 
  $ cd imdbpy
  $ sudo ./setup.py install
  ```
- Go inside IMDB Movie Scanner folder and run install
  ```
  $ cd ..
  $ cd IMDB-movie-scanner
  $ sudo ./setup.py --movies-folder /xMarcello/Development/sites/moviec/profiles/movie_catalog/modules/devel/dummy/movies-test (put your movies folder here)
  ```

The installation will create a file called config.ini which you can edit and customize your options
  Edit config.ini and change these settings to match your site domain where is says example.com
  - cms_api_url
  - cms_cron_url

Usage
========
Go inside IMDB-movie-scanner folder and run: ./scan.py -f [folder] -o [new/all]
  Parameters:
  ```
    -f: Optional folder, if not provided, it will use the folder in config.ini
    -o: new -> will only scan new films. It knows its new if there is not a Summary.txt file on the folder
        all -> will scan all films
  ```
