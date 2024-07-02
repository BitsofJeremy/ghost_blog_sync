import argparse
import os
import sys
import requests
from dotenv import load_dotenv
from atproto import Client, models

load_dotenv()

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


def send_post_to_sky(title, link, description="", image_url=None):
    """Sends a post to Bluesky with title, link, description, and optionally an image"""
    try:
        # If an image URL is provided, download and upload it
        thumb = None
        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                img_data = response.content
                thumb = client.upload_blob(img_data)

        # Create the embed
        embed = models.AppBskyEmbedExternal.Main(
            external=models.AppBskyEmbedExternal.External(
                title=title,
                description=description,
                uri=link,
                thumb=thumb.blob if thumb else None
            )
        )

        # Create the post text
        post_text = f"{title}\n\n{link}"

        # Send the post
        post = client.send_post(text=post_text, embed=embed)

        print(f"Post sent successfully: {post}")
        return True
    except Exception as e:
        print(f"Error sending post: {e}")
        return False


def main(title, link, description="", image_url=None):
    send_post_to_sky(title, link, description, image_url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', help='Post title', required=True)
    parser.add_argument('--link', help='Post link', required=True)
    parser.add_argument('--description', help='Post description', default="")
    parser.add_argument('--image', help='Featured image URL', required=False)

    args = parser.parse_args()
    main(args.title, args.link, args.description, args.image)
    sys.exit(0)