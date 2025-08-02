import telegram
import configparser

def get_telegram_config():
    """Reads Telegram configuration from config.ini."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['API_KEYS']['TELEGRAM_BOT_TOKEN']
    chat_id = config['API_KEYS']['TELEGRAM_CHAT_ID']
    return token, chat_id

async def send_telegram_message(message):
    """
    Sends a message to the specified Telegram chat.
    
    Args:
        message (str): The message to send.
    """
    token, chat_id = get_telegram_config()
    
    if not token or not chat_id:
        print("Telegram bot token or chat ID is not configured.")
        return

    try:
        bot = telegram.Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message)
        print("Telegram message sent successfully.")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(send_telegram_message("Hello from my algo-trading bot!"))