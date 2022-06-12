import time
from get_eps_data import *
from search_twitter import *
from allocations import *
from portfolio_tracker import *
from db_config import engine
import sqlalchemy as sql


def main():
    insp = sql.inspect(engine)
    file_exists = insp.has_table('eps')
    if file_exists is False:
        print('Creating EPS Database...')
        update_eps_data(symbol_list)
        print('Creating Sentiment Database...')
        get_sentiment(symbol_list)
        print('Creating Prices Database...')
        while True: # Run update prices until error is not recieved
            try:
                update_prices(symbol_list)
                break
            except:
                print('Trying Again To Create Prices Database...')
                pass
        print('Creating Allocations and Shares Database...')
        get_allocations(symbol_list)
        get_shares(symbol_list, 10_000)
        print('Creating Portfolio Databases...')
        get_portfolio_value(symbol_list)
        print('Done')
    else:
        # If EPS data is not up-to-date then update it
        if eps_last_date == end_of_month:
            print('Updating EPS Database...')
            update_eps_data(symbol_list)
        else:
            print('EPS Next Year Growth Database Is Up-To-Date')

        # If Sentiment data is not up-to-date then update it
        if sentiment_last_date == today:
            print('Sentiment Database Is Up-To-Date')
        else:
            print('Updating Sentiment Database...')
            get_sentiment(symbol_list)

        # If Price data is not up-to-date then update it
        if prices_last_date == today:
            print('Prices Database Is Up-To-Date')
        else:
            print('Updating Prices Database...')
            while prices_last_date != today:
                try:
                    update_prices(symbol_list)
                    break
                except:
                    time.sleep(10)
                    print('Trying to Update Prices Database Again...')
                    pass

        # If it is the end of the month then update allocations
        if allocations_last_date == end_of_month:
            print('Updating Allocations and Shares Database...')
            get_allocations(symbol_list)
            update_shares(symbol_list)
        else:
            print('Allocations Database Is Up-To-Date')
            print('Shares Database Is Up-To-Date')

        # Update portfolio value and if it is the end of the month then update allocations
        if portfolio_last_date == today:
            print('Portfolio Value Database Is Up-To-Date')
        else:
            print('Updating Portfolio Databases...')
            get_portfolio_value(symbol_list)
        print('Done')

main()