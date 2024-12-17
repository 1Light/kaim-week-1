import os
import pandas as pd
import matplotlib.pyplot as plt
import talib
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def calculate_correlation_with_talib(news_file, input_folder_stock, output_folder):
    """
    Calculate Pearson correlation between sentiment scores and stock data (using TA-Lib indicators)
    
    Args:
        news_file (str): Path to the single news CSV file.
        input_folder_stock (str): Path to the folder containing stock CSV files.
        output_folder (str): Path to the folder where outputs will be saved.
    
    Returns:
        None
    """
    # Ensure the correlation_plots directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the news data
    news_df = pd.read_csv(news_file, parse_dates=['date'])
    news_df['date'] = news_df['date'].dt.normalize()  # Normalize dates to yyyy-mm-dd
    
    # Initialize VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()
    
    # Function to calculate sentiment score for each headline
    def get_sentiment_score(text):
        sentiment = analyzer.polarity_scores(text)
        return sentiment['compound']  # We use the 'compound' score for sentiment
    
    # Calculate sentiment score for each headline
    news_df['sentiment_score'] = news_df['headline'].apply(get_sentiment_score)

    # List all stock files
    stock_files = [f for f in os.listdir(input_folder_stock) if f.endswith('.csv')]

    for stock_file in stock_files:
        # Extract stock symbol from the stock file name (e.g., aapl_historical_data.csv -> AAPL)
        stock_symbol = os.path.splitext(stock_file)[0].replace('_historical_data', '').upper()
        
        # Load each stock dataset
        stock_df = pd.read_csv(os.path.join(input_folder_stock, stock_file), parse_dates=['Date'])
        stock_df['Date'] = stock_df['Date'].dt.normalize()

        # Filter the news data for the corresponding stock symbol
        stock_news_df = news_df[news_df['stock'] == stock_symbol]
        
        if stock_news_df.empty:
            print(f"Warning: No news data found for stock {stock_symbol}. Skipping...")
            continue
        
        # Aggregate sentiment scores by date (compute average daily sentiment score)
        daily_sentiment_df = stock_news_df.groupby('date')['sentiment_score'].mean().reset_index()
        
        # Merge aggregated sentiment with stock data
        aligned_df = pd.merge(daily_sentiment_df, stock_df, left_on='date', right_on='Date', how='inner')
        
        # Ensure output subfolder for each stock exists
        stock_output_folder = os.path.join(output_folder, stock_symbol)
        os.makedirs(stock_output_folder, exist_ok=True)
        
        # Calculate TA-Lib indicators (SMA, RSI, MACD)
        sma = talib.SMA(aligned_df['Close'], timeperiod=20)  # 20-day SMA
        rsi = talib.RSI(aligned_df['Close'], timeperiod=14)  # 14-day RSI
        macd, macdsignal, macdhist = talib.MACD(aligned_df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)  # MACD
        
        # Add the TA-Lib indicators to the DataFrame
        aligned_df['SMA'] = sma
        aligned_df['RSI'] = rsi
        aligned_df['MACD'] = macd
        
        # Drop NaN values resulting from TA-Lib calculations
        aligned_df = aligned_df.dropna(subset=['SMA', 'RSI', 'MACD'])
        
        # Calculate the Pearson correlation between sentiment and each TA-Lib indicator
        corr_sentiment_sma = aligned_df['sentiment_score'].corr(aligned_df['SMA'])
        corr_sentiment_rsi = aligned_df['sentiment_score'].corr(aligned_df['RSI'])
        corr_sentiment_macd = aligned_df['sentiment_score'].corr(aligned_df['MACD'])

        # Print the correlation results
        print(f"Pearson correlation between sentiment and stock returns for {stock_symbol}: {aligned_df['sentiment_score'].corr(aligned_df['Close']):.4f}")
        print(f"Pearson correlation between sentiment and SMA for {stock_symbol}: {corr_sentiment_sma:.4f}")
        print(f"Pearson correlation between sentiment and RSI for {stock_symbol}: {corr_sentiment_rsi:.4f}")
        print(f"Pearson correlation between sentiment and MACD for {stock_symbol}: {corr_sentiment_macd:.4f}")
        
        # Visualization: Plot sentiment vs TA-Lib indicators
        plt.figure(figsize=(10, 6))
        
        # Plot Sentiment vs SMA
        plt.subplot(3, 1, 1)
        plt.scatter(aligned_df['sentiment_score'], aligned_df['SMA'], alpha=0.7, color='blue')
        plt.title(f"Sentiment vs SMA for {stock_symbol}")
        plt.xlabel('Sentiment Score')
        plt.ylabel('SMA (20-day)')

        # Plot Sentiment vs RSI
        plt.subplot(3, 1, 2)
        plt.scatter(aligned_df['sentiment_score'], aligned_df['RSI'], alpha=0.7, color='green')
        plt.title(f"Sentiment vs RSI for {stock_symbol}")
        plt.xlabel('Sentiment Score')
        plt.ylabel('RSI (14-day)')

        # Plot Sentiment vs MACD
        plt.subplot(3, 1, 3)
        plt.scatter(aligned_df['sentiment_score'], aligned_df['MACD'], alpha=0.7, color='red')
        plt.title(f"Sentiment vs MACD for {stock_symbol}")
        plt.xlabel('Sentiment Score')
        plt.ylabel('MACD')

        plt.tight_layout()

        # Save the plot in the respective stock's folder
        plot_file = os.path.join(stock_output_folder, f"{stock_symbol}_sentiment_talib_correlation.png")
        plt.savefig(plot_file, bbox_inches='tight', dpi=300)
        plt.close()

        print(f"Correlation plot saved for {stock_symbol}.")
        
# Define file and folder paths
news_file = os.path.join('cleaned_data', 'raw_analyst_ratings', 'raw_analyst_ratings.csv')
input_folder_stock = os.path.join('cleaned_data', 'yfinance_data')
output_folder = os.path.join('results', 'correlation_plots')

# Run the correlation calculation function
calculate_correlation_with_talib(news_file, input_folder_stock, output_folder)
