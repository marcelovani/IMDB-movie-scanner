#!/usr/bin/env python

import os, sys
import json
import urllib2
import ConfigParser

config = ConfigParser.RawConfigParser()

# Read config file
config.read(os.getcwd() + '/config.ini')

cms_api_url = config.get('CMS','cms_api_url')
print cms_api_url
data = {
        'imdb_id': '1234',
        'genres': 'comedy',
        'title': 'hot shots',
        'countries': 'USA, Australia, Brazil',
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
