# -*- coding: utf-8 -*-
"""
AutoSmartAPI Package

This package contains modules for interacting with the SmartAPI, fetching historical data,
trading sessions, and other financial data.

Author: Mahesh Kumar
Version: 0.1
"""

# Import the main classes and functions that should be accessible when the package is imported
from .smartapi_login import SmartAPI  # Assuming your main class is in a file named 'smartapi.py'

# You can also define version number here if needed
__version__ = '1.0.0.2'
import logging
logging.basicConfig(level=logging.INFO)
logging.info("smartapi_login package loaded successfully!")

# If you want to add a custom message or other initializations
# print("smartapi_login package loaded successfully!")
