from ibapi import *
from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import Contract, ContractDetails
from ibapi.order import Order
import threading

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextValidOrderId = None
    

    def nextValidId(self, orderId: int):
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

        self.reqContractDetails(orderId, c1)
    
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract)

        myorder = Order()
        myorder.orderId = reqId
        myorder.action = "BUY"
        myorder.orderType = "LMT"
        myorder.totalQuantity = 1
        myorder.lmtPrice = 3.00
        myorder.eTradeOnly = ""
        myorder.firmQuoteOnly = ""

        self.placeOrder(reqId, contractDetails.contract, myorder)




app = IBApi()
app.connect(#YOUR IP
)
app.run()
    



# o1 = Order()
# o1.action = "BUY"
# o1.orderType = "LMT"
# o1.totalQuantity = 1
# o1.lmtPrice = 3.00

# orderId = app.nextValidOrderId
# app.placeOrder(orderId, c1, o1)


