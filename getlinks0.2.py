import requests
import getpass
import praw

# Get credentials
USERNAME = input('Enter your reddit account login: ')
PASSWORD = getpass.getpass('Enter your reddit account login: ')

# Developer info for authorization
CLIENT_ID = 'YOUR REDDIT APP USE SCRIPT ID (https://www.reddit.com/prefs/apps)'
SECRET_TOKEN = 'YOUR REDDIT APP SECRET_TOKEN (https://www.reddit.com/prefs/apps)'

# Note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

# Here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD}

# Setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'GetLinksRedditv0.1 by u/HefteBHyk'}

# Send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# Convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# Add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
# While the token is valid (~2 hours) we just add headers=headers to our requests

# Get RefreshToken as user to retrieve info
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET_TOKEN,
    password=PASSWORD,
    user_agent="GetLinksRedditv0.1 by u/HefteBHyk",
    username=USERNAME,
)

# Retrieve the links from the list of saved items

with open('Saved_Links_From_Reddit.md', 'w', encoding='utf-8') as saved_links_md_file:
    # For submissions/items in saved reddit topics
    for item in reddit.user.me().saved(limit=None):
        saved_links_md_file.write('['+item.title+']'+'(https://reddit.com'+item.permalink+')\n...\n\n')
    saved_links_md_file.close()
