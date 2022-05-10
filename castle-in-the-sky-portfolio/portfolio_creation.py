from get_eps_data import *
import pandas as pd


eps_data = pd.read_excel('Data/tickers-and-eps-update.xlsx')
eps_data.drop('Unnamed: 0')
# eps_data_sorted = eps_data.sort_values(axis=1)
print(eps_data)

