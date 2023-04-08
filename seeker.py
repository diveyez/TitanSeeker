import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as datetime
import plotly.graph_objects as go
import os
import get_data as get_data
import plotting as plotting

# Prompt the user for a stock symbol to analyze.
stock_symbol = input("Enter a stock symbol to analyze: ")
# Get the historical data for the stock.
"""stock_data = get_data.get_stock_data(stock_symbol)"""


def finance_bard(stock_symbol):
    """
    This function uses technical analysis to predict the future price of a stock.

    Args:
        stock_symbol (str): The symbol of the stock to analyze.

    Returns:
        float: The predicted price of the stock.
    """

    # Check if stock_data is empty
    if stock_data is None:
        print("No data found for the given stock symbol.")
    else:
        # Plot the technical indicators for the stock.
        plotting.plot_technical_indicators(stock_symbol, stock_data)
        # Load the historical data for the stock.
        stock_data = yf.download(stock_symbol, period="max")

    # Check if stock_data is empty
    if stock_data.empty:
        print("No data found for the given stock symbol.")
        return None

    # Write the historical data to a CSV file.
    stock_data.to_csv(f"{stock_symbol}.csv")

    # Calculate the moving averages for the stock.
    moving_averages = stock_data["Close"].rolling(window=20).mean()

    # Calculate the Bollinger Bands for the stock.
    bollinger_bands = stock_data["Close"].rolling(window=20).std(ddof=1)

    # Calculate the RSI for the stock.
    rsi = stock_data["Close"].rolling(window=14).mean()

    # Calculate the MACD for the stock.
    macd = stock_data["Close"].ewm(span=12, min_periods=9).mean() - stock_data["Close"].ewm(span=26, min_periods=12).mean()

    # Plot the historical data and the technical indicators.
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock_data.index,
                  y=stock_data["Close"], name="Close"))
    fig.add_trace(go.Scatter(x=stock_data.index,
                  y=moving_averages, name="Moving Averages"))
    fig.add_trace(go.Scatter(x=stock_data.index,
                  y=bollinger_bands, name="Bollinger Bands"))
    fig.add_trace(go.Scatter(x=stock_data.index, y=rsi, name="RSI"))
    fig.add_trace(go.Scatter(x=stock_data.index, y=macd, name="MACD"))
    fig.update_layout(
        title=f"{stock_symbol} Historical Data and Technical Indicators")

    # Save the plot as an image file.
    if not os.path.exists("plots"):
        os.mkdir("plots")
    fig.write_image(f"plots/{stock_symbol}_plot.png")

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

    # Return predicted price
    if trend == "Down" and volatility == "High":
        predicted_price = moving_averages[-1] - \
        0.2 * (resistance - moving_averages[-1])
        return predicted_price
