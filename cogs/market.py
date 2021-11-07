"""

This file will store all stock market commands

"""

import discord

from discord.ext import commands


class Market:

    def __init__(self):
        return

    def test(self, ctx, arg1=None, arg2=None):
        await ctx.send(f"TEST {arg1} {arg2}")
