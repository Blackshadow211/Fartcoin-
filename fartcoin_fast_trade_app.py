
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from fartcoin_ai_chart import generate_signals, fetch_fartcoin_data
import smtplib
from email.mime.text import MIMEText

# ========== CONFIG ==========
THRESHOLD_BUY = -0.04
THRESHOLD_SELL = 0.04
EMAIL_ADDRESS = "your_email@gmail.com"  # Replace with your email
APP_PASSWORD = "your_app_password"      # Replace with your app password
RECIPIENT_EMAIL = "recipient_email@gmail.com"  # Replace with recipient

# ========== EMAIL ==========
def send_email_alert(signal, price, date):
    subject = f"Fartcoin {signal} Signal"
    body = f"Signal: {signal}\nPrice: ${price}\nDate: {date.strftime('%Y-%m-%d')}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Email error:", e)
        return False

# ========== MAIN ==========
st.title("Fartcoin AI Trading Signal (Fast Trades Only)")
st.subheader("Fartcoin Price Chart with Buy/Sell Signals")

# Fetch data and generate signals
data = fetch_fartcoin_data()
df = generate_signals(data, threshold_buy=THRESHOLD_BUY, threshold_sell=THRESHOLD_SELL)

# Plot chart
fig, ax = plt.subplots()
ax.plot(df["Date"], df["Price"], label="Price", color="gray")
buy_signals = df[df["Signal"] == "Buy"]
sell_signals = df[df["Signal"] == "Sell"]
ax.scatter(buy_signals["Date"], buy_signals["Buy_Price"], marker="^", color="green", label="Buy")
ax.scatter(sell_signals["Date"], sell_signals["Sell_Price"], marker="v", color="red", label="Sell")
ax.set_title("Fartcoin Price & Signals")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.legend()
st.pyplot(fig)

# Show latest signal
last_signal = df[df["Signal"] != ""].tail(1)
if not last_signal.empty:
    signal_type = last_signal["Signal"].values[0]
    price = last_signal["Price"].values[0]
    signal_date = last_signal["Date"].values[0]
    st.success(f"Last Signal: {signal_type} at ${price} on {signal_date.strftime('%Y-%m-%d')}")
    email_sent = send_email_alert(signal_type, price, signal_date)
    if email_sent:
        st.info("Email alert sent.")
    else:
        st.warning("Failed to send email alert.")
else:
    st.warning("No good trade opportunity within 1 day.")

# Auto-refresh
st.experimental_rerun()
