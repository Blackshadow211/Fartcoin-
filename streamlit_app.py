
import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(signal, confidence, hold_time):
    sender_email = "Remixbooster2@gmail.com"  # <-- Replace with your Gmail
    receiver_email = "Remixbooster2@gmail.com"  # <-- Replace with your Gmail
    app_password = "xjIr szqz jtmv prfo"  # <-- Replace with your App Password

    subject = f"Fartcoin Signal: {signal}"
    body = f"""AI Signal: {signal}
Confidence: {confidence:.2f}%
Estimated Hold Time: {hold_time:.1f} days"""

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
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))

st.set_page_config(page_title="Fartcoin AI Signal", layout="centered", page_icon="")

st.title("Fartcoin AI Trading Signal")
st.markdown("Get Buy/Sell/Hold predictions + holding time estimate")

# Simulated AI signal (replace this with actual AI logic)
signal = random.choice(["Buy", "Sell", "Hold"])
confidence = round(random.uniform(55, 95), 1)
hold_time = round(random.uniform(0.5, 3.5), 1)

st.subheader(f"AI Signal: {signal}")
st.markdown(f"**Confidence:** {confidence}%")
st.markdown(f"**Estimated average hold time:** {hold_time} days")

# Call email alert function
send_email_alert(signal, confidence, hold_time)
