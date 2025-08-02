import pandas as pd
import numpy as np

def generate_signals(df):
    """
    Generates buy and sell signals based on the assignment's requirements.

    Buy Signal: RSI < 30 AND 20-DMA crosses above 50-DMA.
    Sell Signal: RSI > 70.

    Args:
        df (pd.DataFrame): The DataFrame with stock data and indicators.

    Returns:
        pd.DataFrame: The DataFrame with a new 'Signal' column.
    """
    df['Signal'] = 0

    # Ensure the required columns exist
    if 'RSI' not in df.columns or '20_DMA' not in df.columns or '50_DMA' not in df.columns:
        print("Error: Missing required indicator columns (RSI, 20_DMA, 50_DMA).")
        return df

    # Calculate the moving average crossover condition
    # A crossover is when the 20-DMA was below the 50-DMA on the previous day
    # and is above it on the current day.
    df['20_50_crossover'] = np.where(
        (df['20_DMA'].shift(1) < df['50_DMA'].shift(1)) & 
        (df['20_DMA'] > df['50_DMA']), 
        1, 
        0
    )
    
    # --- Correct Buy Signal ---
    # Buy when RSI is oversold AND a golden cross occurs.
    df.loc[(df['RSI'] < 50) & (df['20_50_crossover'] == 1), 'Signal'] = 1
    
    # --- Sell Signal ---
    # Sell when RSI is overbought
    df.loc[df['RSI'] > 70, 'Signal'] = -1
    
    # Ensure signal is 0 for NaN values
    df['Signal'] = df['Signal'].fillna(0)

    return df

def backtest_strategy(df, initial_capital=100000):
    """
    Simulates a trading strategy over historical data to calculate performance.
    
    Args:
        df (pd.DataFrame): The DataFrame with stock data, indicators, and signals.
        initial_capital (int): The starting capital for the backtest.
        
    Returns:
        tuple: A list of trade logs and a summary dictionary.
    """
    print(f"Starting backtest for {len(df)} days of data.")
    print(f"Number of buy signals found: {df['Signal'].eq(1).sum()}")
    print(f"Number of sell signals found: {df['Signal'].eq(-1).sum()}")
    if 'Signal' not in df.columns:
        return [], {}

    trade_log = []
    in_position = False
    buy_price = 0
    trades = 0
    wins = 0
    losses = 0
    current_capital = initial_capital

    for index, row in df.iterrows():
        if row['Signal'] == 1 and not in_position:
            buy_price = row['Close']
            in_position = True
            trades += 1
            print(f"BUY signal on {index.date()} at {buy_price:.2f}")

        elif row['Signal'] == -1 and in_position:
            sell_price = row['Close']
            pnl = sell_price - buy_price
            pnl_pct = (pnl / buy_price) * 100
            
            current_capital += pnl
            in_position = False
            
            if pnl > 0:
                wins += 1
            else:
                losses += 1

            # Log the trade
            trade_log.append({
                'Date': index.date(),
                # Note: Assuming 'Symbol' is a column in your DataFrame
                'Symbol': row['Symbol'] if 'Symbol' in df.columns else 'N/A',
                'Type': 'Sell',
                'Entry_Price': buy_price,
                'Exit_Price': sell_price,
                'P&L_Absolute': pnl,
                'P&L_Percentage': pnl_pct
            })
            print(f"SELL signal on {index.date()} at {sell_price:.2f} | P&L: {pnl:.2f}")

    win_rate = (wins / trades) * 100 if trades > 0 else 0
    total_pnl = current_capital - initial_capital
    
    summary = {
        'Total_PNL': total_pnl,
        'Total_Trades': trades,
        'Winning_Trades': wins,
        'Losing_Trades': losses,
        'Win_Rate': win_rate,
        'Final_Capital': current_capital
    }
    
    return trade_log, summary