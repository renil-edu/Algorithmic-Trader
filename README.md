# Algorithmic Trading Web App

A free, modular Python web application for algorithmic trading research, backtesting, and visualization.  
Users can upload their own Python trading algorithms, select any stock and date range, and instantly see backtest results and price charts-all in a modern web interface.

---

Purpose

This project empowers traders and researchers to:
- Test custom trading algorithms on historical stock data, without writing boilerplate code.
- Visualize price data and backtest results interactively in the browser.
- Prototype and debug strategies quickly, using a standardized Python interface.

No paid APIs, no credit card required, and no hidden costs-just open-source tools and free data.

---

Code Structure

```
algorithmic-trading/
│
├── app.py                # Main Streamlit app (UI, workflow)
├── data_utils.py         # Data fetching and preprocessing (yfinance, cleaning)
├── algo_loader.py        # Dynamic loading of user trading algorithms
├── backtest_engine.py    # Backtesting logic (Backtrader, strategy interface)
├── plot_utils.py         # All plotting functions (candlestick, equity, etc.)
├── requirements.txt      # All dependencies
└── README.md             # This file
```

---

Installation

1. Clone the repository:
   git clone https://github.com/yourusername/algorithmic-trading.git
   cd algorithmic-trading

2. Set up a Python environment (recommended):
   conda create -n algo-trading python=3.10
   conda activate algo-trading

3. Install dependencies:
   pip install -r requirements.txt
   (If you don't have a requirements.txt, use:
   pip install streamlit yfinance backtrader matplotlib mplfinance pandas)

---

Running the App

streamlit run app.py

- Visit http://localhost:8501 in your browser.

---

Usage

1. Enter a stock ticker (e.g., AAPL) and select a date range.
2. Upload your trading algorithm as a .py file.
   Your script must define a function:
   def trade(market_data):
       # market_data: dict with keys 'datetime', 'open', 'high', 'low', 'close', 'volume'
       # return: {'buy': True/False, 'sell': True/False}
3. Click "Run Backtest" to see:
   - Final portfolio value
   - Price chart
   - (If enabled) Candlestick chart, equity curve, and more

---

Features

- Custom Algorithm Upload: Users can upload any Python strategy script using a simple interface.
- Backtesting: Uses Backtrader for realistic, event-driven simulation.
- Free Data: Pulls historical stock data from Yahoo Finance via yfinance.
- Interactive Visualization: Price and (optionally) candlestick charts, equity curves, and more via Matplotlib and mplfinance.
- Modular Design: All core logic is split into reusable modules for easy extension.

---

Example Algorithm

```
def trade(market_data):
    # Simple moving average crossover
    # (implement your own logic here)
    if market_data['close'] > market_data['open']:
        return {'buy': True, 'sell': False}
    elif market_data['close'] < market_data['open']:
        return {'buy': False, 'sell': True}
    else:
        return {'buy': False, 'sell': False}
```
---

Extending the App

- Add new chart types (candlestick, equity curve, drawdown, etc.) in plot_utils.py.
- Add new data sources or live trading support in new modules.
- Integrate additional analytics, risk metrics, or reporting as needed.

---

License

This project is open-source and free to use under the MIT License.

---

Contributing

Pull requests, bug reports, and feature suggestions are welcome!
Please open an issue or submit a PR on GitHub.

---

References

- Backtrader Documentation: https://www.backtrader.com/docu/
- yfinance Documentation: https://github.com/ranaroussi/yfinance
- Streamlit Documentation: https://docs.streamlit.io/
- mplfinance Documentation: https://github.com/matplotlib/mplfinance

---

Happy trading and experimenting!
