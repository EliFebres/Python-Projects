import re
import time
import os.path
import pandas as pd
import datetime as dt
from tqdm import tqdm
from misc.db_config import engine
import pandas_datareader as pdr
from warnings import simplefilter
from datetime import datetime, timedelta


# Remove Pandas PerformanceWarning
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
simplefilter(action="ignore", category=FutureWarning)


def update_prices(symbol_list):
    today = dt.datetime.today()
    yesterday = today - timedelta(days=3)
    prices = []
    for symbol in tqdm(symbol_list):
        ticker_prices = pdr.DataReader(symbol, 'yahoo', yesterday, today)['Adj Close']
        price = round(ticker_prices.tolist()[0], 2)
        prices.append(price)
        time.sleep(2)

    prices_df = pd.DataFrame(columns=symbol_list)
    a_series = pd.Series(prices, index=prices_df.columns)
    prices_df = prices_df.append(a_series, ignore_index=True)
    today = pd.to_datetime('today').normalize()
    prices_df.insert(0,'Date', today)

    # If db doesn't exsist, create one. If it does exist, then update
    prices_df.to_sql('prices', con=engine, if_exists='append', index=False)

# Get Last Date in DB and Get Today's Date
try:
    connection = engine.connect()
    prices_db = pd.read_sql('prices', connection)
    prices_last_date = prices_db['Date'][-1:].values
except:
    prices_last_date = 0


def get_allocations(symbol_list):
    today = pd.to_datetime('today').normalize()
    first_of_month = today.replace(day=1)
    end_of_month = today.replace(day=28)

    connection = engine.connect()
    sentiment_data = pd.read_sql('sentiment', connection)

    current_month_number = (sentiment_data['Date'] > first_of_month) & (sentiment_data['Date'] <= end_of_month)
    current_month_sentiment = sentiment_data.loc[current_month_number]
    sentiment_m_average = current_month_sentiment.mean(axis=0, skipna=True, numeric_only=True)
    top20_sentiment = sentiment_m_average.nlargest(n=20).index.to_list()

    first_q = (40/5)/100
    second_q = (30/5)/100
    third_q = (15/5)/100
    fourth_q = (15/5)/100
    percentage_allocated = [first_q]*5 + [second_q]*5 + [third_q]*5 + [fourth_q]*5

    ticker_allocations = {top20_sentiment[i]: percentage_allocated[i] for i in range(len(top20_sentiment))}

    basic_df = pd.DataFrame(columns=symbol_list)
    s1 = pd.Series(ticker_allocations)
    allocations_df = pd.concat([basic_df, s1.to_frame().T], ignore_index=True).fillna(0.00)
    today = pd.to_datetime('today').normalize()
    allocations_df.insert(0,'Date', today)

    # If db doesn't exsist, create one. If it does exist, then update
    allocations_df.to_sql('allocations', con=engine, if_exists='append', index=False)


# Get Last Date in DB and Get Today's Date
try:
    connection = engine.connect()
    allocations_db = pd.read_sql('allocations', connection)
    allocations_last_date = allocations_db['Date'][-1:].values
except:
    allocations_last_date = 0
    
today = pd.to_datetime('today').normalize()
end_of_month = today.replace(day=28)