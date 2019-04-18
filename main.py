import os
import json
import discord
from discord.ext import commands

# Discord アクセストークン読み込み
with open('token.json') as f:
    df = json.load(f)

token = df['bot']
manager = int(df['manager_id'])

client = discord.Client()

@client.event
async def on_ready():
    # ログインギルドのカスタム絵文字を取得、emojiが50個あるか、「issue」があればスルー、なければ作る
    for guild in bot.guilds:
        is_issue = False
        if len(guild.emojis) == 50:
            is_issue = True
        for emoji in guild.emojis:
            if emoji.name == 'issue':
                is_issue = True
        if is_issue == False:
            path = 'images/issue.png'
            if os.path.isfile(path):
                with open(path, mode='rb') as f:
                    # issue_emoji = discord.File(f)
                    await guild.create_custom_emoji('issue', f, reason='for issueBOT')
            

client.run(token)