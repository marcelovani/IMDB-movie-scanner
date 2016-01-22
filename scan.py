#!/usr/bin/env python

import os, sys, getopt
import pprint
import re
from config import *
from imdbc import *


def scan_movie_files(movies_folder, movie_extensions, list=[]):
    ''' Print files in movies_folder with extensions in movie_extensions, recursively. '''

    try:
       list
    except NameError:
       list = []

    # Get the absolute path of the movies_folder parameter
    movies_folder = os.path.abspath(movies_folder)

    # Get a list of files in movies_folder
    movies_folder_files = os.listdir(movies_folder)

    # Traverse through all files
    for filename in movies_folder_files:
        filepath = os.path.join(movies_folder, filename)

        # Check if it's a normal file or directory
        if os.path.isfile(filepath):

            # Check if the file has an extension of typical video files
            for movie_extension in movie_extensions:
                # Not a movie file, ignore
                if not filepath.endswith(movie_extension):
                    continue

                # Skip folders that contain summary and cover
                summary_file = os.path.join(movies_folder, "Summary.txt")
                if ( os.path.isfile(summary_file) and scan_method == 'new' ):
                    continue

                # Remove strings from the filename
                film = filename.replace('.' + movie_extension, '').lower()

                # Clean fixed strings
                film = re.sub(ur'[\W\_\.\-\(\)\[\]]+', ' ', film, flags=re.UNICODE)

                # Clear single digits if year is present
                film = re.sub(r'(\d{1}).*(\d{4})', r'\2', film)

                # Add parenthesis to year
                film = re.sub(r'(\d{4})', r'(\1)', film)

                # Remove custom strings fom the filename
                for str in eval(ignore_strings):
                    film = film.replace(str.lower(), '')

                # Remove duplicated spaces
                film = re.sub(r'(\s+)', r' ', film)

                info = {"folder": movies_folder, "keywords": film}

                list.append(info)

                scan_movie_files.list = list

                scan_movie_files.counter += 1

                # @TODO display warning if more than one film is in the folder

        elif os.path.isdir(filepath):
            # We got a directory, enter into it for further processing
            scan_movie_files(filepath, movie_extensions, list)

if __name__ == '__main__':

    movies_folder = get_config('Movies','movies_folder')
    extensions = eval(get_config('Options','file_extensions'))
    ignore_strings = get_config('Options','ignore_strings')
    verbose_level = int(get_config('Options','verbose_level'))
    scan_method = 'new'

    # Read command line args
    try:
        myopts, args = getopt.getopt(sys.argv[1:],"f:o:")
    except getopt.GetoptError as e:
        print (str(e))
        print("Usage: %s -f <folder> -o [new|all]" % sys.argv[0])
        sys.exit(2)

    for o, a in myopts:
        if o == '-f':
            movies_folder = a
        elif o == '-o':
            scan_method = a
        else:
            print("Usage: %s -i input -o output" % sys.argv[0])

    if verbose_level > 0:
        print('\n -- Looking for movies in "{0}" --\n'.format(movies_folder))
    # Set the number of processed files equal to zero
    scan_movie_files.counter = 0

    # Start Processing
    scan_movie_files(movies_folder, extensions)

    # We are done. Exit now.
    if verbose_level > 0:
        print('\n -- {0} Movie File(s) found in directory {1} --'.format \
            (scan_movie_files.counter, movies_folder))
        print

    # Fetch imdb data
    if hasattr(scan_movie_files, 'list'):
        get_imdb(scan_movie_files.list)
