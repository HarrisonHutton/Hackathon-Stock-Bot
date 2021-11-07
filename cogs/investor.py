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
        self.portfolio = ... #TODO


    # TODO: Store encoded data [instead of?] returning
    def Encode(self):
      portfolio_json=self.portfolio.Encode()
      temp_dict={self.id:portfolio_json}
      return json.dumps(temp_dict)

    # TODO for this command:
    # Implement market API call
    # Get time
    @commands.command()
    def buy(self, ctx, ticker, quantity):
        market_value = ... # TODO Get stock price
        required_funds = market_value * quantity

        if quantity == 0:
            return # TODO: Bot output

        # elif portfolio does not exist # TODO Check if exists
        #   return # TODO Bot output

        # elif market hours # TODO Time function
        #   return # TODO Bot output

        # elif stock does not exist # TODO API call
        #   return # TODO Bot output

        elif required_funds > self.buying_power:
            return # TODO Bot output
        else:
            self.portfolio.Bought(ticker, quantity)

        return

    @commands.command()
    def sell(self, ctx, ticker, quantity):
        return

    @commands.command()
    def viewPortfolio(self, ctx):
        return

    @commands.command()
    def createPortfolio(self, ctx):
        return


def setup(client):
    client.add_cog(Investor(client))
