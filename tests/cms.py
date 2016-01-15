#!/usr/bin/env python

import os, sys
import json
import urllib2
import imdb
import pprint
import ConfigParser
import re

config = ConfigParser.RawConfigParser()
# Read config file
config.read(os.getcwd() + '/config.ini')
cms_api_url = config.get('CMS','cms_api_url')

i = imdb.IMDb()

movieId = '0234215'
movieId = '0120737'
movieId = '1375666'
movieId = '0926084'
movieId = '0468569'
movieId = '0234215'

in_encoding = sys.stdin.encoding or sys.getdefaultencoding()
out_encoding = sys.stdout.encoding or sys.getdefaultencoding()

movie = i.get_movie(movieId)

def get_people(personList):
    """ Build a list of ids and names """
    ids = []
    names = []
    for person in personList:
        ids.append(person.getID())
        names.append(person.get('name'))
    return {'ids':ids, 'names':names}


outp = u'%s\t: %s : %s' % (movie.movieID, movie.movieID, movie.get('plot summary'))
plot = outp.encode(out_encoding, 'replace')

data = {
        'imdb_id': movie.movieID,
        'genres': movie.get('genre'),
        'title': movie.get('long imdb title'),
        'plot': movie.get('plot summary'),
        'countries': movie.get('country'),
        'directors': get_people(movie.get('director')),
        'rating': movie.get('rating'),
        'votes': movie.get('votes'),
        'thumb': movie.get('cover url'),
        'cover': movie.get('full-size cover url'),
}

print data
exit(0)

req = urllib2.Request(cms_api_url)
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))
print response.read()
