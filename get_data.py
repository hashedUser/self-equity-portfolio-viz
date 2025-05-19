import yfinance as yf
import os
import csv
from datetime import datetime, timedelta

# List of stock symbols
symbols = ['ACC.NS']
'''
'BANKBARODA.NS', 'FEDERALBNK.NS', 'IRFC.NS',
    'LTTS.NS', 'LT.NS', 'NTPCGREEN.NS', 'NTPC.NS',
    'RCF.NS', 'RELIANCE.NS', 'STARCEMENT.NS', 'TATAPOWER.NS'
'''

# Output directory for all files
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Define date range for historical data: past 3 months
end_date = datetime.today().date()
start_date = end_date - timedelta(days=90)

# Metadata file path
info_file = os.path.join(output_dir, "symbol_info.csv")

# Write the header row to symbol info CSV
with open(info_file, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Symbol', 'Name', 'Market', 'Sector'])

# Loop over each stock symbol
for symbol in symbols:
    print(f"Processing {symbol}...")

    try:
        # -----------------------------
        # 1. Fetch historical OHLCV data
        # -----------------------------
        df = yf.download(symbol, start=start_date, end=end_date, progress=False)

        if not df.empty:
            # Ensure consistent naming (replace dot in symbol)
            csv_filename = f"{symbol.replace('.', '_')}_history.csv"
            csv_path = os.path.join(output_dir, csv_filename)

            # Save historical data: Open, High, Low, Close, Adj Close, Volume
            df.to_csv(csv_path)
            print(f"  ✔ Historical OHLCV data saved to {csv_path}")
        else:
            print(f"  ✖ No historical data found for {symbol}")

        # -----------------------------
        # 2. Fetch and save metadata
        # -----------------------------
        stock = yf.Ticker(symbol)
        info = stock.info

        name = info.get('shortName', 'N/A')
        market = info.get('market', 'N/A')
        sector = info.get('sector', 'N/A')

        # Append metadata row to symbol_info.csv
        with open(info_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([symbol, name, market, sector])
            print(f"  ✔ Metadata appended for {symbol}")

    except Exception as e:
        print(f"  ⚠ Error processing {symbol}: {e}")

    print("-" * 40)