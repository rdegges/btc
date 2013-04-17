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
  --version  Show version.

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
VERSION = 'btc 0.1'


class BTC(object):

    def get_api_key(self):
        """Get the API key, or quit with an error."""
        if exists(CONFIG_FILE):
            return open(CONFIG_FILE).read()
        else:
            print 'No API key found! Please run `btc init` to initialize.'
            exit(1)

    def make_get_request(self, path):
        """Make the specified API request, and return the JSON data, or quit
        with an error.
        """
        resp = get('%s/%s?api_key=%s' % (API_URI, path, self.get_api_key()))
        if resp.status_code != 200:
            print 'Error connecting to Coinbase API. Please try again.'
            print 'If the problem persists, please check your API key.'
            exit(1)

        return resp.json()

    def logs(self):
        """List a user's recent Coinbase transactions."""
        json = self.make_get_request('transactions')

        print 'Transaction Logs'
        print '================'
        print dumps(json['transactions'], sort_keys=True, indent=2,
                separators=(',', ': '))
        print '================'

    def sell(self):
        pass

    def test(self):
        """Test the API key to make sure it's working."""
        resp = get('%s/users?api_key=%s' % (API_URI, self.get_api_key()))
        if resp.status_code == 200:
            print 'Your API key is working!'
        else:
            print 'Your API is NOT working. Please check your API key.'
            print 'To update your API key, re-run `btc init`.'

    def transfer(self):
        pass

    def view(self):
        """List current exchange rates."""
        bjson = self.make_get_request('prices/buy')
        sjson = self.make_get_request('prices/sell')

        print 'Bitcoin Exchange Rates'
        print '======================'
        print 'Buy: 1 BTC for %s %s' % (bjson['amount'], bjson['currency'])
        print 'Sell: 1 BTC for %s %s' % (sjson['amount'], sjson['currency'])
        print '======================'


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
        resp = get('%s/users?api_key=%s' % (API_URI, api_key))
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


def main():
    """Handle user input, and do stuff accordingly."""
    arguments = docopt(__doc__, version=VERSION)

    btc = BTC()
    if arguments['init']:
        init()
    elif arguments['logs']:
        btc.logs()
    elif arguments['sell']:
        btc.sell()
    elif arguments['test']:
        btc.test()
    elif arguments['transfer']:
        btc.transfer()
    elif arguments['view']:
        btc.view()


if __name__ == '__main__':
    main()
