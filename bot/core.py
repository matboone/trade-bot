# bot/core.py
import os
from datetime import datetime, timedelta
import pandas as pd
from webull import webull

# --- Webull login via environment variables ---
wb = webull()
wb.login(
    os.getenv("WEBULL_USER"),
    os.getenv("WEBULL_PASS")
)

# Fetch historical data with synthetic timestamps if needed
def fetch_historical_data(symbol, interval='m5', start_date=None, end_date=None):
    # Calculate the number of bars needed based on the interval and date range
    if start_date and end_date:
        time_diff = end_date - start_date
        minutes_per_interval = {
            'm1': 1,
            'm5': 5,
            'm15': 15,
            'm30': 30,
            'h1': 60,
            'd1': 1440
        }
        interval_minutes = minutes_per_interval.get(interval, 5)
        count = min(500, time_diff.total_seconds() // (interval_minutes * 60))
    else:
        count = 500  # Default to 500 if no date range is provided

    # Fetch data from Webull
    data = wb.get_bars(stock=symbol, interval=interval, count=int(count))  # Adjust count
    df = pd.DataFrame(data)

    # Debug raw data
    print("Raw data response shape:", df.shape)
    print("Raw data:", df.head(10))

    # Check if 'timestamp' exists
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df.set_index('timestamp', inplace=True)
    elif 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
    else:
        print("No timestamp found. Generating synthetic timestamps.")
        if start_date and end_date:
            df['datetime'] = pd.date_range(start=start_date, end=end_date, periods=len(df))
        else:
            df['datetime'] = pd.date_range(start=pd.Timestamp.now(), periods=len(df), freq=interval)
        df.set_index('datetime', inplace=True)

    # Filter data by date range
    if start_date and end_date:
        df = df[(df.index >= start_date) & (df.index <= end_date)]

    # Debug filtered data
    if df.empty:
        print("Insufficient data retrieved. Check API parameters or date range.")
        return None
    print(f"Filtered data range: {df.index.min()} to {df.index.max()}")
    print("Filtered DataFrame:", df.head())

    return df

# Apply trading strategies
def apply_strategies(df):
    # MACD Calculation
    df['EMA12'] = df['close'].ewm(span=12).mean()
    df['EMA26'] = df['close'].ewm(span=26).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal_Line'] = df['MACD'].ewm(span=9).mean()

    # MACD Signals
    df['MACD_Signal'] = 0
    df.loc[df['MACD'] > df['Signal_Line'], 'MACD_Signal'] = 1  # Buy
    df.loc[df['MACD'] < df['Signal_Line'], 'MACD_Signal'] = -1  # Sell

    # Debug: Print MACD values
    print("MACD Head:\n", df[['MACD', 'Signal_Line', 'MACD_Signal']].head())

    # Bollinger Bands Calculation
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['Upper_Band'] = df['MA20'] + (df['close'].rolling(window=20).std() * 2)
    df['Lower_Band'] = df['MA20'] - (df['close'].rolling(window=20).std())

    # Bollinger Band Signals
    df['BB_Signal'] = 0
    df.loc[df['close'] < df['Lower_Band'], 'BB_Signal'] = 1  # Buy
    df.loc[df['close'] > df['Upper_Band'], 'BB_Signal'] = -1  # Sell

    # Debug: Print Bollinger Bands values
    print("Bollinger Bands Head:\n", df[['MA20', 'Upper_Band', 'Lower_Band', 'BB_Signal']].head())

    # Combine Signals (Prioritize MACD for simplicity)
    df['Signal'] = df['MACD_Signal']
    return df

# Backtest logic
def backtest(symbol, interval='m5', start_date=None, end_date=None, initial_balance=100):
    df = fetch_historical_data(symbol, interval, start_date, end_date)
    df = apply_strategies(df)

    cash = initial_balance
    position = 0  # Number of shares held
    trade_log = []

    for i, row in df.iterrows():
        signal = row['Signal']
        price = row['close']

        # Debug: Print current iteration details
        print(f"Iteration {i}: Signal={signal}, Price={price}, Cash={cash}, Position={position}")

        if signal == 1 and cash >= price:  # Buy signal
            shares_to_buy = int(cash // price)
            cash -= shares_to_buy * price
            position += shares_to_buy
            trade_log.append(f"BUY {shares_to_buy} shares at ${price:.2f}")

        elif signal == -1 and position > 0:  # Sell signal
            cash += position * price
            trade_log.append(f"SELL {position} shares at ${price:.2f}")
            position = 0

    # Final portfolio value
    final_balance = cash + (position * df.iloc[-1]['close'])
    trade_log.append(f"Final portfolio value: ${final_balance:.2f}")
    return final_balance, trade_log

if __name__ == "__main__":
    start_date = datetime.now() - timedelta(days=7)
    end_date   = datetime.now()

    final_balance, trade_log = backtest(
        "SOFI",
        interval="m30",
        start_date=start_date,
        end_date=end_date,
        initial_balance=100
    )

    for log in trade_log:
        print(log)
    print(f"Final balance: ${final_balance:.2f}")
    print(wb.get_account())
    wb.logout()