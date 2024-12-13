import os
import pandas as pd
import matplotlib.pyplot as plt
import talib

def plot_technical_indicators(file_path, output_folder):
    """
    Visualize the stock data with technical indicators such as Moving Averages (SMA, EMA), RSI, and MACD.
    
    Args:
        file_path (str): Path to the cleaned stock price CSV file.
        output_folder (str): Path to the folder where output PNG files will be saved.

    Returns:
        None
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    # Ensure necessary columns are present
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"File '{file_path}' is missing required columns.")
    
    # Calculate technical indicators using TA-Lib
    df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)  # 50-day Simple Moving Average
    df['SMA_200'] = talib.SMA(df['Close'], timeperiod=200)  # 200-day Simple Moving Average
    df['EMA_50'] = talib.EMA(df['Close'], timeperiod=50)  # 50-day Exponential Moving Average
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)  # 14-day Relative Strength Index
    macd, macd_signal, _ = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)  # MACD
    df['MACD'] = macd
    df['MACD_Signal'] = macd_signal

    # Create the plots
    stock_name = os.path.splitext(os.path.basename(file_path))[0]
    stock_output_folder = os.path.join(output_folder, stock_name)
    os.makedirs(stock_output_folder, exist_ok=True)

    # Plot: Stock Price and Moving Averages (SMA, EMA)
    plt.figure(figsize=(10, 6))
    plt.plot(df['Close'], label='Close Price', color='black', linewidth=1)
    plt.plot(df['SMA_50'], label='50-Day SMA', color='blue', linestyle='--', linewidth=1)
    plt.plot(df['SMA_200'], label='200-Day SMA', color='green', linestyle='--', linewidth=1)
    plt.plot(df['EMA_50'], label='50-Day EMA', color='red', linestyle='-', linewidth=1)
    plt.title(f'{stock_name} - Stock Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend(loc='best')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(stock_output_folder, f'{stock_name}_price_and_moving_averages.png'), dpi=300)
    plt.close()

    # Plot: Relative Strength Index (RSI)
    plt.figure(figsize=(10, 6))
    plt.plot(df['RSI'], label='14-Day RSI', color='orange')
    plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    plt.title(f'{stock_name} - RSI')
    plt.xlabel('Date')
    plt.ylabel('RSI Value')
    plt.legend(loc='best')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(stock_output_folder, f'{stock_name}_RSI.png'), dpi=300)
    plt.close()

    # Plot: MACD and Signal Line
    plt.figure(figsize=(10, 6))
    plt.plot(df['MACD'], label='MACD', color='blue')
    plt.plot(df['MACD_Signal'], label='MACD Signal', color='red', linestyle='--')
    plt.title(f'{stock_name} - MACD and Signal Line')
    plt.xlabel('Date')
    plt.ylabel('MACD Value')
    plt.legend(loc='best')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(stock_output_folder, f'{stock_name}_MACD.png'), dpi=300)
    plt.close()

    print(f"Visualizations for {stock_name} saved to {stock_output_folder}")

# Define the folder paths
input_folder = os.path.join('cleaned_data', 'yfinance_data')  # Path to your stock data folder
output_folder = os.path.join('results', 'visualizations')  # Path to save the output images

# Apply the function to all files in the input folder
stock_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

for stock_file in stock_files:
    file_path = os.path.join(input_folder, stock_file)
    plot_technical_indicators(file_path, output_folder)