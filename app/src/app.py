'''
Current:  Simple route '/' that returns data 

'''
from fastapi import FastAPI
from typing import Union 
import fmath 
import random

app = FastAPI()
#logic here

@app.get("/", tags=["Root"])
async def read_root():
 """OLD Boilerplate code for FastAPI endpoints 
    return json 
""" 
