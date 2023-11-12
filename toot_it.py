# toot_it.py
import argparse
import os
import sys
from mastodon import Mastodon

# Example
#
# python toot_it.py --send "Test from Python"
#
# Get you access token and instance from .env
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
MASTODON_INSTANCE = os.getenv('MASTODON_INSTANCE')

# Initialize
mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=MASTODON_INSTANCE
)


def send_toot(status):
    """ Just sends text to Mastodon """
    res = mastodon.toot(status=status)
    if res:
        print(f'toot sent!')
        return True
    else:
        print(f'doh: {res}')
        return False


def main(**kwargs):
    if kwargs.get('send'):
        send_toot(status=kwargs.get('send'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--send',
        help='Send Tweet',
        required=True
    )

    args = parser.parse_args()

    # Convert the argparse.Namespace to a dictionary: vars(args)
    arg_dict = vars(args)
    # pass dictionary to main
    main(**arg_dict)
    sys.exit(0)
