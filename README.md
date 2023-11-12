# ghost_blog_sync

This is a little script that will grab Ghost blog posts and the post them to Twitter via APIs

Note: Twitter functionality has been disabled.

## The Setup

You will need some key from your Ghost blog, Twitter, and the Mastodon instance you live in.

_note: I am choosing to keep the cross-posting to a minimum_ 

### API Key authentication setup:

- Copy `env-example` to `.env`
- Read the `.env` file as it point to where to get the keys
- Edit it for your setup
- Source it `source .env`

### Python setup:

- Clone the repo: `git clone https://gitlab.com/abvavgjeremy/ghost_blog_sync.git`
- Change into the directory: `cd ghost_blog_sync`
- Create a virtual environment: `virtualenv -p pytho3 venv`
- Source it: `source venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`

### Run it:

- Create a minimal DB: `python db_models.py`
- Run the sync: `python blog_sync.py`

### Extras

Just want to Tweet? 

`python twit_it.py --send "Test from Python"`

Just want to Toot?

`python toot_it.py --send "Test from Python"`

Want to set all your posts to member only, or public?

_note: currently set to public, change visibility to member_

`python update_posts.py`







