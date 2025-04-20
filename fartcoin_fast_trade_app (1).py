
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from fartcoin_ai_chart import generate_signals, fetch_fartcoin_data
from sendgrid_emailer import send_email_alert

# Load and process Fartcoin data
df = fetch_fartcoin_data()
df = generate_signals(df)

# Plotting
st.title("Fartcoin AI Trading Signal (Fast Trades Only)")
st.subheader("Fartcoin Price Chart with Buy/Sell Signals")

fig, ax = plt.subplots()
ax.plot(df['Date'], df['Price'], label='Price', color='gray', marker='o')

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

# Show last signal and send email
last_signal = df[df['Signal'] != ''].tail(1)

if not last_signal.empty:
    signal_type = last_signal['Signal'].values[0]
    price = last_signal['Price'].values[0]
    signal_date = last_signal['Date'].values[0]

    if signal_date is not None:
        st.success(f"Last Signal: {signal_type} at ${price} on {signal_date.strftime('%Y-%m-%d')}")
        email_sent = send_email_alert(signal_type, price, signal_date)
        if email_sent:
            st.info("Email alert sent.")
        else:
            st.warning("Failed to send email alert.")
    else:
        st.warning("No valid trade signal date.")
else:
    st.warning("No good trade opportunity within 1 day.")

# Auto refresh
st.experimental_rerun()
