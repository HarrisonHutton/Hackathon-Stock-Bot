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

#### Optional
* Investor can view a graph of a stocks price movement over time
    * Reason: Stock information over time helps inform an investor's decision

* Investor can share their portfolio with other investors
    * Reason: Viewing other investor's profiles is often useful for gaining insights on profitable stocks

* Investor can place limit buys, limit sells, stop loss, etc.
    * Reason: These advanced tools are useful for experienced investors to execute orders based on market conditions

### Specifications

#### Inputs
* `/createPortfolio [name]` Allows an investor to create a portfolio called `[name]`
    * Reason: This is how the investor starts investing with a new portfolio

* `/buyWithTicker [ticker] [quantity]` Purchase `[quantity]` amount of `[ticker]`
    * Reason: Buying stocks is one of the main components of maintaining a stock portfolio

* `/sellWithTicker [ticker] [quantity]` Sell `[quantity]` amount of `[ticker]`
    * Reason: Selling stocks is one of the main components of maintaining a stock portfolio

#### Outputs
* `/createPortfolio [name]`
    * A message saying that the portfolio was successfully created
        * Reason: The investor should know that their porfolio was created
    * "How to Use" information listing available commands
        * Reason: The investor only needs to know one command, and the bot will inform them of what else they can do

* `/buyWithTicker [ticker] [quantity]`
    * Whether or not the order is allowed to be placed
        * Reason: Investors should not be able to place an order that has no chance of being executed. Reasons include not enough buying power or outside of trading hours
    * Confirmation of order with portfolio buying power, total cost of order, and a prompt to place the order
        * Reason: Investors should know how much buying power they have and how much their order will cost. This helps them decide if they'd really like to place the order.
    * Affirmation of successful buy
        * Reason: Investors need to know if the buy order was executed successfully
    * Notice of unsuccessful buy with reason
        * Reason: The investor should know that the buy order was not executed successfully and why, so that they can try to execute the same or another command if they desire

* `/sellWithTicker [ticker] [quantity]`
    * Whether or not the order is allowed to placed
        * The investor should not be allowed to place an order that will not execute. Reasons include trading outside of hours or trying to sell 0 or more than they own
    * Confirmation of order with the desired quantity, total value of the order, and a prompt to confirm the order
        * Reason: The investor should have an overview of the order before it's executed, so that they can see any mistakes they might have made
    * Affirmation of successful sell with quantity sold and total price of sell order
        * Reason: The investor needs to be notified that the stocks were successfully sold and the amount of money they can expect to be added to their buying power as a result
    * Notice of unsuccessful sell with reason
        * Reason: The investor should be informed if their order wasn't able to be executed, along with the reason why

#### Constraints
* Bot should be able to be added to any Discord server
    * Reason: The bot should be accessible to as many users as possible


### Models
#### Portfolio

### Examples
