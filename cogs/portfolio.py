"""
This file holds the definition of the Portfolio class
"""

import discord
import json

from discord.ext import commands


class Portfolio(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.buying_power = ...
        self.portfolio_value = ...
        self.owned_stocks = ...

    # Finished function
    async def GetQuantity(self, ticker_name):
        return self.owned_stocks.get(ticker_name, 0)

    # Finished function
    async def GetBuyingPower(self):
        return self.buying_power
    
    # TODO for this function:
    # Replace market_value with the actual market value, probably
    # from an API call
    async def GetPortfolioValue(self):
        value = 0
        for ticker in self.owned_stocks:
            quantity = self.owned_stocks[ticker]
            market_value = ... # call to API
            value += (quantity * market_value)
        return value + self.buying_power

    # TODO Bot output
    # Error-checking handled in Investor class
    @commands.command()
    async def Bought(self, ctx, ticker, quantity):
        market_value = ... # call to API
        total_cost = quantity * market_value

        # Buy using buying power then increment amount owned
        self.buying_power -= total_cost
        if ticker in self.owned_stocks:
            self.owned_stocks[ticker] += quantity
        else:
            self.owned_stocks[ticker] = quantity

        return

    # TODO Bot output
    # Error-checking handled in Investor class
    @commands.command()
    async def Sold(self, ctx, ticker, quantity):
        market_value = ... # call to API
        sold_for = quantity * market_value
        self.buying_power += sold_for
        self.owned_stocks[ticker] -= quantity

    # Finished. Returns encoded portfolio data
    def Encode(self):
        encoded = {
            "buying_power": self.buying_power,
            "portfolio_value": self.portfolio_value,
            "owned_stocks": self.owned_stocks
        }
        return json.dumps(encoded)


# Stored in JSON file or database:
# {
#   "1243454": {
#        "buying_power": 23523.56,
#        "portfolio_value": 110244.77,
#        "owned_stocks": {
#           "AAPL": 100,
#           "TSLA": 355,
#           "IBM": 303
#       }
#   }
# }

def setup(client):
    client.add_cog(Portfolio(client))
