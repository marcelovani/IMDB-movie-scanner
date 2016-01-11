#!/usr/bin/env python

import os, sys
import ConfigParser

# Get current folder
pwd = os.getcwd()

# Create config file
cfgfile = open(pwd + '/config.ini','w')
config = ConfigParser.RawConfigParser()

config.add_section('Library')
config.set('Library','imdbpy_folder', os.path.realpath(pwd + '/../imdbpy'))
config.set('Library','imdbpy_limit', '5')

config.add_section('Movies')
config.set('Movies','movies_folder','/Users/marcelovani/Downloads/movies')
config.set('Movies','file_extensions',['avi', 'dat', 'mp4', 'mkv', 'vob', 'mpeg', 'mpg'])

config.add_section('CMS')
config.set('CMS','cms_api_url','http://www.example.com')
config.set('CMS','cms_api_id','admin')
config.set('CMS','cms_api_key','0000-0000-0000-0000')

config.write(cfgfile)
cfgfile.close()
