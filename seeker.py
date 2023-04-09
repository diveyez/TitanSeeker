import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

def finance_bard(stock_symbol):
    """
    This function uses technical analysis to predict the future price of a stock.

    Args:
        stock_symbol (str): The symbol of the stock to analyze.

    Returns:
        float: The predicted price of the stock.
    """

   # Download the historical data for the stock.
    stock_data = yf.download(stock_symbol, period="1y")

    # Write the data to a csv file.
    stock_data.to_csv("stock_data.csv")
    # Load the historical data for the stock.
    stock_data = pd.read_csv("stock_data.csv")

    # Calculate the moving averages for the stock.
    moving_averages = stock_data["Close"].rolling(window=20).mean()

    # Calculate the Bollinger Bands for the stock.
    bollinger_bands = stock_data["Close"].rolling(window=20).std(ddof=1)

    # Calculate the RSI for the stock.
    rsi = stock_data["Close"].rolling(window=14).mean()

    # Calculate the MACD for the stock.
    macd = stock_data["Close"].ewm(span=12, min_periods=9).mean(
    ) - stock_data["Close"].ewm(span=26, min_periods=12).mean()

    # Plot the historical data and the technical indicators.
    plt.plot(stock_data["Date"], stock_data["Close"], label="Close")
    plt.plot(stock_data["Date"], moving_averages, label="Moving Averages")
    plt.plot(stock_data["Date"], bollinger_bands, label="Bollinger Bands")
    plt.plot(stock_data["Date"], rsi, label="RSI")
    plt.plot(stock_data["Date"], macd, label="MACD")
    plt.legend()

    # Identify the current trend.
    if moving_averages[-1] > moving_averages[-2]:
        trend = "Up"
    else:
        trend = "Down"

    # Identify the current volatility.
    if bollinger_bands[-1] > bollinger_bands[-2]:
        volatility = "High"
    else:
        volatility = "Low"

    # Identify the current momentum.
    if rsi[-1] > 50:
        momentum = "Positive"
    else:
        momentum = "Negative"

    # Identify the current support and resistance levels.
    support = stock_data["Close"].min()
    resistance = stock_data["Close"].max()

    # Predict the future price of the stock.
    if trend == "Up" and volatility == "Low":
        predicted_price = moving_averages[-1] + \
            0.1 * (resistance - moving_averages[-1])
    elif trend == "Up" and volatility == "High":
        predicted_price = moving_averages[-1] + \
            0.2 * (resistance - moving_averages[-1])
    elif trend == "Down" and volatility == "Low":
        predicted_price = moving_averages[-1] - \
            0.1 * (resistance - moving_averages[-1])
    elif trend == "Down" and volatility == "High":
        predicted_price = moving_averages[-1] - \
            0.2 * (resistance - moving_averages[-1])

    return predicted_price


if __name__ == "__main__":
    # Get the stock symbol from the user.
    stock_symbol = input("Enter the stock symbol: ")

    # Predict the future price of the stock.
    predicted_price = finance_bard(stock_symbol)

    # Print the predicted price.
    print("The predicted price of the stock is $", predicted_price)
