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
    for guild in client.guilds:
        is_issue = False
        print(len(guild.emojis))
        for emoji in guild.emojis:
            if emoji.name == 'issue':
                is_issue = True
        print(is_issue)
        if is_issue == False:
            path = 'images/issue.png'
            if os.path.isfile(path):
                with open(path, mode='rb') as f:
                    print('絵文字追加')
                    # issue_emoji = discord.File(f)
                    await guild.create_custom_emoji('issue', f, reason='for issueBOT')
                    print('追加完了')
            

client.run(token)