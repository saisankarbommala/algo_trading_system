import configparser
import asyncio
from data_handler import fetch_stock_data, calculate_indicators
from strategy import generate_signals, backtest_strategy
from google_sheets_api import log_trade
from ml_model import train_and_predict_movement # This is for the bonus task
from telegram_alerts import send_telegram_message

async def main_async():
    """
    Main asynchronous function to run the algo-trading prototype.
    It orchestrates the entire process from data fetching to logging.
    """
    # 1. Load Configuration
    # This reads settings from the 'config.ini' file (e.g., stocks, periods)
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # 2. Get the list of stocks to track from the config file
    # It splits the string into a list and removes any extra spaces
    stocks = [s.strip() for s in config['STOCKS']['STOCKS_TO_TRACK'].split(',')]
    
    # 3. Loop through each stock and run the complete process
    for symbol in stocks:
        print(f"--- Processing {symbol} ---")
        print(f"Processing data for {symbol}...")
        
        # a. Fetch the raw stock data from the API
        df = fetch_stock_data(symbol, config)
        if df.empty:
            print(f"Skipping {symbol} due to empty data.")
            continue
        
        # b. Calculate technical indicators (RSI, DMAs) and add them to the DataFrame
        df = calculate_indicators(df)
        
        # c. Clean the data by removing any rows with NaN values. 
        # This is important because the indicators have NaN values at the start.
        df = df.dropna()
        
        # d. Add a 'Symbol' column to the DataFrame, which is needed for logging
        df['Symbol'] = symbol
        
        # e. Generate buy and sell signals based on the strategy logic
        df = generate_signals(df)
        
        # f. Run the backtest to simulate trades and get performance metrics
        trade_log, summary = backtest_strategy(df)
        
        # g. Log the trade results to Google Sheets if any trades were found
        if trade_log:
            log_trade(trade_log, summary)
            
            # h. Send a Telegram message for each individual trade signal (bonus task)
            for trade in trade_log:
                message = (
                    f"**ALGO SIGNAL**\n"
                    f"Symbol: {trade['Symbol']}\n"
                    f"Trade Type: {trade['Type']}\n"
                    f"P&L: {trade['P&L_Absolute']:.2f} ({trade['P&L_Percentage']:.2f}%)"
                )
                await send_telegram_message(message)

        # i. (Optional) Uncomment to run the ML model for the bonus task
        # ml_accuracy = train_and_predict_movement(df)

    # 4. Send a final Telegram message to signal the end of the script
    await send_telegram_message("\n--- Project Execution Complete ---")

def main():
    """
    Standard entry point to run the asynchronous main function.
    """
    asyncio.run(main_async())

if __name__ == "__main__":
    main()