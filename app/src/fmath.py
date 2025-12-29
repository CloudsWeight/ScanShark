import numpy as np 
import pandas as pd 
import json
import random
import matplotlib as plt
from OandaFile import OandaApp as oa 
from finny import Finny

class Fx():

	def __init__(self):
		self.oa = oa()

	def get_rates(self, pair=None, tf='H4', count=36):
		''' eurusd, usdjpy, eurgbp, eurusd, chfjpy
			M1, M5, M15, H1, H4, D, W, M
			count = 1 - 5000 
		'''
		if pair == None:
			pair = random.choice(['eurusd', 'usdjpy', 'eurgbp', 'eurusd', 'chfjpy'])
		
		return self.oa.get_rate(pair,tf,count)

	def df_rates(self, data=None):
		if data != None:
			candles = data['candles']
			df = pd.DataFrame([{
			    'time': candle['time'],
			    'open': float(candle['mid']['o']),
			    'high': float(candle['mid']['h']),
			    'low': float(candle['mid']['l']),
			    'close': float(candle['mid']['c']),
			    'volume': candle['volume']
			} for candle in candles])

		return df 

	def df_echarts(self, df=None):
		e_df = df[['time', 'open', 'close', 'low', 'high']].values.tolist()
		print(e_df)
		return e_df


class Fin():

	def __init__(self):
		self.fin = Finny()

	def find_symbol(self, query='tsmc'):
		return self.fin.find_symbol(query)

	def quote_symbol(self, symbol='tsm'):
		return self.fin.quote_symbol(symbol)

	def news_symbol(self, symbol='tsm', _from="2020-01-01", to="2024-11-12"):
		return self.fin.news_symbol(symbol, _from=_from, to=to)

def clean_json(dirty=None):
	if dirty != None:
		return json.dumps(dirty, indent=2)
	else:
		return 'Need good JSON'


#####################################################################################################
if __name__ == "__main__":
	fhs = Fin()
	print(clean_json(fhs.news_symbol('tsm')))


	
