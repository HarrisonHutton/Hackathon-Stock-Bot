import os
import time

import requests

DATE = '2021-11-05'
KEY = os.environ['API_KEY']

data = {'user': {'bank': 1000, 'invested': 0, 'stocks':  {}}}

def ticker_price(ticker):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + ticker + '&outputsize=compact&apikey=' + KEY
    r = requests.get(url)
    if 'Time Series (Daily)' not in r.json().keys():
        return
    ticker_data = r.json()['Time Series (Daily)'][DATE]['4. close']
    return float(ticker_data)

def sum_stocks(user):
    user_info = data[user]
    user_info['invested'] = 0
    for ticker in user_info['stocks'].keys():
        price = ticker_price(ticker)
        if price == "Please wait":
            break
        user_info['invested'] += price * user_info['stocks'][ticker]
    return

def get_portfolio(user):
    sum_stocks(user)
    print(data[user])

def buy_stock(ticker, amount, user):
    user_info = data[user]
    price = ticker_price(ticker)
    if price == "Please wait":
        print("Please wait")
        return
    cost = ticker_price(ticker) * amount
    print(user_info['bank'], type(user_info['bank']), cost, type(cost))
    if user_info['bank'] < cost:
        return
    user_info['bank'] -= cost
    if ticker not in user_info['stocks'].keys():
        user_info['stocks'][ticker] = amount
    else:
        user_info['stocks'][ticker] += amount


# get_portfolio('user')

# buy_stock('IBM', 2, 'user')
# get_portfolio('user')

# buy_stock('AAPL', 1, 'user')
# buy_stock('IBM', 1, 'user')
# get_portfolio('user')

# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + 'IBM' + '&outputsize=compact&apikey=' + KEY
# r = requests.get(url)
# print(r.json())