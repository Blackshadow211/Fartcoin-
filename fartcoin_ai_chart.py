
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Simulate fetching data (replace with real API call later)
def fetch_fartcoin_data():
    base_date = datetime.today()
    dates = [base_date - timedelta(days=i) for i in range(10)][::-1]
    prices = [1.02, 0.97, 0.93, 0.85, 0.80, 0.95, 1.05, 0.98, 0.87, 0.91]
    df = pd.DataFrame({'Date': dates, 'Price': prices})
    return df

# Generate Buy/Sell signals based on threshold logic
def generate_signals(df, threshold_buy=-0.03, threshold_sell=0.03):
    df = df.copy()
    df['Signal'] = ''
    df['Buy_Price'] = np.nan
    df['Sell_Price'] = np.nan

    for i in range(1, len(df)):
        pct_change = (df.loc[i, 'Price'] - df.loc[i - 1, 'Price']) / df.loc[i - 1, 'Price']
        if pct_change <= threshold_buy:
            df.at[i, 'Signal'] = 'Buy'
            df.at[i, 'Buy_Price'] = df.loc[i, 'Price']
        elif pct_change >= threshold_sell:
            df.at[i, 'Signal'] = 'Sell'
            df.at[i, 'Sell_Price'] = df.loc[i, 'Price']
    return df
