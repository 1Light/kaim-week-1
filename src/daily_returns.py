import os
import pandas as pd

def compute_daily_returns(input_folder_stock, output_folder):
    """
    Compute daily returns (percentage changes) for each stock dataset and save the results.
    
    Args:
        input_folder_stock (str): Path to the folder containing stock CSV files.
        output_folder (str): Path to the folder where outputs will be saved.
    
    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # List all stock files
    stock_files = [f for f in os.listdir(input_folder_stock) if f.endswith('.csv')]
    
    for stock_file in stock_files:
        # Extract stock symbol from the stock file name (e.g., aapl_historical_data.csv -> AAPL)
        stock_symbol = os.path.splitext(stock_file)[0].replace('_historical_data', '').upper()
        
        # Load each stock dataset
        stock_df = pd.read_csv(os.path.join(input_folder_stock, stock_file), parse_dates=['Date'])
        
        # Ensure that the Date column is in the correct datetime format
        stock_df['Date'] = pd.to_datetime(stock_df['Date'])
        
        # Calculate daily returns (percentage change in stock prices)
        stock_df['Daily_Return'] = stock_df['Close'].pct_change() * 100  # Multiply by 100 to get percentage
        
        # Drop rows with NaN values (which will exist for the first row)
        stock_df.dropna(subset=['Daily_Return'], inplace=True)

        # Print the first few rows of the daily returns for verification
        print(f"\nDaily returns for {stock_symbol}:")
        print(stock_df[['Date', 'Close', 'Daily_Return']].head())
        
        # Save the result into the output folder
        stock_output_folder = os.path.join(output_folder, stock_symbol)
        os.makedirs(stock_output_folder, exist_ok=True)
        
        print(f"Daily returns computed and saved for {stock_symbol}.")

# Define the input folder containing stock data and the output folder
input_folder_stock = os.path.join('cleaned_data', 'yfinance_data')
output_folder = os.path.join('results', 'daily_returns')

# Run the function to compute daily returns
compute_daily_returns(input_folder_stock, output_folder)