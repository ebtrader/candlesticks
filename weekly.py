import math
import numpy as np
from finta import TA
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from datetime import datetime

# WMA
# https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/weighted-moving-average-wma/
# https://stackoverflow.com/questions/9621362/how-do-i-compute-a-weighted-moving-average-using-pandas

# https://futures.io/thinkorswim/18306-help-easylanguage-notation-john-ehlers-4-pole-gaussian-filter.html

# https://github.com/peerchemist/finta/blob/master/finta/finta.py

# https://pypi.org/project/yfinance/
# https://plotly.com/python/candlestick-charts/
# https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/
# https://thispointer.com/pandas-convert-dataframe-index-into-column-using-dataframe-reset_index-in-python/#:~:text=To%20convert%20all%20the%20indexes,on%20the%20dataframe%20object%20i.e.&text=It%20converted%20the%20indexes%20'ID,same%20name%20in%20the%20dataframe.

ticker = "NQ=F"
data = yf.download(tickers = ticker, start='2020-04-01', end='2021-05-26')
#data = yf.download(tickers = ticker, period = "5d", interval= "5m")

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# https://pypi.org/project/yfinance/
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")

df1 = pd.DataFrame(data)

print(df1)

#df = df1.reset_index()

#print(df)

# https://github.com/peerchemist/finta

# https://www.datacamp.com/community/tutorials/python-rename-column?utm_source=adwords_ppc&utm_campaignid=1565261270&utm_adgroupid=67750485268&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=&utm_creative=295208661496&utm_targetid=aud-299261629614:dsa-429603003980&utm_loc_interest_ms=&utm_loc_physical_ms=9004005&gclid=CjwKCAjwtJ2FBhAuEiwAIKu19mq1iWE1XmgD7B6yZvBc6XpTuf_fhxNEcZvf_5BBjHEBA6KvjmMXlBoChrAQAvD_BwE

#df2 = df.rename(columns = {'Date': 'date', 'Open':'open', 'High': 'high', 'Low':'low', 'Close':'close','Volume': 'volume'}, inplace = False)

#print(df2)

output = df1.resample('W').agg({'Open': 'first',
                               'High': 'max',
                               'Low': 'min',
                               'Close': 'last',
                               'Volume': 'sum'}
                               )

print(output)
print(df1)
df1.to_csv('daily.csv')
output.to_csv("weekly.csv")
