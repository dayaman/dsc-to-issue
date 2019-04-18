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
    print('We have logged in as {0.user}'.format(client))

client.run(token)