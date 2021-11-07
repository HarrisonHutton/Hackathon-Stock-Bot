import os

import discord
import json
import datetime
import random
from discord.ext import commands
import requests

def is_market_hours():
	d = datetime.datetime.today().weekday()
	h = datetime.time().hour
	m = datetime.time().minute

	allowed_day = (d <= 4)
	allowed_hour = (9 <= h < 4)
	allowed_minute = True
	if h == 9 and m < 30:
		allowed_minute = False

	return allowed_day and allowed_hour and allowed_minute


class Market:

	def __init__(self):
		self.key = os.environ['API_KEY']
		self.date = '2021-11-05'
		self.update_market_date()

		return

	def ticker_price(self, ticker):
		# Alpha Vantage is used for fetching stock price information: https://www.alphavantage.co/
		self.update_market_date()
		url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + ticker + '&outputsize=compact&apikey=' + self.key
		r = requests.get(url)
		if 'Time Series (Daily)' not in r.json().keys():
			return None
		ticker_data = r.json()['Time Series (Daily)'][self.date]['4. close']
		return float(ticker_data)

	def update_market_date(self):
		if datetime.datetime.today().weekday() <= 4:
			self.date = str(datetime.datetime.today())[:10]
		elif datetime.datetime.today().weekday() == 5:
			self.date = str(datetime.datetime.today())[:10]
			self.date = self.date[:9] + str(int(self.date[9]) - 1)
		elif datetime.datetime.today().weekday() == 6:
			self.date = str(datetime.datetime.today())[:10]
			self.date = self.date[:9] + str(int(self.date[9]) - 2)

class Portfolio:

	def __init__(self, bp=100000.0, pv=100000.0, owned=None):
		if owned is None:
			owned = {}
		self.buying_power = int(bp)
		self.portfolio_value = int(pv)
		self.owned_stocks = owned
		self.market = Market  # TODO Global market

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
			market_value = self.market.ticker_price(ticker)
			value += (quantity * market_value)
		return value + self.buying_power

	def bought(self, ticker, quantity):
		market_value = self.market.ticker_price(ticker)
		total_cost = quantity * market_value

		# Buy using buying power then increment amount owned
		self.buying_power -= total_cost
		if ticker in self.owned_stocks:
			self.owned_stocks[ticker] += quantity
		else:
			self.owned_stocks[ticker] = quantity

		return

	def sold(self, ticker, quantity):
		market_value = self.market.ticker_price(ticker)
		sold_for = quantity * market_value
		self.buying_power += sold_for
		self.owned_stocks[ticker] -= quantity
		return market_value

	def get_owned(self):
		return self.owned_stocks

	def total_cost(self, ticker, quantity):
		market_value = self.market.ticker_price(ticker)
		return market_value * quantity

	def serialize(self):
		encoded = {
			"buying_power": self.buying_power,
			"portfolio_value": self.portfolio_value,
			"owned_stocks": self.owned_stocks
		}
		json_blob = json.dumps(encoded)
		return json_blob


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

