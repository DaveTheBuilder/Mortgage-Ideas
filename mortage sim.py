import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Define the mortgage and investment parameters as variables
mortgage_principal = 170000  # Principal amount of the mortgage in £
mortgage_interest_rate = 4.5 / 100  # Annual interest rate of the mortgage
current_monthly_payment = 2252  # Current fixed monthly mortgage payment in £
years_left = 10  # Years left to pay the mortgage

# Toggle between historical data and predicted returns
use_historical_data = False  # Set to False to use predicted returns
predicted_annual_return = 0.08  # Predicted annual return if using future growth

# Step 2: Download S&P 500 historical data if using historical data
if use_historical_data:
    start_date = "2009-10-01"
    end_date = "2024-10-01"
    ticker = "^GSPC"  # S&P 500 index symbol on Yahoo Finance

    # Fetch the historical data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date, interval='1d')

    # Step 3: Filter the data to only include the 26th of each month (or the closest available date)
    data['Date'] = data.index
    data['Day'] = data['Date'].dt.day
    filtered_data = data.groupby([data['Date'].dt.year, data['Date'].dt.month], as_index=False).apply(
        lambda x: x.iloc[(x['Day'] - 26).abs().argsort()[:1]]
    ).reset_index(drop=True)

    # Extract the 'Close' price on the filtered dates
    filtered_data = filtered_data[['Date', 'Close']]
else:
    # Create a date range for the future predictions
    filtered_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-10-01', periods=years_left * 12, freq='M')
    })

# Step 4: Define parameters for investment analysis
monthly_interest_payment = (mortgage_interest_rate / 12) * mortgage_principal
monthly_investment_amount = current_monthly_payment - monthly_interest_payment

# Step 5: Perform the investment analysis and mortgage repayment tracking
investment_value = 0  # Initial investment value
remaining_mortgage_balance = mortgage_principal  # Start with the full mortgage principal
investment_history = []
mortgage_balance_history = []

for i in range(len(filtered_data)):
    # Update investment value based on monthly returns
    if use_historical_data:
        monthly_return = filtered_data['Close'].iloc[i] / filtered_data['Close'].iloc[i - 1] - 1 if i > 0 else 0
        investment_value = investment_value * (1 + monthly_return) + monthly_investment_amount
    else:
        # Use predicted annual return
        monthly_return = predicted_annual_return / 12
        investment_value = investment_value * (1 + monthly_return) + monthly_investment_amount
    
    investment_history.append(investment_value)

    # Calculate the remaining mortgage balance using the fixed monthly repayment of £2,252
    if remaining_mortgage_balance > 0:
        interest_payment = (mortgage_interest_rate / 12) * remaining_mortgage_balance
        principal_payment = current_monthly_payment - interest_payment
        remaining_mortgage_balance -= principal_payment
        mortgage_balance_history.append(max(remaining_mortgage_balance, 0))  # Ensure balance does not go below zero
    else:
        mortgage_balance_history.append(0)  # Once mortgage is paid off, balance remains zero

# Step 6: Plot the investment growth and mortgage repayment over time
plt.figure(figsize=(12, 6))
plt.plot(filtered_data['Date'], investment_history, label='Investment Value', color='blue')
plt.plot(filtered_data['Date'], mortgage_balance_history, label='Mortgage Balance with Repayments', color='green')
plt.axhline(y=mortgage_principal, color='red', linestyle='--', label='Initial Mortgage Principal (£170,000)')
plt.title('Investment Growth and Mortgage Repayment Over Time')
plt.xlabel('Date')
plt.ylabel('Value (£)')
plt.legend()
plt.grid(True)
plt.show()
