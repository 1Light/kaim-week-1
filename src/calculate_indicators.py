import os
import pandas as pd
import talib
import matplotlib.pyplot as plt

def apply_ta_indicators_and_save_images(file_path, output_folder):
    """
    Apply technical analysis indicators using TA-Lib, create plots, and save as PNG images.

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

    # Apply technical indicators
    # 1. Moving Averages
    df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)  # Simple Moving Average (20 days)
    df['EMA_20'] = talib.EMA(df['Close'], timeperiod=20)  # Exponential Moving Average (20 days)

    # 2. Relative Strength Index (RSI)
    df['RSI_14'] = talib.RSI(df['Close'], timeperiod=14)

    # 3. Moving Average Convergence Divergence (MACD)
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(
        df['Close'], fastperiod=12, slowperiod=26, signalperiod=9
    )

    # Print relevant values to the console
    print(f"\nProcessing file: {file_path}")
    print("\nSample of Calculated Indicators:")
    print(df[['Close', 'SMA_20', 'EMA_20', 'RSI_14', 'MACD', 'MACD_Signal', 'MACD_Hist']].tail())

    print("\nBasic Statistics for Indicators:")
    print(df[['SMA_20', 'EMA_20', 'RSI_14', 'MACD', 'MACD_Signal', 'MACD_Hist']].describe())

    # Determine the stock name and create a subfolder for the stock
    stock_name = os.path.splitext(os.path.basename(file_path))[0]
    stock_output_folder = os.path.join(output_folder, stock_name)
    os.makedirs(stock_output_folder, exist_ok=True)

    # Plot and save the indicators
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # Plot Close price and Moving Averages
    axes[0].plot(df.index, df['Close'], label='Close Price', color='blue')
    axes[0].plot(df.index, df['SMA_20'], label='SMA 20', color='green')
    axes[0].plot(df.index, df['EMA_20'], label='EMA 20', color='red')
    axes[0].set_title(f'{stock_name} - Close Price & Moving Averages')
    axes[0].legend()

    # Plot RSI
    axes[1].plot(df.index, df['RSI_14'], label='RSI 14', color='purple')
    axes[1].axhline(70, color='red', linestyle='--', linewidth=0.8, label='Overbought (70)')
    axes[1].axhline(30, color='green', linestyle='--', linewidth=0.8, label='Oversold (30)')
    axes[1].set_title(f'{stock_name} - Relative Strength Index (RSI)')
    axes[1].legend()

    # Plot MACD
    axes[2].plot(df.index, df['MACD'], label='MACD', color='blue')
    axes[2].plot(df.index, df['MACD_Signal'], label='Signal Line', color='red')
    axes[2].bar(df.index, df['MACD_Hist'], label='MACD Histogram', color='gray', alpha=0.5)
    axes[2].set_title(f'{stock_name} - MACD')
    axes[2].legend()

    # Adjust layout and save the plot as a PNG file
    plt.tight_layout()
    output_file = os.path.join(stock_output_folder, f'{stock_name}_indicators.png')
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"Indicators plotted and saved to {output_file}")

# Define the folder paths
input_folder = os.path.join('cleaned_data', 'yfinance_data')
output_folder = os.path.join('results', 'technical_indicators')

# Apply the function to all files in the input folder
stock_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

for stock_file in stock_files:
    file_path = os.path.join(input_folder, stock_file)
    apply_ta_indicators_and_save_images(file_path, output_folder)