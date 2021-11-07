# UBHacking 2021

## Smooth Stocks

## Table of Contents
1. [Description](#Description)
2. [UserStories](#UserStories)
3. [Specifications](#Specifications)
4. [Models](#Models)

### Description
Smooth Stocks is a Discord bot that lets users maintain a faux stock portfolio.

### UserStories
#### Required
* Investor can create a new trading portfolio
    * Reason: Investor need a portfolio to maintain a balance and track which stocks they're invested in

* Investor can place an order to buy or sell American listed stocks
    * Reason: Buying and selling stocks are standard trading activities for any investor's portfolio

* Investor can view their portfolio
    * Reason: Investors need to be aware of the status of their portfolio in order to make decisions or simply view how their investors are faring

* Investor can view available commands to the Smooth Stocks bot
    * Reason: New investors need to know how to use the Smooth Stocks bot to manage their profile

#### Optional
* Investor can view a graph of a stocks price movement over time
    * Reason: Stock information over time helps inform an investor's decision

* Investor can share their portfolio with other investors
    * Reason: Viewing other investor's profiles is often useful for gaining insights on profitable stocks

* Investor can place limit buys, limit sells, stop loss, etc.
    * Reason: These advanced tools are useful for experienced investors to execute orders based on market conditions

### Specifications

#### Inputs
* `/createPortfolio` Allows an investor to create a portfolio

* `/buy [ticker] [quantity]` Purchase `[quantity]` amount of `[ticker]`

* `/sell [ticker] [quantity]` Sell `[quantity]` amount of `[ticker]`

* `/viewPortfolio` Lists information about an investor's portfolio

* `/smoothHelp` Lists available commands for this Discord bot

#### Outputs
* `/createPortfolio`
    * A message saying that the portfolio was successfully created
        * Reason: The investor should know that their porfolio was created

* `/buy [ticker] [quantity]`
    * Whether or not the order is allowed to be placed
        * Reason: Investors should not be able to place an order that has no chance of being executed. Reasons include not enough buying power or outside of trading hours
    * Confirmation of order with portfolio buying power, total cost of order, and a prompt to place the order
        * Reason: Investors should know how much buying power they have and how much their order will cost. This helps them decide if they'd really like to place the order.
    * Affirmation of successful buy
        * Reason: Investors need to know if the buy order was executed successfully
    * Notice of unsuccessful buy with reason
        * Reason: The investor should know that the buy order was not executed successfully and why, so that they can try to execute the same or another command if they desire

* `/sell [ticker] [quantity]`
    * Whether or not the order is allowed to placed
        * The investor should not be allowed to place an order that will not execute. Reasons include trading outside of hours or trying to sell 0 or more than they own
    * Confirmation of order with the desired quantity, total value of the order, and a prompt to confirm the order
        * Reason: The investor should have an overview of the order before it's executed, so that they can see any mistakes they might have made
    * Affirmation of successful sell with quantity sold and total price of sell order
        * Reason: The investor needs to be notified that the stocks were successfully sold and the amount of money they can expect to be added to their buying power as a result
    * Notice of unsuccessful sell with reason
        * Reason: The investor should be informed if their order wasn't able to be executed, along with the reason why

* `/viewPortfolio` Allows an investor to view their portfolio
    * For each stock in portfolio:
        * `ticker | quantity | most recent price | value`
    * Total portfolio value

* `/smoothHelp` Lists commands available to this Discord bot
    * `/smoothHelp` to ...
    * `/buy [ticker] [quantity]` to ...

#### Constraints
* Bot should be able to be added to any Discord server
    * Reason: The bot should be accessible to as many users as possible


### Models

**Portfolio**
An object of this class is contained within an Investor object and is used to manage that investor's portfolio

#### Data
* `_buyingPower`
    * Float e.g. 1000.24
* `_portfolioValue`
    * Float e.g. 3425.53
* `_ownedStocks`
    * Dictionary e.g. {AAPL: 21, TSLA: 25, ...}

#### Methods
* `GetQuantity(tickerName)`
    * Takes ticker name as a string
    * Returns the quantity of tickerName in this portfolio, or 0 if the tickerName is not in `_ownedStocks`
* `GetBuyingPower()`
    * Returns the buying power of this portfolio
* `GetPortfolioValue()`
    * Returns the total value of this portfolio, calculated as `(_buyingPower) * (ticker * price)`
* `Bought(ticker, quantity)`
    * Takes a stock ticker as a string and a quantity purchased as an integer
    * Returns None
    * Updates this portfolio to reflect the purchase of `quantity` shares of `ticker`
* `Sold(ticker, quantity)`
    * Takes a stock ticker as a string and a quantity sold as an integer
    * Return None
    * Updates this portfolio to reflect the sale of `quantity` shares of `ticker`

* `Encode()`
    * Encodes the buying power, stocks, quantity owned, and portfolio value as a JSON dictionary
    * Returns this JSON dictionary

---

**Market**
This object is used to handle anything that needs to access market data or state.

#### Data
* `_recentlyPolled`
    * A dictionary mapping tickers as strings to the most recent price. Updated when an Investor asks for the MostRecentPrice of a stock. Used to reduce API calls.

#### Methods
* MostRecentPrice(ticker)
* IsTradingHours()

---

**Investor**
This class represents a specific investor, and maintains their portfolio.

#### Data
* ID
    * Integer
* Portfolio
    * Object of type Portfolio

#### Methods
* Encode()
    * Return a JSON string encoding all of this investors information

---

### Examples
* /buy[ticker] [quantity]
     - If Allowed
SmoothStocks: You have [buyingPower] buying power. The order will cost [totalprice] dollars to buy. You are trying to buy [quantity] of [ticker]. Are you sure? y/n
User: y
SmoothStocks: Your order has gone through.
-or
User: n
SmoothStocks: Your order has been canceled.
    - If Not Allowed
-outside of trading hours
SmoothStocks: I'm sorry, but your order of [quantity][ticker] cannot be completed. You are trying to buy outside of trading hours. The trading hours are 9:30AM to 4:00PM
-or not enough funds
SmoothStocks: I'm sorry, but your order of [quantity][ticker] cannot be completed. You don't have enough funds.
-or selling zero/none stock/not a real number
SmoothStocks: I'm sorry, but you can't buy nothing.
-or no portfolio
SmoothStocks: I'm sorry, but you don't have a portfolio
-or fake stock
SmoothStocks: I'm sorry, but this stock doesn't exist
* /sell [ticker] [quantity]
    - If Allowed
SmoothStocks: You want to sell [quantity][ticker].
Before you confirm this transaction you have [OldQuantity][ticker]. After confirming this transaction you'll have [NewQuantity][ticker]. Are you sure? y/n
-or selling all
SmoothStocks: Are you sure you want to sell all of your [ticker] stocks? y/n
User: y
SmoothStocks: Your transaction has been compleated
-or
User: n
SmoothStocks: Your transaction has been canceled 
    - If Not Allowed
-selling zero/none stock/not a real number
smothStocks: I'm sorry, but you can't buy nothing.
-or portfolio dosn't exist
SmoothStocks:I'm sorry, but you don't have a portfolio. Please create one with /createPortfolio
-or outside trading hours
SmoothStocks: I’m sorry, but your transaction of [quantity][ticker] cannot be completed. You are trying to sell outside of trading hours. The trading hours are 9:30AM to 4:00PM
-or don't have enough
SmoothStocks: I'm sorry, but you don't have enough [ticker]stocks to sell.
-or don't have enough (varient)
SmoothStocks: I'm sorry, but you don't have any [ticker]stocks to sell.
* /viewPortfolio
    - If allowed
SmoothStocks: Here is your portfolio.[Portfolio]
    - If not allowed
-Not a portfolio
SmoothStocks: I'm Sorry, but you don't own a portfolio. Please use the command /makePortfolio
* /createPortfolio
    - If allowed
SmoothStocks:Here is your new portfolio.[Portfolio](take to /help)
    - If not allowed
SmoothStocks:I'm sorry, but you already own a portfolio. Do you want to replace it with a new one? y/n
user:y
SmoothStocks:Here is your new portfolio.[Portfolio](take to /help)
-or
user:n
SmoothStocks:Ok here is your old portfolio.[Portfolio]
* /help
SmoothStocks:Here are all the commands you can use.
/createPortfolio #Creates Portfolio to use
/viewPortfolio #Shows your portfolio
/buy |ticker|amount| #Allows you to buy and add stocks to your portfolio
/sell |ticker|amount| #Allows you to sell your stock from your portfolio
/help #Shows you the commands(You are using this right now)
