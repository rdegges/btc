#!/usr/bin/env python
"""
btc
~~~

Buy, sell, and transfer bitcoin instantly in your terminal! (Powered by
Coinbase: https://coinbase.com/).

Usage:
  btc init
  btc address
  btc balance
  btc request <btc> <email> [<note>]
  btc send <btc> (<email> | <address>) [<note>]
  btc test
  btc logs
  btc rates
  btc buy <btc>
  btc sell <btc>
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
from textwrap import wrap

from docopt import docopt
from requests import get, post


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

    def make_request(self, path, data={}, method='GET'):
        """Make the specified API request, and return the JSON data, or quit
        with an error.
        """
        params = {
            'api_key': self.get_api_key(),
        }
        if method.lower() == 'post':
            resp = post('%s/%s' % (API_URI, path), params=params,
                data=dumps(data), headers={'Content-Type':
                'application/json'})
        else:
            params = dict(params.items() + data.items())
            resp = get('%s/%s' % (API_URI, path), params=params)

        if resp.status_code != 200:
            print 'Error connecting to Coinbase API. Please try again.'
            print 'If the problem persists, please check your API key.'
            exit(1)

        return resp.json()

    def address(self):
        """Return the user's current bitcoin receive address."""
        json = self.make_request('account/receive_address')

        print 'Your bitcoin receive address is:', json['address']

    def balance(self):
        """Return the amount of bitcoin in this user's account."""
        json = self.make_request('account/balance')

        print 'You have a total of %s %s in your account.' % (json['amount'],
                json['currency'])

    def request(self, amount, email, note):
        """Request bitcoin payment by email address."""
        json = self.make_request('transactions/request_money', data={
            'transaction': {
                'from': email,
                'amount': amount,
                'notes': note
            }
        }, method='POST')

        if not json['success']:
            print 'There Were Error(s) Requesting Bitcoin'
            print '======================================'
            for error in json['errors']:
                print '- %s' % '\n  '.join(wrap(error, 77))
            print '======================================'
            return

        print 'Request successful!'

    def send(self, amount, address, note):
        """Send bitcoin payment by email address or bitcoin address."""
        json = self.make_request('transactions/send_money', data={
            'transaction': {
                'to': address,
                'amount': amount,
                'notes': note
            }
        }, method='POST')

        if not json['success']:
            print 'There Were Error(s) Sending Bitcoin'
            print '==================================='
            for error in json['errors']:
                print '- %s' % '\n  '.join(wrap(error, 77))
            print '==================================='
            return

        print 'Sending Bitcoin Successful'
        print '=========================='
        print dumps(json['transaction'], sort_keys=True, indent=2,
                separators=(',', ': '))
        print '=========================='

    def logs(self):
        """List a user's recent Coinbase transactions."""
        json = self.make_request('transactions')

        print 'Transaction Logs'
        print '================'
        print dumps(json['transactions'], sort_keys=True, indent=2,
                separators=(',', ': '))
        print '================'

    def sell(self, amount):
        """Sell bitcoin."""
        bjson = self.make_request('prices/sell', data={'qty': amount})

        api_key = raw_input("Are you sure you'd like to sell %f BTC? This will give you ~%s %s (y/n) " % (amount, bjson['amount'], bjson['currency'])).strip().lower()
        if api_key != 'y':
            return

        json = self.make_request('sells', method='POST', data={
            'qty': amount,
        })

        if not json['success']:
            print 'There Were Error(s) Selling Your Bitcoin'
            print '========================================'
            for error in json['errors']:
                print '- %s' % '\n  '.join(wrap(error, 77))
            print '========================================'
            return

        print 'Sell Successful'
        print '==============='
        print dumps(json['transfer'], sort_keys=True, indent=2,
                separators=(',', ': '))
        print '==============='

    def test(self):
        """Test the API key to make sure it's working."""
        resp = get('%s/users?api_key=%s' % (API_URI, self.get_api_key()))
        if resp.status_code == 200:
            print 'Your API key is working!'
        else:
            print 'Your API is NOT working. Please check your API key.'
            print 'To update your API key, re-run `btc init`.'

    def rates(self):
        """List current exchange rates."""
        bjson = self.make_request('prices/buy')
        sjson = self.make_request('prices/sell')

        print 'Bitcoin Exchange Rates'
        print '======================'
        print 'Buy: 1 BTC for %s %s' % (bjson['amount'], bjson['currency'])
        print 'Sell: 1 BTC for %s %s' % (sjson['amount'], sjson['currency'])
        print '======================'

    def buy(self, amount):
        """Purchase bitcoin."""
        bjson = self.make_request('prices/buy', data={'qty': amount})

        api_key = raw_input("Are you sure you'd like to purchase %f BTC? This will cost ~%s %s (y/n) " % (amount, bjson['amount'], bjson['currency'])).strip().lower()
        if api_key != 'y':
            return

        json = self.make_request('buys', method='POST', data={
            'qty': amount,
            'agree_btc_amount_varies': True,
        })

        if not json['success']:
            print 'There Were Error(s) Making Your Purchase'
            print '========================================'
            for error in json['errors']:
                print '- %s' % '\n  '.join(wrap(error, 77))
            print '========================================'
            return

        print 'Purchase Successful'
        print '==================='
        print dumps(json['transfer'], sort_keys=True, indent=2,
                separators=(',', ': '))
        print '==================='


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
    elif arguments['address']:
        btc.address()
    elif arguments['balance']:
        btc.balance()
    elif arguments['request']:
        btc.request(float(arguments['<btc>']), arguments['<email>'],
                arguments['<note>'])
    elif arguments['send']:
        address = (arguments['<email>'] if arguments['<email>'] else
                arguments['<address>'])
        btc.send(float(arguments['<btc>']), address, arguments['<note>'])
    elif arguments['logs']:
        btc.logs()
    elif arguments['sell']:
        btc.sell(float(arguments['<btc>']))
    elif arguments['test']:
        btc.test()
    elif arguments['rates']:
        btc.rates()
    elif arguments['buy']:
        btc.buy(float(arguments['<btc>']))


if __name__ == '__main__':
    main()
