# Portfolio Optimization

Portfolio optimization is the process of picking the optimal portfolio from the set of all possible portfolios based on some criterion. Typically, the purpose maximizes aspects such as expected return while minimizing costs such as financial risk.

This program implements portfolio optimization methods, including classical mean-variance optimization techniques and Sharpe Ratio Optimization, as well as more recent developments in the field like Calmar Ratio.

### File Description

| Path			        | Description											                                    |
| --------------------- | ----------------------------------------------------------------------------------------- |
| get_data.py	        | Obtains daily price data for each ticker inputed for the dates specified		            |
| run.py		        | Calculates statistics for and optimizes the portfolio of assets using specified method	|
| data/price_data.xlsx	| Stores daily price data for tickers specified for use in run.py				            |	


### Program Roadmap

Features to be added/upgraded overtime (Not in order)

* Add each ticker in the Efficient Frontier visualization
* Use SQL to store data and replace Excel
* Use Fama-French 4 Factor Model to determine correlation to different investment strategies
