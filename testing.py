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
mt5.login(51692857, "3RufnB3jg@Zz&0","ICMarketsSC-Demo")

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = None

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId

app = IBApi()
app.connect("127.0.0.1", 7496, 1)

t1 = threading.Thread(target=app.run)
t1.start()

# Waiting for TWS connection acknowledgment
while app.nextValidOrderId is None:
    print("Waiting for TWS connection acknowledgment ...")

print("Connection established.")
filename = "counter.txt"
with open(filename, 'w') as file:
    file.write(str(app.nextValidOrderId))

my_contract = Contract()
my_contract.symbol = 'PLUG'
my_contract.secType = 'STK'
my_contract.currency = 'USD'
my_contract.exchange = 'SMART'
my_contract.primaryExchange = 'NASDAQ'

my_order = Order()
my_order.action = "SELL"
my_order.orderType = "MKT"
my_order.totalQuantity = 1
my_order.eTradeOnly = ""
my_order.firmQuoteOnly = ""

order_id = app.nextValidOrderId
print(order_id)
app.placeOrder(order_id, my_contract, my_order)
