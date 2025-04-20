import streamlit as st
import pandas as pd
import requests
import ta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

# 1. Get Fartcoin data
@st.cache_data
def get_fartcoin_data():
    url = "https://api.coingecko.com/api/v3/coins/fartcoin/market_chart?vs_currency=usd&days=90&interval=daily"
    r = requests.get(url)
    data = r.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['close'] = df['price']
    df.drop('price', axis=1, inplace=True)
    return df

# 2. Add indicators
def add_indicators(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
    df['ema'] = ta.trend.EMAIndicator(df['close'], window=10).ema_indicator()
    df['sma'] = ta.trend.SMAIndicator(df['close'], window=10).sma_indicator()
    df['macd'] = ta.trend.MACD(df['close']).macd_diff()
    df.dropna(inplace=True)
    return df

# 3. Create labels
def label_data(df, threshold=0.02):
    df['future_price'] = df['close'].shift(-3)
    df['pct_change'] = (df['future_price'] - df['close']) / df['close']
    df['signal'] = 0
    df.loc[df['pct_change'] > threshold, 'signal'] = 1
    df.loc[df['pct_change'] < -threshold, 'signal'] = -1
    df.dropna(inplace=True)
    return df

# 4. Estimate hold duration
def estimate_hold_duration(df):
    hold_days = []
    for i in range(len(df)):
        if df['signal'].iloc[i] == 1:
            for j in range(i+1, min(i+10, len(df))):
                pct = (df['close'].iloc[j] - df['close'].iloc[i]) / df['close'].iloc[i]
                if pct > 0.02:
                    hold_days.append(j - i)
                    break
    return np.mean(hold_days) if hold_days else None

# 5. Streamlit UI
st.title("Fartcoin AI Trading Signal")
st.markdown("Get Buy/Sell/Hold predictions + holding time estimate")

df = get_fartcoin_data()
df = add_indicators(df)
df = label_data(df)

features = ['rsi', 'ema', 'sma', 'macd']
X = df[features]
y = df['signal']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

latest = X.tail(1)
prediction = model.predict(latest)[0]
proba = model.predict_proba(latest)[0]

signal = "Buy" if prediction == 1 else "Sell" if prediction == -1 else "Hold"
confidence = round(np.max(proba) * 100, 2)

st.subheader(f"AI Signal: **{signal}**")
st.write(f"Confidence: **{confidence}%**")

avg_hold = estimate_hold_duration(df)
if avg_hold:
    st.write(f"Estimated average hold time: **{avg_hold:.1f} days**")
else:
    st.write("Not enough data to estimate hold duration.")

st.line_chart(df['close'])
