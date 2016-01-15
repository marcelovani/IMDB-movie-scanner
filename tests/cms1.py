#!/usr/bin/env python

import os, sys
import json
import urllib2
import ConfigParser
import re, pprint

def get_people(personList):
    """ Build a list of ids and names """
    ids = []
    names = []
    for person in personList:
        ids.append(person.getID())
        names.append(person.get('name'))
    return {'ids':ids, 'names':names}

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
        'directors': get_people([<Person id:0905152[http] name:_Wachowski, Andy_>, <Person id:0905154[http] name:_Wachowski, Lana_>]),
        'cast': get_people([<Person id:0905152[http] name:_Wachowski, Andy_>, <Person id:0905154[http] name:_Wachowski, Lana_>]),
        'plot': 'bla bla bla',
        'rating': '7',
        'votes': '99',
        'thumb': 'http://thumb.jpg',
        'cover': 'http://cover.jpg',
}
print data
exit(0)

req = urllib2.Request(cms_api_url)
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))
print response.read()
