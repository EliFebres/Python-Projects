import pandas as pd
from misc.db_config import engine


def get_shares(symbol_list, portfolio_value):
    
    # Pull price and allocation data to get the initial shares db for each ticker
    connection = engine.connect()
    prices_list = pd.read_sql('prices', connection).iloc[-1:].values.tolist()
    del prices_list[0]
    allocations_list = pd.read_sql('allocations', connection).iloc[-1:].values.tolist()
    del allocations_list[0]

    shares = []
    for num1, num2 in zip(prices_list, allocations_list):
        shares.append((num2 * portfolio_value) / num1)
    
    shares_df = pd.DataFrame(columns=symbol_list)
    a_series = pd.Series(shares, index=shares_df.columns)
    shares_df = shares_df.append(a_series, ignore_index=True)
    today = pd.to_datetime('today').normalize()
    shares_df.insert(0,'Date', today)


    # If db doesn't exsist, create one. If it does exist, then update
    shares_df.to_sql('shares', con=engine, if_exists='append', index=False)


def update_shares(symbol_list): #Figure out how to update shares with SQL
    today = pd.to_datetime('today').normalize()
    end_of_month = today.replace(day=28)

    connection = engine.connect()
    portfolio_value_df = pd.read_sql('prices', connection)
    portfolio_value = portfolio_value_df.iloc[-1:].values.tolist().pop(1)

    if today == end_of_month:
        get_shares(symbol_list, portfolio_value)
    else:
        # copy the first row of the shares db
        shares_list = pd.read_sql('shares', connection).iloc[-1:].values.tolist()
        del shares_list[0]
        shares_df = pd.DataFrame(columns=symbol_list)
        a_series = pd.Series(shares_list, index=shares_df.columns)
        shares_df = shares_df.append(a_series, ignore_index=True)
        today = pd.to_datetime('today').normalize()
        shares_df.insert(0,'Date', today)
        
        # If db doesn't exsist, create one. If it does exist, then update
        shares_df.to_sql('shares', con=engine, if_exists='append', index=False)


# Get Last Date in DB and Get Today's Date
try:
    connection = engine.connect()
    shares_db = pd.read_sql('shares', connection)
    shares_last_date = shares_db['Date'][-1:].values
except:
    shares_last_date = 0


def get_portfolio_value(symbol_list):
    connection = engine.connect()
    shares_list = pd.read_sql('shares', connection).iloc[-1:].values.tolist()
    del shares_list[0]
    prices_list = pd.read_sql('prices', connection).iloc[-1:].values.tolist()
    del prices_list[0]

    values = []
    for num1, num2 in zip(prices_list, shares_list):
        values.append(round(num1 * num2, 2))
    
    #create portfolio values db
    portfolio_df = pd.DataFrame(columns=symbol_list)
    a_series = pd.Series(values, index=portfolio_df.columns)
    portfolio_df = portfolio_df.append(a_series, ignore_index=True)

    #create total portfolio db
    portfolio_sum = portfolio_df.sum(axis=1).values.tolist()
    total_value = {'Total Value': portfolio_sum}
    total_pf_value_df = pd.DataFrame.from_dict(total_value)

    # Add date to db
    today = pd.to_datetime('today').normalize()
    total_pf_value_df.insert(0,'Date', today)
    portfolio_df.insert(0,'Date', today)


    # If db doesn't exsist, create one. If it does exist, then update
    portfolio_df.to_sql('portfolio', con=engine, if_exists='append', index=False)
    total_pf_value_df.to_sql('totalPortfolioValue', con=engine, if_exists='append', index=False)


# Get Last Date in DB and Get Today's Date
try:
    connection = engine.connect()
    portfolio_db = pd.read_sql('portfolio', connection)
    portfolio_last_date = portfolio_db['Date'][-1:].values
except:
    portfolio_last_date = 0