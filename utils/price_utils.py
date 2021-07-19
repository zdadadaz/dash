import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint
import pandas as pd
from utils.draw import plot_price, plot_price_ind

def alpha(ticker):
    ts = TimeSeries(key='L8WFWPCEBY7C91J4', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=ticker,interval='1min', outputsize='full')
    pprint(data.head(2))

def yfinance(ticker):
    return yf.Ticker(ticker)
    # .info: 股票資訊
    # .history(start="2010-01-01",  end=”2020-07-21”): or .history(period='max')股價
    # period = "ytd", 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    # interval = "1m",1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    # https://pypi.org/project/yfinance/


def get_today_price(tickers, postfix):
    res = {'price':[],'change':[], 'percentage':[]}
    for t in tickers:
        a = yfinance(t+postfix)
        df = a.history(period='2d')
        res['price'].append(df.iloc[1,3])
        res['change'].append(df.iloc[1,3]-df.iloc[0,3])
        res['percentage'].append(round((df.iloc[1,3]-df.iloc[0,3])/df.iloc[0,3]*10)/10)
    return res

def get_year_price(tickers, postfix):
    res = {}
    for t in tickers:
        a = yfinance(t+postfix)
        df = a.history(period='ytd')
        res[t] = df
    return res

class Stock:
    def __init__(self, ticker, country): # TW or AX
        self.ticker = ticker
        self.sufix = '.' + country 
        self.dayInfo = {}
        self.yfticker = yfinance(ticker+self.sufix)
        # self._get_today_price()
        # self.yearInfo = self._get_ytd_price()
        
    def _get_today_price(self):
        df = self.yfticker.history(period='2d')
        try:
            self.dayInfo['price'] = df.iloc[1,3]
            self.dayInfo['change'] = df.iloc[1,3]-df.iloc[0,3]
            self.dayInfo['percentage'] = round((df.iloc[1,3]-df.iloc[0,3])/df.iloc[0,3]*10)/10
        except:
            self.dayInfo['price'] = 0
            self.dayInfo['change'] = 0
            self.dayInfo['percentage'] = 0

    def _get_ytd_price(self):
        return self.yfticker.history(period='ytd')
    
    def _get_price(self, interval, period):
        return self.yfticker.history(period=period, interval = interval)

class Stocks:
    def __init__(self, tickers, country):
        self.tickers = tickers
        self.stock_list = []
        for t in tickers:
            self.stock_list.append(Stock(t,country))

    def output_dayprice_all(self,df):
        tickers = set(list(df['ticker']))
        res = {'price':[],'change':[],'percentage':[]}
        for t in self.stock_list:
            if t.ticker in tickers:
                t._get_today_price()
                res['price'].append(t.dayInfo['price'])
                res['change'].append(t.dayInfo['change'])
                res['percentage'].append(t.dayInfo['percentage'])
        df["price"] = pd.Series(res['price'])
        df["change"] = pd.Series(res['change'])
        df["percentage"] = pd.Series(res['percentage'])
        df["gainloss"] = (df["price"]-df["bprice"])*df["unit"]
        return df

    def update_one_fig(self, ticker, interval='1d',period='ytd'):
        for idx,t in enumerate(self.stock_list):
            if str(self.tickers[idx]) == str(ticker):
                tmp = t._get_price(interval, period)
                # plot_price_ind(tmp, 'fig')
                return plot_price(tmp,'fig')
                

    def update_all_fig(self, interval='1d',period='ytd'):
        res = {}
        if interval == '30m':
            period = '60d'
        for idx,t in enumerate(self.stock_list):
            tmp = t._get_price(interval, period)
            res[self.tickers[idx]] = plot_price(tmp,'fig')
        return res

