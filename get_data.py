import yfinance as yf
import os
import pandas as pd
from datetime import datetime, timedelta

# List of stock symbols
symbols = [
    'ACC.NS', 'BANKBARODA.NS', 'FEDERALBNK.NS', 'IRFC.NS',
    'LTTS.NS', 'LT.NS', 'NTPCGREEN.NS', 'NTPC.NS',
    'RCF.NS', 'RELIANCE.NS', 'STARCEMENT.NS', 'TATAPOWER.NS'
]

# Output directory
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Define date range: past 3 months
end_date = datetime.today().date()
start_date = end_date - timedelta(days=90)

# Store combined data in a list
combined_data = []

# Loop over each symbol
for symbol in symbols:
    print(f"Processing {symbol}...")

    try:
        # 1. Download historical OHLCV data
        df = yf.download(symbol, start=start_date, end=end_date, progress=False)

        if not df.empty:
            df['Symbol'] = symbol
            df.reset_index(inplace=True)  # Ensure 'Date' is a column
            combined_data.append(df)
            print(f"  ✔ Historical data collected for {symbol}")
        else:
            print(f"  ✖ No historical data for {symbol}")

        # 2. Print company metadata
        stock = yf.Ticker(symbol)
        info = stock.info

        print(f"  Name   : {info.get('shortName', 'N/A')}")
        print(f"  Market : {info.get('market', 'N/A')}")
        print(f"  Sector : {info.get('sector', 'N/A')}")

    except Exception as e:
        print(f"  ⚠ Error processing {symbol}: {e}")

    print("-" * 40)

# Concatenate all data and save
if combined_data:
    result_df = pd.concat(combined_data, ignore_index=True)
    output_file = os.path.join(output_dir, "all_symbols_history.csv")
    result_df.to_csv(output_file, index=False)
    print(f"✅ Combined historical data saved to {output_file}")
else:
    print("⚠ No data to save.")