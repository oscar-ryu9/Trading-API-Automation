import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import time
import os
import pandas as pd


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

def handle_csv_changes(df):

    adjustment_list = [["Nothing", "Nothing", "NOTHING", -1],["Nothing","Strong Long", "BUY100", 0], ["Nothing", "Long", "BUY75", 0], ["Nothing", "LTP1", "SELL75", 0], ["Nothing", "LTP2", "SELL100",0], ["Nothing", "LExit", "SELL100", 0],["Nothing","Strong Short", "SELL100", 1], ["Nothing", "Short", "SELL75", 1], ["Nothing", "STP1", "BUY75", 1], ["Nothing", "STP2", "BUY100", 1], ["Nothing", "SExit", "BUY100", 1]
                       ["Strong Long", "Nothing", "NOTHING", -1], ["Strong Long", "LExit", "SELL100", 0], ["Strong Long", "LTP1", "SELL75", 0], ["Strong Long", "LTP2", "SELL100", 0],
                       ["Long", "Nothing", "NOTHING", -1], ["Long", "LExit", "SELL100", 0], ["Long", "LTP1", "SELL75", 0], ["Long", "LTP2", "SELL100", 0],
                       ["LTP1", "Nothing", "NOTHING", -1], ["LTP1", "LExit", "SELL100", 0], ["LTP1", "LTP2", "SELL100", 0],
                       ["LTP2", "Nothing", "NOTHING", -1], ["LTP2", "Strong Long", "BUY100", 0], ["LTP2", "Long", "BUY75", 0],["LTP2", "Strong Short", "SELL100", 1], ["LTP2", "Short", "SELL75", 1],
                       ["LExit", "Nothing", "NOTHING", -1], ["LExit", "Strong Long", "BUY100", 0], ["LExit", "Long", "BUY75", 0], ["LExit", "Strong Short", "SELL100", 1], ["LExit", "Short", "SELL75", 1],
                       ["Strong Short", "Nothing", "NOTHING", -1], ["Strong Short", "SExit", "BUY100", 1], ["Strong Short", "STP1", "BUY75", 1], ["Strong Short", "STP2", "BUY100", 1],
                       ["Short", "Nothing", "NOTHING", -1], ["Short", "SExit", "BUY100", 1], ["Short", "STP1", "BUY75", 1], ["Short", "STP2", "BUY100", 1],
                       ["STP1", "Nothing", "NOTHING", -1], ["STP1", "SExit", "BUY100", 1], ["STP1", "STP2", "BUY100", 1],
                       ["STP2", "Nothing", "NOTHING", -1], ["STP2", "Strong Long", "BUY100", 0], ["STP2", "Long", "BUY75", 0],["STP2", "Strong Short", "SELL100", 1], ["STP2", "Short", "SELL75", 1]
                       ["SExit", "Nothing", "NOTHING", -1], ["SExit", "Strong Long", "BUY100", 0], ["SExit", "Long", "BUY75", 0], ["SExit", "Strong Short", "SELL100", 1], ["SExit", "Short", "SELL75", 1]]


    if (df['changed_data'] == 1).any():
        for index, row in df.iterrows():
            current_progress = row['current_progress']
            last_signal = row['last_signal']
            if row['changed_data'] == 1:
                for item in adjustment_list:
                    if current_progress == item[0] and last_signal == item[1]:
                        print(f"Adjusting for {row['symbol']}: {item[2]}, {item[3]}")
                        # TO DO : implement based on item[2] -> BUY100, BUY75, SELL75, SELL100, NOTHING
                        break
                df.at[index, 'changed_data'] = 0
                df.at[index, "current_progress"] = df.at[index, "last_signal"]
                df.at[index, "last_signal"] = "Nothing"

        df.to_csv("update.csv", index=False)
    else:
        print("No action required.")

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = None

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

def run_ib_api():
    app = IBApi()
    app.connect(#YOUR IP
    )

    t1 = threading.Thread(target=app.run)
    t1.start()

    # Waiting for TWS connection acknowledgment
    while app.nextValidOrderId is None:
        print("Waiting for TWS connection acknowledgment ...")

    print("Connection established.")

# Start IB API thread
t_ib_api = threading.Thread(target=run_ib_api)
t_ib_api.start()

# Start CSV monitoring thread
filename = "update.csv"
t_csv_monitor = threading.Thread(target=monitor_csv, args=(filename,))
t_csv_monitor.start()



# #Define Apple stock contract
# c1 = Contract()
# c1.symbol = "AAPL"
# c1.secType = "STK"
# c1.currency = "USD"
# c1.exchange = "SMART"
# c1.primaryExchange = "NASDAQ"

# o1 = Order()
# o1.action = "BUY"
# o1.orderType = "MKT"
# o1.totalQuantity = quantity

# orderId = app.nextValidOrderId
# app.placeOrder(orderId, c1, o1)