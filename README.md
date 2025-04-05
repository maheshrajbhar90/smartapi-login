# SmartAPI - Python Library for Angel Broking API Integration

## 📌 Overview
`SmartAPI` is a Python library designed to interact with the Angel Broking API. It enables users to fetch financial data such as instrument details, live market data, historical OHLC data, and more. It leverages popular libraries like `pandas`, `requests`, and `pyotp` for data handling and secure API authentication.

This wrapper simplifies session management and provides utility methods for traders and analysts to interact seamlessly with Angel Broking's SmartAPI.

---

## ✨ Features

| Feature             | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| **Login**           | Easy authentication using credentials, MPIN, and TOTP                       |
| **Instrument Data** | Fetch instrument tokens, expiry dates, and other metadata                  |
| **Live Market Data**| Retrieve Last Traded Price (LTP) for any symbol                            |
| **Historical Data** | Fetch OHLC (Open, High, Low, Close) data for a given interval and period   |
| **Session Handling**| Separate sessions for historical and trading APIs                          |
| **Time Management** | Fetches current time in IST (Indian Standard Time)                         |

---

## 🛠 Installation

Install all required dependencies using pip:

```bash
pip install pandas requests pytz pyotp
pip install smartapi-login
```

---

## 🚀 Usage

### 1. Import the Library
```python
from smartapi_login import SmartAPIHelper
```

### 2. Initialize the API Class
```python
api = SmartAPIHelper()
```

### 3. Login with Your Credentials
```python
api.login(api_key_hist='YOUR_HISTORICAL_API_KEY',
          api_key_trading='YOUR_TRADING_API_KEY',
          uid='YOUR_USER_ID',
          mpin='YOUR_MPIN',
          totp='YOUR_TOTP_SECRET')
```

### 4. Fetch Instrument Data
```python
instrument_df = api.fetch_instrument_df()
print(instrument_df.head())
```

### 5. Fetch the Last Traded Price (LTP)
```python
ltp = api.get_ltp('WIPRO')
print(f"Last Traded Price: {ltp}")
```

### 6. Fetch Trading Symbols
```python
symbols_df = api.get_tradingsymbols('Nifty Bank')
print(symbols_df.head())
```

### 7. Fetch Historical OHLC Data
```python
ohlc_data = api.get_ohlc('BANKNIFTY', '5minute', 30)
print(ohlc_data.head())
```

### 8. Get Current Time in IST
```python
current_time = api.get_ist_now()
print(f"Current IST Time: {current_time}")
```

---

## 📘 Method Descriptions

| Method                       | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| `login()`                    | Logs in using API keys, user ID, MPIN, and TOTP                            |
| `fetch_instrument_df()`     | Returns instrument metadata as a pandas DataFrame                          |
| `get_historical_data_session()` | Returns a session for accessing historical market data                    |
| `get_trading_api_session()` | Returns a session for trading API                                          |
| `initialize_sessions()`     | Initializes both trading and historical sessions                           |
| `get_ltp(symbol)`           | Returns the Last Traded Price for the given symbol                         |
| `get_tradingsymbols('Nifty Bank')` | Fetches option symbols based on current spot price of Nifty or BankNifty |
| `get_ohlc(symbol, interval, n)` | Fetches OHLC data for specified interval and days                         |
| `get_ist_now()`             | Returns the current IST time                                               |

### ⏱ Supported OHLC Intervals
- `ONE_MINUTE`: 1 Minute
- `THREE_MINUTE`: 3 Minutes
- `FIVE_MINUTE`: 5 Minutes
- `TEN_MINUTE`: 10 Minutes
- `FIFTEEN_MINUTE`: 15 Minutes
- `THIRTY_MINUTE`: 30 Minutes

> Note: For intervals < 1 day, data is available for up to 60 days (as per broker limits).

---

## 💡 Example
```python
# Initialize the API
api = SmartAPIHelper()

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
```

---

## 📬 Contact
Feel free to raise issues or contribute to improvements by opening a pull request or submitting an issue!

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

