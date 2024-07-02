# blog_sync.py

# imports
import os
from db_models import make_session, Posts, Tags
from ghost import get
from twit_it import send_tweet
from cast_it import send_cast
from toot_it import send_toot
from sky_it import send_post_to_sky
import random
import time
from dotenv import load_dotenv
load_dotenv()


WARPCAST_CHANNEL = os.getenv("WARPCAST_CHANNEL")


def random_sleep(min_minutes=5, max_minutes=30):
    """Generate a random sleep interval between min_minutes and max_minutes."""
    seconds = random.randint(min_minutes * 60, max_minutes * 60)
    print(f"Sleeping for {seconds // 60} minutes and {seconds % 60} seconds")
    time.sleep(seconds)


def make_hashtag(text):
    """ helper for hashtags """
    # remove underscore and dashes
    s = text.replace("-", " ").replace("_", " ")
    # split out words
    s = s.split()
    # if only one word, send back with
    # hashtag and capitalize
    if len(text) == 0:
        return f'#{text.capitalize()}'
    # Send back hashtag after camelcase
    return '#' + ''.join(i.capitalize() for i in s)


def main():
    """ Get all posts from DB, if posted skip, if not tweet or toot it out. """
    # get all old posts from blog online
    posts = get()
    # Make a DB session
    sesh = make_session()
    for post in posts:
        # print(post)
        # Look for tags, if not exist, create, return tag_obj
        tag_obj_list = []
        for tag in post['tags']:
            # print(tag)
            tag_exists = sesh.query(Tags).filter(Tags.tag_id == tag['tag_id']).scalar() is not None
            if tag_exists:
                tag_obj = sesh.query(Tags).filter(
                    Tags.tag_id == tag['tag_id']).one()
                tag_obj_list.append(tag_obj)
            else:
                # Tag does not exist, create it and add obj to list
                t = Tags(
                    tag_id=tag['tag_id'],
                    tag_name=tag['tag_name']
                )
                sesh.add(t)
                sesh.commit()
                # Grab that new tag object and drop into list
                tag_obj = sesh.query(Tags).filter(
                    Tags.tag_id == tag['tag_id']).one()
                tag_obj_list.append(tag_obj)

        # Check if posts exists
        post_exists = sesh.query(Posts).filter(Posts.post_uuid == post['post_uuid']).scalar() is not None
        if post_exists:
            print(f"This post exists in DB: {post['title']}")
        else:
            # Add Post to DB
            p = Posts(
                post_id=post['post_id'],
                post_uuid=post['post_uuid'],
            )
            p.title = post['title']
            p.url = post['url']
            p.excerpt = post['excerpt']
            p.feature_image = post['feature_image']
            # For SQL relations to work,
            # need SQL objects in a list
            p.tags = tag_obj_list
            sesh.add(p)
            sesh.commit()

        # Make tags into hashtags
        hashtags = ''
        for tag in tag_obj_list:
            t = make_hashtag(tag.tag_name)
            hashtags += f'{t} '
        # print(f'Hashtags: \n {hashtags}')

        # ### TWITTER ### #
        # Check if posts exists and tweeted
        post_tweeted = sesh.query(Posts).filter(Posts.twitter).filter(
            Posts.post_uuid == post['post_uuid']).scalar() is not None
        if post_tweeted:
            print(f"This post exists in DB and "
                  f"tweeted:  {post['title']}")
        else:
            # send post to twitter
            print("Sending post to Twitter")
            tweet = f"{post['title']} {hashtags} {post['url']}"
            # print(f'Tweet Length: {len(tweet)}')
            print(tweet)
            sent_tweet = send_tweet(status=tweet)
            if sent_tweet:
                # Update the DB we tweeted this post already
                p = sesh.query(Posts).filter(Posts.post_uuid == post['post_uuid']).first()
                p.twitter = True
                sesh.add(p)
                sesh.commit()

            # Going to sleep for 60 seconds to not
            # get rate limited on twitter API
            random_sleep(min_minutes=1, max_minutes=5)

        # ### MASTODON ### #
        # Check if posts exists and tooted
        post_tooted = sesh.query(Posts).filter(Posts.mastodon).filter(
            Posts.post_uuid == post['post_uuid']).scalar() is not None
        if post_tooted:
            print(f"This post exists in DB and "
                  f"tooted:  {post['title']}")
        else:
            # send post to mastodon
            print("Sending post to Mastodon")
            toot = f"{post['title']} {hashtags} {post['url']}"
            print(toot)
            sent_toot = send_toot(status=toot)
            if sent_toot:
                p = sesh.query(Posts).filter(Posts.post_uuid == post['post_uuid']).first()
                p.mastodon = True
                sesh.add(p)
                sesh.commit()

            # Going to sleep for 10 seconds to not
            # get rate limited on mastodon API
            time.sleep(10)

        # ### WARPCAST ### #
        # Check if posts exists and casted
        post_casted = sesh.query(Posts).filter(Posts.warpcast).filter(
            Posts.post_uuid == post['post_uuid']).scalar() is not None
        if post_casted:
            print(f"This post exists in DB and "
                  f"casted:  {post['title']}")
        else:
            # send post to Warpcast
            print("Sending post to Warpcast")
            sent_cast = send_cast(
                status=post['title'],
                link=post['url'],
                channel=WARPCAST_CHANNEL
            )
            if sent_cast:
                p = sesh.query(Posts).filter(Posts.post_uuid == post['post_uuid']).first()
                p.warpcast = True
                sesh.add(p)
                sesh.commit()

            # Going to sleep for 10 seconds to not
            # get rate limited on Warpcast API
            time.sleep(10)

        # ### BLUESKY ### #
        # Check if posts exists and sent to Bluesky
        post_in_sky = sesh.query(Posts).filter(Posts.bluesky).filter(
            Posts.post_uuid == post['post_uuid']).scalar() is not None
        if post_in_sky:
            print(f"This post exists in DB and "
                  f"posted to Bluesky:  {post['title']}")
        else:
            # send post to Bluesky
            print("Sending post to Bluesky")
            sent_sky_post = send_post_to_sky(
                title=post['title'],
                link=post['url'],
                description=post['excerpt'],
                image_url=post['feature_image']
            )
            if sent_sky_post:
                # Update the DB we posted this to Bluesky already
                p = sesh.query(Posts).filter(Posts.post_uuid == post['post_uuid']).first()
                p.bluesky = True
                sesh.add(p)
                sesh.commit()

            # Going to sleep between 5 and 30 min
            # to avoid getting rate limited or banned
            # on Bluesky
            random_sleep(min_minutes=5, max_minutes=30)

    # finish
    print("FINISHED SENDING TO SOCIAL MEDIA")


if __name__ == '__main__':
    main()