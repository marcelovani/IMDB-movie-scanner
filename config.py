#!/usr/bin/env python

import os, sys, getopt
import ConfigParser

def get_config(section, key):
    """ Get config data """

    # @todo statically cache configs

    # Get current folder
    pwd = os.getcwd()

    config = ConfigParser.RawConfigParser()

    # Read config file
    config.read(pwd + '/config.ini')

    return config.get(section, key)
