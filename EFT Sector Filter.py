import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the ETFs for each sector
etfs = {
    'Technology': 'XLK',
    'Healthcare': 'XLV',
    'Consumer Discretionary': 'XLY',
    'Consumer Staples': 'XLP',
    'Financials': 'XLF',
    'Industrials': 'XLI',
    'Energy': 'XLE',
    'Utilities': 'XLU',
    'Real Estate': 'XLRE'
}

# Define the time period for data extraction
start_date = '2004-10-19'  # 20 years ago from today's date
end_date = '2024-10-19'  # Current date

# Create a DataFrame to store adjusted closing prices
price_data = pd.DataFrame()

# Download historical data for each ETF
for sector, etf in etfs.items():
    data = yf.download(etf, start=start_date, end=end_date)
    price_data[sector] = data['Adj Close']

# Calculate monthly returns based on investments on the 26th of each month
# First, ensure we have monthly data
monthly_data = price_data.resample('M').last()  # Get last trading day of each month

# Create a new DataFrame to store monthly returns
monthly_returns = monthly_data.pct_change().dropna()  # Calculate monthly returns

# Extract the monthly return for each ETF as a new DataFrame
monthly_returns_table = monthly_returns.copy()

# Display the monthly returns table
print("Monthly Returns for S&P 500 Sector ETFs:")
print(monthly_returns_table)

# Plotting the cumulative returns
cumulative_returns = (monthly_data / monthly_data.iloc[0]) - 1
plt.figure(figsize=(14, 8))
for sector in cumulative_returns.columns:
    plt.plot(cumulative_returns.index, cumulative_returns[sector], label=sector)

plt.title('Cumulative Returns of S&P 500 Sector ETFs Over the Last 20 Years')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid()
plt.show()
