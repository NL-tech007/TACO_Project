import yfinance as yf

spy = yf.Ticker("SPY")
print(spy.history(period="5d"))