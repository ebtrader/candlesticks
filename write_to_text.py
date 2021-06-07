import yfinance as yf
import datetime
import os.path

ticker = "NQ=F"
data = yf.download(tickers = ticker, start='2010-01-04', end='2018-12-31')
today = datetime.date.today().strftime("%Y%m%d")
file_path = f"data/ticks_{ticker}_{today}.csv"
if not os.path.exists("data"):
    os.makedirs("data")
fd = open(file_path, "w")
fd.write(data.to_csv())

# self.fd.write(f"{time},{tickType},{price},{size}\n")