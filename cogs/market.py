"""

This file will store all stock market commands

"""

import discord

from discord.ext import commands

class Market(commands.Cog):

    def __init__(self, client):
        self.client = client

    # TODO Write market commands here


def setup(client):
    client.add_cog(Market(client))