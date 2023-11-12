# blog_sync.py

# imports
from db_models import make_session, Posts, Tags
from ghost import get
from twit_it import send_tweet
from toot_it import send_toot
import time


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
            tag_exists = sesh.query(Tags).filter(
                Tags.tag_id == tag['tag_id']).scalar() is not None
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

        # ### TWITTER ### #
        # --- DISABLED ---
        # Check if posts exists and tweeted
        # print(tag_obj_list)
        # post_exists = sesh.query(Posts).filter(Posts.twitter).filter(
        #     Posts.post_uuid == post['post_uuid']).scalar() is not None
        # if post_exists:
        #     print(f"This post exists in DB and "
        #           f"tweeted:  {post['title']}")
        # else:
        #     # Add Post to DB
        #     p = Posts(
        #         post_id=post['post_id'],
        #         post_uuid=post['post_uuid'],
        #     )
        #     p.title = post['title']
        #     p.url = post['url']
        #     p.excerpt = post['excerpt']
        #     p.feature_image = post['feature_image']
        #     # For SQL relations to work,
        #     # need SQL objects in a list
        #     p.tags = tag_obj_list
        #
        #     # Make tags into hashtags
        #     hashtags = ''
        #     for tag in tag_obj_list:
        #         t = make_hashtag(tag.tag_name)
        #         hashtags += f'{t} '
        #     # print(f'Hashtags: \n {hashtags}')
        #
        #     # send post to twitter
        #     print("Sending post to Twitter")
        #     tweet = f"{post['title']} {hashtags} {post['url']}"
        #     # print(f'Tweet Length: {len(tweet)}')
        #     print(tweet)
        #     sent_tweet = send_tweet(status=tweet)
        #     if sent_tweet:
        #         p.twitter = True
        #         sesh.add(p)
        #         sesh.commit()
        #     else:
        #         # Try again some other time. Next run.
        #         sesh.add(p)
        #         sesh.commit()
        #     # Going to sleep for 45 seconds to not
        #     # get rate limited on twitter API
        #     time.sleep(45)

        # ### MASTODON ### #

        # Check if posts exists and tooted
        # print(tag_obj_list)
        post_exists = sesh.query(Posts).filter(Posts.mastodon).filter(
            Posts.post_uuid == post['post_uuid']).scalar() is not None
        if post_exists:
            print(f"This post exists in DB and "
                  f"tooted:  {post['title']}")
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

            # Make tags into hashtags
            hashtags = ''
            for tag in tag_obj_list:
                t = make_hashtag(tag.tag_name)
                hashtags += f'{t} '
            # print(f'Hashtags: \n {hashtags}')

            # send post to mastodon
            print("Sending post to Mastodon")
            toot = f"{post['title']} {hashtags} {post['url']}"
            # print(f'toot Length: {len(toot)}')
            print(toot)
            sent_toot = send_toot(status=toot)
            if sent_toot:
                p.mastodon = True
                sesh.add(p)
                sesh.commit()
            else:
                # Try again some other time. Next run.
                sesh.add(p)
                sesh.commit()
            # Going to sleep for 45 seconds to not
            # get rate limited on mastodon API
            time.sleep(45)

    # finish
    print("FINISHED")


if __name__ == '__main__':
    main()
