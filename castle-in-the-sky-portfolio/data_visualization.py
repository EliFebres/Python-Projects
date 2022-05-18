from cProfile import label
from locale import normalize
from turtle import color
import pandas as pd
import matplotlib.pyplot as plt

def visualize_data():
    pass


# Get labels and values for allocation pie chart
allocations_df = pd.read_excel('Data/allocations-df.xlsx').iloc[0]
allocations_df.drop(index=allocations_df.index[0], axis=0, inplace=True)
allocations_dict = allocations_df.to_dict()
pie_labels = list(allocations_dict.keys())
pie_values = list(allocations_dict.values())

# Get labels and values for portfolio value (line chart)
portfolio_value_df = pd.read_excel('Data/total-portfolio-value.xlsx')
tv_y = portfolio_value_df['Date'].tolist()
tv_x = portfolio_value_df['Total Value'].tolist()




fig1, pie_ax1 = plt.subplots()
pie_ax1.pie(pie_values, labels=pie_labels, startangle=90, autopct='%1.1f%%')
pie_ax1.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

plt.plot(tv_x, tv_y, color='blue', marker='o', label='Castle In The Sky Portfolio')
plt.show()
