#!/usr/bin/env python

import os, sys
import json
import urllib2
import imdb
import pprint

i = imdb.IMDb()

cms_api_url = 'http://movie-catalog.local:8083/api/imdb/movie/add'
movieId = '0234215'

in_encoding = sys.stdin.encoding or sys.getdefaultencoding()
out_encoding = sys.stdout.encoding or sys.getdefaultencoding()

movie = i.get_movie(movieId)

outp = u'%s\t: %s : %s' % (movie.movieID, movie.movieID, movie.get('plot summary'))
plot = outp.encode(out_encoding, 'replace')

data = {
        'imdb_id': movie.movieID,
        'genres': movie.get('genre'),
        'title': movie.get('long imdb title'),
        'plot': movie.get('plot summary'),
        'rating': movie.get('rating'),
        'votes': movie.get('votes'),
        'thumb': movie.get('cover url'),
        'cover': movie.get('full-size cover url'),
}

req = urllib2.Request(cms_api_url)
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))
print response.read()
