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

mt5.initialize()
mt5.login(#YOUR LOGIN
    )

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = None

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

app = IBApi()
app.connect(#YOUR IP
    )

t1 = threading.Thread(target=app.run)
t1.start()

# Waiting for TWS connection acknowledgment
while app.nextValidOrderId is None:
    print("Waiting for TWS connection acknowledgment ...")

print("Connection established.")
filename = "counter.txt"
with open(filename, 'w') as file:
    file.write(str(app.nextValidOrderId))

class CSVMonitor:
    def __init__(self, filename):
        self.filename = filename
        self.last_modified = None

    def is_modified(self):
        current_modified = os.path.getmtime(self.filename)
        if self.last_modified is None or current_modified > self.last_modified:
            self.last_modified = current_modified
            return True
        return False

    def process_csv(self):
        try:
            df = pd.read_csv(self.filename)
            # Process the CSV data here
            # print(df.head())  # For demonstration, just printing the first few rows
            # Call a function to handle CSV changes, e.g., place orders based on CSV data
            handle_csv_changes(df)
        except Exception as e:
            print("Error processing CSV:", e)

def monitor_csv(filename):
    csv_monitor = CSVMonitor(filename)
    print("Monitoring CSV file for changes...")
    try:
        while True:
            if csv_monitor.is_modified():
                print("CSV file modified, processing...")
                csv_monitor.process_csv()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Monitoring stopped.")


# Start CSV monitoring thread
filename = "update.csv"
t_csv_monitor = threading.Thread(target=monitor_csv, args=(filename,))
t_csv_monitor.start()


