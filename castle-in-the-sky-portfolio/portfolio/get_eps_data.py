import time
import os.path
import pandas as pd
from tqdm import tqdm
from misc.db_config import engine
from warnings import simplefilter
from finvizfinance.quote import finvizfinance

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
simplefilter(action="ignore", category=FutureWarning)

# Get Next Year EPS Grwoth for Each Ticker in S&P500

def get_sp500_tickers():
    data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    first_table = data[0]
    second_table = data[1]
    df = first_table
    symbols = df['Symbol'].values.tolist()
    textfile = open('data/S&P500_tickers.txt', 'w')
    for symbol in symbols:
            textfile.write(f"{symbol},")
    textfile.close()

textfile = open('Data/S&P500_tickers.txt', 'r') 
symbols = textfile.read()
symbol_list = symbols.split(',')
symbol_list.pop(-1)
symbol_list.remove('BRK.B')
symbol_list.remove('BF.B')
symbol_list.remove('BALL')
textfile.close()


def update_eps_data(tickers):
    ticker_eps_growth = []
    step = 25
    x = 0
    y = step
    for i in tqdm(range((len(symbol_list)//step)+1)):
        for ticker in tickers[x:y]:
            stock = finvizfinance(ticker)
            stock_fundamentals = stock.ticker_fundament()['EPS next Y']
            string_to_number = stock_fundamentals[:-1]
            try:
                eps_percent = round(float(string_to_number) / 100, 4)
            except ValueError:
                eps_percent = 0.0
            ticker_eps_growth.append(eps_percent)
        x += step
        y += step
        time.sleep(3.5)
        

    eps_next_df = pd.DataFrame(columns=tickers)
    a_series = pd.Series(ticker_eps_growth, index=eps_next_df.columns)
    eps_next_df = eps_next_df.append(a_series, ignore_index=True)
    today = pd.to_datetime('today').normalize()
    eps_next_df.insert(0,'Date', today)

    # If db doesn't exsist, create one. If it does exist, then update
    eps_next_df.to_sql('eps', con=engine, if_exists='append', index=False)


# Get Last Date in DB and Get Today's Date
try:
    connection = engine.connect()
    eps_db = pd.read_sql('eps', connection)
    eps_last_date = eps_db['Date'][-1:].values
except:
    eps_last_date = 0

print(eps_last_date)