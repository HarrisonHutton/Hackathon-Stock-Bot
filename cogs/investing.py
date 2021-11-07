import discord
import json
import datetime
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
		self.buying_power = bp
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

class Investor(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.id = client.author.User.id
		self.portfolio = None

	# TODO: Store encoded data [instead of?] returning
	def encode(self):
		portfolio_json = self.portfolio.encode()
		temp_dict = {self.id: portfolio_json}
		return json.dumps(temp_dict)

	# TODO for this command:
	# Implement market API call
	@commands.command()
	async def buy(self, ctx, ticker=None, quantity=None):

		if ticker is None or quantity is None:
			await ctx.send(f"\
				The buy command takes both a ticker symbol \
				and a quantity. Please try again.\
			")

		in_market_hours = is_market_hours()

		market_value = 5.05  # TODO Get with market API call
		portfolio_exists = (self.portfolio is not None)

		stock_exists = True  # TODO check if stock exists
		cost = market_value * int(quantity)
		buying_power = await self.portfolio.GetBuyingPower()

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

		elif cost > buying_power:
			await ctx.send(f"\
				I'm sorry, but you don't have enough funds to \
				purchase {quantity} shares of {ticker}, which would \
				cost {cost}. Your available buying power is \
				{buying_power}.\
			")
			return

		else:  # TODO prompt for confirmation
			await self.portfolio.Bought(ticker, quantity)
			await ctx.send(f"\
				Your order to purchase {quantity} shares of \
				{ticker} executed successfully. You now own \
				{self.portfolio.GetQuantity(ticker)} shares.\
			")
			return

	@commands.command()
	async def sell(self, ctx, ticker=None, quantity=None):
		avail_to_sell = self.portfolio.GetQuantity(ticker)
		in_market_hours = is_market_hours()
		portfolio_exists = (self.portfolio is not None)

		if ticker is None or quantity is None:
			await ctx.send(f"\
				The buy command takes both a ticker symbol \
				and a quantity. Please try again.\
			")
			return

		elif quantity == 0:
			await ctx.send(f"\
				I'm sorry, but you can't sell 0 shares \
				of a stock.\
			")

		elif not portfolio_exists:
			await ctx.send(f"\
				I'm sorry, but your portfolio couldn't be found. \
				Please make a portfolio before trading by \
				executing the createPortfolio command.")
			return

		elif not in_market_hours:
			await ctx.send(f"\
				I'm sorry, but your order to sell {quantity} shares\
				of {ticker} couldn't be completed. Available market\
				hours are M-F 9:30AM until 4:00PM, EST.\
			")
			return

		elif avail_to_sell < quantity:
			await ctx.send(f"\
				I'm sorry, but your order to sell {quantity} shares of {ticker} \
				couldn't be completed. Your portfolio only contains {avail_to_sell} shares of {ticker}.\
			")
			return

		else:  # TODO Ask for confirmation
			avg_price = ...  # TODO avg sale price
			await self.portfolio.Sold(ticker, quantity)
			await ctx.send(f"\
				Your order to sell {quantity} shares of \
				{ticker} was executed successfully, for an \
				average price of {avg_price}.\
			")
			return

	@commands.command()
	async def view_portfolio(self, ctx):
		blob = self.portfolio.Encode()
		port_info = json.loads(blob)
		buying_power = port_info["buying_power"]
		port_value = port_info["portfolio_value"]
		stocks = port_info["owned_stocks"]

		output = f"Buying power: {buying_power}\n"
		output += f"Portfolio Value: {port_value}\n"

		for ticker in stocks:
			output += f"{ticker}: {stocks[ticker]} shares"

		await ctx.send(output)
		return

	# TODO load an existing portfolio
	@commands.command()
	async def create_portfolio(self, ctx):
		self.portfolio = Portfolio(self.client)


def setup(client):
	client.add_cog(Investor(client))
