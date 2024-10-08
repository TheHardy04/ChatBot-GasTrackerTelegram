import requests
import telepot
from apscheduler.schedulers.background import BackgroundScheduler
import time

# Fetch gas price data from the Etherscan API
def get_gas_data():
    api_key = "JR9PWKZBEUESZW11T6GZXW8YC44638RUFW"
    url = "https://api.etherscan.io/api"
    params = {
        "module": "gastracker",
        "action": "gasoracle",
        "apikey": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes

        data = response.json()

        if data["status"] == "1":
            # Get FastGasPrice and GasUsedRatio
            fast_gas_price = data["result"]["FastGasPrice"]
            gas_used_ratio = data["result"]["gasUsedRatio"]

            # Extract the first value and round to 2 decimal places
            first_gas_used_ratio = float(gas_used_ratio.split(',')[0])
            first_gas_used_ratio_rounded = round(first_gas_used_ratio, 2)

            return fast_gas_price, first_gas_used_ratio_rounded
        else:
            print(f"API Error: {data['message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


# Create the message to be sent
def get_message(gas_data):
    if gas_data:
        fast_gas_price, first_gas_used_ratio = gas_data
        message = (f"Fast Gas Price: {fast_gas_price} Gwei\n"
                   f"First Gas Used Ratio: {first_gas_used_ratio}%")
        return message
    else:
        return "Unable to retrieve gas data."


# Send the message via Telegram
def send_message():
    chat_id = "7577785128"
    gas_data = get_gas_data()

    # Create and send the message
    message = get_message(gas_data)
    bot.sendMessage(chat_id, message)

    # Confirm message delivery
    print(f"Message sent: {message}")


# Set up the scheduler to run the function at a regular interval
def run_scheduler(func, time_interval_seconds=120):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func, 'interval', seconds=time_interval_seconds)
    scheduler.start()

    # Keep the script alive
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    # Telegram bot token
    telegram_token = "7678891919:AAEqJhce4dV3JWMPzUwOYcS6z64aXqNcKRc"

    # Initialize the Telegram bot
    bot = telepot.Bot(telegram_token)

    # Set the time interval for the scheduler (in seconds)
    time_interval = 5  # 2 minutes
    run_scheduler(send_message, time_interval)
