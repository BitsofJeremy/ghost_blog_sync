# Ghost Blog Sync

Welcome to Ghost Blog Sync! This Python application helps you automatically share your Ghost blog posts on various social media platforms.

## Supported Social Media Platforms

- [x] Twitter
- [x] Warpcast
- [x] Bluesky
- [ ] Mastodon (currently disabled, but can be re-enabled)

## Getting Started

### Prerequisites

Before you begin, make sure you have the following installed on your system:

- Python 3.7 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

### Installation

1. Clone the repository or download the project files:
   ```
   git clone https://github.com/BitsofJeremy/ghost_blog_sync.git
   ```
   If you don't have Git, you can download the ZIP file and extract it.

2. Navigate to the project directory:
   ```
   cd ghost_blog_sync
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```
   This creates an isolated Python environment for the project.

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Configuration

1. Copy the example environment file:
   ```
   cp env-example .env
   ```

2. Open the `.env` file in a text editor and fill in your API keys and credentials for Ghost and the social media platforms you want to use. The file contains instructions on where to find these keys.

3. Save and close the `.env` file.

## Usage

1. Create the initial database:
   ```
   python db_models.py
   ```
   This sets up a SQLite database to store information about your blog posts.

2. Run the sync script:
   ```
   python blog_sync.py
   ```
   This script will fetch your Ghost blog posts and share them on the configured social media platforms.

### Individual Platform Posting

You can also post to individual platforms using these commands:

- Twitter: `python twit_it.py --send "Your message here"`
- Warpcast: `python cast_it.py --send "Your message here"`
- Bluesky: `python sky_it.py --title "Your title" --link "https://your-link.com" --description "Your description"`

## Customization

- To enable Mastodon posting, uncomment the relevant section in `blog_sync.py`.
- You can adjust the sleep times between posts in `blog_sync.py` to avoid rate limiting.

## Troubleshooting

If you encounter any issues:

1. Make sure your `.env` file is correctly filled out.
2. Check that your virtual environment is activated when running scripts.
3. Ensure you have the latest version of the code and have installed all requirements.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [GNU Affero General Public License v3.0](LICENSE).