from clr; import; AddReference; 
AddReference("System"); 
AddReference("QuantConnect.Algorithm");
AddReference("QuantConnect.Common");

from System import *
from QuantConnect import *
from QuantConnect.Orders import *
from QuantConnect.Algorithm import *
from QuantConnect.Algorithm.Framework import *
from QuantConnect.Algorithm.Framework.Alphas import *
from QuantConnect.Algorithm.Framework.Portfolio import *
from QuantConnect.Algorithm.Framework.Selection import *
from datetime import datetime, timedelta
import numpy as np
from collections import deque

### <summary>
### Regression algorithm for testing ScheduledUniverseSelectionModel scheduling functions.
### </summary>
class ScheduledUniverseSelectionModelRegressionAlgorithm(QCAlgorithm):
    '''Regression algorithm for testing ScheduledUniverseSelectionModel scheduling functions.'''

    def Initialize(self):

        self.SetStartDate(2010, 2, 1)
        self.SetEndDate(2012, 9, 1)
        self.quantity = 100
        
        # Add assets you'd like to see
        self.ticker ="TSLA" #"NFLX" "TSLA"
        #self.tesla = self.AddEquity(ticker = self.ticker, extendedMarketHours = True).Symbol
        self.tesla = self.AddEquity(self.ticker, Resolution.Minute, Market.USA, True, 1, True)

        #self.netflix = self.AddEquity("NFLX")

        # define our 30 minute trade bar consolidator. we can
        # access the 30 minute bar from the DataConsolidated events
        thirtyMinuteConsolidator = TradeBarConsolidator(timedelta(minutes=30))

        # attach our event handler. the event handler is a function that will
        # be called each time we produce a new consolidated piece of data.
        thirtyMinuteConsolidator.DataConsolidated += self.ThirtyMinuteBarHandler

        # this call adds our 30 minute consolidator to
        # the manager to receive updates from the engine
        self.SubscriptionManager.AddConsolidator(self.ticker, thirtyMinuteConsolidator)
        self.__last = 1
        self.premarkethigh = []
        self.premarketlow = []
        self.limitPriceLong = False
        self.stopPriceLong = False
        self.stopPriceShort = False
        self.myclose = False
        self.indicatorlong = False
        self.indicatorshort = False
        self.mymax = False
        self.mylow = False
        self.indicatornotstoplong = False
        self.indicatornotstopshort = False
        self.almostlong = 0.77
        self.almostshort = 1.23
        self.secondtimelong = False
        self.secondtimeshort = False
        self.limitshort = []
        self.limitlong = []
        self.stoplong = []
        self.stopshort = []
        self.longdoble = deque(maxlen = 2)
        self.shortdoble = deque(maxlen = 2)
        self.counter = 0
        self.countershort = 0
        self.counterindicator = False
        self.counterindicatorshort = False
        self.mymessage1 = None #Limit price (Take Profit)
        self.mymessage2 = None
        self.stoplongdoble = []
        self.stopshortdoble = []
        self.stopshort75 = []
        self.stoplong75 = []
        self.mo = []
        self.comparator = None
        self.comparator1 = None
    def OnData(self, data):
        myhour = data[self.ticker].Time.hour
        myminute = data[self.ticker].Time.minute
        """
        if ((myhour < 9) or (myhour == 9 and myminute < 30)) or myhour > 16:
            negative = False
            if len(self.limitlong) > 0:
                if self.limitlong[-1].Status == OrderStatus.Filled:
                    negative =False
            if len(self.stoplong) > 0:
                if self.stoplong[-1].Status == OrderStatus.Filled:
                    negative = False
            if len(self.stoplongdoble) > 0:
                if self.stoplongdoble[-1].Status == OrderStatus.Filled:
                    negative = False
            if negative == True:
                self.Transactions.CancelOpenOrders()
                self.stoplong = []
                self.stoplongdoble = []
                self.stoplong75 = []
                self.limitlong = []
        """
                    
        
        if myhour > 2 and myhour <= 24:
            if len(self.limitlong) > 0:
                if self.limitlong[-1].Status == OrderStatus.Filled:
                    self.Debug("Order Filled" + self.mymessage1)
                    openOrders = self.Transactions.GetOpenOrders()
                    if len(openOrders)> 0:
                        for x in openOrders:
                            self.Transactions.CancelOrder(x.Id)
                    
                    self.limitlong = []
                    self.stoplong = []
                    self.stoplongdoble = []
                    self.stoplong75 = []
                    self.mo = []
                    self.indicatorlong = False
                    self.indicatornotstoplong = False
                    self.counterindicator = False
                    self.counterindicatorshort = False
                    self.longdoble = deque(maxlen = 2)
                    
            if len(self.limitshort) > 0:
                if self.limitshort[-1].Status == OrderStatus.Filled:
                    self.Debug("Order Filled")
                    openOrders = self.Transactions.GetOpenOrders()
                    if len(openOrders)> 0:
                        for x in openOrders:
                            self.Transactions.CancelOrder(x.Id)
                    self.limitshort = []
                    self.stopshort = []
                    self.stopshortdoble = []
                    self.stopshort75 = []
                    self.mo = []
                    self.indicatorlong = False
                    self.indicatornotstoplong = False
                    self.counterindicator = False
                    self.counterindicatorshort = False
                    self.shortdoble = deque(maxlen = 2)
                    
            if len(self.stoplong) > 0 or len(self.stoplongdoble) > 0:
                #self.Debug("RRRRRRR {} {} ".format(len(self.stoplong), len(self.stoplongdoble)))
                if len(self.stoplong) > 0:
                    if self.stoplong[-1].Status == OrderStatus.Filled:
                        self.Debug(str(self.Portfolio[self.ticker].Quantity))
                        self.Debug("Order Filled" + self.mymessage2)
                        openOrders = self.Transactions.GetOpenOrders()
                        if len(openOrders)> 0:
                            for x in openOrders:
                                self.Transactions.CancelOrder(x.Id)
                        self.limitlong = []
                        self.stoplong = []
                        self.stoplongdoble = []
                        self.stoplong75 = []
                        self.mo = []
                        self.indicatorlong = False
                        self.indicatornotstoplong = False
                        self.counterindicator = False
                        self.counterindicatorshort = False
                        self.longdoble = deque(maxlen = 2)
                        ################################
                        
                if len(self.stoplongdoble) > 0:
                    if self.stoplongdoble[-1].Status == OrderStatus.Filled:
                        self.Debug(str(self.Portfolio[self.ticker].Quantity))
                        openOrders = self.Transactions.GetOpenOrders()
                        if len(openOrders)> 0:
                            for x in openOrders:
                                self.Transactions.CancelOrder(x.Id)
                        self.Debug("Order Filled" + self.mymessage2)
                        self.limitlong = []
                        self.stoplong = []
                        self.stoplongdoble = []
                        self.stoplong75 = []
                        self.mo = []
                        self.indicatorlong = False
                        self.indicatornotstoplong = False
                        self.counterindicator = False
                        self.counterindicatorshort = False
                        self.longdoble = deque(maxlen = 2)
                
                if len(self.stoplong75) > 0:
                    if self.stoplong75[-1].Status == OrderStatus.Filled:
                        self.Debug(str(self.Portfolio[self.ticker].Quantity))
                        openOrders = self.Transactions.GetOpenOrders()
                        if len(openOrders)> 0:
                            for x in openOrders:
                                self.Transactions.CancelOrder(x.Id)
                        self.Debug("Order Filled" + self.mymessage2)
                        self.limitlong = []
                        self.stoplong = []
                        self.stoplongdoble = []
                        self.stoplong75 = []
                        self.mo = []
                        self.indicatorlong = False
                        self.indicatornotstoplong = False
                        self.counterindicator = False
                        self.counterindicatorshort = False
                        self.longdoble = deque(maxlen = 2)
                        
            if len(self.stopshort) > 0 or len(self.stopshortdoble) > 0:
                if len(self.stopshort) > 0:
                    if self.stopshort[-1].Status == OrderStatus.Filled:
                        self.Debug(str(self.Portfolio[self.ticker].Quantity))
                        self.Debug("Order Filled" + self.mymessage2)
                        openOrders = self.Transactions.GetOpenOrders()
                        if len(openOrders)> 0:
                            for x in openOrders:
                                self.Transactions.CancelOrder(x.Id)
                        self.limitshort = []
                        self.stopshort = []
                        self.stopshortdoble = []
                        self.stopshort75 = []
                        self.mo = []
                        self.indicatorshort = False
                        self.indicatornotstopshort = False
                        self.counterindicator = False
                        self.counterindicatorshort = False
                        self.shortdoble = deque(maxlen = 2)
                        ############################
                if len(self.stopshortdoble) > 0:
                    if self.stopshortdoble[-1].Status == OrderStatus.Filled:
                        self.Debug(str(self.Portfolio[self.ticker].Quantity))
                        self.Debug("Order Filled" + self.mymessage2)
                        openOrders = self.Transactions.GetOpenOrders()
                        if len(openOrders)> 0:
                            for x in openOrders:
                                self.Transactions.CancelOrder(x.Id)
                        self.limitshort = []
                        self.stopshort = []
                        self.stopshortdoble = []
                        self.stopshort75 = []
                        self.mo = []
                        self.indicatorshort = False
                        self.indicatornotstopshort = False
                        self.counterindicator = False
                        self.counterindicatorshort = False
                        self.shortdoble = deque(maxlen = 2)
                
                if len(self.stopshort75) > 0:
                    if self.stopshort75[-1].Status == OrderStatus.Filled:
                        self.Debug("Order Filled" + self.mymessage2)
                        openOrders = self.Transactions.GetOpenOrders()
                        if len(openOrders)> 0:
                            for x in openOrders:
                                self.Transactions.CancelOrder(x.Id)
                        self.limitshort = []
                        self.stopshort = []
                        self.stopshortdoble = []
                        self.stopshort75 = []
                        self.mo = []
                        self.indicatorshort = False
                        self.indicatornotstopshort = False
                        self.counterindicator = False
                        self.counterindicatorshort = False
                        self.shortdoble = deque(maxlen = 2)
                   
                if len(self.mo) > 0:
                    if self.mo[-1].Status == OrderStatus.Filled:
                        openOrders = self.Transactions.GetOpenOrders()
                        if len(openOrders)> 0:
                            for x in openOrders:
                                self.Transactions.CancelOrder(x.Id)
                    self.limitshort = []
                    self.stopshort = []
                    self.stopshortdoble = []
                    self.stopshort75 = []
                    self.limitlong = []
                    self.stoplong = []
                    self.stoplongdoble = []
                    self.stoplong75 = []
                    self.mo = []
                    self.indicatorshort = False
                    self.indicatornotstopshort = False
                    self.counterindicator = False
                    self.counterindicatorshort = False
                    self.indicatorlong = False
                    self.indicatornotstoplong = False
                    self.counterindicator = False
                    self.counterindicatorshort = False
                    self.shortdoble = deque(maxlen = 2)
                    self.Debug(" MMMMMMMMMODENA ")    
   
   

    def ThirtyMinuteBarHandler(self, sender, consolidated):
        '''This is our event handler for our 30 minute trade bar defined above in Initialize(). So each time the
        consolidator produces a new 30 minute bar, this function will be called automatically. The 'sender' parameter
         will be the instance of the IDataConsolidator that invoked the event, but you'll almost never need that!'''

        #self.Debug(str(consolidated.Close))
        #self.Debug(str(type(consolidated.Time.hour))) 
        
        myhour = consolidated.Time.hour
        myday = consolidated.Time.day
        myminute = consolidated.Time.minute
        if (myday != self.__last) and len(self.premarkethigh) > 0:
            self.premarkethigh = []
            self.premarketlow = []
        if ((myhour == 9 and myminute < 30) or (myhour < 9)) and (myday == self.__last or self.__last == 1):
            self.premarkethigh.append(consolidated.High)
            self.premarketlow.append(consolidated.Low)
        if myhour == 9 and myminute == 30:
            self.mymax = np.max(self.premarkethigh)
            self.mylow = np.min(self.premarketlow)
            
            #Open Long Position
            if consolidated.Open > self.mymax:
                #self.Debug(str(consolidated.Time) + " Open : " + str(consolidated.Open) +  " PremarketHigh: " + str(self.premarkethigh[-1]))
                if not self.Portfolio.Invested:
                    # when logged into IB as a Financial Advisor, this call will use order properties
                    # set in the DefaultOrderProperties property of QCAlgorithm
                    
                    close = consolidated.Close
                    self.myclose = close
                    self.stopPriceLong = self.mymax * 1.61 * 0.75 # Trigger stop limit when price falls
                    self.rangelong = self.mymax * 1.61 * self.almostlong
                    self.limitPriceLong = self.mymax * 1.61 * 0.95 # Sell equal or better than 1.61 > close
                    self.MarketOrder(self.ticker, self.quantity)
                    #self.SetHoldings(self.ticker, 1) # place market order
                    self.Debug("Placing Long Position, quantity: Quantity {} and Price {}".format(self.quantity, self.myclose))
                    limitlong = self.LimitOrder(self.ticker, -self.quantity, self.limitPriceLong)
                    self.limitlong.append(limitlong)
                    self.mymessage1 = " Take profit: Quantity {}, price {}".format(-self.quantity, self.limitPriceLong)
                    self.mo.append(self.StopMarketOrder(self.ticker, -self.quantity, self.mymax * 0.95))
                    self.comparator1 = self.mymax * 0.95
                   
                            
            if consolidated.Open < self.mylow:
                #self.Debug(str(consolidated.Time) + " Open : " + str(consolidated.Open) +  " PremarketLow: " + str(self.premarketlow[-1]))
                if not self.Portfolio.Invested:
                    # when logged into IB as a Financial Advisor, this call will use order properties
                    # set in the DefaultOrderProperties property of QCAlgorithm
                    close = consolidated.Close
                    self.myclose = close
                    self.stopPriceShort = close * (1 / 1.61) * 1.25 # Trigger stop limit when price Increase
                    self.rangeshort = close * (1 / 0.61) * self.almostshort
                    self.limitPriceShort = close * (1/ 1.61) * 1.05 # lower than 1 - 0.61 > close
                    self.MarketOrder(self.ticker, - self.quantity)
                    #self.SetHoldings(self.ticker, -1) # place market order
                    self.Debug("Placing Short Position, quantity: " + str(-self.quantity))   
                    limitshort = self.LimitOrder(self.ticker, self.quantity, self.limitPriceShort )
                    self.limitshort.append(limitshort)
                    self.mo.append(self.StopMarketOrder(self.ticker, self.quantity, self.mylow * 1.05))
                    
                    
        #Closing Positions
        #Filter Regular Trading Time
        #((Hour > 9:00 am) or (Hour > 9:30)) and Hour <= 4:00 PM
        """
        if myhour == 9 and myminute == 30:
            if self.Portfolio[self.ticker].Quantity > 0:
                self.mo = self.StopMarketOrder(self.ticker, -myquantity, self.myclose * 0.95)
            if self.Portfolio[self.ticker].Quantity < 0:
                self.mo = self.StopMarketOrder(self.ticker, -myquantity, self.myclose * 0.95)
        """
                
                

        if ((myhour > 10) or (myhour == 9 and myminute > 30)) and myhour <= 16:
        

            
            # Close Long Position        
            if self.Portfolio.Invested:
              
                #Check if we are long
                if self.Portfolio[self.ticker].Quantity > 0:
                    
                    #Get open orders
                    openOrders = self.Transactions.GetOpenOrders()
                    prices = []
                    if len(openOrders)> 0:
                        for x in openOrders:
                            prices.append(x.Price)
                    prices1 = list(set(prices))
                    self.Log((prices))
                    
                    #Get close price
                    close = self.Securities[self.ticker].Close
                    #Add data to deque to compare
                    self.longdoble.append(close)
                    
                    #Stop loss 
                    #Price is greather than 75% Rule, stop loss.
                    if close > self.stopPriceLong and not self.indicatorlong:
                        if len(self.stoplong75) == 0:
                            myset = list(set(prices).intersection(set([self.myclose * 0.95])))
                            self.Debug(str(myset) + " " + str(prices))
                            if len(myset) == 0:
                                self.indicatorlong = True
                                myquantity = self.quantity #self.Portfolio[self.ticker].Quantity
                                self.stoplong75.append(self.StopMarketOrder(self.ticker, -myquantity, self.myclose * 0.95))
                                self.mymessage2 = " Stop Loss (Price Reach 75%): Quantity {}, price {}".format(-myquantity, self.limitPriceLong)
                                self.Debug("Stop loss 75% " + str(len(self.stoplong75)))
                    #Price did not reach the 75% rule, and now is lower than the PM (line 203 to 207)
                    if close > self.myclose and self.indicatornotstoplong == False:
                        self.indicatornotstoplong = True
                    if close < self.mylow and self.indicatornotstoplong and not self.indicatorlong:
                        if len(self.stoplong) == 0:
                            stoplossorder = self.mymax * 0.95
                            myset = list(set(prices).intersection(set([stoplossorder])))
                            self.Debug(str(myset) + " " + str(prices))
                            if len(myset):
                                myquantity = self.quantity #self.Portfolio[self.ticker].Quantity
                                self.stoplong.append(self.StopMarketOrder(self.ticker, -myquantity, stoplossorder))
                                self.mymessage2 = " Stop Loss (Price Did Not Reach 75%): Quantity {}, price {}".format(-myquantity, stoplossorder)
                                self.Debug("Stop Loss Not 75% " + str(len(self.stoplong)))
                        self.indicatornotstoplong = "Done"
                    #The price cross two times the PM (From line 214-226)
                    if len(self.longdoble) > 1:
                        if (self.longdoble[0] > self.mylow) and (self.longdoble[-1] < self.mylow):
                            self.counter = self.counter + 1
                    #Do not do nothing if the price has crossed two times the PM

                    #Place stop market order
                    if self.counter == 2:
                        if len(self.stoplongdoble) == 0:
                            stoplossorder = self.mymax * 0.95
                            myset = list(set(prices).intersection(set([stoplossorder])))
                            self.Debug(str(myset) + " " + str(prices))
                            if len(myset):
                                myquantity = self.quantity #self.Portfolio[self.ticker].Quantity
                                self.stoplongdoble.append(self.StopMarketOrder(self.ticker, -myquantity, stoplossorder))
                                self.counter == 0
                                self.counterindicator = True #indicate price has crossed two time the entry price
                                self.mymessage2 = " Stop Loss (Price two time the entry price): Quantity {}, price {}".format(myquantity, stoplossorder)
                                self.Debug("Stop Loss 5% " + str(len(self.stoplongdoble)))


                #Short Postion
                #Check if we are short
                if self.Portfolio[self.ticker].Quantity < 0:
                    
                    #Get close price
                    close = self.Securities[self.ticker].Close
                    #Add data to deque to compare
                    self.shortdoble.append(close)
                    
                    #Stop loss 
                    #Price reach the 75% Rule, stop loss.
                    if close < self.stopPriceShort and not self.indicatorshort:
                        if len(self.stopshort75) == 0:
                            self.indicatorshort = True
                            myquantity = self.quantity #self.Portfolio[self.ticker].Quantity
                            self.stopshort75.append(self.StopMarketOrder(self.ticker, myquantity, self.myclose * 1.05))
                            self.mymessage2 = " Stop Loss (Price Reach 75%): Quantity {}, price {}".format(myquantity, self.limitPriceShort)
                    #Price did not reach the 75% rule, and now it is greather than the PM (line 250 to 255)
                    if close > self.myclose and self.indicatornotstopshort == False:
                        self.indicatornotstopshort = True
                    if close > self.mymax and self.indicatornotstopshort and not self.indicatorshort:
                        if len(self.stopshort) == 0:
                            stoplossorder = self.mymax * 1.05
                            myquantity = self.quantity #self.Portfolio[self.ticker].Quantity
                            self.stopshort.append(self.StopMarketOrder(self.ticker, myquantity, stoplossorder))
                            self.mymessage2 = " Stop Loss (Price Did Not Reach 75%): Quantity {}, price {}".format(myquantity, stoplossorder)
                            self.indicatornotstopshort = "Done"
                    #The price cross two times the PM (line 257-270)
                    if len(self.shortdoble) > 1:
                        if (self.shortdoble[0] < self.mymax) and (self.shortdoble[-1] > self.mymax):
                            self.countershort = self.countershort + 1
                    #Do not do nothing if the price has crossed two times the entry price
          
                    #Place stop market order
                    if self.countershort == 2:
                        if len(self.stopshortdoble) == 0:
                            stoplossorder = self.mymax * 1.05
                            myquantity = self.quantity #self.Portfolio[self.ticker].Quantity
                            self.stopshortdoble.append(self.StopMarketOrder(self.ticker, myquantity, stoplossorder))
                            self.countershort == 0
                            self.counterindicatorshort = True #indicate price has crossed two time the entry price
                            self.mymessage2 = " Stop Loss (Price cross two time the PM): Quantity {}, price {}".format(myquantity, stoplossorder)
                        

                        
        self.__last = myday
