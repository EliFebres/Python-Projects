import pandas as pd
import pandas_datareader as pdr
import numpy as np
import datetime as dt

start_date = dt.datetime(2016,1,1)
end_date = dt.datetime(2022,1,1)
days_between = end_date - start_date
rf = 0.02

# Get Data for each Asset Class
tickers = ['SPY', 'QQQ', 'GLD', 'BND']
ticker_prices = pdr.DataReader(tickers, 'yahoo', start= start_date, end= end_date)['Adj Close']

# Combine each dataset and remove NaN Rows
data_frames = [ticker_prices]
price_data = pd.concat(data_frames, axis=1,).dropna()

price_data.to_excel('Data\price_data.xlsx')
