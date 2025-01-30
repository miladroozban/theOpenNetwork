import pymongo

def mongodb(fetch_date, symbol, timeframe, candle_date, candle_open, candle_high, candle_low, candle_close, candle_volume):
  url = "mongodb://localhost:27017/"
  ton_cli = pymongo.MongoClient(url)
  ton_db = ton_cli["theOpenNetwork"]
  market_col = ton_db["marketData"]

  # Define the filter (criteria for matching documents)
  filter_criteria = {"data_date": fetch_date, "symbol": symbol, "timeframe": timeframe}

  # Data to be updated
  update_data = {
      "fetch_date" : fetch_date,
      "symbol": symbol,
      "time_frame" : timeframe,
      "candle_date": candle_date,
      "open": candle_open,
      "high": candle_high,
      "low": candle_low,
      "close": candle_close,
      "volume": candle_volume
  }

  # Update or insert the document
  result = market_col.replace_one(filter_criteria, update_data, upsert=True)

  if result.upserted_id:
      print(f"New Data has been added with ID: {result.upserted_id} and Symbol: {symbol}")
  else:
      print("Document has been updated successfully.")

  ton_cli.close()