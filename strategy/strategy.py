# Import the core module
import math
import cashAlgoAPI

# Declare and implement a class: Strategy 
class Strategy:

    #Initialize Strategy 
    def init(self):
        self.cnt = 0
        self.current_date = 0
        self.stock_code_x = self.config.get("MarketData","ProductCode_1")
        self.stock_code_y = self.config.get("MarketData","ProductCode_2")
        self.initialCapital = float(self.config.get("Risk","InitialCapital"))
        self.current_data_x = cashAlgoAPI.MarketData([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) 
        self.current_data_y = cashAlgoAPI.MarketData([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) 
        #self.delta = abs(math.log(float(self.config.get("Strategy","Delta")), math.e))
        self.delta = abs(float(self.config.get("Strategy", "Delta")))
        self.gamma = float(self.config.get("Strategy", "Gamma"))
        #self.mu    = float(self.config.get("Strategy", "Mu"))
        self.std = float(self.config.get("Strategy", "std"))
        self.mean   = float(self.config.get("Strategy", "mean"))
        self.mins   = int(self.config.get("Strategy", "SmaDays"))
        self.sma_mins   = int(self.config.get("Strategy", "Sma"))
        self.close = float(self.config.get("Strategy", "close"))
        self.cut_loss = float(self.config.get("Strategy", "CutLoss"))
        self.list = []
        self.sma = []
        self.signal = 0
        self.y_price_ln_predict = 0.0
        self.volume_hold_x = 0
        self.volume_hold_y = 0
        self.position_x = 0
        self.position_y = 0
        
        return

    #Process Market Data.
    def onMarketDataUpdate(self,market, code, md):
        return
        
    def doTrading():
        return
         
    #Used in OHLC mode.
    def onOHLCFeed(self,of):
    
        # transfer data
        md=cashAlgoAPI.MarketData([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) 
        md.timestamp   = of.timestamp
        md.market      = of.market
        md.productCode = str(of.productCode)
        md.lastPrice   = of.close
        md.askPrice1   = of.close
        md.bidPrice1   = of.close
       	#md.lastVolume  = 1
       
           
        #Get daily price
        if( md.timestamp[9:15]=="160000"):
            
            # when receive a stock x data, do:
            #   1. store current_data_x
            #   2. predict theoretical price of stock y, ln(PriceY_t) = Gamma*ln(PriceX_t) + Mu
            #   3. wait next stock y data
        
            if(md.productCode == self.stock_code_x):
                #print "receive a x"
                self.current_data_x = md
               # self.y_price_ln_predict = self.gamma * math.log(self.current_data_x.lastPrice, math.e) + self.mu
                self.y_price_ln_predict = self.gamma * math.log(self.current_data_x.lastPrice, math.e) 
                return

            # when receive a stock y data, do:
            #   1. store current_data_y
            #   2. check strategy status: 
            #       1) standing by to trade
            #          a. check if could do trading [y_price_ln_diff >= delta or <= -delta]
            #          b. if could, do trade
            #       2) waiting to clear
            #          a. check if two stocks match
            #          b. if matching, do clearing
            if(md.productCode == self.stock_code_y):
                #print "receive a y"
                self.current_data_y = md
                
                y_price_ln_actual = math.log(float(self.current_data_y.lastPrice), math.e)
                #y_price_ln_diff   = y_price_ln_actual - self.y_price_ln_predict
               
                diff = y_price_ln_actual - self.y_price_ln_predict
                print(diff)
                y_price_ln_diff = (diff - self.mean)/self.std
                print(y_price_ln_diff)
                #moving window of price diff

                #self.movingWindow(self.list, self.mins, diff)
                
                if(self.mins==0):
                    self.list.pop(0)
                else:
                    self.mins=self.mins - 1           
                self.list.append(y_price_ln_diff )
        
                avr = sum(self.list)/len(self.list)
                #self.movingWindow1(self.sma, self.sma_mins, avr)
                if(self.sma_mins==0):
                    self.sma.pop(0)
                else:
                    self.sma_mins=self.sma_mins - 1           
                self.sma.append(avr)
                
                if(len(self.sma)>1):
                    if((self.sma[1]-self.sma[0])*y_price_ln_diff<0):
                        self.signal = 1
                
                #if(md.timestamp[9:13] == "0930"): print y_price_ln_diff
                if(self.position_x == 0 and  self.position_y == 0):
                    #print "check if could trade"
                    if(y_price_ln_diff >= self.delta and self.signal == 1):
                        print md.timestamp, y_price_ln_diff, "do trade long x, short y."
                        self.cnt+=1
                        self.volume_hold_y = self.initialCapital/self.current_data_y.lastPrice
                        self.volume_hold_x = self.initialCapital*self.gamma/self.current_data_x.lastPrice
                        self.position_y = -1
                        self.position_x = 1
                        order1 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_y, str(self.cnt), self.current_data_y.lastPrice, self.volume_hold_y, "open", 2, "insert", "market_order", "today")
                        self.cnt+=1
                        order2 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_x, str(self.cnt), self.current_data_x.lastPrice, self.volume_hold_x, "open", 1, "insert", "market_order", "today")
                        self.mgr.insertOrder(order1)
                        self.mgr.insertOrder(order2)
                    elif(y_price_ln_diff <= -self.delta and self.signal ==1):
                        print md.timestamp, y_price_ln_diff, "do trade short x, long y."
                        self.cnt+=1
                        self.volume_hold_y = self.initialCapital/self.current_data_y.lastPrice
                        self.volume_hold_x = self.initialCapital*self.gamma/self.current_data_x.lastPrice
                        self.position_y = 1
                        self.position_x = -1
                        order1 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_y, str(self.cnt), self.current_data_y.lastPrice, self.volume_hold_y, "open", 1, "insert", "market_order", "today")
                        self.cnt+=1
                        order2 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_x, str(self.cnt), self.current_data_x.lastPrice, self.volume_hold_x, "open", 2, "insert", "market_order", "today")
                        self.mgr.insertOrder(order1)
                        self.mgr.insertOrder(order2)
                    else: return
                else:
                    #cut loss
                    if(self.position_x ==1 and y_price_ln_diff >= self.cut_loss):
                         print md.timestamp, y_price_ln_diff, "do clear."
                         self.cnt+=1
                         self.position_y = 0
                         self.position_x = 0
                         order1 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_y, str(self.cnt), self.current_data_y.lastPrice, self.volume_hold_y, "open", 1, "insert", "market_order", "today")
                         self.cnt+=1
                         order2 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_x, str(self.cnt), self.current_data_x.lastPrice, self.volume_hold_x, "open", 2, "insert", "market_order", "today")
                         self.mgr.insertOrder(order1)
                         self.mgr.insertOrder(order2)
                    #close win  
                    if(self.position_x ==1 and y_price_ln_diff <=self.close):
                        print md.timestamp, y_price_ln_diff, "do clear."
                        self.cnt+=1
                        self.position_y = 0
                        self.position_x = 0
                        order1 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_y, str(self.cnt), self.current_data_y.lastPrice, self.volume_hold_y, "open", 1, "insert", "market_order", "today")
                        self.cnt+=1
                        order2 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_x, str(self.cnt), self.current_data_x.lastPrice, self.volume_hold_x, "open", 2, "insert", "market_order", "today")
                        self.mgr.insertOrder(order1)
                        self.mgr.insertOrder(order2)
                     #cut loss
                    if(self.position_x == -1 and y_price_ln_diff <= self.cut_loss*-1):
                        print md.timestamp, y_price_ln_diff, "do clear."
                        self.cnt+=1
                        self.position_y = 0
                        self.position_x = 0
                        order1 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_y, str(self.cnt), self.current_data_y.lastPrice, self.volume_hold_y, "open", 2, "insert", "market_order", "today")
                        self.cnt+=1
                        order2 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_x, str(self.cnt), self.current_data_x.lastPrice, self.volume_hold_x, "open", 1, "insert", "market_order", "today")
                        self.mgr.insertOrder(order1)
                        self.mgr.insertOrder(order2)
                    if(self.position_x == -1 and y_price_ln_diff >= self.close*-1):
                        print md.timestamp, y_price_ln_diff, "do clear."
                        self.cnt+=1
                        self.position_y = 0
                        self.position_x = 0
                        order1 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_y, str(self.cnt), self.current_data_y.lastPrice, self.volume_hold_y, "open", 2, "insert", "market_order", "today")
                        self.cnt+=1
                        order2 = cashAlgoAPI.Order(md.timestamp, "SEHK", self.stock_code_x, str(self.cnt), self.current_data_x.lastPrice, self.volume_hold_x, "open", 1, "insert", "market_order", "today")
                        self.mgr.insertOrder(order1)
                        self.mgr.insertOrder(order2)
                    else: return
                        
        '''
        # Open Long Position
        if md.lastPrice>=max(self.list) and self.range>=self.minrange and self.range<=self.maxrange and self.position==0 and not max(self.list)==999999 and not md.timestamp[9:11]=="16":
            order = cashAlgoAPI.Order(md.timestamp, "HKFE", md.productCode, str(self.cnt), md.askPrice1, 1, "open", 1, "insert", "market_order", "today")
            self.mgr.insertOrder(order)
            print "Place an BUY order at %s" %md.timestamp + "Price at %s" %md.askPrice1 
            self.cnt+=1
            self.position=1
            self.target=self.range
            self.openPrice=md.askPrice1
            
        # Open Short Position
        if md.lastPrice<=min(self.list) and self.range>=self.minrange and self.range<=self.maxrange and self.position==0 and not max(self.list)==999999 and not md.timestamp[9:11]=="16":
            order = cashAlgoAPI.Order(md.timestamp, "HKFE", md.productCode, str(self.cnt), md.bidPrice1, 1, "open", 2, "insert", "market_order", "today")
            self.mgr.insertOrder(order)
            print "Place an SELL order at %s" %md.timestamp + "Price at %s" %md.bidPrice1 
            self.cnt+=1
            self.position=-1
            self.target=self.range
            self.openPrice=md.bidPrice1
            
        # Win close position (Long)
        if self.position==1 and md.lastPrice>=(self.openPrice+self.target):
            order = cashAlgoAPI.Order(md.timestamp, "HKFE", md.productCode, str(self.cnt), md.bidPrice1, 1, "open", 2, "insert", "market_order", "today")
            self.mgr.insertOrder(order)
            print "Place an SELL order at %s" %md.timestamp + "Price at %s, (Win)" %md.bidPrice1 
            self.cnt+=1
            self.position=0
            
        # Win close position (Short)
        if self.position==-1 and md.lastPrice<=(self.openPrice-self.target):
            order = cashAlgoAPI.Order(md.timestamp, "HKFE", md.productCode, str(self.cnt), md.askPrice1, 1, "open", 1, "insert", "market_order", "today")
            self.mgr.insertOrder(order)
            print "Place an BUY order at %s" %md.timestamp + "Price at %s, (Win)" %md.askPrice1 
            self.cnt+=1
            self.position=0
            
        # Cut loss position (Long)
        if self.position==1 and md.lastPrice<=min(self.list):
            order = cashAlgoAPI.Order(md.timestamp, "HKFE", md.productCode, str(self.cnt), md.bidPrice1, 1, "open", 2, "insert", "market_order", "today")
            self.mgr.insertOrder(order)
            print "Place an SELL order at %s" %md.timestamp + "Price at %s, (Cut)" %md.bidPrice1
            self.cnt+=1
            self.position=0
            
        # Cut loss position (Short)
        if self.position==-1 and md.lastPrice>=max(self.list):
            order = cashAlgoAPI.Order(md.timestamp, "HKFE", md.productCode, str(self.cnt), md.askPrice1, 1, "open", 1, "insert", "market_order", "today")
            self.mgr.insertOrder(order)
            print "Place an BUY order at %s" %md.timestamp + "Price at %s, (Cut)" %md.askPrice1
            self.cnt+=1 
            self.position=0
            
        # Dayend cut (Long)
        if self.position==1 and md.timestamp[9:13]=="1614":
            order = cashAlgoAPI.Order(md.timestamp, "HKFE", md.productCode, str(self.cnt), md.bidPrice1, 1, "open", 2, "insert", "market_order", "today")
            self.mgr.insertOrder(order)
            print "Place an SELL order at %s" %md.timestamp + "Price at %s, (Dayend Cut)" %md.bidPrice1
            self.cnt+=1
            self.position=0 
            
        # Dayend cut (Short)
        if self.position==-1 and md.timestamp[9:13]=="1614":
            order = cashAlgoAPI.Order(md.timestamp, "HKFE", md.productCode, str(self.cnt), md.askPrice1, 1, "open", 1, "insert", "market_order", "today")
            self.mgr.insertOrder(order)
            print "Place an BUY order at %s" %md.timestamp + "Price at %s, (Dayend Cut)" %md.askPrice1
            self.cnt+=1 
            self.position=0
        '''
        
        return
    '''
    def movingWindow1(list,range,price):
        if(range==0):
            list.pop(0)
        else:
            range=range - 1           
        list.append(price)
        return
    '''
    #Process Order
    def onOrderFeed(self,of):
        return

    #Process Trade
    def onTradeFeed(self,tf):
        return

    #Process Position
    def onPortfolioFeed(self,portfolioFeed):
        return

    #Process PnL
    def onPnlperffeed(self,pf):
        return