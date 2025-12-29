import random
import json
import requests
import numpy 
import pandas
import finnhub
from dotenv import load_dotenv
import os
load_dotenv()
FH_KEY = os.environ["FH_KEY"]

class Finny():
	'''
	Get FinnHub API Stock data

	'''
	def __init__(self, api_key=FH_KEY):
		self.base_url = 'https://finnhub.io/api/v1'
		self.client = finnhub.Client(api_key=api_key)

	def find_symbol(self, query='tsmc'):
		query = query
		return self.client.symbol_lookup(query)

	def quote_symbol(self, symbol='aapl'):
		symbol = symbol.upper()
		return self.client.quote(symbol)

	def news_symbol(self, symbol='tsm', _from="2020-01-02", to="2024-12-11"):
		return self.client.company_news(symbol, _from=_from, to=to)


if __name__ == '__main__':
	fhs = Finny()
	apple = fhs.find_symbol('apple')
	print(json.dumps(apple, indent=2))
