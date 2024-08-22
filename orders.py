import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time
import os
import pandas as pd
import datetime
import dateutil.relativedelta
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import time
import re
import numpy as np


def increment_counter():
    # Read current count from file
    with open("counter.txt", 'r') as file:
        count = int(file.read().strip())

    # Increment count
    count += 1

    # Write updated count back to file
    with open("counter.txt", 'w') as file:
        file.write(str(count))

    return count

def order_information(index, instruction, hint):

    symbols = ["PLTR", "INTC", "PLUG", "RKLB", "PCG", "UPWK", "SNAP", "LYFT", "STNE", "SOFI", "HOOD", "QS"]
    dict = {'PLTR': ['PLTR', 'STK', 'USD', 'SMART', 'NYSE'], 'INTC': ['INTC', 'STK', 'USD', 'SMART', 'NASDAQ'], 'PLUG': ['PLUG', 'STK', 'USD', 'SMART', 'NASDAQ'], 'RKLB': ['RKLB', 'STK', 'USD', 'SMART', 'NASDAQ'], 'PCG': ['PCG', 'STK', 'USD', 'SMART', 'NYSE'], 'UPWK': ['UPWK', 'STK', 'USD', 'SMART', 'NASDAQ'], 'SNAP': ['SNAP', 'STK', 'USD', 'SMART', 'NYSE'], 'LYFT': ['LYFT', 'STK', 'USD', 'SMART', 'NASDAQ'], 'STNE': ['STNE', 'STK', 'USD', 'SMART', 'NASDAQ'], 'SOFI': ['SOFI', 'STK', 'USD', 'SMART', 'NASDAQ'], 'HOOD': ['HOOD', 'STK', 'USD', 'SMART', 'NASDAQ'], 'QS': ['QS', 'STK', 'USD', 'SMART', 'NYSE']}
    symbol = symbols[index]

    scrape_type = dict[symbol][4]
    if scrape_type == "NASDAQ":
        scrape_symbol = symbol + ".NAS"
    else:
        scrape_symbol = symbol + ".NYSE"
    
    current_share = get_current_shares(symbol)
    
    if instruction != "NOTHING":

        timeframe = mt5.TIMEFRAME_H1
        date_from = datetime.now() - timedelta(days=10)
        date_to = datetime.now() + timedelta(days=1)

        prices = pd.DataFrame(mt5.copy_rates_range(scrape_symbol, timeframe, date_from, date_to))
        prices["time"] = pd.to_datetime(prices['time'], unit = 's')

        final_price = prices.iloc[-1]["close"]

        string_inst, number_inst = extract_string_and_number(instruction)
        
        owned_quantity = 0
        quantity = 0
        my_restriction = 100
        string_inst2 = None

        if current_share == 0:
            restriction = (number_inst/100) * my_restriction

            quantity = int(restriction // final_price)

        if current_share != 0 and hint[1] != 2:
            owned_quantity = current_share
            multiplier = number_inst/100
            quantity = int(np.floor(multiplier * owned_quantity))

        if current_share != 0 and hint[1] == 2:
            owned_quantity = current_share
            if hint[0] == "Strong Long" or hint[0] == "Long" or hint[0] == "LTP1":
                string_inst2 = "SELL"
            else:
                string_inst2 = "BUY"
            restriction = (number_inst/100) * my_restriction

            quantity = int(restriction // final_price)
            

        quantity_i_have = owned_quantity
        quantity_for_share = quantity
        order_instruction_first = string_inst2
        order_instruction_second = string_inst
    else:
        return None, None, None, None, None


    return dict[symbol], quantity_i_have, quantity_for_share, order_instruction_first, order_instruction_second

def get_current_shares(symbol):
    data = pd.read_csv("possession.csv")
    row = data[data['symbol'] == symbol]
    if not row.empty:
        return row['current_shares'].values[0]
    else:
        return None

def extract_string_and_number(input_string):
    # Define the regular expression pattern to match alphabetic characters and digits
    pattern = r'([a-zA-Z]+)(\d+)'
    
    # Use re.match to find the pattern in the input string
    match = re.match(pattern, input_string)
    
    # Check if a match is found
    if match:
        # Extract the string and number parts from the match
        extracted_string = match.group(1)
        extracted_number = int(match.group(2))
        return extracted_string, extracted_number
    else:
        # If no match is found, return None for both parts
        return None, None
    

my, quantity_i_have, quantity_for_share, order_instruction_first, order_instruction_second = order_information(9, "NOTHING", ["Nothing, -1"])