def handle_csv_changes(df):

    adjustment_list = [["Nothing", "Nothing", "NOTHING", -1],["Nothing","Strong Long", "BUY100", 0], ["Nothing", "Long", "BUY75", 0], ["Nothing", "LTP1", "NOTHING", -1], ["Nothing", "LTP2", "NOTHING",-1], ["Nothing", "LExit", "NOTHING", -1],["Nothing","Strong Short", "SELL100", 1], ["Nothing", "Short", "SELL75", 1], ["Nothing", "STP1", "NOTHING", -1], ["Nothing", "STP2", "NOTHING", -1], ["Nothing", "SExit", "NOTHING", -1],
                       ["Strong Long", "Nothing", "NOTHING", -1], ["Strong Long", "LExit", "SELL100", 0], ["Strong Long", "LTP1", "SELL75", 0], ["Strong Long", "LTP2", "SELL100", 0],["Strong Long", "Short", "SELL75", 2], ["Strong Long", "Strong Short", "SELL100", 2],
                       ["Long", "Nothing", "NOTHING", -1], ["Long", "LExit", "SELL100", 0], ["Long", "LTP1", "SELL75", 0], ["Long", "LTP2", "SELL100", 0],["Long", "Strong Short", "SELL100", 2], ["Long", "Short", "SELL75", 2],
                       ["LTP1", "Nothing", "NOTHING", -1], ["LTP1", "LExit", "SELL100", 0], ["LTP1", "LTP2", "SELL100", 0],["LTP1", "Short", "SELL75", 2], ["LTP1", "Strong Short", "SELL100", 2],
                       ["LTP2", "Nothing", "NOTHING", -1], ["LTP2", "Strong Long", "BUY100", 0], ["LTP2", "Long", "BUY75", 0],["LTP2", "Strong Short", "SELL100", 1], ["LTP2", "Short", "SELL75", 1],
                       ["LExit", "Nothing", "NOTHING", -1], ["LExit", "Strong Long", "BUY100", 0], ["LExit", "Long", "BUY75", 0], ["LExit", "Strong Short", "SELL100", 1], ["LExit", "Short", "SELL75", 1],
                       ["Strong Short", "Nothing", "NOTHING", -1], ["Strong Short", "SExit", "BUY100", 1], ["Strong Short", "STP1", "BUY75", 1], ["Strong Short", "STP2", "BUY100", 1], ["Strong Short", "Long", "BUY75", 2], ["Strong Short", "Strong Long", "BUY100", 2],
                       ["Short", "Nothing", "NOTHING", -1], ["Short", "SExit", "BUY100", 1], ["Short", "STP1", "BUY75", 1], ["Short", "STP2", "BUY100", 1],["Short", "Long", "BUY75", 2], ["Short", "Strong Long", "BUY100", 2],
                       ["STP1", "Nothing", "NOTHING", -1], ["STP1", "SExit", "BUY100", 1], ["STP1", "STP2", "BUY100", 1],["STP1", "Long", "BUY75", 2], ["STP1", "Strong Long", "BUY100", 2],
                       ["STP2", "Nothing", "NOTHING", -1], ["STP2", "Strong Long", "BUY100", 0], ["STP2", "Long", "BUY75", 0],["STP2", "Strong Short", "SELL100", 1], ["STP2", "Short", "SELL75", 1],
                       ["SExit", "Nothing", "NOTHING", -1], ["SExit", "Strong Long", "BUY100", 0], ["SExit", "Long", "BUY75", 0], ["SExit", "Strong Short", "SELL100", 1], ["SExit", "Short", "SELL75", 1]]
    symbols = ["PLTR", "INTC", "PLUG", "RKLB", "PCG", "UPWK", "SNAP", "LYFT", "STNE", "SOFI", "HOOD", "QS"]

    if (df['changed_data'] == 1).any():
        for index, row in df.iterrows():
            current_progress = row['current_progress']
            last_signal = row['last_signal']
            if row['changed_data'] == 1:
                for i in range(len(adjustment_list)):
                    if adjustment_list[i][0] == current_progress and adjustment_list[i][1] == last_signal:

                        instruction = adjustment_list[i][2]
                        hint = [adjustment_list[i][0], adjustment_list[i][3]]
                        contract, quantity_i_have, quantity_for_share, order_instruction_first, order_instruction_second = order_information(index, instruction, hint)
                        
                        # Find the price of the latest market
                        dict = {'PLTR': ['PLTR', 'STK', 'USD', 'SMART', 'NYSE'], 'INTC': ['INTC', 'STK', 'USD', 'SMART', 'NASDAQ'], 'PLUG': ['PLUG', 'STK', 'USD', 'SMART', 'NASDAQ'], 'RKLB': ['RKLB', 'STK', 'USD', 'SMART', 'NASDAQ'], 'PCG': ['PCG', 'STK', 'USD', 'SMART', 'NYSE'], 'UPWK': ['UPWK', 'STK', 'USD', 'SMART', 'NASDAQ'], 'SNAP': ['SNAP', 'STK', 'USD', 'SMART', 'NYSE'], 'LYFT': ['LYFT', 'STK', 'USD', 'SMART', 'NASDAQ'], 'STNE': ['STNE', 'STK', 'USD', 'SMART', 'NASDAQ'], 'SOFI': ['SOFI', 'STK', 'USD', 'SMART', 'NASDAQ'], 'HOOD': ['HOOD', 'STK', 'USD', 'SMART', 'NASDAQ'], 'QS': ['QS', 'STK', 'USD', 'SMART', 'NYSE']}
                        symbol = symbols[index]
                        scrape_type = dict[symbol][4]
                        if scrape_type == "NASDAQ":
                            scrape_symbol = symbol + ".NAS"
                        else:
                            scrape_symbol = symbol + ".NYSE"

                        timeframe = mt5.TIMEFRAME_M15
                        date_from = datetime.now() - timedelta(days=10)
                        date_to = datetime.now() + timedelta(days=1)

                        prices = pd.DataFrame(mt5.copy_rates_range(scrape_symbol, timeframe, date_from, date_to))
                        prices["time"] = pd.to_datetime(prices['time'], unit = 's')

                        final_price = prices.iloc[-1]["close"]
                        if contract != None:
                            print("BOUGHT/SOLD SOMETHING " + str(contract[0]))
                            text = ""
                            string1 = str(contract[0]) + "\n"
                            text += string1
                            if order_instruction_first != None:
                                string2 = str(order_instruction_first) + ", " + str(quantity_i_have) +  "\n"
                                text += string2
                                modify_shares(symbols[index], 0)
                            string3 = str(order_instruction_second) + ", " + str(quantity_for_share) + "\n"
                            string4 = str(final_price)
                            text += string3
                            text += string4
                            calculate_new_share(symbols[index], adjustment_list[i], order_instruction_second, quantity_for_share)

                            path = "April_Test/" + symbol + ".txt"
                            with open(path, 'a') as file:
                                file.write(text + "\n\n")
                        
                            
                        if contract != None:

                            my_contract = Contract()
                            my_contract.symbol = contract[0]
                            my_contract.secType = contract[1]
                            my_contract.currency = contract[2]
                            my_contract.exchange = contract[3]
                            my_contract.primaryExchange = contract[4]

                            if order_instruction_first != None:
                                prereq = Order()
                                prereq.action = order_instruction_first
                                prereq.orderType = "MKT"
                                prereq.totalQuantity = quantity_i_have
                                prereq.eTradeOnly = ""
                                prereq.firmQuoteOnly = ""

                            my_order = Order()
                            my_order.action = order_instruction_second
                            my_order.orderType = "MKT"
                            my_order.totalQuantity = quantity_for_share
                            my_order.eTradeOnly = ""
                            my_order.firmQuoteOnly = ""

                            if order_instruction_first != None:
                                id = read_counter()
                                app.placeOrder(id, my_contract, prereq)
                                increment_counter()
                            
                            id = read_counter()
                            app.placeOrder(id, my_contract, my_order)
                            increment_counter()

                        if adjustment_list[i][2] == "NOTHING":
                            df.at[index, 'last_signal'] = "Nothing"
                        else:
                            df.at[index, 'current_progress'] = df.at[index, 'last_signal']
                            df.at[index, 'last_signal'] = "Nothing"


                df.at[index, 'changed_data'] = 0
        df.to_csv("update.csv", index=False)
            
    else:
        print("No action required.")

