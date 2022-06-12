import pandas as pd
from db_config import engine



connection = engine.connect()
#Check all 7 tables

#EPS Data
eps_df = pd.read_sql('eps', connection)
#Sentiment Data
sentiment_df = pd.read_sql('sentiment', connection)
#Price Data
prices_df = pd.read_sql('prices', connection)
#Allocation Data
allocations_df = pd.read_sql('allocations', connection)
#Shares Data
shares_df = pd.read_sql('shares', connection)
#Portfolio Data
portfolio_df = pd.read_sql('portfolio', connection)
portfolio_value_df = pd.read_sql('totalPortfolioValue', connection)