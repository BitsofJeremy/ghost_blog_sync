import os
import time
from dotenv import load_dotenv
from atproto import Client
import random

# Load environment variables
load_dotenv()

# Bluesky credentials
BLUESKY_USERNAME = os.getenv('BLUESKY_USERNAME')
BLUESKY_PASSWORD = os.getenv('BLUESKY_PASSWORD')


def random_delay(min_seconds=5, max_seconds=15):
    """Generate a random delay between min_seconds and max_seconds."""
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Waiting for {delay:.2f} seconds...")
    time.sleep(delay)


def get_all_posts(client):
    """Fetch all posts from the user's feed."""
    cursor = None
    all_posts = []

    while True:
        try:
            response = client.get_author_feed(client.me.did, cursor=cursor, limit=100)
            all_posts.extend(response.feed)

            if not response.cursor:
                break

            cursor = response.cursor
            random_delay(10, 20)  # Delay between pagination requests
        except Exception as e:
            print(f"Error fetching posts: {e}")
            random_delay(30, 60)  # Longer delay on error

    return all_posts


def delete_posts(client, posts):
    """Delete all given posts."""
    for post in posts:
        try:
            success = client.delete_post(post.post.uri)
            if success:
                print(f"Deleted post: {post.post.uri}")
            else:
                print(f"Failed to delete post: {post.post.uri}")
            random_delay()  # Delay between delete operations
        except Exception as e:
            print(f"Error deleting post {post.post.uri}: {e}")
            random_delay(30, 60)  # Longer delay on error


def main():
    client = Client()
    try:
        client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)
        print("Logged in successfully.")

        print("Fetching all posts...")
        all_posts = get_all_posts(client)
        print(f"Found {len(all_posts)} posts.")

        print("Starting to delete posts...")
        delete_posts(client, all_posts)

        print("Finished deleting all posts.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
