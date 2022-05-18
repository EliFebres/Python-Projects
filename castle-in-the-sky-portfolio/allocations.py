from datetime import datetime, timedelta
import datetime as dt
import pandas as pd
import pandas_datareader as pdr
import re
from tqdm import tqdm
import time
import os.path
from warnings import simplefilter


today = dt.datetime.today()
yesterday = today - timedelta(days=1)
ticker_prices = pdr.get_data_yahoo('MSFT', yesterday, today)['Adj Close']
price = round(ticker_prices.tolist()[0], 2)

# Remove of Pandas PerformanceWarning
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


def update_prices(symbol_list):
    today = dt.datetime.today()
    yesterday = today - timedelta(days=1)
    prices = []
    for symbol in tqdm(symbol_list):
        ticker_prices = pdr.get_data_yahoo(symbol, yesterday, today)['Adj Close']
        price = round(ticker_prices.tolist()[0], 2)
        prices.append(price)
        time.sleep(1)

    prices_df = pd.DataFrame(columns=symbol_list)
    a_series = pd.Series(prices, index=prices_df.columns)
    prices_df = prices_df.append(a_series, ignore_index=True)
    today = pd.to_datetime('today').normalize()
    prices_df.insert(0,'Date', today)

    # If db doesn't exsist, create one. If it does exist, then update
    file_exists = os.path.exists('Data/prices.xlsx')
    if file_exists:
        df2 = pd.read_excel('Data/prices.xlsx')
        result = pd.concat([prices_df, df2], ignore_index=True, sort=False)
        result.to_excel('Data/prices-update.xlsx', index=False)
        df3 = pd.read_excel('Data/prices-update.xlsx')
        df3.to_excel('Data/prices.xlsx', index=False)
    else:
        prices_df.to_excel('Data/prices.xlsx', index=False)
    
# Get Last Date in DB and Get Today's Date
prices_df = pd.read_excel('Data/tickers-and-eps.xlsx')
prices_last_date = prices_df['Date'][0]
today = pd.to_datetime('today').normalize()



def get_allocations(symbol_list):
    today = pd.to_datetime('today').normalize()
    first_of_month = today.replace(day=1)
    end_of_month = today.replace(day=30)

    sentiment_data = pd.read_excel('Data/sentiment.xlsx')

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
    file_exists = os.path.exists('Data/allocations-df.xlsx')
    if file_exists:
        df2 = pd.read_excel('Data/allocations-df.xlsx')
        result = pd.concat([allocations_df, df2], ignore_index=True, sort=False)
        result.to_excel('Data/allocations-df-update.xlsx', index=False)
        df3 = pd.read_excel('Data/allocations-df-update.xlsx')
        df3.to_excel('Data/allocations-df.xlsx', index=False)
    else:
        allocations_df.to_excel('Data/allocations-df.xlsx', index=False)


# Get Last Date in DB and Get Today's Date
try:
    allocations_df = pd.read_excel('Data/allocations-df.xlsx')
    allocations_df_date = allocations_df['Date'][0]
except:
    allocations_df_date = 0

end_of_month = today.replace(day=30)