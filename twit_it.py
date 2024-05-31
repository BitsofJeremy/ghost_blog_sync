# twit_it.py
import argparse
import os
import sys
import tweepy
from dotenv import load_dotenv
load_dotenv()


# Example
#
# python twit_it.py --send "Test from Python"

# Twitter Oauth keys
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
oauth_token = os.getenv('OAUTH_TOKEN')
oauth_token_secret = os.getenv('OAUTH_TOKEN_SECRET')

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=oauth_token, access_token_secret=oauth_token_secret
)


def send_tweet(status):
    """ Just sends text to Twitter """
    response = client.create_tweet(text=status)
    print(response)
    if response:
        print(f'tweet sent!')
        return True
    else:
        print(f'doh: {response}')
        return False


def main(**kwargs):
    if kwargs.get('send'):
        send_tweet(status=kwargs.get('send'))


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
