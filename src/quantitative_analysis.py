import os
import pandas as pd
import talib
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np

# Download VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

def apply_ta_indicators_and_save_images(file_path, output_folder, sentiment_data=None):
    """
    Apply technical analysis indicators using TA-Lib, perform sentiment analysis, create plots, 
    and save as PNG images.
    
    Args:
        file_path (str): Path to the cleaned stock price CSV file.
        output_folder (str): Path to the folder where output PNG files will be saved.
        sentiment_data (str): Path to sentiment analysis data file (optional).
        
    Returns:
        None
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')

    # Ensure necessary columns are present
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"File '{file_path}' is missing required columns.")

    # Apply technical indicators using TA-Lib
    df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
    df['EMA_20'] = talib.EMA(df['Close'], timeperiod=20)
    df['RSI_14'] = talib.RSI(df['Close'], timeperiod=14)
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['Bollinger_Upper'], df['Bollinger_Middle'], df['Bollinger_Lower'] = talib.BBANDS(df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df['ATR'] = talib.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['Stochastic_K'], df['Stochastic_D'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=14, slowk_period=3, slowd_period=3)

    # Calculate correlation between Close and Volume
    df['Correlation_Close_Volume'] = df['Close'].rolling(window=20).corr(df['Volume'])

    # Calculate the rolling volatility (standard deviation) for Close
    df['Volatility'] = df['Close'].rolling(window=20).std()

    # Print relevant values to the console
    print(f"\nProcessing file: {file_path}")
    print("\nSample of Calculated Indicators:")
    print(df[['Close', 'SMA_20', 'EMA_20', 'RSI_14', 'MACD', 'MACD_Signal', 'Bollinger_Upper', 
              'Bollinger_Lower', 'ATR', 'Stochastic_K', 'Stochastic_D', 'Correlation_Close_Volume', 
              'Volatility']].tail())

    # Perform Sentiment Analysis if sentiment data is provided
    if sentiment_data:
        sentiment_df = pd.read_csv(sentiment_data)
        sentiment_analyzer = SentimentIntensityAnalyzer()
        sentiment_df['Sentiment'] = sentiment_df['Text'].apply(lambda x: sentiment_analyzer.polarity_scores(x)['compound'])
        sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'])
        sentiment_df.set_index('Date', inplace=True)
        
        # Merge sentiment data with stock data
        df = df.join(sentiment_df[['Sentiment']], how='left')

    # Determine the stock name and create a subfolder for the stock
    stock_name = os.path.splitext(os.path.basename(file_path))[0]
    stock_output_folder = os.path.join(output_folder, stock_name)
    os.makedirs(stock_output_folder, exist_ok=True)

    # Plot and save the indicators
    fig, axes = plt.subplots(4, 1, figsize=(12, 16), sharex=True)

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

    # Plot ATR and Bollinger Bands
    axes[3].plot(df.index, df['Close'], label='Close Price', color='blue')
    axes[3].plot(df.index, df['Bollinger_Upper'], label='Bollinger Upper Band', color='green')
    axes[3].plot(df.index, df['Bollinger_Lower'], label='Bollinger Lower Band', color='red')
    axes[3].fill_between(df.index, df['Bollinger_Lower'], df['Bollinger_Upper'], color='yellow', alpha=0.2)
    axes[3].set_title(f'{stock_name} - Bollinger Bands & ATR')
    axes[3].legend()

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