def read_counter():
    # Read current count from file
    with open("counter.txt", 'r') as file:
        count = int(file.read().strip())

    return count

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

        timeframe = mt5.TIMEFRAME_M15
        date_from = datetime.now() - timedelta(days=10)
        date_to = datetime.now() + timedelta(days=1)

        prices = pd.DataFrame(mt5.copy_rates_range(scrape_symbol, timeframe, date_from, date_to))
        prices["time"] = pd.to_datetime(prices['time'], unit = 's')

        final_price = prices.iloc[-1]["close"]

        string_inst, number_inst = extract_string_and_number(instruction)
        
        owned_quantity = 0
        quantity = 0
        my_restriction = 300
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

def calculate_new_share(symbol, lis, instruction, shares):
    if lis[3] == 2:
        add_shares(symbol, shares)
    elif lis[3] == 0 and instruction == "BUY":
        add_shares(symbol, shares)
    elif lis[3] == 0 and instruction == "SELL":
        add_shares(symbol, -shares)
    elif lis[3] == 1 and instruction == "BUY":
        add_shares(symbol, -shares)
    else:
        add_shares(symbol, shares)


def modify_shares(symbol, new_shares):
    df = pd.read_csv('possession.csv')

    df.loc[df['symbol'] == symbol, 'current_shares'] = new_shares

    df.to_csv('possession.csv', index=False)

def add_shares(symbol, additional_shares):
    df = pd.read_csv('possession.csv')

    df.loc[df['symbol'] == symbol, 'current_shares'] += additional_shares

    df.to_csv('possession.csv', index=False)

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
    

import mss
import pandas as pd
import time

# Define the colors to scan for
colors_to_scan_for = [
    (175, 150, 0),   # Strong Long Color
    (100, 100, 220), # Long Color
    (150, 0, 150),   # LTP1 Color
    (100, 50, 150),  # LTP2 Color
    (220, 120, 220),  # LExit Color
    (176, 151, 2),   # Strong Short Color
    (101, 101, 222), # Short Color
    (151, 1, 151),   # STP1 Color
    (101, 51, 151),  # STP2 Color
    (221, 121, 221),  # SExit Color
]

