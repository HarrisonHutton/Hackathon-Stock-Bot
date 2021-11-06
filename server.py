"""

This file creates the discord bot

"""

import os
import discord

from discord.ext import commands

token = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='-')

"""
Event listeners:
"""

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')
  await client.change_presence(activity=discord.Activity(type = discord.ActivityType.watching, name ="The Market"))