# update_posts.py

# This converts all posts from public to members only
# A good example of how to use the admin API for Ghost

from datetime import datetime as date
import jwt
import os
import requests
import pprint
from ghost import get

pp = pprint.PrettyPrinter(indent=4)
# Create an integration, then copy the admin key to an ENV
GHOST_ADMIN_KEY = os.getenv('GHOST_ADMIN_KEY')
# Put your domain in an EMV
GHOST_DOMAIN = os.getenv('GHOST_DOMAIN')


def get_jwt():
    """ Get JWT from API based on admin key """
    # Split the key into ID and SECRET
    id, secret = GHOST_ADMIN_KEY.split(':')

    # Prepare header and payload
    iat = int(date.now().timestamp())

    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
    payload = {
        'iat': iat,
        'exp': iat + 5 * 60,
        'aud': '/v3/admin/'
    }
    # Create the token (including decoding secret)
    token = jwt.encode(
        payload,
        bytes.fromhex(secret),
        algorithm='HS256',
        headers=header
    )
    # print(token)
    return token


def update_post():
    """ Use the ghost.py script to get all posts from the blog API.
     Iterate over each and update visibility to 'members' """
    posts = get()
    #
    jwt_token = get_jwt()
    for post in posts:
        # print(post)
        post_id = post['post_id']
        updated_at = post['updated_at']
        url = f'https://{GHOST_DOMAIN}/ghost/api/v3/admin/posts/{post_id}/'
        # Change visibility to 'member'
        body = {
            "posts": [{
                "visibility": "public",
                "updated_at": updated_at
            }]
        }
        headers = {'Authorization': f'Ghost {jwt_token}'}
        res = requests.put(url, json=body, headers=headers)
        response = res.json()
        pp.pprint(response)
    print("DONE")


if __name__ == '__main__':
    update_post()
