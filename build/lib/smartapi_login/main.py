# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 11:02:25 2024

@author: Mahesh_Kumar
"""


import subprocess
import sys

# List of libraries to check
required_libraries = [
    'pandas',
    'requests',
    'pytz',
    'pyotp',
]

def install_libraries(libraries):
    """Install libraries using pip if they are not already installed"""
    for library in libraries:
        try:
            __import__(library)
        except ImportError:
            print(f"Library {library} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])

# Install required libraries
install_libraries(required_libraries)


import pandas as pd
import requests
import time
from datetime import timedelta, date, datetime
from pytz import timezone
from SmartApi import SmartConnect
import pyotp
import json



class SmartAPIHelper:
    
    def __init__(self):
        # Initialization code, this can be used to set default values or load from files
        self.api_key_hist = None
        self.api_key_trading = None
        self.uid = None
        self.mpin = None
        self.totp = None
    
    def run(self):
        print("Initializing sessions...")
        self.initialize_sessions()
        print("Fetching data...")
        df = self.get_tradingsymbols()
        print("Processing complete.")


    def login(self, api_key_hist, api_key_trading, uid, mpin, totp):        
        """
        Takes user input for credentials if they are not provided.
        These credentials will not be saved permanently.
        """
        self.api_key_hist = api_key_hist  # Use iloc for position-based access
        self.api_key_trading = api_key_trading
        self.uid = uid
        self.mpin = mpin
        self.totp = totp
        print("Login successful! Credentials will not be saved.")
  
    
    def fetch_instrument_df(self):
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    
            data = response.json()
            Instrument_df = pd.DataFrame(data)
            
            return Instrument_df
    
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data. Error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON. Error: {e}")
            return None
        

    def get_historical_data_session(self):
        obj = SmartConnect(api_key=self.api_key_hist)
        data = obj.generateSession(self.uid, self.mpin, pyotp.TOTP(self.totp).now())
        hist_data_refreshToken = data['data']['refreshToken']
        hist_data_feedToken = obj.getfeedToken()
        return obj

    def get_trading_api_session(self):
        obj_trading = SmartConnect(api_key=self.api_key_trading)
        trading_data = obj_trading.generateSession(self.uid, self.mpin, pyotp.TOTP(self.totp).now())
        trading_refreshToken = trading_data['data']['refreshToken']
        trading_feedToken = obj_trading.getfeedToken()
        return obj_trading

 

    def initialize_sessions(self):
        try:
            obj = self.get_historical_data_session()
            obj_trading = self.get_trading_api_session()
            
            return obj,obj_trading
            
        except Exception as e:
            print("An error occurred during session initialization:", str(e))
        
        pass
        

    def get_ltp(self,symbol):
        try:     
            obj=self.get_historical_data_session()
            Instrument_df=self.fetch_instrument_df()
            token = Instrument_df.loc[Instrument_df['symbol'] == symbol, 'token'].values[0]
            exch_seg = Instrument_df.loc[Instrument_df['symbol'] == symbol, 'exch_seg'].values[0]
            price = obj.ltpData(exch_seg, symbol, token)
            ltp = price['data']['ltp']
            time.sleep(0.5)
            return ltp
            
        except Exception as e:
            print("An error occurred:", str(e))
            return None

    def get_tradingsymbols(self,symbol):
        spot_price = self.get_ltp(symbol)
        
        if spot_price is not None:
            Instrument_df=self.fetch_instrument_df()

            spot_price = round(spot_price / 100) * 100
    
            df_options = Instrument_df[(Instrument_df['name'].isin(['NIFTY', 'BANKNIFTY'])) & (Instrument_df['instrumenttype'] == 'OPTIDX')]
            df_bnf_only = df_options[df_options['name'] == 'BANKNIFTY']
            df_bnf_only = df_bnf_only[['token', 'symbol', 'expiry', 'strike', 'instrumenttype', 'name']]
    
            expiry_dates = min(df_bnf_only['expiry'], key=lambda date: datetime.strptime(date, '%d%b%Y').date())
            df_bnf_only = df_bnf_only[df_bnf_only['expiry'] == expiry_dates]
            df_bnf_only['strike'] = pd.to_numeric(df_bnf_only['strike'], errors='coerce') / 100
    
            lower_strike = spot_price - 1500
            upper_strike = spot_price + 1500
            df_bnf_only = df_bnf_only[(df_bnf_only['strike'] >= lower_strike) & (df_bnf_only['strike'] <= upper_strike)]
    
            df_bnf_only.reset_index(drop=True, inplace=True)
            df_bnf_only['LTP'] = df_bnf_only['symbol'].apply(self.get_ltp)
    
            return df_bnf_only
        else:
            print("Error: Spot price is None.")
            return None
        

    def get_ohlc(self, symbol, interval, n): 
        
        obj=self.get_historical_data_session()
        Instrument_df=self.fetch_instrument_df()
 
        token = Instrument_df.loc[((Instrument_df['symbol'] == symbol), 'token')].values[0]
        exch_seg = Instrument_df.loc[(Instrument_df['symbol'] == symbol), 'exch_seg'].values[0]
        try:
            historicParam = {
                "exchange": exch_seg,
                "symboltoken": token,
                "interval": interval,
                "fromdate": f'{date.today() - timedelta(days=n)} 09:15',
                "todate": f'{date.today() - timedelta(days=0)} 15:30'
            }

            col = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            ohlc = obj.getCandleData(historicParam)['data']
            data = pd.DataFrame(ohlc, columns=col, index=None)
            # data['timestamp'] = pd.to_datetime(data['timestamp'], format='%Y-%m-%dT%H:%M:%S%z', dayfirst=True)
            data['timestamp'] = pd.to_datetime(data['timestamp'], format='mixed')



            data['symbol'] = symbol
            time.sleep(0.7)

        except Exception as e:
            print("Historic Api failed: {}".format(str(e)))
        return data
       

    def get_ist_now(self):
        ist = timezone('Asia/Kolkata')
        now = datetime.now(ist)
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        return timestamp



    






  
        
        
        
