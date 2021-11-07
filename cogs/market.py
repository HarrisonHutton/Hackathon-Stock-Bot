"""

This file will store all stock market commands

"""

import discord

from discord.ext import commands


class Market(commands.Cog):

    def __init__(self, client):
        self.client = client

    # TODO Write market commands here

    @commands.command()
    async def test(self, ctx, arg1=None, arg2=None):
        await ctx.send(f"TEST {arg1} {arg2}")


def setup(client):
    client.add_cog(Market(client))
