# Importing libraries
import yfinance as yf

# Gather data function
def get_returns(ticker):
    data = yf.download(ticker, start="2018-01-01", end="2025-12-31")
    close = data["Close"].squeeze()
    return close.pct_change().dropna()