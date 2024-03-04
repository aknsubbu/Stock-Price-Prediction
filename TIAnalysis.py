from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr

from TACalculation import TechnicalIndicators


ticker = TechnicalIndicators("IRCTC.NS")
ticker.populateFields()

# # list all the properties of the ticker object
print("Ticker News\n\n\n")
print(ticker.news)
print("\n\nTicker Recommendations\n\n\n")
print(ticker.recommendations)
print("\n\nTicker RSI\n\n\n")
print(ticker.rsi)
print("\n\nTicker Short Moving Avg\n\n\n")
print(ticker.short_mavg)
print("\n\nTicker Long Moving Avg\n\n\n")
print(ticker.long_mavg)
print("\n\nTicker Historical Mean\n\n\n")
print(ticker.historicalMeanVal)
print("\n\nTicker History\n\n\n")
print(ticker.history)
print("\n\nTicker Info\n\n\n")
print(ticker.info)
print("\n\n\n\n\n")


# def establishTrendDirection(ticker, required_ticks: int = 10):
#     def get_trend_direction():
#         return 1 if ticker.short_mavg.iloc[-1] > ticker.short_mavg.iloc[-2] else 0

#     def check_consistent_trend_direction(required_ticks):
#         direction = get_trend_direction()
#         consistent_ticks = 1

#         for i in range(-2, -required_ticks - 1, -1):  # Start from the last tick
#             if get_trend_direction() == direction:
#                 consistent_ticks += 1
#             else:
#                 break

#         return consistent_ticks >= required_ticks

#     # Example usage
#     trend_direction = get_trend_direction()
#     consistent_trend = check_consistent_trend_direction(required_ticks)

#     print(f"Trend Direction: {'Bullish' if trend_direction == 1 else 'Bearish'}")

#     if consistent_trend:
#         print(f"The trend has been consistently {'Bullish' if trend_direction == 1 else 'Bearish'} for at least {required_ticks} price ticks.")
#     else:
#         print(f"The trend is not consistent for the required number of ticks.")

#     return trend_direction


# def check_crossover_and_warning(self, required_ticks=150, percent_threshold=5):
#     crossover_warning = False
#     percent_threshold += 100
#     # Check for crossover
#     crossover_condition = self.history['Close'].iloc[-1] > percent_threshold * self.short_mavg.iloc[-1] and \
#                           self.history['Close'].iloc[-2] <= percent_threshold * self.short_mavg.iloc[-2]

#     if crossover_condition:
#         print("Crossover detected! Warning issued.")
#         crossover_warning = True

#     # Check if the price is consistently 5% above the moving average for the last x ticks
#     price_above_threshold = (self.history['Close'].iloc[-required_ticks:] > percent_threshold * self.short_mavg.iloc[-required_ticks:]).all()

#     if price_above_threshold:
#         print(f"The price has been consistently 5% above the moving average for the last {required_ticks} ticks. Warning issued.")
#         crossover_warning = True

#     return 1 if crossover_warning else 0


# crossover_warning = check_crossover_and_warning(ticker, required_ticks=150, percent_threshold=5)

# if not crossover_warning:
#     print("No crossovers or warnings detected.")


def check_volatility(
    self, required_ticks=1000, consistency_ticks=500, volatility_threshold=0.15
):
    high_volatility_warning = False

    # Calculate daily returns
    daily_returns = self.history["Close"].pct_change().dropna()

    # Calculate volatility
    volatility = daily_returns.rolling(window=required_ticks, min_periods=1).std()

    # Check if volatility stays above 15% for more than 500 out of 1000 ticks
    high_volatility_ticks = (volatility > volatility_threshold).sum()

    if high_volatility_ticks > consistency_ticks:
        print(
            f"Volatility has stayed above {volatility_threshold * 100}% for more than {consistency_ticks} out of {required_ticks} ticks. Warning issued."
        )
        high_volatility_warning = True

    return 1 if high_volatility_warning else 0


volatility_warning = check_volatility(
    ticker, required_ticks=1000, consistency_ticks=500, volatility_threshold=0.15
)

if not volatility_warning:
    print("No high volatility warnings detected.")


