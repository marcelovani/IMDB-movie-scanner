#!/usr/bin/env python

import os, sys, getopt
import pprint
import re
from config import *
from imdbc import *


def scan_movie_files(movies_folder, movie_extensions, list=[]):
    ''' Print files in movies_folder with extensions in movie_extensions, recursively. '''

    folder_scanned = 0

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

        blacklisted = False
        for bname in eval(blacklist_folders):
            if ( movies_folder.find(bname) != -1 ):
                blacklisted = True

        # Check if it's a normal file or directory
        if not blacklisted and os.path.isfile(filepath):

            # Check if the file has an extension of typical video files
            for movie_extension in movie_extensions:
                # Not a movie file, ignore
                if not filepath.lower().endswith(movie_extension.lower()):
                    continue

                # Skip folders that contain summary and cover
                summary_file = os.path.join(movies_folder, "Summary.txt")
                if ( os.path.isfile(summary_file) and scan_method == 'new' ):
                    continue

                # Only query IMDB for the first movie found in the folder
                if folder_scanned:
                    continue
                folder_scanned = 1

                # Remove strings from the filename
                keywords = filename.replace('.' + movie_extension, '').lower()

                # Clean fixed strings
                keywords = re.sub(ur'[\_\.\(\)\[\]]+', ' ', keywords, flags=re.UNICODE)

                # Clear single digits if year is present
                #keywords = re.sub(r'(\s\d{1}\s)(.*)(\d{4})', r' \2\3', keywords)

                # Add parenthesis to year
                keywords = re.sub(r'(\d{4})', r'(\1)', keywords)

                # Remove custom strings fom the filename
                for str in eval(ignore_strings):
                    keywords = keywords.replace(str.lower(), '')

                # Remove duplicated spaces
                keywords = re.sub(r'(\s+)', r' ', keywords)

                info = {"folder": movies_folder, "keywords": keywords}

                if verbose_level > 1:
                    print "Filename: " + filepath
                    print "Keywords: " + keywords
                    print

                list.append(info)

                scan_movie_files.list = list

                scan_movie_files.counter += 1

                # @TODO display warning if more than one film is in the folder

        elif os.path.isdir(filepath):
            # We got a directory, enter into it for further processing
            scan_movie_files(filepath, movie_extensions, list)

def usage():
    print("Usage: %s -f <folder> -o [new|all] -d -h" % sys.argv[0])
    print("-f <folder> The folder where to scan your movies")
    print("-o new      Only process folders that do not have Summary.txt")
    print("   all      Process all folders")
    print("-d          Dry run. Do not save anything")
    print("-h          This help")
    print

if __name__ == '__main__':

    movies_folder = get_config('Movies','movies_folder')
    blacklist_folders = get_config('Movies','blacklist_folders')
    extensions = eval(get_config('Options','file_extensions'))
    ignore_strings = get_config('Options','ignore_strings')
    verbose_level = int(get_config('Options','verbose_level'))
    scan_method = 'new'
    dry_run = 0

    # Read command line args
    try:
        myopts, args = getopt.getopt(sys.argv[1:],"f:o:dh")
    except getopt.GetoptError as e:
        print (str(e))
        usage()
        sys.exit(2)

    for o, a in myopts:
        if o == '-f':
            movies_folder = a
        elif o == '-o':
            scan_method = a
        elif o == '-d':
            dry_run = 1
        elif o == '-h':
            usage()
        else:
            usage()

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
    if not dry_run:
        if hasattr(scan_movie_files, 'list'):
            get_imdb(scan_movie_files.list, scan_method)
