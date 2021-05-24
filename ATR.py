from finta import TA
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
from datetime import datetime

# https://github.com/peerchemist/finta/blob/master/finta/finta.py

# https://pypi.org/project/yfinance/
# https://plotly.com/python/candlestick-charts/
# https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/
# https://thispointer.com/pandas-convert-dataframe-index-into-column-using-dataframe-reset_index-in-python/#:~:text=To%20convert%20all%20the%20indexes,on%20the%20dataframe%20object%20i.e.&text=It%20converted%20the%20indexes%20'ID,same%20name%20in%20the%20dataframe.

ticker = "NQ=F"
data = yf.download(tickers = ticker, period = "12mo")

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

# ATR
num_periods_ATR = 21
multiplier = 1

df2['ATR_diff'] = df2['high'] - df2['low']
df2['ATR'] = df2['ATR_diff'].rolling(window=num_periods_ATR).mean()
df2['Line'] = df2['TEMA']
df2['upper_band'] = df2['Line'] + multiplier * df2['ATR']
df2['lower_band'] = df2['Line'] - multiplier * df2['ATR']

print(df2)

# df2.to_csv("SMA.csv")

# https://community.plotly.com/t/how-to-plot-multiple-lines-on-the-same-y-axis-using-plotly-express/29219/9

# https://plotly.com/python/legend/#legend-item-names

# fig1 = px.scatter(df2, x='date', y=['close', 'open', 'high', 'low'], title='SPY Daily Chart')

fig1 = go.Figure(data=[go.Candlestick(x=df2['date'],
                open=df2['open'],
                high=df2['high'],
                low=df2['low'],
                close=df2['close'])]

)

fig1.add_trace(
    go.Scatter(
        x=df2['date'],
        y=df2['upper_band'],
        name='upper band',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        showlegend=True)
)

fig1.add_trace(
    go.Scatter(
        x=df2['date'],
        y=df2['lower_band'],
        name='lower band',
        mode="lines",
        line=go.scatter.Line(color="gray"),
        showlegend=True)
)


fig1.add_trace(
    go.Scatter(
        x=df2['date'],
        y=df2['TEMA'],
        name="TEMA",
        mode="lines",
        line=go.scatter.Line(color="blue"),
        showlegend=True)
)

fig1.show()

