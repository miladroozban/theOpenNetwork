
import ccxt
import pandas as pd
import time
import os

class FetchData:
    def __init__(self,exchange,symbols,timeframe,since_date,candles_limit,sleep_time,daily_candles_limit,rate,columns):

        self.exchange = exchange
        self.symbol = symbols
        self.timeframe = timeframe
        self.since = since_date
        self.limit = candles_limit
        self.sleep_time = sleep_time
        self.iteration = daily_candles_limit
        self.rate = rate
        self.columns = columns

    def run(self):
        self.fetch()
        project_path = os.path.dirname(os.path.abspath(__file__))
        dataset_dir = os.path.join(project_path, 'dataset')
        output_path = os.path.join(dataset_dir, 'merged_dataset.csv')
        csv_files = [f for f in os.listdir(dataset_dir) if f.endswith('.csv')]


        # Merge data
        first_csv = None
        for file in csv_files:
            print(f"{file} merging started.")
            file_path = os.path.join(dataset_dir, file)

            df = pd.read_csv(file_path)
            if first_csv is None:
                first_csv = 1
                df.to_csv(output_path,index=False)
                print(f"{file} merged successfully.")
            else :
                rest_csvs = pd.read_csv(output_path)
                df.drop(["timestamp","timeframe"],axis=1,inplace=True)
                concat = pd.concat([rest_csvs, df] , axis=1)
                concat.to_csv(output_path,index=False)
                print(f"{file} merged successfully.")
    def fetch(self):
        project_path = os.path.dirname(os.path.abspath(__file__))
        for symbol in self.symbol:
            base_currency = symbol.split('/')[0].lower()
            dataset_name = f"{base_currency}_dataset.csv"
            dataset_path = os.path.join(project_path, 'dataset', dataset_name)
        #--------------------------------------------------------------------------------------------------------------

            for tf in self.timeframe:
                self.since = 1666902600000
                r = self.rate[self.timeframe.index(tf)]           # rate
                i = self.iteration[self.timeframe.index(tf)]      #iteration

                try:
                    for x in range (i):
                        fetched = self.exchange.fetch_ohlcv(symbol, timeframe=tf, since=self.since, limit=self.limit)

                        print(f"{len(fetched)} candles data from {i * self.limit} in {symbol} market fetched")
                        df = pd.DataFrame(fetched, columns=self.columns)

                        if "timeframe" in df.columns:
                                df["timeframe"] = tf
                        else:
                                df.insert(1, "timeframe", tf)

                        dataset = df.rename(columns={
                            col: f"{base_currency}_{col}"
                            if col != "timestamp" else col
                            for col in self.columns
                        })


                        header = not os.path.exists(dataset_path)
                        dataset.to_csv(dataset_path, mode='a', index=False , header=header)
                        print("dataset saved")

                    #-------------------------------------------------------------------------------------------------

                        self.since += (self.limit * 60000 * r)  # converting minutes to milliseconds / formula : minutes * 60000
                        time.sleep(self.sleep_time)


                except (ccxt.NetworkError, ccxt.ExchangeError) as e:
                    print(f"Error fetching {symbol} ({tf}): {e}")
                    raise


        return print ("data has been fetched and saved")

fetching_data = FetchData(
                exchange = ccxt.kucoin(),
                symbols = ['TON/USDT','BTC/USDT','ETH/USDT'],
                timeframe = ['1m','5m'],
                since_date = 1666902600000,
                candles_limit = 1440,
                sleep_time = 2,
                daily_candles_limit = [10,5], # number of candles from 27 oct 2022 to 2 feb 2022 equals : 829
                rate = [1,5],
                columns = ["timestamp", "open", "high", "low", "close", "volume"])
fetching_data.run()












