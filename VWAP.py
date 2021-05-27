import math
import numpy as np
from finta import TA
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from datetime import datetime

# https://futures.io/thinkorswim/18306-help-easylanguage-notation-john-ehlers-4-pole-gaussian-filter.html

# https://github.com/peerchemist/finta/blob/master/finta/finta.py

# https://pypi.org/project/yfinance/
# https://plotly.com/python/candlestick-charts/
# https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/
# https://thispointer.com/pandas-convert-dataframe-index-into-column-using-dataframe-reset_index-in-python/#:~:text=To%20convert%20all%20the%20indexes,on%20the%20dataframe%20object%20i.e.&text=It%20converted%20the%20indexes%20'ID,same%20name%20in%20the%20dataframe.

ticker = "NQ=F"
# data = yf.download(tickers = ticker, start='2019-01-01', end='2019-12-31')
data = yf.download(tickers = ticker, period = "5d", interval="5m")

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# https://pypi.org/project/yfinance/
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")

df1 = pd.DataFrame(data)

print(df1)

df = df1.reset_index()

print(df)

# https://github.com/peerchemist/finta

# https://www.datacamp.com/community/tutorials/python-rename-column?utm_source=adwords_ppc&utm_campaignid=1565261270&utm_adgroupid=67750485268&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=&utm_creative=295208661496&utm_targetid=aud-299261629614:dsa-429603003980&utm_loc_interest_ms=&utm_loc_physical_ms=9004005&gclid=CjwKCAjwtJ2FBhAuEiwAIKu19mq1iWE1XmgD7B6yZvBc6XpTuf_fhxNEcZvf_5BBjHEBA6KvjmMXlBoChrAQAvD_BwE

df2 = df.rename(columns = {'Date': 'date', 'Open':'open', 'High': 'high', 'Low':'low', 'Close':'close','Volume': 'volume'}, inplace = False)

print(df2)
num_periods = 21
df2['SMA'] = TA.SMA(df2, 9)
df2['FRAMA'] = TA.FRAMA(df2, 10)
df2['TEMA'] = TA.TEMA(df2, num_periods)
df2['VWAP'] = TA.VWAP(df2)

# how to get previous row's value
# df2['previous'] = df2['lower_band'].shift(1)

# # how to get the power of another column
df2['test'] = 5
# df2['square'] = df2['test'].pow(2)
# df2['square'] = df2['test']**2

# recursive
df2.loc[0, 'diff'] = df2.loc[0, 'test'] * 0.4
df2.loc[1, 'diff'] = df2.loc[1, 'test'] * 0.4
df2.loc[2, 'diff'] = df2.loc[2, 'test'] * 0.4
df2.loc[3, 'diff'] = df2.loc[3, 'test'] * 0.4

for i in range(4, len(df2)):
    df2.loc[i, 'diff'] = df2.loc[i, 'test'] + df2.loc[i-1, 'diff'] + df2.loc[i-2, 'diff']


# for i in range(1, len(df2)):
#     df2.loc[i, 'diff'] = df2.loc[i, 'test'] + df2.loc[i-1, 'diff']




# pi
# df2['pi'] = math.pi

# cosine
# df2['cos'] = np.cos(df2['test'])



# Gauss
num_periods_gauss = 16.5
df2['symbol'] = 2 * math.pi / num_periods_gauss
df2['beta'] = (1 - np.cos(df2['symbol']) ) / ((1.414)**(0.5) - 1)
df2['alpha'] = - df2['beta'] + (df2['beta']**2 + df2['beta'] * 2)**2

# Gauss equation
# initialize
df2.loc[0, 'gauss'] = df2.loc[0, 'close']
df2.loc[1, 'gauss'] = df2.loc[1, 'close']
df2.loc[2, 'gauss'] = df2.loc[2, 'close']
df2.loc[3, 'gauss'] = df2.loc[3, 'close']
df2.loc[4, 'gauss'] = df2.loc[4, 'close']

for i in range (4, len(df2)):
    df2.loc[i, 'gauss'] = df2.loc[i, 'VWAP'] * df2.loc[i, 'alpha']**4 + (4 * (1 - df2.loc[i, 'alpha']))*df2.loc[i-1, 'gauss'] \
                          - (6 * ((1 - df2.loc[i, 'alpha']) ** 2) * df2.loc[i - 2, 'gauss']) \
                          + (4 * (1 - df2.loc[i, 'alpha']) ** 3) * df2.loc[i - 3, 'gauss'] \
                          - ((1 - df2.loc[i, 'alpha']) ** 4) * df2.loc[i - 4, 'gauss']

# ATR

# https://www.statology.org/exponential-moving-average-pandas/
num_periods_ATR = 21
multiplier = 1

df2['ATR_diff'] = df2['high'] - df2['low']
df2['ATR'] = df2['ATR_diff'].ewm(span=num_periods_ATR, adjust=False).mean()
# df2['ATR'] = df2['ATR_diff'].rolling(window=num_periods_ATR).mean()
df2['Line'] = df2['gauss']
df2['upper_band'] = df2['Line'] + multiplier * df2['ATR']
df2['lower_band'] = df2['Line'] - multiplier * df2['ATR']

multiplier_1 = 1.6
multiplier_2 = 1.4

df2['upper_band_1'] = df2['Line'] + multiplier_1 * df2['ATR']
df2['lower_band_1'] = df2['Line'] - multiplier_1 * df2['ATR']

df2['upper_band_2'] = df2['Line'] + multiplier_2 * df2['ATR']
df2['lower_band_2'] = df2['Line'] - multiplier_2 * df2['ATR']


print(df2)

df2.to_csv("gauss.csv")

# https://community.plotly.com/t/how-to-plot-multiple-lines-on-the-same-y-axis-using-plotly-express/29219/9

# https://plotly.com/python/legend/#legend-item-names

# fig1 = px.scatter(df2, x='date', y=['close', 'open', 'high', 'low'], title='SPY Daily Chart')

fig1 = go.Figure(data=[go.Candlestick(x=df2['Datetime'],
                open=df2['open'],
                high=df2['high'],
                low=df2['low'],
                close=df2['close'])]

)

fig1.add_trace(
    go.Scatter(
        x=df2['Datetime'],
        y=df2['upper_band'],
        name='upper band',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        showlegend=True)
)

fig1.add_trace(
    go.Scatter(
        x=df2['Datetime'],
        y=df2['lower_band'],
        name='lower band',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        showlegend=True)
)

fig1.add_trace(
    go.Scatter(
        x=df2['Datetime'],
        y=df2['upper_band_1'],
        name='upper band_1',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        showlegend=True)
)

fig1.add_trace(
    go.Scatter(
        x=df2['Datetime'],
        y=df2['lower_band_1'],
        name='lower band_1',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        showlegend=True)
)


fig1.add_trace(
    go.Scatter(
        x=df2['Datetime'],
        y=df2['Line'],
        name="Gauss",
        mode="lines",
        line=go.scatter.Line(color="blue"),
        showlegend=True)
)

fig1.show()

