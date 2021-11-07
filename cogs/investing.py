import discord
import json
import datetime
import random
from discord.ext import commands


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
		return


class Portfolio:

	def __init__(self, bp=100000.0, pv=100000.0, owned=None):
		if owned is None:
			owned = {}
		self.buying_power = int(bp)
		self.portfolio_value = pv
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
			market_value = 5.05  # TODO Get market value
			value += (quantity * market_value)
		return value + self.buying_power

	def bought(self, ticker, quantity, market_value):
		total_cost = quantity * market_value

		# Buy using buying power then increment amount owned
		self.buying_power -= total_cost
		if ticker in self.owned_stocks:
			self.owned_stocks[ticker] += quantity
		else:
			self.owned_stocks[ticker] = quantity

		return

	def sold(self, ticker, quantity, market_value):
		sold_for = int(quantity) * market_value
		self.buying_power += int(sold_for)
		self.owned_stocks[ticker] -= int(quantity)

	def get_owned(self):
		return self.owned_stocks

	def custom_encode(self):
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

	# TODO: Store encoded data [instead of?] returning
	def encode(self):
		#portfolio_json = self.portfolio.encode()
		#temp_dict = {self.id: portfolio_json}
		#return json.dumps(temp_dict)
		return json.dumps({})

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
		elif not portfolio_exists:
			await ctx.send(f"\
				I'm sorry, but your portfolio couldn't be found. Please make a portfolio before trading by executing the createPortfolio command.\
			")
			return

		in_market_hours = is_market_hours()
		market_value = random.randint(1, 1250)  # TODO Get with market API call

		stock_exists = True  # TODO check if stock exists
		cost = market_value * int(quantity)
		buying_power = self.portfolio.get_buying_power()

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
			self.portfolio.bought(ticker, int(quantity), market_value)
			await ctx.send(f"\
				Your order to purchase {quantity} shares of {ticker} executed successfully at an average price of {market_value}, for a total cost of {cost}. You now own {self.portfolio.get_quantity(ticker)} shares.\
			")
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
			return

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

		avail_to_sell = self.portfolio.get_quantity(ticker)
		in_market_hours = is_market_hours()

		if quantity == 0:
			await ctx.send(f"\
				I'm sorry, but you can't sell 0 shares of a stock.\
			")

		elif not in_market_hours:
			# await ctx.send(f"\
			# 	I'm sorry, but your order to sell {quantity} shares of {ticker} couldn't be completed. Available market hours are M-F 9:30AM until 4:00PM, EST.\
			# ")
			await ctx.send(f"\
				Available market hours are M-F 9:30AM - 4:00PM EST. For UBHacking, this restriction has been temporarily lifted.\
			")
			avg_price = random.randint(1, 1250)
			total = int(quantity) * avg_price
			self.portfolio.sold(ticker, quantity, avg_price)
			await ctx.send(f"\
				Your order to sell {quantity} shares of {ticker} was executed successfully, for an average price of ${avg_price}.00/share. The total sold value is ${total}.00\
			")
			return

		elif avail_to_sell < quantity:
			await ctx.send(f"\
				I'm sorry, but your order to sell {quantity} shares of {ticker} couldn't be completed. Your portfolio only contains {avail_to_sell} shares of {ticker}.\
			")
			return

		else:  # TODO Ask for confirmation
			avg_price = random.randint(1, 1250)  # TODO avg sale price
			self.portfolio.sold(ticker, quantity)
			await ctx.send(f"\
				Your order to sell {quantity} shares of {ticker} was executed successfully, for an average price of {avg_price}.\
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


def setup(client):
	client.add_cog(Investor(client))