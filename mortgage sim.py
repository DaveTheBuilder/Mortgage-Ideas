import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Define the mortgage parameters for three separate loans
loans = [
    {'principal': 32926, 'interest_rate': 5.99 / 100, 'years_left': 4},
    {'principal': 84816, 'interest_rate': 4.04 / 100, 'years_left': 10 + 5/12},  # 10 years 5 months remaining
    {'principal': 51584, 'interest_rate': 4.04 / 100, 'years_left': 7 + 9/12}   # 7 years 9 months remaining
]
 
# Combined mortgage principal for reference
total_mortgage_principal = sum(loan['principal'] for loan in loans)
current_monthly_payment = 2252  # Current fixed total monthly mortgage payment in £

# Toggle between historical data and predicted returns
use_historical_data = False  # Set to True to use historical data, False to use predicted returns

# Step 2: Define the top 6 sector ETFs and their predicted annual returns
etfs = ['XLK', 'XLV', 'XLY', 'XLP', 'XLF', 'XLI']  # Technology, Healthcare, Consumer Discretionary, Consumer Staples, Financials, Industrials
predicted_annual_returns = {
    'XLK': 0.10,  # Technology - 10% estimated return
    'XLV': 0.08,  # Healthcare - 8% estimated return
    'XLY': 0.09,  # Consumer Discretionary - 9% estimated return
    'XLP': 0.07,  # Consumer Staples - 7% estimated return
    'XLF': 0.08,  # Financials - 8% estimated return
    'XLI': 0.075  # Industrials - 7.5% estimated return
}

# Step 3: Download historical data for each ETF if using historical data
if use_historical_data:
    start_date = "2009-10-01"
    end_date = "2024-10-01"

    # Create a DataFrame to store adjusted closing prices
    price_data = pd.DataFrame()

    # Download historical data for each ETF
    for etf in etfs:
        data = yf.download(etf, start=start_date, end=end_date, interval='1d')
        price_data[etf] = data['Adj Close']

    # Filter to only include the 26th of each month (or the closest available date)
    filtered_data = price_data.resample('M').last()  # Get last trading day of each month
else:
    # Create a date range for future predictions
    filtered_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-10-01', periods=max(loan['years_left'] for loan in loans) * 12, freq='M')
    })

# Step 4: Define parameters for investment analysis
monthly_interest_payments = [(loan['interest_rate'] / 12) * loan['principal'] for loan in loans]
monthly_investment_amount = current_monthly_payment - sum(monthly_interest_payments)

# Step 5: Perform the investment analysis and target growth tracking
investment_value = 0  # Initial investment value
target_investment_value = 0  # Initial target value using mortgage payments
investment_history = []
target_investment_history = []

for i in range(len(filtered_data)):
    # Update investment value based on monthly returns
    if use_historical_data:
        # Calculate monthly returns for each ETF
        if i > 0:
            monthly_returns = filtered_data.iloc[i] / filtered_data.iloc[i - 1] - 1
        else:
            monthly_returns = pd.Series([0] * len(etfs), index=etfs)

        # Spread investment equally across ETFs
        investment_value += monthly_investment_amount / len(etfs)

        # Update the investment value for each ETF
        for etf in etfs:
            investment_value += (investment_value / len(etfs)) * monthly_returns[etf]
    else:
        # Use predicted annual return for each ETF
        for etf in etfs:
            monthly_return = predicted_annual_returns[etf] / 12  # Convert annual return to monthly return
            investment_value += monthly_investment_amount / len(etfs)  # Add investment amount equally to each ETF
            investment_value *= (1 + monthly_return)  # Update investment with the ETF's predicted return

    investment_history.append(investment_value)

    # Accumulate the target investment value using the fixed monthly repayment amount
    target_investment_value += current_monthly_payment
    target_investment_history.append(target_investment_value)

# Custom function to compress the y-axis above a threshold
def compress_y_values(value, threshold=2000000, factor=0.1):
    return value if value <= threshold else threshold + (value - threshold) * factor

# Apply the compression to the investment and target histories
compressed_investment_history = [compress_y_values(v) for v in investment_history]
compressed_target_investment_history = [compress_y_values(v) for v in target_investment_history]

# Step 6: Plot the investment growth and target value accumulation with compressed y-axis
plt.figure(figsize=(18, 10))  # Larger chart size for better visibility
plt.plot(filtered_data['Date'], compressed_investment_history, label='Investment Value', color='blue')
plt.plot(filtered_data['Date'], compressed_target_investment_history, label='Target Value Accumulation', color='green')
plt.axhline(y=compress_y_values(total_mortgage_principal), color='red', linestyle='--', label=f'Initial Mortgage Principal (£{total_mortgage_principal})')

# Increase granularity of x-axis and y-axis
plt.xticks(pd.date_range(start=filtered_data['Date'].min(), end=filtered_data['Date'].max(), freq='Y'), rotation=45)
plt.locator_params(axis='y', nbins=20)  # More detailed y-axis tick marks

# Set the maximum y-axis value to focus on the relevant range
plt.ylim(0, compress_y_values(500000))  # Set maximum y-axis to £500,000

plt.title('Investment Growth and Target Value Accumulation Over Time with Compressed Y-Axis')
plt.xlabel('Date')
plt.ylabel('Value (£)')
plt.legend()
plt.grid(True)
plt.tight_layout()  # Adjust layout to prevent overlapping labels
plt.show()
