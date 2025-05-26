import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# List of symbols
symbols = [
    'ACC.NS', 'BANKBARODA.NS', 'FEDERALBNK.NS', 'IRFC.NS',
    'LTTS.NS', 'LT.NS', 'NTPCGREEN.NS', 'NTPC.NS',
    'RCF.NS', 'RELIANCE.NS', 'STARCEMENT.NS', 'TATAPOWER.NS'
]

def create_output_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def get_date_range(days: int = 90):
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def download_historical_data(symbol: str, start_date, end_date) -> pd.DataFrame:
    return yf.download(symbol, start=start_date, end=end_date, progress=False)

def print_symbol_info(symbol: str):
    stock = yf.Ticker(symbol)
    info = stock.info
    print(f"  Name   : {info.get('shortName', 'N/A')}")
    print(f"  Market : {info.get('market', 'N/A')}")
    print(f"  Sector : {info.get('sector', 'N/A')}")

def save_data_to_csv(df: pd.DataFrame, symbol: str, output_dir: str):
    filename = f"{symbol.replace('.', '_')}_history.csv"
    file_path = os.path.join(output_dir, filename)
    df.to_csv(file_path)
    print(f"  ✔ Saved historical data to {file_path}")

def process_symbol(symbol: str, output_dir: str, start_date, end_date):
    print(f"Processing {symbol}...")
    try:
        df = download_historical_data(symbol, start_date, end_date)

        if not df.empty:
            save_data_to_csv(df, symbol, output_dir)
        else:
            print(f"  ✖ No historical data for {symbol}")

        print_symbol_info(symbol)

    except Exception as e:
        print(f"  ⚠ Error processing {symbol}: {e}")

    print("-" * 40)

def main():
    output_dir = "data"
    create_output_dir(output_dir)
    start_date, end_date = get_date_range(90)

    for symbol in symbols:
        process_symbol(symbol, output_dir, start_date, end_date)

if __name__ == "__main__":
    main()