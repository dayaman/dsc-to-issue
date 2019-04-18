import os
import json
import discord
import aiohttp
import asyncio
import async_timeout
from discord.ext import commands
from datetime import datetime, timedelta

# Discord アクセストークン読み込み
with open('token.json') as f:
    df = json.load(f)

token = df['bot']
manager = int(df['manager_id'])
ghub_u = df['ghub_user']
ghub_t = df['ghub_token']
repo = df['repo']

client = discord.Client()

@client.event
async def on_ready():
    # ログインギルドのカスタム絵文字を取得、emojiが50個あるか、「issue」があればスルー、なければ作る
    for guild in client.guilds:
        is_issue = False
        for emoji in guild.emojis:
            if emoji.name == 'issue':
                is_issue = True
        if is_issue == False:
            path = 'images/issue.png'
            if os.path.isfile(path):
                with open(path, mode='rb') as f:
                    try:
                        await guild.create_custom_emoji(name='issue', image=f.read(), reason='for issueBOT')
                    except discord.errors.HTTPException:
                        pass

@client.event
async def on_reaction_add(reaction, user):
    if user.id != manager:
        return

    if reaction.emoji.name == 'issue':
        await make_issue(reaction.message.content.split('。')[0], reaction.message.content+' '+reaction.message.jump_url)

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
                pass
            
            return await response.read()

client.run(token)