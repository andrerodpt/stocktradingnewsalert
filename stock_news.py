import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from credentials import NEWSAPI_KEY

NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'

class StockNews:
    def __init__(self, company_name) -> None:
        # Get the current date
        current_date = datetime.now()

        # Subtract one month
        one_month_ago = current_date - relativedelta(months=1)

        self.company_name = company_name
        self.date_from = one_month_ago.strftime('%Y-%m-%d')
        self.sort = 'publishedAt'
        self.apiKey = NEWSAPI_KEY

    def get_stock_news(self):
        PARAMS = {
            "searchIn": 'title',
            "q": self.company_name,
            "language": 'en',
            "from": self.date_from,
            "sortBy": self.sort,
            "apiKey": self.apiKey
        }

        try:
            # Make the API request
            response = requests.get(url=NEWS_API_ENDPOINT, params=PARAMS)
            response.raise_for_status()
            
            # Parse the JSON data from the response
            data = response.json()
            sliced_news = data['articles'][:3]
            return sliced_news

        except requests.exceptions.RequestException as e:
            print(f"Error making the API request: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding the JSON response: {e}")
        except KeyError as e:
            print(f"KeyError: {e}")