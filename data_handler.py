import yfinance as yf
import pandas as pd
import ta

def fetch_stock_data(symbol, config):
    """
    Fetches historical stock data and cleans the column names.
    
    This function now uses a robust method to handle multi-level columns
    to ensure the rest of the code works correctly.
    """
    try:
        period = config['BACKTESTING']['PERIOD']
        data = yf.download(symbol, period=period, interval="1d")
        
        # --- FINAL FIX: FLATTEN COLUMNS ---
        # Get the top-level column names (e.g., 'Open', 'High', 'Low', etc.)
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
        
        if data.empty:
            print(f"Warning: No data found for {symbol}.")
            return pd.DataFrame()
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

def calculate_indicators(df):
    """
    Calculates RSI and Moving Averages using the 'ta' library.
    
    This function now works correctly with the simplified column names.
    """
    if 'Close' not in df.columns:
        return df
    
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    df['20_DMA'] = ta.trend.sma_indicator(df['Close'], window=20)
    df['50_DMA'] = ta.trend.sma_indicator(df['Close'], window=50)

    return df