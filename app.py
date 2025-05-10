import streamlit as st
import yfinance as yf
import backtrader as bt

import pandas as pd

import matplotlib.pyplot as plt
import importlib.util
import sys
import os
import tempfile

# --- Standardized interface for user algorithm ---
class TradingStrategyInterface(bt.Strategy):
    params = dict(
        user_algo=None,  # user algorithm module
    )

    def __init__(self):
        self.user_algo = self.p.user_algo

    def next(self):
        # Prepare market data for user algo
        current_data = {
            'datetime': self.datas[0].datetime.datetime(0),
            'open': float(self.datas[0].open[0]),
            'high': float(self.datas[0].high[0]),
            'low': float(self.datas[0].low[0]),
            'close': float(self.datas[0].close[0]),
            'volume': float(self.datas[0].volume[0])
        }
        try:
            actions = self.user_algo.trade(current_data)
        except Exception as e:
            st.error(f"Error in user algorithm execution: {e}")
            actions = {}

        # Execute actions
        if actions.get('buy', False):
            if not self.position:
                self.buy()
        if actions.get('sell', False):
            if self.position:
                self.sell()

# --- Load user algorithm from uploaded file ---
def load_user_algorithm(uploaded_file_path):
    spec = importlib.util.spec_from_file_location("user_algo", uploaded_file_path)
    user_algo = importlib.util.module_from_spec(spec)
    sys.modules["user_algo"] = user_algo
    spec.loader.exec_module(user_algo)
    return user_algo

# --- Streamlit App ---
def main():
    st.title("Algorithmic Trading Web App")

    st.markdown("""
    1. Enter a stock ticker and date range.
    2. Upload your trading algorithm Python file.
    3. Click 'Run Backtest' to see results.
    ---
    **Your algorithm file must define a function:**

    ```
    def trade(market_data):
        # market_data is a dict with keys: datetime, open, high, low, close, volume
        # return: {'buy': True/False, 'sell': True/False}
        ...
    ```
    """)

    ticker = st.text_input("Stock ticker (e.g., AAPL):", value="AAPL")
    start_date = st.date_input("Start date")
    end_date = st.date_input("End date")
    uploaded_file = st.file_uploader("Upload your trading algorithm (.py file)", type=["py"])

    if st.button("Run Backtest"):
        if not ticker:
            st.error("Please enter a stock ticker.")
            return
        if not start_date or not end_date:
            st.error("Please select start and end dates.")
            return
        if not uploaded_file:
            st.error("Please upload your trading algorithm Python file.")
            return

        # After downloading data
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            st.error("No data found for the given ticker and date range.")
            return

        # If columns are MultiIndex, flatten by using the second level (price type)
        if isinstance(data.columns, pd.MultiIndex):
            # Use the first level (e.g., 'Open', 'Close', etc.)
            data.columns = data.columns.get_level_values(0)


        # Make all columns lowercase for consistency
        data.columns = [str(c).lower() for c in data.columns]




        # Save uploaded file to a temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        # Load user algorithm
        try:
            user_algo = load_user_algorithm(tmp_file_path)
        except Exception as e:
            st.error(f"Failed to load user algorithm: {e}")
            os.remove(tmp_file_path)
            return

        # Backtrader setup
        cerebro = bt.Cerebro()
        data_feed = bt.feeds.PandasData(dataname=data)
        cerebro.adddata(data_feed)
        cerebro.addstrategy(TradingStrategyInterface, user_algo=user_algo)
        cerebro.broker.setcash(10000.0)

        # Run backtest
        try:
            cerebro.run()
        except Exception as e:
            st.error(f"Error running backtest: {e}")
            os.remove(tmp_file_path)
            return

        final_value = cerebro.broker.getvalue()
        st.success(f"Final Portfolio Value: ${final_value:,.2f}")

                # Plot closing price (robust to column variations)
        fig, ax = plt.subplots()

        # Show columns for debugging
        st.write("Data columns:", data.columns.tolist())
        st.write("First few rows of data:", data.head())

        # Try common variations of the close column
        close_col = None
        for candidate in ['close', 'Close', 'CLOSE', 'adj close', 'Adj Close', 'adjclose', 'AdjClose']:
            if candidate in data.columns:
                close_col = candidate
                break

        if close_col:
            data[close_col].plot(ax=ax)
            ax.set_title(f"Closing Price of {ticker}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            st.pyplot(fig)
        else:
            st.error(f"No 'close' or 'adj close' column found. Columns are: {data.columns.tolist()}")

        os.remove(tmp_file_path)


if __name__ == "__main__":
    main()
