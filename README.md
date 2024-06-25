# ghost_blog_sync

This is a little app that will grab blog posts from my Ghost blog and then post them to social media via APIs

### Social Media Supported

- [x] Warpcast (cast_it.py)
- [x] Twitter (twit_it.py)
- [x] Mastodon (toot_it.py)
- [x] ~~BlueSky (sky_it.py)~~ _Accidently caused my account to get banned, so disabling._
- [] Threads (?? not sure if this is possible nicely ??)
- [] LinkedIn (?? Do I bother with LI ??)

## The Setup

You will need API keys from your Ghost blog,and social media accounts

### API Key authentication setup:

- Copy `env-example` to `.env`
- Read the `.env` file as it point to where to get the keys
- Edit it for your setup
- Source it `source .env`

### Python setup:

- Clone the repo: `git clone https://github.com/BitsofJeremy/ghost_blog_sync.git`
- Change into the directory: `cd ghost_blog_sync`
- Create a virtual environment: `virtualenv -p python3 venv`
- Source it: `source venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`

### Run it:

- Create a minimal database: `python db_models.py`
- Run the sync: `python blog_sync.py`

### Extra: Individual Script Functionality INCLUDED!

Just want to Tweet? 

`python twit_it.py --send "Test from Python"`

Just want to Toot?

`python toot_it.py --send "Test from Python"`

Just want to Cast?

`python cast_it.py --send "Test from Python"`

Just want to post to Bluesky?

`python sky_it.py --send "Test from Python"`

Want to set all your blog posts in Ghost set to member only, or fully public?

_note: currently set to public, change `visibility` to member_

`python update_posts.py`







