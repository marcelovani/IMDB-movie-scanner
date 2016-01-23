#!/usr/bin/env python

import os, sys
import urllib, urllib2
from spell import *
from config import *
from cms import *

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

limit = int(get_config('IMDB','limit'))
use_dic = get_config('Options','use_dic')
verbose_level = int(get_config('Options','verbose_level'))

def get_imdb(list, scan_method):
    ''' Get IMDB data. '''

    if not list:
            return

    i = imdb.IMDb()

    # Traverse through all files
    for item in list:
        folder = item['folder']
        keywords = item['keywords']

        # search imdb
        in_encoding = sys.stdin.encoding or sys.getdefaultencoding()
        out_encoding = sys.stdout.encoding or sys.getdefaultencoding()

        if verbose_level > 1:
            print "Folder: " + folder
            print "Keywords: " + keywords

        if use_dic == 1:
            keywords = spellcheck(keywords)
            if verbose_level > 0:
                print "Keywords: " + keywords

        title = unicode(keywords, in_encoding, 'replace')
        try:
            # Do the search, and get the results (a list of Movie objects).
            results = i.search_movie(title, limit)
        except imdb.IMDbError, e:
            print "Probably you're not connected to Internet.  Complete error report:"
            sys.exit(3)

        if results:
            # Print the results.
            if verbose_level > 4:
                print '%s result%s for "%s":' % (len(results),
                                                    ('', 's')[len(results) != 1],
                                                    title.encode(out_encoding, 'replace'))
                print 'movieID\t: imdbID : title'

            # Print the long imdb title for every movie.
            if verbose_level > 2:
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
            filmInfo = movie.summary() + '\n'
            filmInfo += u'IMDB ID: %s.\n' % movieID

            # save covers
            thumb_url = movie.get('cover url')
            cover_url = movie.get('full-size cover url')

            if cover_url:
                filmInfo += u'Cover: %s.\n' % cover_url + '\n'
                print 'Fetching cover'
                try:
                    # Fetch online image
                    if ( not os.path.isfile(folder + "/thumb.jpg") or scan_method == 'all' ):
                        urllib.urlretrieve (thumb_url, folder + "/thumb.jpg")
                    if ( not os.path.isfile(folder + "/folder.jpg") or scan_method == 'all' ):
                        urllib.urlretrieve (cover_url, folder + "/folder.jpg")
                except imdb.IMDbError, e:
                    print "NOTICE: Could not download cover:"
            else:
                print 'NOTICE: No cover available'

            # Write film info
            write_info(folder, filmInfo.encode(out_encoding, 'replace'))

            if verbose_level > 0:
                print 'Sending to CMS'
            send_cms(folder, movie)
        else:
            print 'NOTICE: No results found for ' + title

        print


def write_info(folder, info):
    ''' Write local film info. '''

    # Create file
    summaryFile = open(folder + '/Summary.txt','w')
    summaryFile.write(info)
    summaryFile.close()

    if verbose_level > 3:
        print info
