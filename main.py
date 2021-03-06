import os
import json
import discord
from discord.ext import commands
from recghub import make_issue

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
        try:
            await make_issue(reaction.message.content.split('。')[0], reaction.message.content+' '+reaction.message.jump_url)
        except:
            pass

client.run(token)