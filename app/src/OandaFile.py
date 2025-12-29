import requests
import json 
import csv
import argparse
from datetime import datetime 
import os
import random
from dotenv import load_dotenv
load_dotenv()

SECRET = os.environ['SECRET']
ACCTS = os.environ["ACCTS"]

class OandaApp():
	def __init__(self, token=None, account=None):
		self.BASE_URL ='https://api-fxtrade.oanda.com'
		if account is not None:
			self.account = {
					'URL':f'{self.BASE_URL}/v3/accounts', # Accounts Endpoint
					'acctId': account,
					'current':f'{account}'
					}
		self.account = {
					'URL':f'{self.BASE_URL}/v3/accounts', # Accounts Endpoint
					'acctId': ACCTS,
					'current':f'{ACCTS[0]}'
						}
		#if token is None:
			#self.token = SECRET
		self.token = token
		self.HEADER = { # Headers and Auth
					'Authorization': 'Bearer {}'.format(f'{SECRET}'),
				} 
		self.ENDPOINT = { 
						'instruments':f'{self.BASE_URL}/v3/instruments/',
						'candles': f'{self.BASE_URL}/candles?',
						}
		self.instruments = {
					# CURRENCY PAIRS
					'URL':f'{self.BASE_URL}/v3/instruments/', 
					'current':'USD_JPY/',
					'eurusd':'EUR_USD/', 
					'usdjpy':'USD_JPY/', 
					'usdchf':'USD_CHF/',
					'eurjpy': 'EUR_JPY/',
					'chfjpy': 'CHF_JPY/',
					'gbpusd': 'GBP_USD/',
					'eurgbp': 'EUR_GBP/',
					'usdmxn': 'USD_MXN/', 
					}
		self.count = {
						'URL':'count=',
						'current':'1' # [default=500, maximum=5000] dont use with "FROM and TO"
						}
		self.candles = {'URL':'/candles?',
						'granularity':{
						'current':'&granularity=H4',
						'S5':'&granularity=S5',
						'M5':'&granularity=M5',
						'M15':'&granularity=M15',
						'H1':'&granularity=H1', 
						'H4':'&granularity=H4',
						'D':'&granularity=D',
						'W':'&granularity=W',
						'M':'&granularity=M',
						 },
					}
		self.current_url = (
			 f"{self.instruments['URL']}{self.instruments['current']}"
			 f"{self.candles['URL']}"
			 f"{self.count['URL']}{self.count['current']}"
			 f"{self.candles['granularity']['current']}"
			 				) # As Above So Below
	# Example:	https://api-fxtrade.oanda.com/v3/instruments/EUR_USD/candles?count=6&price=M&granularity=S5
	def get_accts(self, url=None, header=None):
		if header is None:
			header = self.HEADER
		if url is None:
			url = f"{self.account['URL']}"
		r = requests.get(url=url, headers=header)
		print(f"{r.status_code}, /n {r.content}")

	def get_acct(self, url=None, header=None):
		r = requests.get(url=url, headers=header)
		print(f"{r.status_code}")

	def get_rate(self, rate='eurusd', tf='M5', count=300 ): # if you make changes then update with this method 
		
		url = (
					 f"{self.instruments['URL']}{self.instruments[rate]}"
					 f"{self.candles['URL']}"
					 f"{self.count['URL']}{count}"
					 f"{self.candles['granularity'][tf]}"
					 )
		r = requests.get(url, headers=self.HEADER)
		data = json.loads(r.content)
		return data

	def test_rate(self):
		rl = ['eurusd','usdmxn','usdjpy']
		tf = ["M5", "H4", 'D']
		count = [1, 10, 31]

		return self.get_rate(random.choice(rl), random.choice(tf), random.choice(count))

	def dump(self, data=None):
		if data != None:
			return json.dumps(data, indent=2)
		else:
			print('Load JSON')

if __name__ == '__main__':
	#print("Null stuff")
	trade = OandaApp()
	print(trade.dump(trade.test_rate()))
