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
    async def buy(self, ctx, ticker, quantity):
        market_value = 5.00 # TODO Get stock price
        required_funds = market_value * quantity
        portfolio_exists =  # TODO check if exists
        in_market_hours = ... # TODO get time
        stock_exists = ... # TODO check if stock exists
        cost = ... # TODO get total cost
        buying_power = self.portfolio.GetBuyingPower()

        if quantity == 0:
            await ctx.send(f"\
                I'm sorry, but you can't buy 0 shares \
                of a stock.\
            ")
            return

        elif not portfolio_exists:
            await ctx.send(f"\
                I'm sorry, but your portfolio couldn't be found. \
                Please make a portfolio before trading by \
                executing the createPortfolio command.\
            ")
            return

        elif not in_market_hours:
            await ctx.send(f"\
                I'm sorry, but your order to sell {quantity} shares\
                of {ticker} couldn't be completed. Available market\
                hours are M-F 9:30AM until 4:00PM, EST.\
                ")
            return

        elif not stock_exists:
            await ctx.send(f"\
                I'm sorry, but {ticker} couldn't be found.\
            ")
            return

        elif required_funds > buying_power:
            await ctx.send(f"\
                I'm sorry, but you don't have enough funds to \
                purchase {quantity} shares of {ticker}, which would \
                cost {cost}. Your available buying power is \
                {buying_power}.\
            ")
            return

        else: # TODO prompt for confirmation
            self.portfolio.Bought(ticker, quantity)
            await ctx.send(f"\
                Your order to purchase {quantity} shares of \
                {ticker} executed successfully. You now own \
                {self.portfolio.GetQuantity(ticker)} shares.\
            ")
            return

        return

    @commands.command()
    async def sell(self, ctx, ticker, quantity):
        avail_to_sell = self.portfolio.GetQuantity(ticker)
        in_market_hours = ... # TODO check if market hours
        has_portfolio = ... # TODO check if has portfoliio

        if quantity == 0:
            await ctx.send(f"\
                I'm sorry, but you can't sell 0 shares \
                of a stock.\
            ")

        elif not has_portfolio: # TODO check if exists
            await ctx.send(f"\
                I'm sorry, but your portfolio couldn't be found. \
                Please make a portfolio before trading by \
                executing the createPortfolio command.")
            return

        elif not in_market_hours: # TODO check if market hours
           await ctx.send(f"\
                I'm sorry, but your order to sell {quantity} shares\
                of {ticker} couldn't be completed. Available market\
                hours are M-F 9:30AM until 4:00PM, EST.\
           ")
           return

        elif avail_to_sell < quantity:
            await ctx.send(f"\
                I'm sorry, but your order to sell {quantity} shares of {ticker} couldn't be completed. Your portfolio only contains {avail_to_sell} shares of {ticker}.\
            ")
            return
        
        else: # TODO Ask for confirmation
            avg_price = ...  # TODO avg sale price
            self.portfolio.Sold(ticker, quantity)
            await ctx.send(f"\
                Your order to sell {quantity} shares of \
                {ticker} was executed successfully, for an \
                average price of {avg_price}.\
            ")
            return

        return

    @commands.command()
    async def viewPortfolio(self, ctx):
        blob = self.portfolio.Encode()
        port_info = json.loads(blob)
        buying_power = port_info["buying_power"]
        port_value = port_info["portfolio_value"]
        stocks = port_info["owned_stocks"]

        output = "Buying power: {buying_power}\n"
        output += "Portfolio Value: {port_value}\n"

        for ticker in stocks:
            output += "{ticker}: {stocks[ticker]} shares"
        
        await ctx.send(output)
        return

    # TODO create a portfolio
    @commands.command()
    async def createPortfolio(self, ctx):
        return


def setup(client):
    client.add_cog(Investor(client))
