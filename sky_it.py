import argparse
import os
import sys
from dotenv import load_dotenv
from atproto import Client

load_dotenv()

# Example
# python sky_it.py --send 'Hello from Python!'

# Bluesky credentials
username = os.getenv('BLUESKY_USERNAME')
password = os.getenv('BLUESKY_PASSWORD')

if not username or not password:
    print("Error: Bluesky credentials not found in .env file")
    sys.exit(1)

# Initialize client and login
client = Client()
try:
    client.login(username, password)
except Exception as e:
    print(f"Error logging in: {e}")
    sys.exit(1)


def send_post_to_sky(status):
    """Sends text to Bluesky"""
    try:
        response = client.send_post(text=status)
        print(f"Post sent successfully: {response}")
        return True
    except Exception as e:
        print(f"Error sending post: {e}")
        return False


def main(**kwargs):
    if kwargs.get('send'):
        send_post_to_sky(status=kwargs.get('send'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--send',
        help='Send Bluesky Post',
        required=True
    )

    args = parser.parse_args()
    arg_dict = vars(args)
    main(**arg_dict)
    sys.exit(0)
