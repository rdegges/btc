#!/usr/bin/env python
"""
btc
~~~

Buy, sell, and transfer bitcoin instantly at your terminal! (Powered by
Coinbase: https://coinbase.com/).

Usage:
  btc init                      Initialize btc.
  btc test                      Test your API key.
  btc logs                      View recent transactions.
  btc view                      View current bitcoin exchange rates.
  btc buy <btc>                 Buy bitcoin.
  btc sell <btc>                Sell bitcoin.
  btc transfer <btc> <address>  Transfer bitcoin.
  btc (-h | --help)             Show this screen.
  btc --version                 Show version.

Written by Randall Degges <http://www.rdegges.com/>. Like the software? Send a
tip to Randall: 14m3gaa3TvEgN7Ltc4377v3MVCPnyunuqS
"""


from json import dumps
from os.path import exists, expanduser
from sys import exit

from docopt import docopt
from requests import get


##### GLOBALS
API_URI = 'https://coinbase.com/api/v1'
CONFIG_FILE = expanduser('~/.btc')


class BTC(object):

    def get_api_key(self):
        """Get the API key, or quit with an error."""
        if exists(CONFIG_FILE):
            return open(CONFIG_FILE).read()
        else:
            print 'No API key found! Please run `btc init` to initialize.'
            exit(1)

    def logs(self):
        """List a user's recent Coinbase transactions."""
        resp = get('%s/transactions?api_key=%s' % (API_URI,
            self.get_api_key()))
        if resp.status_code != 200:
            print 'Error connecting to Coinbase API. Please try again.'
            print 'If the problem persists, please check your API key.'
            return

        print 'Transaction Logs'
        print '================'
        print dumps(resp.json()['transactions'], sort_keys=True, indent=2,
                separators=(',', ': '))
        print '================'


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


