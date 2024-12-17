import os
import pandas as pd
import matplotlib.pyplot as plt

def normalize_dates(news_file, input_folder_stock, output_folder):
    """
    Normalize dates in a single news dataset and multiple stock datasets to align them and save the cleaned output.
    
    Args:
        news_file (str): Path to the single news CSV file.
        input_folder_stock (str): Path to the folder containing stock CSV files.
        output_folder (str): Path to the folder where outputs will be saved.
    
    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the news data
    news_df = pd.read_csv(news_file, parse_dates=['date'])
    news_df['date'] = news_df['date'].dt.normalize()  # Normalize dates to yyyy-mm-dd

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
        
        # Merge datasets on the date
        aligned_df = pd.merge(stock_news_df, stock_df, left_on='date', right_on='Date', how='inner')
        
        # Save results into output subfolder
        stock_output_folder = os.path.join(output_folder, stock_symbol)
        os.makedirs(stock_output_folder, exist_ok=True)
        
        # Visualization: Group data by quarter for NVDA, else group by month
        if stock_symbol == 'NVDA':
            aligned_df['period'] = aligned_df['date'].dt.to_period('Q')  # Group by quarter
            grouped_counts = aligned_df['period'].value_counts().sort_index()
            x_label = "Quarter"
        else:
            aligned_df['period'] = aligned_df['date'].dt.to_period('M')  # Group by month
            grouped_counts = aligned_df['period'].value_counts().sort_index()
            x_label = "Month"

        # Plot
        plt.figure(figsize=(10, 6))
        grouped_counts.plot(kind='bar', color='blue', alpha=0.7)
        plt.title(f"{stock_symbol} - Number of News Articles per {x_label}")
        plt.xlabel(x_label)
        plt.ylabel("Number of Articles")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot
        plot_file = os.path.join(stock_output_folder, f"{stock_symbol}_normalized_dates.png")
        plt.savefig(plot_file, bbox_inches='tight', dpi=300)
        plt.close()

        print(f"Normalized data and plot saved for {stock_symbol}.")

# Define file and folder paths
news_file = os.path.join('cleaned_data', 'raw_analyst_ratings', 'raw_analyst_ratings.csv')
input_folder_stock = os.path.join('cleaned_data', 'yfinance_data')
output_folder = os.path.join('results', 'normalized_dates')

# Run the normalization function
normalize_dates(news_file, input_folder_stock, output_folder)