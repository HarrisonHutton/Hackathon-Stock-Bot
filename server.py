"""

This file creates the discord bot. This doesn't need to be modified anymore.

"""

import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

token = os.environ['DISCORD_TOKEN']

client = commands.Bot(command_prefix='/')

"""
Event listeners:
"""

@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')
  await client.change_presence(activity=discord.Activity(type = discord.ActivityType.watching, name ="The Market"))


"""
Commands:
"""

@client.command()
async def load(ctx, extension):
  if str(ctx.author.id) in ['287790861939376128', '214184731158249473', '551134962259329034', '252185844956266497']:
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'```Commands in {extension}.py have been loaded.```')
  else:
    await ctx.send(f'```You do not have permission to edit commands.```')


@client.command()
async def unload(ctx, extension):
  if str(ctx.author.id) in ['287790861939376128', '214184731158249473', '551134962259329034', '252185844956266497']:
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'```Commands in {extension}.py have been unloaded.```')
  else:
    await ctx.send(f'```You do not have permission to edit commands.```')


@client.command()
async def reload(ctx, extension):
  if str(ctx.author.id) in ['287790861939376128', '214184731158249473', '551134962259329034', '252185844956266497']:
    client.reload_extension(f'cogs.{extension}')
    await ctx.send(f'```Commands in {extension}.py have been reloaded.```')
  else:
    await ctx.send(f'```You do not have permission to edit commands.```')


"""
Load all cogs:
"""

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

# This starts the bot
client.run(token)