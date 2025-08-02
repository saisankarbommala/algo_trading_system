import gspread
from oauth2client.service_account import ServiceAccountCredentials
import configparser

def setup_google_sheets_client():
    """Sets up the gspread client for Google Sheets access using a service account."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        config['API_KEYS']['GOOGLE_SERVICE_ACCOUNT_KEY_PATH'], scope)
    client = gspread.authorize(creds)
    return client

def log_trade(trade_log, summary):
    """
    Logs the backtest results to a Google Sheet.
    
    This version includes a fix for the "Object of type date is not JSON serializable" error.
    """
    try:
        client = setup_google_sheets_client()
        config = configparser.ConfigParser()
        config.read('config.ini')
        sheet_name = config['GOOGLE_SHEETS']['SHEET_NAME']
        
        spreadsheet = client.open(sheet_name)
        
        # --- NEW CODE: Convert the 'Date' to a string before logging ---
        # Create a new list with the dates converted to strings
        logged_trades = []
        for trade in trade_log:
            trade['Date'] = str(trade['Date'])
            logged_trades.append(list(trade.values()))
            
        # Log to 'Trade Log' tab
        trade_worksheet = spreadsheet.worksheet('Trade Log')
        if trade_worksheet.row_count < 2:
            trade_worksheet.append_row(list(trade_log[0].keys()))
        trade_worksheet.append_rows(logged_trades)
        
        # Log to 'Summary P&L' tab
        summary_worksheet = spreadsheet.worksheet('Summary P&L')
        summary_worksheet.clear()
        summary_worksheet.append_row(list(summary.keys()))
        summary_worksheet.append_row(list(summary.values()))
        
        print("Successfully logged trade data to Google Sheets.")
    except Exception as e:
        print(f"Error logging to Google Sheets: {e}")