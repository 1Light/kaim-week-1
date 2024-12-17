import os
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer

def perform_sentiment_analysis(news_file, output_folder):
    """
    Perform sentiment analysis on the headlines in the news dataset and save the results.
    
    Args:
        news_file (str): Path to the single news CSV file containing headlines.
        output_folder (str): Path to the folder where outputs will be saved.
    
    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the news data
    news_df = pd.read_csv(news_file)
    
    # Initialize VADER SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()

    # Perform sentiment analysis on each headline and store the scores
    news_df['sentiment_score'] = news_df['headline'].apply(lambda x: sia.polarity_scores(str(x))['compound'])

    # Optional: Visualize sentiment distribution
    plt.figure(figsize=(10, 6))
    news_df['sentiment_score'].hist(bins=20, color='blue', alpha=0.7)
    plt.title("Sentiment Score Distribution of Headlines")
    plt.xlabel("Sentiment Score")
    plt.ylabel("Frequency")
    plt.tight_layout()

    # Save the plot
    plot_file = os.path.join(output_folder, "sentiment_score_distribution.png")
    plt.savefig(plot_file, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"Sentiment score distribution plot saved to {plot_file}")

# Define file and folder paths
news_file = os.path.join('cleaned_data', 'raw_analyst_ratings', 'raw_analyst_ratings.csv')
output_folder = os.path.join('results', 'sentiment_analysis')

# Run sentiment analysis
perform_sentiment_analysis(news_file, output_folder)