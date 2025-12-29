'''
Current:  Simple route '/' that returns data from a random currency pair

To Do:  Create multiple currency pair inputs that use the following parameters for the fmath.Fx.get_rates(rate,tf,count) function:
  * rate: eurusd, usdjpy, gbpusd, eurjpy, eurgbp, chfjpy, zarjpy, usdmxn, usdchf, etcetc
  * tf: S5, M5, M15, H1, H4, H8, D, W, M
  * count: 1-500


'''
from fastapi import FastAPI
from typing import Union 
import fmath 
import random

app = FastAPI()
fx = fmath.Fx()
to_df = fx.df_rates

@app.get("/", tags=["Root"])
async def read_root():
    pair = random.choice(['eurusd', 'usdjpy', 'eurgbp', 'eurusd', 'chfjpy'])
    rates = fx.get_rates(pair, 'H1', 30)
    #df = to_df(rates)
    return {"rates": rates
            }
