#!/usr/bin/env python

import os, sys, getopt
import ConfigParser
import pprint
import json
import re
import urllib, urllib2

# Import the IMDbPY package.
try:
    import imdb
except ImportError:
    print 'You need to install the IMDbPY package!'
    sys.exit(1)


# List movies
# input() workaround to support Python 2. Python 3 renamed raw_input() => input().
# Alias input() to raw_input() if raw_input() exists (Python 2).
try:
    input = raw_input
except NameError:
    pass

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

                film = filename.replace('.' + movie_extension, '')
                film = re.sub(ur'[\W_]+', ' ', film, flags=re.UNICODE)

                info = {
                        "folder": movies_folder,
                        "keywords": film,
                    }
                list.append(info)
                scan_movie_files.list = list

                scan_movie_files.counter += 1

                # @TODO display warning if more than one film is in the folder

        elif os.path.isdir(filepath):
            # We got a directory, enter into it for further processing
            scan_movie_files(filepath, movie_extensions, list)


def get_imdb(list, limit):
    ''' Get IMDB data. '''

    i = imdb.IMDb()

    # Traverse through all files
    for item in list:
        folder = item['folder']
        keywords = item['keywords']

        # Skip folders that contain summary and cover
        if ( not os.path.isfile(folder + "/Summary.txt") or scan_method == 'all' ):

            if ( not os.path.isfile(folder + "/folder.jpg") or scan_method == 'all' ):

                # search imdb
                in_encoding = sys.stdin.encoding or sys.getdefaultencoding()
                out_encoding = sys.stdout.encoding or sys.getdefaultencoding()

                title = unicode(keywords, in_encoding, 'replace')
                try:
                    # Do the search, and get the results (a list of Movie objects).
                    results = i.search_movie(title, limit)
                except imdb.IMDbError, e:
                    print "Probably you're not connected to Internet.  Complete error report:"
                    print e
                    sys.exit(3)

                # Print the results.
                print '    %s result%s for "%s":' % (len(results),
                                                    ('', 's')[len(results) != 1],
                                                    title.encode(out_encoding, 'replace'))
                print 'Folder ' + folder
                print 'movieID\t: imdbID : title'

                # Print the long imdb title for every movie.
                for movie in results:
                    outp = u'%s\t: %s : %s' % (movie.movieID, i.get_imdbID(movie),
                                                movie['long imdb title'])
                    print outp.encode(out_encoding, 'replace')

                #get close matches only example
                #words = ['hello', 'Hallo', 'hi', 'house', 'key', 'screen', 'hallo', 'question', 'format']
                #difflib.get_close_matches('Hello', words)

                # Use first result
                movie = results[0]
                i.update(movie)
                movieID = movie.movieID

                # print movie info
                filmInfo = movie.summary()
                filmInfo += u'IMDB ID: %s.\n' % movieID

                # save covers
                thumb_url = movie.get('cover url')
                cover_url = movie.get('full-size cover url')

                if cover_url:
                    filmInfo += u'Cover: %s.\n' % cover_url
                    print 'Fetching cover'
                    try:
                        # Fetch online image
                        if ( not os.path.isfile(folder + "/thumb.jpg")):
                            urllib.urlretrieve (thumb_url, folder + "/thumb.jpg")
                        if ( not os.path.isfile(folder + "/folder.jpg")):
                            urllib.urlretrieve (cover_url, folder + "/folder.jpg")
                    except imdb.IMDbError, e:
                        print "NOTICE: Could not download cover:"
                        print e
                else:
                    print 'NOTICE: No cover available'

                # Write film info
                write_info(folder, filmInfo.encode(out_encoding, 'replace'))

                print 'Sending to CMS'
                send_cms(folder, movie)

def write_info(folder, info):
    ''' Write local film info. '''

    # Create file
    summaryFile = open(folder + '/Summary.txt','w')
    summaryFile.write(info)
    summaryFile.close()

    print info


def send_cms(folder, movie):
    ''' Send info to end point. '''

    config = ConfigParser.RawConfigParser()
    config.read(pwd + '/config.ini')
    cms_api_url = config.get('CMS','cms_api_url')

    data = {
        'folder': folder,
        'owned': 'owned',
        'imdb_id': movie.movieID,
        'genres': movie.get('genre'),
        'title': movie.get('long imdb title'),
        'plot': movie.get('plot summary'),
        'countries': movie.get('country'),
        'directors': get_people(movie.get('director')),
        'cast': get_people(movie.get('cast')),
        'writer': get_people(movie.get('writer')),
        'rating': movie.get('rating'),
        'votes': movie.get('votes'),
        'thumb': movie.get('cover url'),
        'cover': movie.get('full-size cover url'),
    }

    req = urllib2.Request(cms_api_url)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))
    print response.read()

def get_people(personList):
    """ Build a list of ids and names """
    ids = []
    names = []
    if type(personList) is list:
        for person in personList:
            ids.append(person.getID())
            names.append(person.get('name'))
    else:
        person = personList
        ids.append(person.getID())
        names.append(person.get('name'))

    return {'ids':ids, 'names':names}

if __name__ == '__main__':

    # Get current folder
    pwd = os.getcwd()

    config = ConfigParser.RawConfigParser()

    # Read config file
    config.read(pwd + '/config.ini')

    imdbpy_folder = config.get('Library','imdbpy_folder')
    limit = config.get('Library','imdbpy_limit')
    movies_folder = config.get('Movies','movies_folder')
    extensions = eval(config.get('Movies','file_extensions'))
    cms_api_url = config.get('CMS','cms_api_url')
    cms_cron_url = config.get('CMS','cms_cron_url')
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

    print('\n -- Looking for movies in "{0}" --\n'.format(movies_folder))
    # Set the number of processed files equal to zero
    scan_movie_files.counter = 0

    # Start Processing
    scan_movie_files(movies_folder, extensions)

    # We are done. Exit now.
    print('\n -- {0} Movie File(s) found in directory {1} --'.format \
            (scan_movie_files.counter, movies_folder))
    print

    # Fetch imdb data
    get_imdb(scan_movie_files.list, limit)

