
import ccxt
import pandas as pd
import time
import os

#handle root data
dataset_name = "dataset.csv"
script_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(project_path,'dataset', dataset_name)

# defining settings
exchange = ccxt.kucoin()
symbols = ['TON/USDT','BTC/USDT','ETH/USDT']
timeframe = '1m'
since_date = 1666902600000
candles_limit = 1440
sleep_time = 1
columns = ["timestamp", "open", "high", "low", "close", "volume"]
daily_candles_limit = 10  # number of candles from 27 oct 2022 to 2 feb 2022 equals : 829




def volume_correction (symbol_dataframe):
    symbol_dataframe = symbol_dataframe["volume"].tolist()
    for i in range(len(symbol_dataframe)):
        symbol_dataframe[i] = str(symbol_dataframe[i]).replace('.', '')
    return symbol_dataframe
def fetch_candle_data(symbol, timeframe_data, since, limit, daily_candles):
    candle_data = []
    try:
        for x in range(daily_candles):
            data = exchange.fetch_ohlcv(symbol, timeframe_data, since=since, limit=limit)
            candle_data.extend(data)
            print(f" {len(candle_data)} candles data from {daily_candles * candles_limit} in {symbol} market fetched")
            since += (candles_limit * 60000)  # converting minutes to milliseconds / formula : minutes * 60000
            time.sleep(sleep_time)

    except ccxt.NetworkError as e:
        print(f"Network error for {symbol} : ", e)
        raise
    except ccxt.ExchangeError as e:
        print(f"Exchange error for {symbol} : ", e)
        raise
    return candle_data
def save_to_csv(data, path, symbol):
    try:
        data.to_csv(path, index=False)
    except OSError as e:
        print(f"{e} , if you've opened {path}, please close and try again")
        raise
def dataset_creator():
    dataset = None

    for symbol in symbols:
        print(f"Fetching data for {symbol}...")
        candle_data = fetch_candle_data(symbol, timeframe, since_date, candles_limit, daily_candles_limit)
        df = pd.DataFrame(candle_data, columns=["timestamp", "open", "high", "low", "close", "volume"])

        if "timeframe" in df.columns:
            df["timeframe"] = timeframe
        else:
            df.insert(1, "timeframe", timeframe)



        if dataset is None:
            dataset = df.rename(columns={
                "open": f"{symbol.split('/')[0].lower()}_open",
                "high": f"{symbol.split('/')[0].lower()}_high",
                "low": f"{symbol.split('/')[0].lower()}_low",
                "close": f"{symbol.split('/')[0].lower()}_close",
                "volume": f"{symbol.split('/')[0].lower()}_volume"
            })


            save_to_csv(dataset, dataset_path, symbol)
            print(f"{symbol} has been saved to {dataset_name}")
        else:

            for col in ["open", "high", "low", "close", "volume"]:

                dataset[f"{symbol.split('/')[0].lower()}_{col}"] = df[col]
                save_to_csv(dataset, dataset_path, symbol)
        print(f"{symbol} has been saved to {dataset_name}")
    return print("ALL data has been saved")
def arrange_dataset():
    try:
        with open(dataset_path, 'r') as f:
            dataset = pd.read_csv(f)
            # dataset.set_index('timestamp', inplace=True)
            new_order = [
                'timestamp', 'timeframe',
                'ton_open', 'btc_open', 'eth_open',
                'ton_high', 'btc_high', 'eth_high',
                'ton_low', 'btc_low', 'eth_low',
                'ton_close', 'btc_close', 'eth_close',
                'ton_volume', 'btc_volume', 'eth_volume']
            dataset = dataset[new_order]
            dataset.to_csv(dataset_path, index=False)
        print("dataset has been arranged")
    except FileNotFoundError as e:
        print(e)
        raise

    except OSError as e:
        print(f"{e} , if you've opened dataset file, please close and try again")
        raise


dataset_creator()
arrange_dataset()




