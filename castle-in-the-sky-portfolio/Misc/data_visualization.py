from cProfile import label
from locale import normalize
from turtle import color
import pandas as pd
from db_config import engine
import matplotlib.pyplot as plt
import numpy as np
import testfolio as tsf


# Get labels and values for allocation pie chart
connection = engine.connect()
allocations_df = pd.read_sql('allocations', connection).iloc[0]
allocations_df = allocations_df.replace(0, np.nan)
allocations_df = allocations_df.dropna()
allocations_df.drop(index=allocations_df.index[0], axis=0, inplace=True)
allocations_dict = allocations_df.to_dict()
pie_labels = list(allocations_dict.keys())
pie_values = list(allocations_dict.values())

# Get labels and values for portfolio value (line chart)
connection = engine.connect()
portfolio_value_df = pd.read_sql('totalPortfolioValue', connection)
tv_y = portfolio_value_df['Date'].tolist()
tv_x = portfolio_value_df['Total Value'].tolist()

# Visualize Data
fig1, pie_ax1 = plt.subplots()
pie_ax1.pie(pie_values, labels=pie_labels, startangle=90, autopct='%1.1f%%')
pie_ax1.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

plt.plot(tv_x, tv_y, color='blue', marker='o', label='Castle In The Sky Portfolio')
plt.show()