def establishTrendDirection(
    ticker, short_required_ticks: int = 10, long_required_ticks: int = 100
):
    def get_trend_direction():
        short_trend = (
            1 if ticker.short_mavg.iloc[-1] > ticker.short_mavg.iloc[-2] else 0
        )
        long_trend = 1 if ticker.long_mavg.iloc[-1] > ticker.long_mavg.iloc[-2] else 0
        return short_trend, long_trend

    def check_consistent_trend_direction(required_ticks, trend_values):
        consistent_ticks = 1

        for i in range(-2, -required_ticks - 1, -1):  # Start from the last tick
            if trend_values[i] == trend_values[i - 1]:
                consistent_ticks += 1
            else:
                break

        return consistent_ticks >= required_ticks

    short_trend, long_trend = get_trend_direction()
    short_consistent_trend = check_consistent_trend_direction(
        short_required_ticks, [short_trend, long_trend]
    )
    long_consistent_trend = check_consistent_trend_direction(
        long_required_ticks, [short_trend, long_trend]
    )

    print(f"Short-Term Trend Direction: {'Bullish' if short_trend == 1 else 'Bearish'}")
    print(f"Long-Term Trend Direction: {'Bullish' if long_trend == 1 else 'Bearish'}")

    if short_consistent_trend:
        print(
            f"The short-term trend has been consistently {'Bullish' if short_trend == 1 else 'Bearish'} for at least {short_required_ticks} price ticks."
        )
    else:
        print(
            f"The short-term trend is not consistent for the required number of ticks."
        )

    if long_consistent_trend:
        print(
            f"The long-term trend has been consistently {'Bullish' if long_trend == 1 else 'Bearish'} for at least {long_required_ticks} price ticks."
        )
    else:
        print(
            f"The long-term trend is not consistent for the required number of ticks."
        )

    return short_trend, long_trend


def check_crossover_and_warning(
    self, short_required_ticks=150, long_required_ticks=500, percent_threshold=5
):
    crossover_warning = False
    percent_threshold += 100

    short_crossover_condition = (
        self.history["Close"].iloc[-1] > percent_threshold * self.short_mavg.iloc[-1]
        and self.history["Close"].iloc[-2]
        <= percent_threshold * self.short_mavg.iloc[-2]
    )

    long_crossover_condition = (
        self.history["Close"].iloc[-1] > percent_threshold * self.long_mavg.iloc[-1]
        and self.history["Close"].iloc[-2]
        <= percent_threshold * self.long_mavg.iloc[-2]
    )

    if short_crossover_condition or long_crossover_condition:
        print("Crossover detected! Warning issued.")
        crossover_warning = True

    # Check if the price is consistently 5% above the moving average for the last x ticks for both short and long-term
    short_price_above_threshold = (
        self.history["Close"].iloc[-short_required_ticks:]
        > percent_threshold * self.short_mavg.iloc[-short_required_ticks:]
    ).all()
    long_price_above_threshold = (
        self.history["Close"].iloc[-long_required_ticks:]
        > percent_threshold * self.long_mavg.iloc[-long_required_ticks:]
    ).all()

    if short_price_above_threshold or long_price_above_threshold:
        print(
            f"The price has been consistently 5% above the moving average for the last {short_required_ticks} ticks (short-term). Warning issued."
        )
        print(
            f"The price has been consistently 5% above the moving average for the last {long_required_ticks} ticks (long-term). Warning issued."
        )
        crossover_warning = True

    return 1 if crossover_warning else 0


crossover_warning = check_crossover_and_warning(
    ticker, short_required_ticks=150, long_required_ticks=500, percent_threshold=5
)

if not crossover_warning:
    print("No crossovers or warnings detected.")


def predict_based_on_rsi(self, overbought_threshold=70, oversold_threshold=30):
    rsi_prediction = 0  # Default to a potential decrease

    current_rsi = self.rsi.iloc[-1]

    if current_rsi < oversold_threshold:
        print(
            f"RSI is below {oversold_threshold} (oversold region). Potential increase is likely. RSI: {current_rsi}"
        )
        rsi_prediction = 1

    elif current_rsi > overbought_threshold:
        print(
            f"RSI is above {overbought_threshold} (overbought region). Potential decrease is likely. RSI: {current_rsi}"
        )
        rsi_prediction = 0

    else:
        print(
            f"RSI is between {oversold_threshold} and {overbought_threshold}. No clear signal. RSI: {current_rsi}"
        )

    return rsi_prediction


# Example usage
rsi_prediction = predict_based_on_rsi(
    ticker, overbought_threshold=70, oversold_threshold=30
)

if rsi_prediction:
    print("RSI suggests a potential increase.")
else:
    print("RSI suggests a potential decrease.")


def make_cumulative_prediction(
    short_trend, long_trend, crossover_warning, volatility_warning, rsi_prediction
):

    cumulative_prediction = (
        short_trend
        + long_trend
        + crossover_warning
        + volatility_warning
        + rsi_prediction
    ) >= 3

    if cumulative_prediction:
        print("Cumulative Prediction: Potential Increase")
    else:
        print("Cumulative Prediction: Potential Decrease")

    return cumulative_prediction


# short_trend, long_trend = establishTrendDirection(ticker, short_required_ticks=10, long_required_ticks=100)
# crossover_warning = check_crossover_and_warning(ticker, short_required_ticks=150, long_required_ticks=500, percent_threshold=5)
# volatility_warning = check_volatility(ticker, required_ticks=1000, consistency_ticks=500, volatility_threshold=0.15)
# rsi_prediction = predict_based_on_rsi(ticker, overbought_threshold=70, oversold_threshold=30)

# cumulative_prediction = make_cumulative_prediction(short_trend, long_trend, crossover_warning, volatility_warning, rsi_prediction)
