SmartAPI - Python Library for Angel Broking API Integration
Overview
This Python library (SmartAPI) is designed to interact with the Angel Broking API for fetching financial data such as instrument details, live market data, historical data, and more. The library makes use of several popular Python libraries, including pandas, requests, and pyotp, to handle data fetching, processing, and API authentication.

The provided script includes functions for logging in, fetching market data, handling sessions, and calculating live market prices and historical data for specific instruments.

Features
Login: Allows users to login with their credentials and store them for API interactions.
Instrument Data: Fetches instrument details such as tokens, expiry dates, and more.
Live Market Data: Retrieves the last traded price (LTP) for instruments.
Historical Data: Fetches OHLC (Open, High, Low, Close) data for instruments.
Session Handling: Initializes and manages separate sessions for historical and trading APIs.
Time Zone Management: Provides functionality to fetch the current time in IST (Indian Standard Time).
Installation
This library requires several Python packages. You can install the required dependencies using pip.

Step 1: Install Required Libraries
To ensure that all necessary libraries are installed, the following Python script checks for and installs the missing libraries:

$pip install pandas requests pytz pyotp

$pip install SmartApi

Usage
Here’s how you can use the SmartAPI class in your script:

1. Initialize the SmartAPI class
api = SmartAPI()

2. Login with Your Credentials   
You need to provide your credentials for logging into the API:
api.login(api_key_hist='YOUR_HISTORICAL_API_KEY', 
          api_key_trading='YOUR_TRADING_API_KEY', 
          uid='YOUR_USER_ID', 
          mpin='YOUR_MPIN', 
          totp='YOUR_TOTP_SECRET')


3. Fetch Instrument Data
To fetch the instrument details (e.g., symbol, token, exchange segment):
instrument_df = api.fetch_instrument_df()
print(instrument_df.head())



4. Fetch the Last Traded Price (LTP)
To get the LTP for a specific instrument (e.g., 'WIPRO'):
ltp = api.get_ltp('WIPRO')
print(f"Last Traded Price: {ltp}")


5. Fetch Trading Symbols
To fetch the trading symbols based on the current spot price:
symbols_df = api.get_tradingsymbols()
print(symbols_df.head())


6. Fetch Historical Data (OHLC)
To fetch OHLC data for a specific symbol:
ohlc_data = api.get_ohlc('BANKNIFTY', '5minute', 30)  # 30 days of data
print(ohlc_data.head())


8. Get Current Time in IST
To get the current time in IST:
current_time = api.get_ist_now()
print(f"Current IST Time: {current_time}")
Methods:
login(api_key_hist, api_key_trading, uid, mpin, totp)
Logs in with the provided credentials (API keys, user ID, MPIN, and TOTP secret).

fetch_instrument_df()
Fetches the instrument details (tokens, expiry dates, etc.) and returns it as a pandas DataFrame.

get_historical_data_session()
Generates a session for accessing historical market data.

get_trading_api_session()
Generates a session for trading-related API interactions.

initialize_sessions()
Initializes both historical and trading API sessions.

get_ltp(symbol)
Fetches the Last Traded Price (LTP) for a given symbol.

get_tradingsymbols()
Fetches the trading symbols based on the spot price of Nifty or BankNifty.

get_ohlc(symbol, interval, n)
Fetches the OHLC data for the given symbol over the specified interval and number of days.

get_ist_now()
Fetches the current time in IST (Indian Standard Time).

Example
Here’s an example of how to use the entire class:

# Initialize the API
api = SmartAPI()

# Login
api.login(api_key_hist='your_api_key_hist', 
          api_key_trading='your_api_key_trading', 
          uid='your_user_id', 
          mpin='your_mpin', 
          totp='your_totp_secret')

# Fetch instrument data
instrument_df = api.fetch_instrument_df()
print(instrument_df.head())

# Fetch LTP
ltp = api.get_ltp('Nifty Bank')
print(f"LTP: {ltp}")

# Fetch OHLC data
ohlc_data = api.get_ohlc('BANKNIFTY', '5minute', 30)
print(ohlc_data.head())





