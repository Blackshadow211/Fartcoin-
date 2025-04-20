
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime

def fetch_fartcoin_data(limit=100):
    url = "https://api.mexc.com/api/v3/klines?symbol=FARTUSDT&interval=1h&limit=" + str(limit)
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])
    df['Date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['Price'] = df['close'].astype(float)
    return df[['Date', 'Price']]

def generate_signals(df):
    df['Signal'] = ''
    df['Buy_Price'] = np.nan
    df['Sell_Price'] = np.nan

    for i in range(2, len(df)-1):
        # Simple logic: Buy if current price is less than previous two and next price is higher (local min)
        if df['Price'][i] < df['Price'][i-1] and df['Price'][i] < df['Price'][i-2] and df['Price'][i] < df['Price'][i+1]:
            df.at[i, 'Signal'] = 'Buy'
            df.at[i, 'Buy_Price'] = df['Price'][i]
        # Sell if current price is higher than previous two and next price is lower (local max)
        elif df['Price'][i] > df['Price'][i-1] and df['Price'][i] > df['Price'][i-2] and df['Price'][i] > df['Price'][i+1]:
            df.at[i, 'Signal'] = 'Sell'
            df.at[i, 'Sell_Price'] = df['Price'][i]
    return df

def plot_chart(df):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['Date'], df['Price'], label='Price', color='gray', marker='o')

    buy_signals = df[df['Signal'] == 'Buy']
    sell_signals = df[df['Signal'] == 'Sell']

    ax.scatter(buy_signals['Date'], buy_signals['Buy_Price'], label='Buy', marker='^', color='green', s=100)
    ax.scatter(sell_signals['Date'], sell_signals['Sell_Price'], label='Sell', marker='v', color='red', s=100)

    ax.set_title("Fartcoin Price & Signals")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    return fig
