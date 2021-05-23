import yfinance as yf
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

# https://pypi.org/project/yfinance/
# https://plotly.com/python/candlestick-charts/
# https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/

data = yf.download(tickers = "SPY", period = "3mo")
data.to_csv("SPY.csv")
# print(data)

# df = pd.DataFrame(data)
#
# print(df)

df = pd.read_csv('SPY.csv')

print(df)

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

fig.show()
