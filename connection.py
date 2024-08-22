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