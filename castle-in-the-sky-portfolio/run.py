import os.path
import time

file_exists = os.path.exists('Data/tickers-and-eps.xlsx')
if file_exists is False:
    from get_eps_data import *
    update_eps_data(symbol_list[:15])
    from search_twitter import *
    get_sentiment(symbol_list[:15])
    from allocations import *
    update_prices(symbol_list[:15])
    get_allocations(symbol_list[:15])
    from portfolio_tracker import *
    get_shares(symbol_list[:15], 10_000)
    get_portfolio_value(symbol_list[:15])
else:
    # If EPS data is not up-to-date then update it
    from get_eps_data import *
    if eps_db_last_date == today:
        print('EPS Next Year Growth Database Is Up-To-Date')
    else:
        print('Updating Database...')
        update_eps_data(symbol_list[:15])

    # If Sentiment data is not up-to-date then update it
    from search_twitter import *
    if sentiment_db_last_date == today:
        print('Sentiment Database Is Up-To-Date')
    else:
        print('Updating Database...')
        get_sentiment(symbol_list[:15])

    # If Price data is not up-to-date then update it
    from allocations import *
    if prices_last_date == today:
        print('Prices Database Is Up-To-Date')
    else:
        print('Updating Database...')
        update_prices(symbol_list[:15])

    # If it is the end of the month then update allocations
    if allocations_df_date == end_of_month:
        print('Updating Database...')
        get_allocations(symbol_list[:15])
    else:
        print('Allocations Database Is Up-To-Date')

    # Update portfolio value and if it is the end of the month then update allocations
    from portfolio_tracker import *
    if today == shares_df_date:
        print('Shares Database Is Up-To-Date')
        print('Portfolio Value Database Is Up-To-Date')
    else:
        update_shares(symbol_list[:15])
        get_portfolio_value(symbol_list[:15])