import pandas as pd
import numpy as np

def test_epu():
    url = "https://www.policyuncertainty.com/media/Spain_Policy_Uncertainty_Data.xlsx"
    print(f"Downloading EPU data from {url}...")
    try:
        # The file often has headers or titles on the first few rows
        df = pd.read_excel(url)
        print("Raw columns:", df.columns.tolist())
        print("First few rows:")
        print(df.head(10))
        
        # We need to find the Year, Month, EPU
        # Sometimes the real header is on row 1 or 2
    except Exception as e:
        print("Failed to download or parse:", e)

if __name__ == "__main__":
    test_epu()
