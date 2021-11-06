# UBHacking 2021

## Smooth Stocks

## Table of Contents
1. [Description](#Description)
1. [User Stories]()
2. [Specifications](#Specifications)
3. [Wireframes](#Wireframes)
4. [Schemas](#Schemas)

### Description
Smooth Stocks is a Discord bot that lets users maintain a faux stock portfolio.

### User Stories
#### Required
* Investor can create a new trading portfolio
    * Reason: Investor need a portfolio to maintain a balance and track which stocks they're invested in

* Investor can place an order to buy or sell American listed stocks
    * Reason: Buying and selling stocks are standard trading activities for any investor's portfolio

#### Optional
* Investor can view a graph of a stocks price movement over time
    * Reason: Stock information over time helps inform an investor's decision

* Investor can share their portfolio with other investors
    * Reason: Viewing other investor's profiles is often useful for gaining insights on profitable stocks

* Investor can place limit buys, limit sells, stop loss, etc.
    * Reason: These advanced tools are useful for experienced investors to execute orders based on market conditions

### Specifications

#### Inputs
* `/command` Allows an investor to run a command with the Smooth Stocks bot
    * Reason: `/command` Is a familiar way to enter commands for many Discord users

#### Outputs
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
    * Affirmation of successful sell

* 

#### Constraints


### Wireframes


### Schemas
