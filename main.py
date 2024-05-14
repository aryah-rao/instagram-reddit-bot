'''
Aryah Rao
main.py
October 2023
This file scrapes pictures from the internet and posts on an instagram account.
'''

import json
import time
import os
from instagrapi import Client
from instagrapi.exceptions import ClientError
import praw
import requests

# Limits
REDDIT_LIMIT = 7
POST_LIMIT = 2

# Clean up
def clean_up():
    "removes all .jpg files in the current directory"
    current_directory = os.getcwd()
    for file_name in os.listdir(current_directory):
        # check if the file ends with .jpg
        if file_name.endswith('.jpg'):
            file_path = os.path.join(current_directory, file_name)
            os.remove(file_path)

# Get instagram credentials
def get_instagram_creds(source):
    """
    reads credentials from a JSON file and returns the subreddit,
    username, and password for the Instagram account
    """
    dirname="."
    filename="creds.json"
    with open(os.path.join(dirname, filename), encoding='utf-8') as f:
        D = json.load(f)
        instagram = D[source]

    return instagram["subreddit"], instagram["username"], instagram["password"]

# Get reddit credentials
def get_reddit_creds():
    """
    reads credentials for Reddit from a JSON file and returns
    the client ID, client secret, username, password, and user
    agent for the Reddit account
    """
    dirname="."
    filename="creds.json"
    with open(os.path.join(dirname, filename), encoding='utf-8') as file:
        dict_json = json.load(file)
        reddit = dict_json["reddit"]

    return reddit["reddit_client_id"], reddit["reddit_client_secret"], \
        reddit["reddit_username"], reddit["reddit_password"], reddit["reddit_user_agent"]

# Get the 'hot' posts from 'meirl' subreddit
def get_reddit_post(reddit, reddit_subreddit_name, reddit_limit):
    """
    searches for hot posts on the specified subreddit on Reddit that have a .jpg image
    attached to them, and returns a list of posts that have not been uploaded before
    """
    hot_posts = reddit.subreddit(reddit_subreddit_name)\
        .search(query='url:jpg', sort='hot', limit=reddit_limit)

    return [post for post in hot_posts if not is_post_uploaded(post.id)]

# Check if the post has been uploaded before
def is_post_uploaded(post_id):
    """
    checks if the specified post ID is in the text file of uploaded post IDs,
    and returns True if it is, False otherwise
    """
    with open("uploaded_posts.txt", "r", encoding='utf-8') as f:
        uploaded_posts = f.read().splitlines()

        return post_id in uploaded_posts

# Mark the post as uploaded
def mark_post_uploaded(post_id):
    """
    appends the specified post ID to the text file of uploaded post IDs
    """
    with open("uploaded_posts.txt", "a", encoding='utf-8') as f:
        f.write(post_id + "\n")

# Upload images to instagram
def upload_instagram(instagram_client, hot_posts, reddit_subreddit_name, post_limit):
    """
    downloads the .jpg image from each post in the list of hot posts,
    adds a caption to the image containing the post title and author's username,
    and posts the image on Instagram using the specified client. It also marks
    each post as uploaded by appending its ID to the text file of uploaded post IDs.
    """
    try:
        for i in range(post_limit):
            post = hot_posts[i]
            try:
                # Download the image from the post
                image_url = post.url
                image_file = requests.get(image_url, timeout=7).content
                image_filename = post.id + ".jpg"

                # Get the title of the top post
                post_title = post.title

                # Get the username of the author of the top post
                post_author = post.author.name

                # Save the image in the local file system
                with open(image_filename, "wb") as handler:
                    handler.write(image_file)

                # Add caption to the post
                caption = f"{post_title}\
                    \n\nMirrored from a post on /r/{reddit_subreddit_name} by /u/{post_author}"

                # Post the image on Instagram
                instagram_client.photo_upload(image_filename, caption)
                print(f"\nUploaded post {post.id}: {caption}\n")

                # Mark the post as uploaded
                mark_post_uploaded(post.id)

            except ClientError as exception:
                if "429" in str(exception):
                    print("Too many requests. Waiting for 10 minutes...")
                    time.sleep(600)  # Wait for 10 minutes and try again
                elif "302" in str(exception):
                    print("Instagram detected suspicious  activity, check account.")
                else:
                    print(exception)
    except IndexError:
        print("No valid posts found.")

# Main function
def main():
    """
    authenticates the Reddit and Instagram accounts using the credentials,
    scrapes hot posts from Reddit and posts them on Instagram,
    saves the sessioncookies for the Instagram account, and cleans
    up the local directory by removing all .jpg files.
    """

    print("****************************************************************************")
    print("Initializing meirl bot.")
    print("****************************************************************************")

    # Authenticate Reddit
    print("Getting Reddit credentials...")
    reddit_client_id, reddit_client_secret, reddit_username, \
        reddit_password, reddit_user_agent = get_reddit_creds()
    reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     username=reddit_username,
                     password=reddit_password,
                     user_agent=reddit_user_agent)

    # Authenticate Instagram
    print("Getting Instagram credentials...")
    reddit_subreddit, instagram_username, instagram_password=get_instagram_creds("instagram_meirl")
    instagram_client_meirl = Client()

    print("Authenticated Reddit and Instagram.")

    # Try to load the session cookies from file
    if os.path.isfile("cookies_meirl.json"):
        instagram_client_meirl = Client(json.load(open('cookies_meirl.json', encoding='utf-8')))
        print("Instagram session details loaded.")

    # Login if not already logged in
    if instagram_client_meirl.username is None:
        instagram_client_meirl.login(instagram_username, instagram_password)
        print("Logged into Instagram using username/password.")

    # Upload posts
    print("Validating posts...")
    hot_posts = get_reddit_post(reddit, reddit_subreddit, REDDIT_LIMIT)
    upload_instagram(instagram_client_meirl, hot_posts, reddit_subreddit, POST_LIMIT)

    # Save the session cookies to file
    json.dump(
    instagram_client_meirl.get_settings(),
    open('cookies_meirl.json', 'w', encoding='utf-8'))

    # Clean up
    print("Cleaning up images...")
    clean_up()
    print("Cleaned up .jpg files.")
    print("Instagram uploader has finished successfully!\n")

main()
