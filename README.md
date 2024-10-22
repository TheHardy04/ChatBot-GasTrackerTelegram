# Ethereum Gas Price Telegram Bot

This Project is a Student Project for the course "Computer Networks" at Hanyang University, Seoul, South Korea. 

It is a Telegram bot that fetches Ethereum gas price data from the Etherscan API and sends it to a user via Telegram every 2 minutes.

## Features
- Fetch Ethereum gas prices every 2 minutes using the Etherscan API.
- Send the Fast Gas Price and First Gas Used Ratio to a user.
- Ability to reset change tracking with the `/restart` command.

## Prerequisites
- Python 3.9 (The version I used) or higher
- A Telegram bot token from [BotFather](https://core.telegram.org/bots#botfather).
- An API key from [Etherscan](https://etherscan.io/apis).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TheHardy04/ChatBot-GasTrackerTelegram.git
   cd my-telegram-gas-tracker
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
3. Set up the `config.py` file:
   ```python
   # Constants for API and Telegram bot
   API_KEY = "Your Etherscan API Key"
   TELEGRAM_TOKEN = "Your Telegram Bot Token"
   CHAT_ID = "Your Chat Id"  # to find ChatID https://api.telegram.org/bot<YourBOTToken>/getUpdates
   TIME_INTERVAL = 120  # Time interval for sending updates (in seconds)
   ```
   
## Run the bot

You only have to run this command
```bash
python main.py
```

## Usage 
- The bot will send a report to your telegram every 2 minutes 
- To reset the tracking of the change, use the `/restart` command.

--- 

## Acknowledgments
- [Hanyang University](http://www.hanyang.ac.kr/)

