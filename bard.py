import yfinance as yf
import os
import get_data
import plotting


def finance_bard():
    """
    This function uses technical analysis to predict the future price of a stock.

    Returns:
        float: The predicted price of the stock.
    """
    # Prompt the user for a stock symbol to analyze.
    stock_symbol = input("Enter a stock symbol to analyze: ")

    # Get the historical data for the stock.
    stock_data = get_data.get_stock_data(stock_symbol)

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
    macd = stock_data["Close"].ewm(span=12, min_periods=9).mean(
    ) - stock_data["Close"].ewm(span=26, min_periods=12).mean()

    # Plot the historical data and the technical indicators.
    plotting.plot_stock_data(stock_symbol, stock_data,
                             moving_averages, bollinger_bands, rsi, macd)

    # Identify the current trend.
    trend = "Up" if moving_averages[-1] > moving_averages[-2] else "Down"
    # Identify the current volatility.
    volatility = "High" if bollinger_bands[-1] > bollinger_bands[-2] else "Low"
    # Identify the current momentum.
    momentum = "Positive" if rsi[-1] > 50 else "Negative"
    # Return predicted price
    if trend == "Down" and volatility == "High":
        # Identify the current support and resistance levels.
        support = stock_data["Close"].min()
        resistance = stock_data["Close"].max()

        return moving_averages[-1] - 0.2 * (resistance - moving_averages[-1])
