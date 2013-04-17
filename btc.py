#!/usr/bin/env python
"""
btc
~~~

Buy, sell, and transfer bitcoin instantly at your terminal! (Powered by
Coinbase: https://coinbase.com/).

Usage:
  btc init
  btc test
  btc logs
  btc view
  btc buy <btc>
  btc sell <btc>
  btc transfer <btc> <address>
  btc (-h | --help)
  btc --version

Options:
  -h --help  Show this screen.
  -version   Show version.

Written by Randall Degges <http://www.rdegges.com/>.
"""


from json import dumps
from os.path import exists, expanduser
from sys import exit

from docopt import docopt
from requests import get


##### GLOBALS
API_KEY = None
CONFIG_FILE = expanduser('~/.btc')


def init():
    """Initialize `btc`.

    This will store the user's API key in their home directory: ~/.btc, and
    ensure the API key specified actually works.
    """
    print 'Initializing `btc`...\n'

    finished = False
    while not finished:
        api_key = raw_input('Enter your Coinbase API key here: ').strip()
        if not api_key:
            print '\nNot sure how to find your Coinbase API key?'
            print 'You can get one here: ' \
                'https://coinbase.com/account/integrations\n'
            continue

        # Validate the API key.
        resp = get('https://coinbase.com/api/v1/users?api_key=%s' % api_key)
        if resp.status_code == 200:
            f = open(CONFIG_FILE, 'wb')
            f.write(api_key)
            f.close()

            print '\nSuccessfully initialized `btc`!'
            print 'Your API key is stored here:', CONFIG_FILE, '\n'
            print 'Run `btc` for usage information.'
            finished = True
        else:
            print '\nYour API key is not working, please verify it is ' \
                'correct, and try again.\n'


def logs():
    """List a user's recent Coinbase transactions."""
    resp = get('https://coinbase.com/api/v1/transactions?api_key=%s' % API_KEY)
    if resp.status_code != 200:
        print 'Error connecting to Coinbase API. Please try again.'
        return

    print 'Transaction Logs'
    print '================'
    print dumps(resp.json()['transactions'], sort_keys=True, indent=2,
            separators=(',', ': '))
    print '================'
