
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime, timedelta

# EMAIL CONFIGURATION
SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "xjlrszqzjtmvprfo"

# FAKE LIVE DATA FETCH (replace with MEXC API integration for real prices)
def fetch_price_data():
    base_date = datetime.now() - timedelta(days=9)
    dates = [base_date + timedelta(days=i) for i in range(10)]
    prices = np.round(np.random.normal(loc=1.0, scale=0.1, size=10), 2)
    return pd.DataFrame({'Date': dates, 'Price': prices})

# TRADING STRATEGY - FAST TRADES
def generate_fast_signals(df):
    df['Signal'] = ''
    df['Buy_Price'] = np.nan
    df['Sell_Price'] = np.nan
    for i in range(1, len(df) - 1):
        if df['Price'][i] < df['Price'][i-1] and df['Price'][i] < df['Price'][i+1]:
            df.at[i, 'Signal'] = 'Buy'
            df.at[i, 'Buy_Price'] = df['Price'][i]
        elif df['Price'][i] > df['Price'][i-1] and df['Price'][i] > df['Price'][i+1]:
            df.at[i, 'Signal'] = 'Sell'
            df.at[i, 'Sell_Price'] = df['Price'][i]
    return df

# EMAIL ALERT FUNCTION
def send_email_alert(signal, price, date):
    subject = f"Fartcoin {signal} Alert"
    body = f"A {signal} signal has been triggered for Fartcoin at {price} USD on {date.strftime('%Y-%m-%d')}."

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False

# STREAMLIT APP
st.set_page_config(layout="wide")
st.title("Fartcoin AI Trading Signal (Fast Trades Only)")
st.markdown("Get Buy/Sell predictions based on price changes within 1 day.")

df = fetch_price_data()
df = generate_fast_signals(df)

# CHART
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df['Date'], df['Price'], marker='o', label='Price', color='gray')

# Add buy/sell markers
buy_signals = df[df['Signal'] == 'Buy']
sell_signals = df[df['Signal'] == 'Sell']
ax.scatter(buy_signals['Date'], buy_signals['Buy_Price'], marker='^', color='green', label='Buy', s=100)
ax.scatter(sell_signals['Date'], sell_signals['Sell_Price'], marker='v', color='red', label='Sell', s=100)

ax.set_title("Fartcoin Price & Signals")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.legend()
st.pyplot(fig)

# SHOW LAST SIGNAL + EMAIL
last_signal = df[df['Signal'] != ''].tail(1)
if not last_signal.empty:
    signal_type = last_signal['Signal'].values[0]
    price = last_signal['Price'].values[0]
    signal_date = last_signal['Date'].values[0]
    st.success(f"Last Signal: {signal_type} at ${price} on {signal_date.strftime('%Y-%m-%d')}")
    email_sent = send_email_alert(signal_type, price, signal_date)
    if email_sent:
        st.info("Email alert sent.")
    else:
        st.warning("Failed to send email alert.")
else:
    st.warning("No good trade opportunity within 1 day.")

# AUTO REFRESH
st.experimental_rerun()
