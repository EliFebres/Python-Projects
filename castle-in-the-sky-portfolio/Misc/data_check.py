import pandas as pd
from db_config import engine


connection = engine.connect()
#Check all 7 tables

#EPS Data
eps_df = pd.read_sql('eps', connection)
print(eps_df)
#Sentiment Data
sentiment_df = pd.read_sql('sentiment', connection)
print(sentiment_df)
#Price Data
prices_df = pd.read_sql('prices', connection)
print(prices_df)
#Allocation Data
allocations_df = pd.read_sql('allocations', connection)
print(allocations_df)
#Shares Data
shares_df = pd.read_sql('shares', connection)
print(shares_df)
#Portfolio Data
portfolio_df = pd.read_sql('portfolio', connection)
portfolio_value_df = pd.read_sql('totalPortfolioValue', connection)
print(portfolio_df)
print(portfolio_value_df)