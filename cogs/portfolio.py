"""
This file holds the definition of the Portfolio class
"""

import discord
import json
import market

from discord.ext import commands


class Portfolio:

    def __init__(self, bp=100000.0, pv=100000.0, owned=None):
        if owned is None:
            owned = {}
        self.buying_power = bp
        self.portfolio_value = pv
        self.owned_stocks = owned
        self.market = market.Market  # TODO Global market

    # Finished function
    def get_quantity(self, ticker_name):
        return self.owned_stocks.get(ticker_name, 0)

    # Finished function
    def get_buying_power(self):
        return self.buying_power

    def get_portfolio_value(self):
        value = 0
        for ticker in self.owned_stocks:
            quantity = self.owned_stocks[ticker]
            market_value = 5.05  # TODO Get market value
            value += (quantity * market_value)
        return value + self.buying_power

    def bought(self, ticker, quantity):
        market_value = 5.05  # TODO Get market value
        total_cost = quantity * market_value

        # Buy using buying power then increment amount owned
        self.buying_power -= total_cost
        if ticker in self.owned_stocks:
            self.owned_stocks[ticker] += quantity
        else:
            self.owned_stocks[ticker] = quantity

        return

    def sold(self, ticker, quantity):
        market_value = 5.05  # TODO Get market value
        sold_for = quantity * market_value
        self.buying_power += sold_for
        self.owned_stocks[ticker] -= quantity

    def encode(self):
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
