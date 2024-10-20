Mortgage Investment Analysis
This project analyzes the potential growth of investments made with funds that would otherwise go towards paying off a mortgage. It compares two scenarios:

Investment of the funds into sector ETFs.
Accumulation of the same funds as if they were used to pay off the mortgage directly.
The analysis uses historical data from ETFs or predicted returns to estimate future investment values.

Features
Simulates mortgage payments across multiple loans with varying terms and interest rates.
Compares investment growth against fixed mortgage payments.
Allows toggling between historical data and future predictions for investment analysis.
Visualizes investment growth and target accumulation with a compressed y-axis for better clarity.
Prerequisites
Python 3.7+
Required packages:
yfinance
pandas
matplotlib
numpy
Installation
Install the required packages using pip:

bash
Copy code
pip install yfinance pandas matplotlib numpy
Usage
Step 1: Define Mortgage Parameters
Modify the loans list to set up your mortgage details:

python
Copy code
loans = [
    {'principal': 32926, 'interest_rate': 5.99 / 100, 'years_left': 4},
    {'principal': 84816, 'interest_rate': 4.04 / 100, 'years_left': 10 + 5/12},  # 10 years 5 months remaining
    {'principal': 51584, 'interest_rate': 4.04 / 100, 'years_left': 7 + 9/12}   # 7 years 9 months remaining
]
Step 2: Configure Investment ETFs
Specify your ETF list and their predicted annual returns:

python
Copy code
etfs = ['XLK', 'XLV', 'XLY', 'XLP', 'XLF', 'XLI']
predicted_annual_returns = {
    'XLK': 0.10,
    'XLV': 0.08,
    'XLY': 0.09,
    'XLP': 0.07,
    'XLF': 0.08,
    'XLI': 0.075
}
Step 3: Toggle Historical Data
Use historical data or predicted returns for your analysis:

python
Copy code
use_historical_data = False  # Set to True to use historical data, False to use predicted returns
Step 4: Run the Analysis
Execute the code to perform the investment analysis and visualize the results.

Step 5: Visualize the Results
The results will be displayed in a plot that shows both the investment value growth and the target value accumulation over time.

Example Plot
The plot illustrates the growth of the investment in comparison to the fixed mortgage payments, with a compressed y-axis to focus on relevant value ranges.

Customization
You can adjust parameters such as interest rates, the number of years left on the mortgage, ETF selection, and expected returns to tailor the analysis to your needs.

License
This project is licensed under the MIT License.

Feel free to modify and enhance the code to suit your specific analysis needs!
