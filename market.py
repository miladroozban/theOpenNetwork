from dataclasses import replace

import ccxt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
from datetime import datetime
from database import mongodb  #database
from sklearn.preprocessing import StandardScaler
from scipy import stats
import os
# import tft_torch


#  defining scale methode
scale = StandardScaler()

# defining exchange
exchange = ccxt.binance()

# Define the symbol and timeframe
symbol = 'BTC/USDT'
timeframe = '1h'
candles_limit = 24
fetch_date = datetime.today()

def timestamp_to_year(timestamp):
    time_object = datetime.fromtimestamp(timestamp / 1000)
    return time_object.year


# Fetch historical candle data
ohlcv_data = exchange.fetch_ohlcv(symbol, timeframe, limit=candles_limit)
# data framing by pandas
data_frame = pd.DataFrame(ohlcv_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
data_frame["date"] = pd.to_datetime(data_frame["timestamp"], unit='ms')
data_frame["year"] = data_frame["timestamp"].apply(timestamp_to_year)

scaling = data_frame[["volume"]]
scaled_volume = StandardScaler().fit_transform(scaling)

candle_data = pd.DataFrame(data_frame, columns=['date', 'year', 'month', 'open', 'high', 'low', 'close', 'volume'])

timestamp_date = np.array([newDate[0] for newDate in ohlcv_data])
date = np.array(candle_data['date'])
year_of_date = np.array(candle_data['year'])

# converting to Array for calculation by models
candle_open = np.array(candle_data["open"])  #O
candle_high = np.array(candle_data["high"])  #H
candle_low = np.array(candle_data["low"])  #L
candle_close = np.array(candle_data["close"])  #C
candle_volume = np.array(candle_data["volume"])  #V

candle_data_list = [candle_open, candle_high, candle_low, candle_close, candle_volume]
for x in range(len(candle_data_list)):
    candle_data_list[x] = candle_data_list[x].tolist()

# updating database
database_update = 0
if database_update == 1:
    mongodb(
        fetch_date,
        symbol,
        timeframe,
        date.tolist(),
        candle_data_list[0],
        candle_data_list[1],
        candle_data_list[2],
        candle_data_list[3],
        candle_data_list[4])
else:
    print(" Database was already updated")


# calculation of standard deviation and (mean,median,mode) value with these functions

def calc_std(data_list):
    return [float(np.std(data)) for data in data_list]


def mean(candle_close_data):
    return float(np.mean(candle_close_data))


def median(candle_close_data):
    return float(np.median(candle_close_data))


def mode(candle_close_data):
    return stats.mode(candle_close_data)[0]


# applying data to functions
dataset_std = calc_std(candle_data_list)
candle_close_mean = mean(candle_close)
candle_close_median = median(candle_close)
candle_close_mode = mode(candle_close)

mean_median_mode_dict = {
    "mean": candle_close_mean,
    "median": candle_close_median,
    "mode": candle_close_mode
}

candles_dataset_dict = {
    "open": dataset_std[0],
    "high": dataset_std[1],
    "low": dataset_std[2],
    "close": dataset_std[3],
    "volume": dataset_std[4]
}

# print result
for x in candles_dataset_dict:
    print(f" {x} std: {candles_dataset_dict[x]}")
for x in mean_median_mode_dict:
    print(f" {x} value: {mean_median_mode_dict[x]}")

# figures directory
project_root = os.path.dirname(os.path.abspath(__file__))
figures_dir = os.path.join(project_root, 'figures')



def figur_path(input_title):
    fetch_date_str = fetch_date.today().strftime('%Y-%m-%d')
    path = f"{figures_dir}\\{input_title}-{fetch_date_str}.png"
    corrected_path = path.replace(" ", "-")
    return corrected_path




plt.figure(1, figsize=(10, 6)).set_facecolor('lightgrey')
title = "Price changes"
plt.title(title)
plt.xlabel("Date")
plt.ylabel("Price")
plt.scatter( date, candle_low)
plt.scatter( date, candle_high)
plt.scatter( date, candle_close)
plt.plot(date, candle_close)
plt.savefig(figur_path("PriceChanges"),dpi=400)
plt.show()


plt.figure(2, figsize=(10, 6)).set_facecolor('lightgrey')
plt.title("Volume changes")
plt.xlabel("Date")
plt.ylabel("Volume")
plt.scatter( date, candle_volume)
plt.plot(date,candle_volume)
plt.savefig(figur_path("VolumeChanges"),dpi=400)
plt.show()


plt.figure(3, figsize=(10, 6)).set_facecolor('lightgrey')
plt.title("Volume and Price Comparison")
plt.xlabel("Volume")
plt.ylabel("Price")
plt.scatter(candle_volume,candle_close )
plt.savefig(figur_path("VolumeAndPrice"),dpi=400)
plt.show()


# plt.plot(close_line, poly_model(close_line))
