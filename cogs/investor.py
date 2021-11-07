"""

This file will store all data in portfolio

"""

import discord

from discord.ext import commands

class Investor(commands.Cog):

    def __init__(self, client):
        self.client = client

    # TODO: Data members and methods


def setup(client):
    client.add_cog(Investor(client))
