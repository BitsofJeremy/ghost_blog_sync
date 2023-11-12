# twit_it.py
import argparse
import os
import sys
import tweepy

# Example
#
# python twit_it.py --send "Test from Python"

# Twitter Oauth keys
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
oauth_token = os.getenv('OAUTH_TOKEN')
oauth_token_secret = os.getenv('OAUTH_TOKEN_SECRET')

# Setup the app Oauth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(oauth_token, oauth_token_secret)

# Initialize the api
api = tweepy.API(auth)


def send_tweet(status):
    """ Just sends text to Twitter """
    res = api.update_status(status)
    if res:
        print(f'tweet sent!')
        return True
    else:
        print(f'doh: {res}')
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
