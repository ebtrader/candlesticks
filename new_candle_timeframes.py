import math
import numpy as np
from finta import TA
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from datetime import datetime


ticker = "NQ=F"
data = yf.download(tickers = ticker, start='2019-01-01', end='2019-12-31')
# data = yf.download(tickers = ticker, period = "1y")

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# https://pypi.org/project/yfinance/
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")

df1 = pd.DataFrame(data)

# print(df1)

df = df1.reset_index()

# print(df)

df2 = df.rename(columns = {'Date': 'date', 'Open':'open', 'High': 'high', 'Low':'low', 'Close':'close','Volume': 'volume'}, inplace = False)

print(df2)
df2.to_csv('daily.csv')

n = 5

df3 = df2.groupby(np.arange(len(df2))//n).max()
print('df3 max:', df3)

df4 = df2.groupby(np.arange(len(df2))//n).min()
print('df4 min:', df4)

df5 = df2.groupby(np.arange(len(df2))//n).first()
print('df5 open:', df5)

df6 = df2.groupby(np.arange(len(df2))//n).last()
print('df6 close:', df6)


agg_df = pd.DataFrame()

agg_df['date'] = df6['date']
agg_df['low'] = df4['low']
agg_df['high'] = df3['high']
agg_df['open'] = df5['open']
agg_df['close'] = df6['close']

print(agg_df)
