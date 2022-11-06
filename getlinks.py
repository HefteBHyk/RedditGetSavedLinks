import requests
import credentials
import praw

# Get credentials
(USERNAME,PASSWORD) = credentials.recordcredentials()

# DoubleCheck if credentials file is okay
while True:
    # Check if username or password is empty
    if not USERNAME or not PASSWORD:
        print('Login or password is empty. Repeat the entry.')
        credentials.os.remove('login_info_for_reddit.txt')
        #Repeat until the file created correctly
        (USERNAME,PASSWORD) = credentials.recordcredentials()
        continue
    else:
        break

# Developer info for authorization
CLIENT_ID = 'UW6v9vZGoV8FqnrE5-O2oQ'
SECRET_TOKEN = 'CjXGFW8_e0g9PaLK4lVziI_A1zLO2w'

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

with open('Saved_Links_From_Reddit.md','w',encoding='utf-8') as saved_links_md_file:
    # For submissions/items in saved reddit topics
    for item in reddit.user.me().saved(limit=None):
        saved_links_md_file.write('['+item.title+']'+'(https://reddit.com'+item.permalink+')\n...\n\n')
    saved_links_md_file.close()