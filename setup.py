#!/usr/bin/env python

import os, sys, getopt
import ConfigParser

def usage(code, msg=''):
    print 'Usage:'
    print '  --version: Displays version'
    print '  --movies-folder: Specify where your movies are located'
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)

try:
    opts, args = getopt.getopt(sys.argv[1:], 'ho:v', ['help', 'movies-folder=', 'version'])
except getopt.GetoptError as err:
	usage(0)

# parse options
for option, arg in opts:
    if option in ('-h', '--movies-folder'):
    	movies_folder = arg
    elif option in ('-V', '--version'):
        print '1.0'
        sys.exit(0)


if __name__ == "__main__":
	# Get current folder
	pwd = os.getcwd()

	# Create config file
	cfgfile = open(pwd + '/config.ini','w')
	config = ConfigParser.RawConfigParser()

	config.add_section('Library')
	config.set('Library','imdbpy_folder', os.path.realpath(pwd + '/../imdbpy'))
	config.set('Library','imdbpy_limit', '5')

	config.add_section('Movies')
	config.set('Movies','movies_folder', movies_folder)
	config.set('Movies','file_extensions',['avi', 'dat', 'mp4', 'mkv', 'vob', 'mpeg', 'mpg'])

	config.add_section('CMS')
	config.set('CMS','cms_api_url','http://www.example.com')
	config.set('CMS','cms_cron_url','http://www.example.com/cron.php')
	config.set('CMS','cms_api_id','admin')
	config.set('CMS','cms_api_key','0000-0000-0000-0000')

  config.add_section('Options')
	config.set('Options','use_dic', 0)

	config.write(cfgfile)
	cfgfile.close()
