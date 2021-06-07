import math
import numpy as np
from finta import TA
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd

from datetime import datetime

# https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date

df1 = pd.read_csv('finals/SQL_Streaming.csv')

#print(df1)

clean_df = pd.DataFrame()
clean_df['date'] = df1['time']
# print(clean_df)

# https://github.com/ebtrader/goose_algo/blob/master/Goose_WTDEHMA.py
# df['converted_time'] = pd.to_datetime(df['time'], unit = 's') - pd.Timedelta(4, unit = 'h')
# https://stackoverflow.com/questions/19231871/convert-unix-time-to-readable-date-in-pandas-dataframe
clean_df['id'] = df1['id']
clean_df['date'] = pd.to_datetime(clean_df['date'], unit = 's') - pd.Timedelta(4, unit = 'h')
clean_df['close'] = df1['price']


# print(clean_df)

df2 = clean_df

# print(df2)

n = 144

df3 = df2.groupby(np.arange(len(df2))//n).max()
# print('df3 max:', df3)

df4 = df2.groupby(np.arange(len(df2))//n).min()
# print('df4 min:', df4)

df5 = df2.groupby(np.arange(len(df2))//n).first()
# print('df5 open:', df5)

df6 = df2.groupby(np.arange(len(df2))//n).last()
# print('df6 close:', df6)


agg_df = pd.DataFrame()
agg_df['id'] = df6['id']
agg_df['date'] = df6['date']
agg_df['open'] = df5['close']
agg_df['high'] = df3['close']
agg_df['low'] = df4['close']
agg_df['close'] = df6['close']

agg_df.to_csv('agg.csv')

print(agg_df)

fig1 = go.Figure(data=[go.Candlestick(x=agg_df['date'],
                open=agg_df['open'],
                high=agg_df['high'],
                low=agg_df['low'],
                close=agg_df['close'])]

)

fig1.show()