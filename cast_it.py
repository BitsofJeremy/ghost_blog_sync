# cast_it.py
import argparse
import os
import sys

from farcaster import Warpcast
from dotenv import load_dotenv

# Example
#
# python cast_it.py --send "Test from Python to bitsofjeremy" \
# --link "https://bits.jeremyschroeder.net/" \
# --channel "bitsofjeremy"

load_dotenv()
client = Warpcast(mnemonic=os.environ.get("MNEMONIC_ENV_VAR"))


def send_cast(status=None, link=None, parent=None, channel=None):
    """ Sends to Warpcast """
    if status:
        # status is expecting a string
        status = str(status)
    if link:
        # embeds is expecting an array
        link = [link]
    if parent:
        # parent is expecting a string
        parent = str(parent)
    if channel:
        # channel is expecting a string
        channel = str(channel)

    # Send it!
    response = client.post_cast(
        text=status,
        embeds=link,
        parent=parent,
        channel_key=channel
    )
    print(response)
    if response:
        print(f'cast sent!')
        return True
    else:
        print(f'doh: {response}')
        return False


def main(**kwargs):
    """ This is used for the standalone script """
    status = kwargs.get('status')
    link = kwargs.get('link')
    parent = kwargs.get('parent')
    channel = kwargs.get('channel')

    send_cast(
        status=status,
        link=link,
        parent=parent,
        channel=channel
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--status',
        help='Cast Text',
        required=True
    )
    parser.add_argument(
        '--link',
        help='Add a link to a cast',
        default=None,
        required=False
    )
    parser.add_argument(
        '--parent',
        help='Attach Cast to Parent Cast [replying to another cast]',
        default=None,
        required=False
    )
    parser.add_argument(
        '--channel',
        help='Send cast to a Warpcast channel',
        default=None,
        required=False
    )
    args = parser.parse_args()

    # Convert the argparse.Namespace to a dictionary: vars(args)
    arg_dict = vars(args)
    # pass dictionary to main
    main(**arg_dict)
    sys.exit(0)
