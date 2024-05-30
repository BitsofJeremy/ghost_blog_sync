# ghost.py

import argparse
import os
import requests
import sys

import pprint
pp = pprint.PrettyPrinter(indent=4)
GHOST_API_KEY = os.getenv('GHOST_API_KEY')
GHOST_DOMAIN = os.getenv('GHOST_DOMAIN')


def get():
    url = f'https://{GHOST_DOMAIN}/ghost/api/v3/' \
          f'content/posts/?key={GHOST_API_KEY}&limit=all&' \
          f'order=published_at%20asc&include=tags'
    res = requests.get(url)
    data = res.json()
    # pp.pprint(data)
    all_posts = []
    for post in data['posts']:
        tags = []
        for t in post['tags']:
            tag_dict = {
                'tag_id': t['id'],
                'tag_name': t['name']
            }
            tags.append(tag_dict)
        p = {
            'post_id': post['id'],
            'post_uuid': post['uuid'],
            'title': post['title'],
            'url': post['url'],
            # Grab the custom_excerpt as those are from me
            'excerpt': post['custom_excerpt'],
            'feature_image': post['feature_image'],
            'published': post['published_at'],
            'updated_at': post['updated_at'],
            'tags': tags,
            'visibility': post['visibility']
        }
        all_posts.append(p)
    return all_posts


def main(**kwargs):
    if kwargs.get('get_posts'):
        res = get()
        pp.pprint(res)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--get_posts',
        help='Get all posts',
        action='store_true',
        required=True
    )

    args = parser.parse_args()

    # Convert the argparse.Namespace to a dictionary: vars(args)
    arg_dict = vars(args)
    # pass dictionary to main
    main(**arg_dict)
    sys.exit(0)

