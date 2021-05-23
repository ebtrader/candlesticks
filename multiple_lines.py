import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
from datetime import datetime

# https://pypi.org/project/yfinance/
# https://plotly.com/python/candlestick-charts/
# https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/
# https://thispointer.com/pandas-convert-dataframe-index-into-column-using-dataframe-reset_index-in-python/#:~:text=To%20convert%20all%20the%20indexes,on%20the%20dataframe%20object%20i.e.&text=It%20converted%20the%20indexes%20'ID,same%20name%20in%20the%20dataframe.


data = yf.download(tickers = "SPY", period = "3mo")

df1 = pd.DataFrame(data)

print(df1)

df = df1.reset_index()

print(df)

# https://community.plotly.com/t/how-to-plot-multiple-lines-on-the-same-y-axis-using-plotly-express/29219/9

fig1 = px.line(df, x='Date', y=['Close', 'Open'], title='SPY Daily Chart')
fig1.show()
