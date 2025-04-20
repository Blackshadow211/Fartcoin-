
import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Mock Fartcoin price data and signals
def get_price_data():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=10)
    prices = np.random.uniform(low=0.8, high=1.2, size=10).round(4)
    signals = [random.choice(['Hold', 'Buy', 'Sell']) for _ in range(10)]
    return pd.DataFrame({'Date': dates, 'Price': prices, 'Signal': signals})

# Mock AI signal generator
def generate_signal():
    signal = random.choice(["Buy", "Sell", "Hold"])
    confidence = round(random.uniform(0.6, 0.95), 2)
    hold_time = round(random.uniform(0.5, 3.0), 1)
    return signal, confidence, hold_time

# Email alert function
def send_email_alert(signal, confidence, hold_time):
    sender_email = "Remixbooster2@gmail.com"
    receiver_email = "Remixbooster2@gmail.com"
    app_password = "YOUR_16_DIGIT_APP_PASSWORD"

    subject = f"Fartcoin AI Signal: {signal}"
    body = f"""
    Signal: {signal}
    Confidence: {confidence * 100:.1f}%
    Estimated hold time: {hold_time:.1f} days
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

# Streamlit UI
st.title("Fartcoin AI Trading Signal (Fast Trades Only)")

# Show chart with historical signals
df = get_price_data()
st.subheader("Fartcoin Price Chart with Buy/Sell Signals")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df['Date'], df['Price'], label='Price', color='gray', linewidth=2)
buy_signals = df[df['Signal'] == 'Buy']
sell_signals = df[df['Signal'] == 'Sell']
ax.scatter(buy_signals['Date'], buy_signals['Price'], color='green', marker='^', s=100, label='Buy')
ax.scatter(sell_signals['Date'], sell_signals['Price'], color='red', marker='v', s=100, label='Sell')
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.set_title("Fartcoin Price & Signals")
ax.legend()
ax.grid(True)
fig.autofmt_xdate()
st.pyplot(fig)

# Run signal prediction
signal, confidence, hold_time = generate_signal()
if hold_time <= 1 and signal in ["Buy", "Sell"]:
    st.success(f"AI Signal: {signal}")
    st.write(f"Confidence: {confidence * 100:.1f}%")
    st.write(f"Estimated hold time: {hold_time:.1f} days")
    send_email_alert(signal, confidence, hold_time)
else:
    st.warning("No good trade opportunity within 1 day.")
