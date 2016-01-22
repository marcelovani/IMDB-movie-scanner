#!/usr/bin/env python

import urllib, urllib2
import json
from config import *

cms_api_url = get_config('CMS','cms_api_url')
cms_cron_url = get_config('CMS','cms_cron_url')
verbose_level = int(get_config('Options','verbose_level'))

def send_cms(folder, movie):
    ''' Send info to end point. '''

    cms_api_url = get_config('CMS','cms_api_url')

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
    if verbose_level > 1:
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
        if personList:
            person = personList
            ids.append(person.getID())
            names.append(person.get('name'))

    return {'ids':ids, 'names':names}