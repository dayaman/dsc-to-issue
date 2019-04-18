import json
import aiohttp
import asyncio
import async_timeout
from datetime import datetime, timedelta

with open('token.json') as f:
    df = json.load(f)

ghub_u = df['ghub_user']
ghub_t = df['ghub_token']
repo = df['repo']

async def make_issue(title, body, labels=[]):
    url = 'https://api.github.com/repos/{}/{}/issues'.format(ghub_u, repo)
    auther = aiohttp.BasicAuth(ghub_u, ghub_t)
    async with aiohttp.ClientSession(auth=auther) as session:
        issue = {'title': title,
                 'body': body,
                 'labels': labels}
        response = await fetch(session, url, json.dumps(issue))
        return response

async def fetch(session, url, data_json):
    with async_timeout.timeout(10):
        async with session.post(url, data=data_json) as response:
            
            if response.status != 201:
                print(response.status)
                exit()
            
            return await response.read()