def scan_market_for_colors(x1, y1, x2, y2, colors):
    with mss.mss() as sct:
        # Get information about the monitor
        monitor_info = sct.monitors[2]
        monitor_width = monitor_info['width']
        monitor_height = monitor_info['height']
        
        # Capture the screen
        screenshot = sct.grab(monitor_info)
        
        # Initialize list to store whether each color is found
        colors_found = [False] * len(colors)
        # Dictionary to store coordinates of each color found
        color_coordinates = {color: [] for color in colors}
        
        # Search for each specified color
        for i, color in enumerate(colors):
            for y in range(y1, y2):
                for x in range(x1, x2):
                    pixel = screenshot.pixel(x, y)
                    # Check if the pixel matches the specified color
                    if pixel == color:
                        colors_found[i] = True
                        # Store the coordinates of the color
                        color_coordinates[color].append((x, y))

        for key, value in color_coordinates.items():
            color_coordinates[key] = filter_x_within_50(value)
        
        return colors_found, color_coordinates

def reverse_search(dictionary, target_value):
    for key, value_list in dictionary.items():
        if target_value in value_list:
            return key
    return None

def filter_x_within_50(coords):
    filtered_coords = []
    seen_x_values = set()
    for x, y in coords:
        if all(abs(x - seen_x) > 50 for seen_x in seen_x_values):
            filtered_coords.append((x, y))
            seen_x_values.add(x)
    return filtered_coords

def get_order(color_coords):
    list = []
    for key, value_list in color_coords.items():
        for value in value_list:
            list.append(value)
    
    sorted_list = sorted(list, key=lambda point: point[0])

    ordered_list = []
    for i in range(len(sorted_list)):
        ordered_list.append(reverse_search(color_coords, sorted_list[i]))
    
    classification_dict = {
        (175, 150, 0): "Strong Long",
        (100, 100, 220): "Long",
        (150, 0, 150): "LTP1",
        (100, 50, 150): "LTP2",
        (220, 120, 220): "LExit",
        (176, 151, 2): "Strong Short",
        (101, 101, 222): "Short",
        (151, 1, 151): "STP1",
        (101, 51, 151): "STP2",
        (221, 121, 221): "SExit"
    }

    # Iterate through the list and classify each tuple
    classified_list = [classification_dict[t] for t in ordered_list]

    return ', '.join(classified_list), classified_list

last_all_orders = [[], [], [], [], [], [], [], [], [], [], [], []]
i = 0
while True:
    # Read the CSV file
    coordinates_df = pd.read_csv("coordinates.csv")

    # Extract market coordinates from the DataFrame
    market_coordinates = []
    for index, row in coordinates_df.iterrows():
        market_name = row['symbol']
        x1, y1, x2, y2 = row['x1'], row['y1'], row['x2'], row['y2']
        market_coordinates.append((market_name, x1, y1, x2, y2))
    
    all_color_coordinates = {}
    for market_info in market_coordinates:
        market_name, x1, y1, x2, y2 = market_info
        colors_found, color_coordinates = scan_market_for_colors(x1, y1, x2, y2, colors_to_scan_for)
        all_color_coordinates[market_name] = color_coordinates

    all_orders = []
    all_orders_print = []
    for key, value_list in all_color_coordinates.items():
        order, order_list = get_order(value_list)
        all_orders.append(order_list)
        all_orders_print.append(order)
    

    if i == 0:
        last_all_orders = all_orders
        i+=1
    
    df = pd.read_csv("update.csv")


    for i in range(len(all_orders)):
        if all_orders[i] != last_all_orders[i] and all_orders[i] != []:
            df.at[i, "last_signal"] = all_orders[i][-1]
            df.at[i, "changed_data"] = 1
            df.to_csv("update.csv", index=False)

    time.sleep(0)  # Adjust the sleep time as needed
    last_all_orders = all_orders