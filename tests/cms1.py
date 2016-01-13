#!/usr/bin/env python

import os, sys
import json
import urllib2

cms_api_url = 'http://movie-catalog.local:8083/api/imdb/movie/add'

data = {
        'imdb_id': '1234',
        'genres': 'comedy',
        'title': 'hot shots',
        'plot': 'bla bla bla',
        'rating': '7',
        'votes': '99',
        'thumb': 'http://thumb.jpg',
        'cover': 'http://cover.jpg',
}

req = urllib2.Request(cms_api_url)
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))
print response.read()
