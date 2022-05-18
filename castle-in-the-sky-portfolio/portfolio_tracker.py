import pandas as pd
from get_eps_data import *


def get_shares(symbol_list, portfolio_value):
    
    # Pull price and allocation data to get the initial shares db for each ticker
    prices_list = pd.read_excel('Data/prices.xlsx').iloc[0].values.tolist()
    del prices_list[0]
    allocations_list = pd.read_excel('Data/allocations-df.xlsx').iloc[0].values.tolist()
    del allocations_list[0]

    shares = []
    for num1, num2 in zip(prices_list, allocations_list):
        shares.append((num2 * portfolio_value) / num1)
    
    shares_df = pd.DataFrame(columns=symbol_list)
    a_series = pd.Series(shares, index=shares_df.columns)
    shares_df = shares_df.append(a_series, ignore_index=True)
    today = pd.to_datetime('today').normalize()
    shares_df.insert(0,'Date', today)


    file_exists = os.path.exists('Data/shares.xlsx')
    if file_exists:
        df2 = pd.read_excel('Data/shares.xlsx')
        result = pd.concat([shares_df, df2], ignore_index=True, sort=False)
        result.to_excel('Data/shares-update.xlsx', index=False)
        df3 = pd.read_excel('Data/shares-update.xlsx')
        df3.to_excel('Data/shares.xlsx', index=False)
    else:
        shares_df.to_excel('Data/shares.xlsx', index=False)


def update_shares(symbol_list):
    today = pd.to_datetime('today').normalize()
    end_of_month = today.replace(day=30)

    portfolio_value_df = pd.read_excel('Data/total-portfolio-value.xlsx')
    portfolio_value = portfolio_value_df.iloc[0].values.tolist().pop(1)

    if today == end_of_month:
        get_shares(symbol_list, portfolio_value)
    else:
        # copy the first row of the shares db
        shares_df = pd.read_excel('Data/shares.xlsx')
        shares_list = pd.read_excel('Data/shares.xlsx').iloc[0].values.tolist()
        del shares_list[0]
        shares_df = pd.DataFrame(columns=symbol_list)
        a_series = pd.Series(shares_list, index=shares_df.columns)
        shares_df = shares_df.append(a_series, ignore_index=True)
        today = pd.to_datetime('today').normalize()
        shares_df.insert(0,'Date', today)
        # Add the copied row to the updated db
        df2 = pd.read_excel('Data/shares.xlsx')
        result = pd.concat([shares_df, df2], ignore_index=True, sort=False)
        result.to_excel('Data/shares-update.xlsx', index=False)
        df3 = pd.read_excel('Data/shares-update.xlsx')
        df3.to_excel('Data/shares.xlsx', index=False)

# Get Last Date in DB and Get Today's Date
try:
    shares_df = pd.read_excel('Data/shares.xlsx')
    shares_df_date = shares_df['Date'][0]
except:
    shares_df_date = 0

today = pd.to_datetime('today').normalize()
end_of_month = today.replace(day=30)


def get_portfolio_value(symbol_list):
    shares_list = pd.read_excel('Data/shares.xlsx').iloc[0].values.tolist()
    del shares_list[0]
    prices_list = pd.read_excel('Data/prices.xlsx').iloc[0].values.tolist()
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


    file_exists = os.path.exists('Data/portfolio-value.xlsx')
    if file_exists:
        df2 = pd.read_excel('Data/portfolio-value.xlsx')
        result = pd.concat([portfolio_df, df2], ignore_index=True, sort=False)
        result.to_excel('Data/portfolio-value-update.xlsx', index=False)
        df3 = pd.read_excel('Data/portfolio-value-update.xlsx')
        df3.to_excel('Data/portfolio-value.xlsx', index=False)

        df4 = pd.read_excel('Data/total-portfolio-value.xlsx')
        result = pd.concat([total_pf_value_df, df4], ignore_index=True, sort=False)
        result.to_excel('Data/total-portfolio-value-update.xlsx', index=False)
        df5 = pd.read_excel('Data/total-portfolio-value-update.xlsx')
        df5.to_excel('Data/total-portfolio-value.xlsx', index=False)
    else:
        portfolio_df.to_excel('Data/portfolio-value.xlsx', index=False)
        total_pf_value_df.to_excel('Data/total-portfolio-value.xlsx', index=False)

