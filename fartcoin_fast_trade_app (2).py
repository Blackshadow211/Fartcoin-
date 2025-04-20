
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fartcoin_ai_chart import generate_signals, fetch_fartcoin_data
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText

# Email configuration (edit these if needed)
EMAIL_ADDRESS = "remixbooster2@gmail.com"
EMAIL_PASSWORD = "xjlrszqzjtmvprfo"
TO_EMAIL = "remixbooster2@gmail.com"

def send_email_alert(signal, price, date):
    try:
        msg = MIMEText(f"Fartcoin {signal} signal at ${price} on {date.strftime('%Y-%m-%d')}")
        msg["Subject"] = f"Fartcoin {signal} Alert"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        return False

st.set_page_config(page_title="Fartcoin Fast Trade AI", layout="centered")
st.title("Fartcoin AI Trading Signal (Fast Trades Only)")
st.subheader("Fartcoin Price Chart with Buy/Sell Signals")

# Fetch data & generate signals
df = fetch_fartcoin_data()
df = generate_signals(df)

# Plot
fig, ax = plt.subplots()
ax.plot(df["Date"], df["Price"], label="Price", color="gray", marker="o")

buy_signals = df[df["Signal"] == "Buy"]
sell_signals = df[df["Signal"] == "Sell"]
ax.scatter(buy_signals["Date"], buy_signals["Buy_Price"], marker="^", color="green", label="Buy")
ax.scatter(sell_signals["Date"], sell_signals["Sell_Price"], marker="v", color="red", label="Sell")

ax.set_title("Fartcoin Price & Signals")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.legend()
st.pyplot(fig)

# Show last signal + email alert
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

# Auto refresh every 10 seconds
st.experimental_rerun()
