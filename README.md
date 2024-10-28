# Reddit to Instagram Bot

![Python](https://img.shields.io/badge/Python-100%25-blue)
![License](https://img.shields.io/badge/License-MIT-green)

This project is a Python script that scrapes hot posts from a specified subreddit on Reddit, downloads the associated images, and posts them on Instagram with appropriate captions. It automates the process of curating content from Reddit and sharing it on Instagram.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup](#setup)
4. [Usage](#usage)
5. [Acknowledgements](#acknowledgements)
6. [License](#license)

## Features

- Scrapes hot posts from a specified subreddit on Reddit
- Filters posts to include only those with .jpg images
- Downloads the images from the selected posts
- Generates captions for Instagram posts using the post title and author's username
- Uploads the images to Instagram with the generated captions
- Keeps track of uploaded posts to avoid duplicates
- Handles Instagram's rate limiting and other errors gracefully
- Saves and loads Instagram session cookies for efficient authentication

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.x installed
- Required Python packages: `instagrapi`, `praw`, `requests`
- Reddit API credentials (client ID, client secret, username, password, user agent)
- Instagram account credentials (username, password)

## Setup

1. **Clone the repository:** 
   ```bash
   git clone https://github.com/aryah-rao/instagram-reddit-bot.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd instagram-reddit-bot
   ```

3. **Install the required Python packages:**
   ```bash
   pip install instagrapi praw requests
   ```

4. **Create a `creds.json` file in the project directory with the following structure:**
   ```json
   {
     "reddit": {
       "reddit_client_id": "your_reddit_client_id",
       "reddit_client_secret": "your_reddit_client_secret",
       "reddit_username": "your_reddit_username",
       "reddit_password": "your_reddit_password",
       "reddit_user_agent": "your_reddit_user_agent"
     },
     "instagram": {
       "subreddit": "subreddit_name",
       "username": "your_instagram_username",
       "password": "your_instagram_password"
     }
   }
   ```
   Replace the placeholders with your actual Reddit and Instagram credentials.

5. **Adjust the REDDIT_LIMIT and POST_LIMIT variables in the script to control the number of posts to scrape from Reddit and the number of posts to upload on Instagram, respectively:**
   ```python
   REDDIT_LIMIT = 10  # Number of posts to scrape from Reddit
   POST_LIMIT = 5     # Number of posts to upload to Instagram
   ```

## Usage

To run the bot, execute the following command in the project directory:
```bash
python meirl_bot.py
```

The script will authenticate with Reddit and Instagram, scrape hot posts from the specified subreddit, download the images, generate captions, and upload the posts to Instagram. It will also save the uploaded post IDs to avoid duplicates and clean up the downloaded images after the upload is complete.

## Acknowledgements
This project utilizes the following libraries:

- Instagrapi - A Python wrapper for the Instagram Private API
- PRAW - Python Reddit API Wrapper
- Requests - A simple HTTP library for Python

## License
This project is open-source and available under the MIT License.
