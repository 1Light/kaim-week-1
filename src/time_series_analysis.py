import pandas as pd
import os
import matplotlib.pyplot as plt
from dateutil import parser
import seaborn as sns

def analyze_publication_frequency(file_path, timestamp_column='date', threshold_factor=3):
    """
    Analyzes publication frequency over time and detects patterns in publishing times.

    Args:
        file_path (str): Path to the CSV file containing the data.
        timestamp_column (str): Column name containing timestamps.
        threshold_factor (float): Factor for detecting spikes (default is 3 standard deviations above mean).

    Returns:
        None
    """
    # Create the 'results/time_series_analysis' folder if it doesn't exist
    os.makedirs('results/time_series_analysis', exist_ok=True)

    # Load the dataset
    df = pd.read_csv(file_path)

    df[timestamp_column] = pd.to_datetime(df[timestamp_column], errors='coerce')

    # Check if the timestamp column exists
    if timestamp_column not in df.columns:
        print(f"Error: '{timestamp_column}' column not found in the dataset.")
        return
    
    # Extract useful time-based features
    df['date'] = pd.to_datetime(df[timestamp_column])
    df['hour'] = df[timestamp_column].dt.hour
    df['day_of_week'] = df[timestamp_column].dt.day_name()

    # 1. Publication frequency over time
    print("Analyzing publication frequency over time...")
    df_daily = df.groupby('date').size()
    plt.figure(figsize=(12, 6))
    df_daily.plot(kind='line', title='Publication Frequency Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.tight_layout()
    plt.savefig('results/time_series_analysis/publication_frequency_over_time.png', dpi=300)

    # 2. Detect spikes in publication frequency
    print("Detecting spikes in publication frequency...")
    threshold = df_daily.mean() + threshold_factor * df_daily.std()
    spikes = df_daily[df_daily > threshold]
    print("Spike dates:", spikes)

    """ 
    # Plot spikes in a separate graph
    plt.figure(figsize=(12, 6))
    spikes.plot(kind='bar', color='red', title='Publication Frequency Spikes')
    plt.axhline(y=threshold, color='orange', linestyle='--', label=f'Threshold ({threshold_factor}σ)')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles (Spikes)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/time_series_analysis/publication_frequency_spikes.png', dpi=300)
    """

    # 3. Analyze hourly publication patterns
    print("Analyzing publication patterns by hour of day...")
    hourly_counts = df.groupby('hour').size()
    plt.figure(figsize=(12, 6))
    hourly_counts.plot(kind='bar', color='skyblue', title='Publication Frequency by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Articles')
    plt.xticks(range(0, 24))
    plt.tight_layout()
    plt.savefig('results/time_series_analysis/publication_frequency_by_hour.png', dpi=300)

    # 4. Weekly trends
    print("Analyzing weekly publication patterns...")
    day_of_week_counts = df.groupby('day_of_week').size().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )
    plt.figure(figsize=(10, 5))
    sns.barplot(x=day_of_week_counts.index, y=day_of_week_counts.values, palette='viridis', hue=None, legend=False)
    plt.title('Publication Frequency by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Articles')
    plt.tight_layout()
    plt.savefig('results/time_series_analysis/publication_frequency_by_day_of_week.png', dpi=300)

# Define the file path
file_path = os.path.join('cleaned_data', 'raw_analyst_ratings', 'raw_analyst_ratings.csv')

analyze_publication_frequency(file_path)