from collections import deque

# Keep state between calls
prices = deque(maxlen=50)

def trade(market_data):
    prices.append(market_data['close'])
    if len(prices) < 50:
        return {'buy': False, 'sell': False}

    sma_20 = sum(list(prices)[-20:]) / 20
    sma_50 = sum(prices) / 50

    # Buy signal: 20-SMA crosses above 50-SMA
    if sma_20 > sma_50:
        return {'buy': True, 'sell': False}
    # Sell signal: 20-SMA crosses below 50-SMA
    elif sma_20 < sma_50:
        return {'buy': False, 'sell': True}
    else:
        return {'buy': False, 'sell': False}
