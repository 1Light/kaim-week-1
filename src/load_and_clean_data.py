import gdown
import pandas as pd
from dateutil import parser
import os

def download_from_gdrive(file_id, output_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)

def load_and_clean_data():

    file_ids = {
        "nvda_historical_data": "1gEiOJZS3kBPa9U9OFcdsnAtOd7wQaVYN",
        "meta_historical_data": "1SlI2VsvSCMjTe7vSd0DbOhUW9_pJrsQy",
        "msft_historical_data": "1iJ7_yF00867bptJgdi-ZsHnFLjvYvkPr",
        "tsla_historical_data": "1VVqiS9jlogAKbWNSy8Y6sN5CwmY8IxxH",
        "amzn_historical_data": "1kU2PfZhXU6pY0OvSE7iGp0EnzcGE33Wg",
        "goog_historical_data": "1YVgIUPhgEHzvzALCrS7KDsFbFV2df9PG",
        "aapl_historical_data": "1q7tFYDGcQ2roBaSPYCEL06wr0Rk3qWIs"
    }

    # Define local paths to save the data temporarily
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'yfinance_data'))
    os.makedirs(base_path, exist_ok=True)  
    
    # Define file paths for each dataset
    nvda_path = os.path.join(base_path, 'nvda_historical_data.csv')
    meta_path = os.path.join(base_path, 'meta_historical_data.csv')
    msft_path = os.path.join(base_path, 'msft_historical_data.csv')
    tsla_path = os.path.join(base_path, 'tsla_historical_data.csv')
    amzn_path = os.path.join(base_path, 'amzn_historical_data.csv')
    goog_path = os.path.join(base_path, 'goog_historical_data.csv')
    aapl_path = os.path.join(base_path, 'aapl_historical_data.csv')

    # Loop over each file ID to download and load data
    data_frames = {}  # Dictionary to hold all the loaded data frames

    for file_name, file_id in file_ids.items():
        # Define file path for each dataset
        file_path = os.path.join(base_path, f'{file_name}.csv')
        
        # Download the file if it doesn't exist
        if not os.path.exists(file_path):
            print(f"Downloading {file_name}...")
            download_from_gdrive(file_id, file_path)
        
        # Load the data (after confirming they are downloaded)
        data = pd.read_csv(file_path)

        # Convert the 'date' column to datetime format
        data['Date'] = data['Date'].apply(lambda x: parser.parse(x, fuzzy=True, ignoretz=True))

        # Adjust for Dividends and Stock Splits
        if 'Dividends' in data.columns:
            # Adjust stock prices based on the dividends
            data['Adj Close'] = data['Close'] - data['Dividends']
        
        if 'Stock Splits' in data.columns:
            # Adjust stock prices based on stock splits (example: for a 2-for-1 split, price halved)
            data['Adj Close'] = data.apply(
                lambda row: row['Close'] / row['Stock Splits'] if row['Stock Splits'] != 0 else row['Close'], 
                axis=1
            )

        # Check and correct negative values for stock price columns (Open, High, Low, Close)
        stock_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Dividends', 'Stock Splits']
        for col in stock_columns:
            if col in data.columns:
                print(f"Checking column: {col}")
                # Loop through each value in the column
                for idx, value in data[col].items(): 
                    if value < 0:
                        print(f"Original value in {col} at index {idx}: {value}")
                        # Convert negative value to positive
                        data.at[idx, col] = abs(value)
        
        # Store the dataframe in the dictionary
        data_frames[file_name] = data
    
    # Load each dataset into individual variables for cleaning
    meta_data = data_frames['meta_historical_data']
    tsla_data = data_frames['tsla_historical_data']
    nvda_data = data_frames['nvda_historical_data']
    msft_data = data_frames['msft_historical_data']
    amzn_data = data_frames['amzn_historical_data']
    goog_data = data_frames['goog_historical_data']
    aapl_data = data_frames['aapl_historical_data']

    print(meta_data.head())

    """
    # Print the first few rows to verify successful load
    print(meta_data.head())

    # Check the data types of the columns
    print(meta_data.dtypes)

    # Check for missing data
    print(meta_data.isnull().sum())
    """

    # Save each cleaned dataset to a new file
    cleaned_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cleaned_data', 'yfinance_data'))
    os.makedirs(cleaned_path, exist_ok=True)

    for file_name, data in data_frames.items():
        cleaned_file_path = os.path.join(cleaned_path, f'{file_name}.csv')
        data.to_csv(cleaned_file_path, index=False)  # Save without the index column
        print(f"Saved cleaned data for {file_name}.") 

load_and_clean_data()
