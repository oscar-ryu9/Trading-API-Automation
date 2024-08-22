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


    if (df['changed_data'] == 1).any():
        for index, row in df.iterrows():
            current_progress = row['current_progress']
            last_signal = row['last_signal']
            if row['changed_data'] == 1:
                for i in range(len(adjustment_list)):
                    if adjustment_list[i][0] == current_progress and adjustment_list[i][1] == last_signal:
                        print(f"Adjusting for {row['symbol']}: {adjustment_list[i][2]}, {adjustment_list[i][3]}")

                        #Some missing code here but not necessarily needed.

                        if adjustment_list[i][2] == "NOTHING":
                            df.at[index, 'last_signal'] = "Nothing"
                        else:
                            df.at[index, 'current_progress'] = df.at[index, 'last_signal']
                            df.at[index, 'last_signal'] = "Nothing"


                df.at[index, 'changed_data'] = 0
        df.to_csv("update.csv", index=False)
            
    else:
        print("No action required.")



# instruction = adjustment_list[i][2]
# hint = [adjustment_list[i][0], adjustment_list[i][3]]
# contract, quantity_i_have, quantity_for_share, order_instruction_first, order_instruction_second = order_information(index, instruction, hint)

# if contract != None:
#     print(contract[0])
#     if order_instruction_first != None:
#         print(order_instruction_first, quantity_i_have)
#     print(order_instruction_second, quantity_for_share)
    
# if contract != None:

#     my_contract = Contract()
#     my_contract.symbol = contract[0]
#     my_contract.secType = contract[1]
#     my_contract.currency = contract[2]
#     my_contract.exchange = contract[3]
#     my_contract.primaryExchange = contract[4]

#     if order_instruction_first != None:
#         prereq = Order()
#         prereq.action = order_instruction_first
#         prereq.orderType = "MKT"
#         prereq.totalQuantity = quantity_i_have
#         prereq.eTradeOnly = ""
#         prereq.firmQuoteOnly = ""

#     my_order = Order()
#     my_order.action = order_instruction_second
#     my_order.orderType = "MKT"
#     my_order.totalQuantity = quantity_for_share
#     my_order.eTradeOnly = ""
#     my_order.firmQuoteOnly = ""

#     if order_instruction_first != None:
#         id = read_counter()
#         app.placeOrder(id, my_contract, prereq)
#         increment_counter()
    
#     id = read_counter()
#     app.placeOrder(id, my_contract, my_order)