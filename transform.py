import os
import warnings
import pandas as pd

warnings.filterwarnings('ignore')

data_dir = "data"  # change if needed
all_data = []

def extract_symbol_from_filename(filename):
    return filename.replace("NS_history.csv", "").replace("_", "")

def transform_csv(file_path, symbol):
    df = pd.read_csv(file_path, header=[0, 1])
    df.columns = [col[0] if col[0] != "Price" else "Date" for col in df.columns]
    df = df.drop(index=[0, 1]).reset_index(drop=True)

    df["Symbol"] = symbol

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Keep only the required columns
    df = df[["Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]]

    return df

for file in os.listdir(data_dir):
    if file.endswith("_history.csv"):
        path = os.path.join(data_dir, file)
        symbol = extract_symbol_from_filename(file)
        try:
            transformed_df = transform_csv(path, symbol)
            all_data.append(transformed_df)
            print(f"✅ Processed {file} → Symbol: {symbol}")
        except Exception as e:
            print(f"⚠️ Failed to process {file}: {e}")

if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Define output path
    output_path = os.path.join(data_dir, "combined_stock_data.csv")
    
    # Save to CSV
    final_df.to_csv(output_path, index=False)
    print(f"✅ Combined data saved to {output_path}")
else:
    print("⚠️ No data to combine.")