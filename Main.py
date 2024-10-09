import requests
import telepot
from telepot.loop import MessageLoop
from apscheduler.schedulers.background import BackgroundScheduler
import time

import os

config_file_path = 'config.py'

if not os.path.exists(config_file_path):
    with open(config_file_path, 'w') as config_file:
        config_file.write('''# Constants for API and Telegram bot
API_KEY = "Your Etherscan API Key"
TELEGRAM_TOKEN = "Your Telegram Bot Token"
CHAT_ID = "Your Chat Id"  # to find ChatID https://api.telegram.org/bot<YourBOTToken>/getUpdates
TIME_INTERVAL = 120  # Time interval for sending updates (in seconds)
''')
    print(f"{config_file_path} created. Please update it with your API_KEY, TELEGRAM_TOKEN, and CHAT_ID.")
    exit(0)

from config import API_KEY, TELEGRAM_TOKEN, CHAT_ID, TIME_INTERVAL

# Variable to store the initial FastGasPrice for calculating the change
initial_fast_gas_price = None


def get_gas_data():
    """
    Fetch gas price data from the Etherscan API.

    Returns:
        tuple: (fast_gas_price, first_gas_used_ratio_rounded) if successful.
        None: if the request fails or data is invalid.
    """
    url = "https://api.etherscan.io/api"
    params = {
        "module": "gastracker",
        "action": "gasoracle",
        "apikey": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "1":
            fast_gas_price = float(data["result"]["FastGasPrice"])
            fast_gas_price = round(fast_gas_price, 2)
            gas_used_ratio = data["result"]["gasUsedRatio"]

            # Extract and round the first GasUsedRatio value to 2 decimal places
            first_gas_used_ratio = float(gas_used_ratio.split(',')[0])
            first_gas_used_ratio_rounded = round(first_gas_used_ratio, 2)

            return fast_gas_price, first_gas_used_ratio_rounded
        else:
            print(f"API Error: {data['message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def create_message(gas_data):
    """
    Create a cheerful message with gas price data, including the change in FastGasPrice.

    Args:
        gas_data (tuple): The gas price data (FastGasPrice, FirstGasUsedRatio).

    Returns:
        str: A cheerful, emoji-filled message ready to send, or a failure message if data is invalid.
    """
    global initial_fast_gas_price

    if gas_data:
        fast_gas_price, first_gas_used_ratio = gas_data

        if initial_fast_gas_price is None:
            initial_fast_gas_price = fast_gas_price

        # Calculate the price change
        price_change = round(fast_gas_price - initial_fast_gas_price, 2)

        # Prepare a cheerful message with emojis
        message = (f"🚀 *Fast Gas Price Update* 🚀\n\n"
                   f"💨 Fast Gas Price: *{fast_gas_price} Gwei*\n"
                   f"📊 First Gas Used Ratio: *{first_gas_used_ratio}%*\n"
                   f"🔄 Change: *{price_change} Gwei*\n\n"
                   f"Keep an eye on the gas prices! 💡🔥")

        return message
    return "⚠️ Oops! Unable to retrieve gas data. Please try again later!"

def send_telegram_message():
    """
    Fetch gas data, format it, and send it as a Telegram message.
    """
    gas_data = get_gas_data()
    message = create_message(gas_data)

    try:
        bot.sendMessage(CHAT_ID, message, parse_mode='Markdown')  # Mardown for bold text
        print(f"Message sent: {message}")
    except telepot.exception.TelegramError as e:
        print(f"Error sending message: {e}")

# Handle incoming commands
def handle_command(msg):
    global initial_fast_gas_price

    chat_id = msg['chat']['id']
    command = msg['text']

    if command == '/restart':
        gas_data = get_gas_data()
        if gas_data:
            initial_fast_gas_price = gas_data[0]
            bot.sendMessage(chat_id, "Bot has been restarted. Change values have been reset to 0.")
            message = create_message(gas_data)
            bot.sendMessage(chat_id, message,parse_mode = 'Markdown')
            print("Change values reset by /restart command.")
        else:
            bot.sendMessage(chat_id, "⚠️ Failed to reset change values. Unable to retrieve gas data.")
            print("Failed to reset change values. Unable to retrieve gas data.")
    else:
        bot.sendMessage(chat_id, "Unknown command. Please use /restart to reset.")


if __name__ == '__main__':
    # Initialize the Telegram bot
    bot = telepot.Bot(TELEGRAM_TOKEN)

    # Start the message scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_telegram_message, 'interval', seconds=TIME_INTERVAL)
    scheduler.start()
    # Start the message loop
    MessageLoop(bot, handle_command).run_as_thread()

    print("Bot is running")
    send_telegram_message()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
