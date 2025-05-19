import yfinance as yf
import os
from datetime import datetime, timedelta

# List of stock symbols
symbols = [
    'ACC.NS', 'BANKBARODA.NS', 'FEDERALBNK.NS', 'IRFC.NS',
    'LTTS.NS', 'LT.NS', 'NTPCGREEN.NS', 'NTPC.NS',
    'RCF.NS', 'RELIANCE.NS', 'STARCEMENT.NS', 'TATAPOWER.NS'
]

# Output directory for historical data
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Define date range: past 3 months
end_date = datetime.today().date()
start_date = end_date - timedelta(days=90)

# Loop over each symbol
for symbol in symbols:
    print(f"Processing {symbol}...")

    try:
        # 1. Download historical OHLCV data
        df = yf.download(symbol, start=start_date, end=end_date, progress=False)

        if not df.empty:
            file_path = os.path.join(output_dir, f"{symbol.replace('.', '_')}_history.csv")
            df.to_csv(file_path)
            print(f"  ✔ Saved historical data to {file_path}")
        else:
            print(f"  ✖ No historical data for {symbol}")

        # 2. Print metadata (do NOT save to file)
        stock = yf.Ticker(symbol)
        info = stock.info

        print(f"  Name   : {info.get('shortName', 'N/A')}")
        print(f"  Market : {info.get('market', 'N/A')}")
        print(f"  Sector : {info.get('sector', 'N/A')}")

    except Exception as e:
        print(f"  ⚠ Error processing {symbol}: {e}")

    print("-" * 40)