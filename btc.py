"""
    btc
    ~~~

    Buy, sell, and transfer bitcoin instantly at your terminal! (Powered by
    Coinbase: https://coinbase.com/).

    For help, run `btc` with no parameters.
"""


from os.path import expanduser

from requests import get


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
            f = open(expanduser('~/.btc'), 'wb')
            f.write(api_key)
            f.close()

            print '\nSuccessfully initialized `btc`!'
            print 'Run `btc` for usage information.'
            finished = True
        else:
            print '\nYour API key is not working, please verify it is ' \
                'correct, and try again.\n'


init()