class Investor(commands.Cog):

	def __init__(self, bot):
		self.client = bot
		self.id = bot.user
		self.portfolio = None
		self.currently_investing = {}

	# TODO: Store encoded data [instead of?] returning
	def serialize(self):
		#portfolio_json = self.portfolio.encode()
		#temp_dict = {self.id: portfolio_json}
		#return json.dumps(temp_dict)
		return json.dumps({})


	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		message = reaction.message
		if str(reaction) not in ['✅', '❌']:
			return False
		if not user.bot:
			if self.currently_investing.get(str(message), '') == str(user.id) and str(reaction) == '✅':
				await message.channel.send(f'{user.name} has confirmed their purchase.')
			elif self.currently_investing.get(str(message), '') == str(user.id) and str(reaction) == '❌':
				await message.channel.send(f'{user.name} has canceled their purchase.')
			else:
				return False


	# TODO for this command:
	# Implement market API call
	@commands.command()
	async def buy(self, ctx, ticker=None, quantity=None):
		portfolio_exists = (self.portfolio is not None)

		if ticker is None or quantity is None:
			await ctx.send(f"\
				The buy command takes both a ticker symbol and a quantity. Please try again.\
			")
			return

		try:
			int(quantity)
		except ValueError:
			await ctx.send("I'm sorry, but the quantity you entered is not valid.")
			return

		if not ticker.isalpha():
			await ctx.send("I'm sorry, but the ticker you entered is not valid.")
			return

		elif not portfolio_exists:
			await ctx.send(f"\
				I'm sorry, but your portfolio couldn't be found. Please make a portfolio before trading by executing the createPortfolio command.\
			")
			return

		quantity = int(quantity)
		in_market_hours = is_market_hours()

		stock_exists = True  # TODO check if stock exists
		cost = self.portfolio.total_cost(ticker, quantity)
		buying_power = self.portfolio.get_buying_power()
		message = ctx.channel.last_message

		if quantity == 0:
			await ctx.send(f"\
				I'm sorry, but you can't buy 0 shares of a stock.\
			")
			return

		elif not in_market_hours:
			# await ctx.send(f"\
			# 	I'm sorry, but your order to purchase {quantity} shares of {ticker} couldn't be completed. Available market hours are M-F 9:30AM until 4:00PM, EST.\
			# ")
			await ctx.send(f"\
				Available market hours are M-F 9:30AM - 4:00PM EST. For UBHacking, this restriction has been temporarily lifted.\
			")
			self.portfolio.bought(ticker, quantity)
			await ctx.send(f"\
				Your order to purchase {quantity} shares of {ticker} executed successfully at an average price of {market_value}, for a total cost of {cost}. You now own {self.portfolio.get_quantity(ticker)} shares.\
			")
			self.currently_investing[str(message)] = str(ctx.author.id)
			await message.add_reaction('✅')
			await message.add_reaction('❌')
			await self.view_portfolio(ctx)
			return

		elif not stock_exists:
			await ctx.send(f"\
				I'm sorry, but {ticker} couldn't be found.\
			")
			return

		elif cost > buying_power:
			await ctx.send(f"\
				I'm sorry, but you don't have enough funds to purchase {quantity} shares of {ticker}, which would cost {cost}. Your available buying power is {buying_power}.\
			")
			return

		else:  # TODO prompt for confirmation
			self.portfolio.bought(ticker, quantity)
			await ctx.send(f"\
				Your order to purchase {quantity} shares of {ticker} executed successfully. You now own {self.portfolio.get_quantity(ticker)} shares.\
			")
			await message.add_reaction('✅')
			await message.add_reaction('❌')

	@commands.command()
	async def sell(self, ctx, ticker=None, quantity=None):
		portfolio_exists = (self.portfolio is not None)

		if ticker is None or quantity is None:
			await ctx.send(f"\
				The buy command takes both a ticker symbol and a quantity. Please try again.\
			")
			return

		elif not portfolio_exists:
			await ctx.send(f"\
				I'm sorry, but your portfolio couldn't be found. Please make a portfolio before trading by executing the createPortfolio command.")
			return

		quantity = int(quantity)
		quantity_owned = self.portfolio.get_quantity(ticker)
		in_market_hours = is_market_hours()

		if quantity == 0:
			await ctx.send(f"\
				I'm sorry, but you can't sell 0 shares of a stock.\
			")

		elif quantity_owned < quantity:
			if quantity_owned == 0:
				await ctx.send(f"\
					I'm sorry, but you don't own any shares of {ticker}.\
				")
			else:
				await ctx.send(f"\
					I'm sorry, but your order to sell {quantity} shares of {ticker} couldn't be completed. Your portfolio only contains {avail_to_sell} shares of {ticker}.\
				")
			return

		elif not in_market_hours:
			# await ctx.send(f"\
			# 	I'm sorry, but your order to sell {quantity} shares of {ticker} couldn't be completed. Available market hours are M-F 9:30AM until 4:00PM, EST.\
			# ")
			await ctx.send(f"\
				Available market hours are M-F 9:30AM - 4:00PM EST. For UBHacking, this restriction has been temporarily lifted.\
			")
			avg_price = self.portfolio.sold(ticker, quantity, avg_price)
			total = quantity * avg_price
			await ctx.send(f"\
				Your order to sell {quantity} shares of {ticker} was executed successfully, for an average price of ${avg_price}.00/share. The total sold value is ${total}.00\
			")
			return

		else:  # TODO Ask for confirmation
			avg_price = self.portfolio.sold(ticker, quantity)
			total = avg_price * quantity
			await ctx.send(f"\
				Your order to sell {quantity} shares of {ticker} was executed successfully, for an average price of {avg_price}.00/share. The total sold value is ${total}.00\
			")
			return

	@commands.command()
	async def view_portfolio(self, ctx):
		if self.portfolio is None:
			await ctx.send("Please create a portfolio before trying to view it")
			return

		buying_power = self.portfolio.get_buying_power()
		port_value = self.portfolio.get_portfolio_value()
		stocks = self.portfolio.get_owned()

		output = f"Buying power: {buying_power}\n"
		output += f"Portfolio Value: {port_value}\n"

		if len(stocks) == 0:
			output += "You do not own any stocks"
		else:
			for ticker in stocks:
				output += f"{ticker}: {stocks[ticker]} shares"

		await ctx.send(output)
		return

	# TODO load an existing portfolio
	@commands.command()
	async def create_portfolio(self, ctx):
		if self.portfolio is None:
			self.portfolio = Portfolio()
			await ctx.send("Investing portfolio successfully created. Your available funds (buying power) are $100,000.00")
		else:
			await ctx.send("At this time, investors can only have one portfolio. To view your portfolio, type /view_portfolio.")

	@commands.command()
	async def smooth_help(self, ctx):
		output = "Available commands for Smooth Stocks:\n\n"
		output += "- `/create_portfolio`   To create a new investment portfolio\n\n"
		output += "- `/view_portfolio`   To view your portfolio (if it exists)\n\n"
		output += "- `/buy [ticker] [quantity]`   To buy *quantity* shares of *ticker*\n\n"
		output += "- `/sell [ticker] [quantity]`   To sell *quantity* shares of *ticker*\n\n"
		output += "- `/help`   To list available commands"
		await ctx.send(output)


def setup(client):
	client.add_cog(Investor(client))
