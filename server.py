"""

This file creates the discord bot. This doesn't need to be modified anymore.

"""

import os
import discord
import json
from discord import User

from dotenv import load_dotenv
from discord.ext import commands

token = os.environ['DISCORD_TOKEN']

client = commands.Bot(command_prefix='/')

fp = open("investors.json", "a")
investor_data = json.load(fp)
investors = []

"""
Event listeners:
"""


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.watching, name ="The Market"))


@client.event
async def on_message(message):
    com = message.content
    ctx = client.get_context(message)
    unique_id = message.author.id

    if com == "/create_portfolio":
        if unique_id in investor_data:

        else:
            return


    elif com == "/view_portfolio":
        return

    elif com == "/buy":
        return

    elif com == "/sell":
        return

    else:




"""
Load all cogs:
"""

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# This starts the bot
client.run(token)


fp.write(json.dumps(investor_data))
fp.close()
