import os
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scipy.stats import pearsonr

def calculate_correlation(news_file, input_folder_stock):
    """
    Calculate the Pearson correlation coefficient between average daily sentiment scores
    and stock daily returns.
    
    Args:
        news_file (str): Path to the single news CSV file.
        input_folder_stock (str): Path to the folder containing stock CSV files.
    
    Returns:
        None
    """
    # Initialize the sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Load the news data
    news_df = pd.read_csv(news_file, parse_dates=['date'])
    news_df['date'] = news_df['date'].dt.normalize()  # Normalize dates to yyyy-mm-dd

    # Calculate daily sentiment scores
    news_df['sentiment'] = news_df['headline'].apply(lambda x: analyzer.polarity_scores(str(x))['compound'])

    # Group by date and calculate the average sentiment score for each day
    avg_sentiment_per_day = news_df.groupby('date')['sentiment'].mean()

    # List all stock files
    stock_files = [f for f in os.listdir(input_folder_stock) if f.endswith('.csv')]

    # Prepare a dictionary to store stock returns and dates
    stock_returns = {}

    for stock_file in stock_files:
        # Extract stock symbol from the stock file name (e.g., AAPL_historical_data.csv -> AAPL)
        stock_symbol = os.path.splitext(stock_file)[0].replace('_historical_data', '').upper()

        # Load the stock data
        stock_df = pd.read_csv(os.path.join(input_folder_stock, stock_file), parse_dates=['Date'])
        stock_df['Date'] = stock_df['Date'].dt.normalize()  # Normalize dates

        # Calculate the daily stock returns
        stock_df['Return'] = stock_df['Close'].pct_change()

        # Group by date and get the daily return (ignoring the first NaN return)
        stock_returns[stock_symbol] = stock_df.groupby('Date')['Return'].mean().dropna()

    # Calculate the Pearson correlation for each stock
    for stock_symbol, returns in stock_returns.items():
        # Align stock returns with average sentiment data on the date
        merged_data = pd.merge(avg_sentiment_per_day, returns, left_index=True, right_index=True, how='inner')
        
        if not merged_data.empty:
            # Calculate Pearson correlation
            corr_coefficient, _ = pearsonr(merged_data['sentiment'], merged_data['Return'])
            print(f"Pearson correlation between sentiment and stock returns for {stock_symbol}: {corr_coefficient:.4f}")
        else:
            print(f"No common dates found for sentiment and stock returns for {stock_symbol}. Skipping correlation calculation.")

# Define file and folder paths
news_file = os.path.join('cleaned_data', 'raw_analyst_ratings', 'raw_analyst_ratings.csv')
input_folder_stock = os.path.join('cleaned_data', 'yfinance_data')

# Run the correlation function
calculate_correlation(news_file, input_folder_stock)