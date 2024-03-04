from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr

yf.pdr_override()  # Activate yfinance's pdr_override


class TechnicalIndicators:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.history = None
        self.recommendations = None
        self.news = None
        self.rsi = None
        self.short_mavg = None
        self.long_mavg = None
        self.mean_value = None

    def featureExtract(self):
        # Use pandas_datareader to get historical data
        now = datetime.now()
        nowDate = datetime.now().strftime("%Y-%m-%d")
        threeMonthsAgo = datetime.now() - timedelta(days=100)
        threeMonthsAgoDate = threeMonthsAgo.strftime("%Y-%m-%d")

        self.history = pdr.get_data_yahoo(
            self.symbol, start=threeMonthsAgoDate, end=nowDate
        )
        self.recommendations = self.ticker.recommendations
        self.news = self.ticker.news
        self.info = self.ticker.info

    def NewsFilter(self):
        filteredNews = []
        for i in self.news:
            title = i["title"]
            date = i["providerPublishTime"]
            dateFinal = datetime.utcfromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")
            filteredNews.append([title, dateFinal])

        self.news = filteredNews


# !TODO Check why this is throwing an error
    # def InfoFilter(self):
    #     info = self.info
    #     fields_of_interest = [
    #         "auditRisk",
    #         "boardRisk",
    #         "compensationRisk",
    #         "shareHolderRightsRisk",
    #         "overallRisk",
    #         "governanceEpochDate",
    #         "compensationAsOfEpochDate",
    #         "maxAge",
    #         "priceHint",
    #         "previousClose",
    #         "open",
    #         "dayLow",
    #         "dayHigh",
    #         "regularMarketPreviousClose",
    #         "regularMarketOpen",
    #         "regularMarketDayLow",
    #         "regularMarketDayHigh",
    #         "dividendRate",
    #         "dividendYield",
    #         "exDividendDate",
    #         "payoutRatio",
    #         "fiveYearAvgDividendYield",
    #         "beta",
    #         "trailingPE",
    #         "forwardPE",
    #         "volume",
    #         "regularMarketVolume",
    #         "averageVolume",
    #         "averageVolume10days",
    #         "averageDailyVolume10Day",
    #         "bidSize",
    #         "askSize",
    #         "marketCap",
    #         "fiftyTwoWeekLow",
    #         "fiftyTwoWeekHigh",
    #         "priceToSalesTrailing12Months",
    #         "fiftyDayAverage",
    #         "twoHundredDayAverage",
    #         "trailingAnnualDividendRate",
    #         "trailingAnnualDividendYield",
    #         "currency",
    #         "enterpriseValue",
    #         "profitMargins",
    #         "floatShares",
    #         "sharesOutstanding",
    #         "sharesShort",
    #         "sharesShortPriorMonth",
    #         "sharesShortPreviousMonthDate",
    #         "dateShortInterest",
    #         "sharesPercentSharesOut",
    #         "heldPercentInstitutions",
    #         "shortRatio",
    #         "impliedSharesOutstanding",
    #         "bookValue",
    #         "priceToBook",
    #         "lastFiscalYearEnd",
    #         "nextFiscalYearEnd",
    #         "mostRecentQuarter",
    #         "earningsQuarterlyGrowth",
    #         "netIncomeToCommon",
    #         "trailingEps",
    #         "forwardEps",
    #         "pegRatio",
    #         "lastSplitFactor",
    #         "lastSplitDate",
    #         "enterpriseToRevenue",
    #         "enterpriseToEbitda",
    #         "52WeekChange",
    #         "SandP52WeekChange",
    #         "lastDividendValue",
    #         "lastDividendDate",
    #         "exchange",
    #         "quoteType",
    #         "symbol",
    #         "underlyingSymbol",
    #         "shortName",
    #         "longName",
    #         "firstTradeDateEpochUtc",
    #         "timeZoneFullName",
    #         "timeZoneShortName",
    #         "uuid",
    #         "messageBoardId",
    #         "gmtOffSetMilliseconds",
    #         "currentPrice",
    #         "targetHighPrice",
    #         "targetLowPrice",
    #         "targetMeanPrice",
    #         "targetMedianPrice",
    #         "recommendationMean",
    #         "recommendationKey",
    #         "numberOfAnalystOpinions",
    #         "totalCash",
    #         "totalCashPerShare",
    #         "ebitda",
    #         "totalDebt",
    #         "quickRatio",
    #         "currentRatio",
    #         "totalRevenue",
    #         "debtToEquity",
    #         "revenuePerShare",
    #         "returnOnAssets",
    #         "returnOnEquity",
    #         "freeCashflow",
    #         "operatingCashflow",
    #         "earningsGrowth",
    #         "revenueGrowth",
    #         "grossMargins",
    #         "ebitdaMargins",
    #         "operatingMargins",
    #         "financialCurrency",
    #         "trailingPegRatio",
    #     ]

    #     infoVals = {}
    #     for field in fields_of_interest:
    #         infoVals[field] = info[field]
    #     self.info = infoVals

    def TACalculation(self):
        if "Close" not in self.history.columns:
            print("Error: 'Close' column not found in historical data.")
            return

        # Calculate RSI
        delta = self.history["Close"].diff()
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        period = 14
        avg_gain = gains.rolling(window=period, min_periods=1).mean()
        avg_loss = losses.rolling(window=period, min_periods=1).mean()
        rs = avg_gain / avg_loss
        self.rsi = 100 - (100 / (1 + rs))

        # Calculate Moving Averages
        short_window = 50
        long_window = 200
        self.short_mavg = (
            self.history["Close"].rolling(window=short_window, min_periods=1).mean()
        )
        self.long_mavg = (
            self.history["Close"].rolling(window=long_window, min_periods=1).mean()
        )

        print("\n\nTechnical analysis calculations completed.\n\n\n")

    def historicalMean(self):
        if "Close" not in self.history.columns:
            print("Error: 'Close' column not found in historical data.")
            return

        # Calculate Historical Mean
        self.historicalMeanSeries = self.history["Close"].expanding().mean()
        self.historicalMeanVal = self.historicalMeanSeries.iloc[-1]

    def populateFields(self):
        self.featureExtract()
        self.historicalMean()
        self.TACalculation()
        self.NewsFilter()
        # self.InfoFilter()


# # Example usage
# stockSym = TechnicalIndicators("IRCTC.NS")
# stockSym.featureExtract()
# stockSym.TACalculation()
# stockSym.historicalMean()

# print("RSI Values \n")
# print(stockSym.rsi)
# print("Short Moving Avg \n")
# print(stockSym.short_mavg)
# print("Long Moving Avg \n")
# print(stockSym.long_mavg)
# print("Mean Value \n")
# print(stockSym.mean_value)
# print("Historical Mean \n")
# print(stockSym.historicalMeanVal)

