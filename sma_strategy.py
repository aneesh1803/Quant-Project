import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fetch_stock_data(ticker_symbol, period="1y"):
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period=period)
    return df

def calculate_moving_averages(df, short_window=3, long_window=10):
    df['SMA_Short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_Long'] = df['Close'].rolling(window=long_window).mean()
    return df

def generate_trade_signals(df):
    df['Buy_Signal'] = (df['SMA_Short'] > df['SMA_Long']) & (df['SMA_Short'].shift(1) <= df['SMA_Long'].shift(1))
    df['Sell_Signal'] = (df['SMA_Short'] < df['SMA_Long']) & (df['SMA_Short'].shift(1) >= df['SMA_Long'].shift(1))
    return df

def backtest_strategy(df):
    buy_prices = df.loc[df['Buy_Signal'], 'Close']
    sell_prices = df.loc[df['Sell_Signal'], 'Close']

    if sell_prices.index[0] < buy_prices.index[0]:
        sell_prices = sell_prices.iloc[1:]

    min_len = min(len(buy_prices), len(sell_prices))
    buy_prices, sell_prices = buy_prices.iloc[:min_len], sell_prices.iloc[:min_len]

    profits = sell_prices.values - buy_prices.values
    total_profit = profits.sum()

    print(f"Total Trades Executed: {len(profits)}")
    print(f"Total Profit/Loss: ${total_profit:.2f}")
    print(f"Average Profit per Trade: ${profits.mean():.2f}")
    print(f"Winning Trades: {sum(profits > 0)} / {len(profits)}")

def plot_strategy(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Close'], label="Closing Price", color="blue")
    plt.plot(df.index, df['SMA_Short'], label="Short SMA", color="yellow")
    plt.plot(df.index, df['SMA_Long'], label="Long SMA", color="red")

    plt.scatter(df.index[df['Buy_Signal']], df['Close'][df['Buy_Signal']], marker='^', color='green', label='Buy Signal', edgecolors='black')
    plt.scatter(df.index[df['Sell_Signal']], df['Close'][df['Sell_Signal']], marker='v', color='red', label='Sell Signal', edgecolors='black')

    plt.legend()
    plt.title("Stock Price with Buy/Sell Signals")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

if __name__ == "__main__":
    ticker_symbol = "AAPL"  
    df = fetch_stock_data(ticker_symbol)
    df = calculate_moving_averages(df)
    df = generate_trade_signals(df)
    
    print("Backtest Results:")
    backtest_strategy(df)
    
    plot_strategy(df)
