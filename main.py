import requests
import json
import time
from credentials import ALPHAVANTAGE_KEY
from stock_news import StockNews
from telegram import Telegram

# STOCK = "MSFT"
# COMPANY_NAME = "Microsoft"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


def get_stock_prices():
    PARAMS = {
        "function": 'TIME_SERIES_DAILY',
        "symbol": STOCK,
        "apikey": ALPHAVANTAGE_KEY
    }

    try:
        # Make the API request
        response = requests.get(url=STOCK_ENDPOINT, params=PARAMS)
        response.raise_for_status()
        
        # Parse the JSON data from the response
        data = response.json()

        # Check if the "Time Series (Daily)" data is available in the response
        if "Time Series (Daily)" in data:
            time_series_data = data["Time Series (Daily)"]

            # Get the dates in the time series data and convert them to a list
            dates = list(time_series_data.keys())

            # Sort the dates in descending order to get the most recent dates first
            sorted_dates = sorted(dates, reverse=True)

            # Extract the closing prices for the two most recent days if available
            if len(sorted_dates) >= 2:
                previous_day = sorted_dates[0]
                day_before_that = sorted_dates[1]

                closing_price_previous_day = time_series_data[previous_day]["4. close"]
                closing_price_day_before_that = time_series_data[day_before_that]["4. close"]

                price_variation = abs(float(closing_price_previous_day) - float(closing_price_day_before_that))
                return (closing_price_previous_day, closing_price_day_before_that, price_variation)
            else:
                print("Not enough data available to find the closing prices for the previous days.")
        else:
            print("Time Series (Daily) data not found in the API response.")

    except requests.exceptions.RequestException as e:
        print(f"Error making the API request: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding the JSON response: {e}")
    except KeyError as e:
        print(f"KeyError: {e}")

def format_message(closing_prices, news):
    closing_price_previous_day = float(closing_prices[0])
    closing_price_day_before_that = float(closing_prices[1])
    message = ''
    if closing_price_previous_day >= closing_price_day_before_that:
        variation_percentage = round(((closing_price_previous_day - closing_price_day_before_that) / closing_price_day_before_that) * 100, 2)
        message += f"{STOCK}: 🔺{variation_percentage}\n"
    else:
        variation_percentage = round(((closing_price_day_before_that - closing_price_previous_day) / closing_price_day_before_that) * 100, 2)
        message += f"{STOCK}: 🔻{variation_percentage}\n"
    message += f"Headline: {news['title']}\n"
    message += f"Brief: {news['content']}\n"
    message += f"url: {news['url']}"
    return message
    
closing_prices = get_stock_prices()
closing_price_previous_day = closing_prices[0]
closing_price_day_before_that = closing_prices[1]
price_variation = closing_prices[2]

if price_variation >= (5 * float(closing_price_previous_day) / 100) or True:
    news = StockNews(company_name=COMPANY_NAME)
    news_data = news.get_stock_news()
    telegram_bot = Telegram()
    for single_new in news_data:
        message = format_message(closing_prices, single_new)
        send_message_return = telegram_bot.send_message(message)
        time.sleep(1)


