"""

This file will store all data in Investor

"""

import discord
import json

from discord.ext import commands

class Investor(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.id = ... # TODO 
        self.portfolio= ... #TODO


    def Encode(self):
      portfolio_json=self.portfolio.Encode()
      temp_dict={self.id:portfolio_json}
      return json.dumps(temp_dict)
    # TODO: Data members and methods


def setup(client):
    client.add_cog(Investor(client))
