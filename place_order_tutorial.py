import ibapi
from ibapi.client import *
from ibapi.wrapper import *
import threading

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = None
    

    def nextValidId(self, orderId):
        self.nextValidOrderId = orderId



app = IBApi()
app.connect(#Your IP
    )

t1 = threading.Thread(target = app.run)
t1.start()
    

#Waiting for TWS connection acknoledgement

while (app.nextValidOrderId == None):
    print("Waiting for TWS connection acknoledgement ...")

print("Connection established.")


filename = "counter.txt"
with open(filename, 'w') as file:
    file.write(str(app.nextValidOrderId))


c1 = Contract()
c1.symbol = "PLUG"
c1.secType = "STK"
c1.currency = "USD"
c1.exchange = "SMART"
c1.primaryExchange = "NASDAQ"

c2 = Contract()
c2.symbol = "RKLB"
c2.secType = "STK"
c2.currency = "USD"
c2.exchange = "SMART"
c2.primaryExchange = "NASDAQ"

myorder = Order()
myorder.orderId = app.nextValidOrderId
myorder.action = "BUY"
myorder.orderType = "LMT"
myorder.totalQuantity = 1
myorder.lmtPrice = 3.00
myorder.eTradeOnly = ""
myorder.firmQuoteOnly = ""

