from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 
from alpaca_trade_api import REST 
from timedelta import Timedelta 
from finbert_utils import estimate_sentiment
import pandas as pd
from dotenv import load_dotenv
import os 

load_dotenv()


API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL= "https://paper-api.alpaca.markets"

ALPACA_CREDS={
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True
}

class Trading (Strategy) :
    def initialize(self,symbol:str="SPY",risk_percent:float=.5):
        self.symbol = symbol
        self.sleeptime = "1H"
        self.last_trade = None
        self.risk_percent = risk_percent
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

    def analysis(self):
        cash = self.get_cash()
        last_price = self.get_last_prices(self.symbol)
        history = self.get_historical_data(self.symbol,6,'months')
        short_mavg = history['close'].rolling(window=20).mean()
        long_mavg = history['close'].rolling(window=50).mean()
        rsi = self.get_rsi(history)
        return cash, last_price, short_mavg, long_mavg, rsi
    


#testing
start_date = datetime(2020,1,1)
end_date = datetime(2023,12,31) 
broker = Alpaca(ALPACA_CREDS)   
stock = Trading(name='mlstrat', broker=broker, 
                    parameters={"symbol":"SPY", 
                                "cash_at_risk":.5})
stock.initialize()
print(stock.analysis())