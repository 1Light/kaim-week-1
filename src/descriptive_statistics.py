import pandas as pd
import os
import matplotlib.pyplot as plt

def generate_headline_length_stats_image(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Check dataset size
    print(f"Total rows in DataFrame: {df.shape[0]}")

    # Remove null and duplicate rows
    df = df[df['headline'].notnull()].drop_duplicates()

    # Check for unexpected duplicates or nulls
    print(f"Duplicate rows after cleanup: {df.duplicated().sum()}")
    print(f"Null values in 'headline': {df['headline'].isnull().sum()}")

    # Step 1: Calculate headline length
    df['headline_length'] = df['headline'].apply(len)

    # Step 2: Descriptive Statistics on headline length
    headline_length_stats = df['headline_length'].describe()

    # Prepare data for tabulation
    statistics = {
        "Statistic": headline_length_stats.index.tolist(),
        "Headline Length": headline_length_stats.values.tolist()
    }

    # Create a DataFrame from the statistics dictionary
    df_stats = pd.DataFrame(statistics)
    print(df_stats)

    # Create the 'results/descriptive_statistics' folder if it doesn't exist
    os.makedirs('results/descriptive_statistics', exist_ok=True)

    # Create a plot and add the table
    fig, ax = plt.subplots(figsize=(8, 4))  # Set the figure size
    ax.axis('off')  # Hide the axes

    # Render the table into the plot
    table = ax.table(cellText=df_stats.values, colLabels=df_stats.columns, loc='center', cellLoc='center', colColours=['#f5f5f5']*2)

    # Save the table as an image
    plt.tight_layout()  # Adjust layout to avoid cutting off labels
    plt.savefig('results/descriptive_statistics/headline_length_stats.png', bbox_inches='tight', dpi=300)


def count_articles_per_publisher(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Step 1: Count the number of articles per publisher
    publisher_counts = df['publisher'].value_counts()

    # Step 2: Get the top 10 publishers with the most articles
    top_10_publishers = publisher_counts.head(10)
    print(top_10_publishers)

    # Step 3: Create a bar plot for the top 10 publisher counts
    fig, ax = plt.subplots(figsize=(10, 6))  # Set the figure size
    top_10_publishers.plot(kind='bar', ax=ax, color='#6fa3ef')  # Bar chart with custom color
    ax.set_title('Top 10 Publishers by Number of Articles')
    ax.set_xlabel('Publisher')
    ax.set_ylabel('Number of Articles')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")  # Rotate labels for readability

    # Create the 'results/descriptive_statistics' folder if it doesn't exist
    os.makedirs('results/descriptive_statistics', exist_ok=True)

    # Save the plot as an image in the specified folder
    plt.tight_layout()  # Adjust layout to avoid cutting off labels
    plt.savefig('results/descriptive_statistics/articles_per_publisher.png', dpi=300)


def analyze_publication_dates_over_time(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Step 2: Extract the date (or other time components) for analysis
    # You can choose the level of granularity for the analysis, e.g., by day, month, or year
    df['publication_day'] = df['date'].dt.date  # Extract day (or use .dt.month/.dt.year)

    # Step 3: Count the number of articles published per day
    daily_publication_counts = df['publication_day'].value_counts().sort_index()

    # Step 4: Create a plot to visualize trends over time (articles per day)
    fig, ax = plt.subplots(figsize=(10, 6))  # Set the figure size
    daily_publication_counts.plot(kind='line', ax=ax, color='#6fa3ef', marker='o')  # Line plot with markers
    ax.set_title('Number of Articles Published per Day Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Articles')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")  # Rotate labels for readability

    # Create the 'results/descriptive_statistics' folder if it doesn't exist
    os.makedirs('results/descriptive_statistics', exist_ok=True)

    # Save the plot as an image in the specified folder
    plt.tight_layout()  # Adjust layout to avoid cutting off labels
    plt.savefig('results/descriptive_statistics/articles_per_day.png', dpi=300)

def analyze_publication_dates_per_week(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Step 1: Ensure 'date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Step 2: Check if the conversion was successful and handle any issues
    if df['date'].isnull().any():
        print(f"Warning: Some rows have invalid or missing publication dates ({df['date'].isnull().sum()} rows).")

    # Step 3: Extract the day of the week from the 'date' column
    # .dt.weekday: Monday=0, Tuesday=1, ..., Sunday=6
    df['publication_day_of_week'] = df['date'].dt.weekday  # Monday = 0, Sunday = 6

    # Step 4: Map weekdays to names (optional for readability)
    weekday_map = {
        0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'
    }
    df['weekday_name'] = df['publication_day_of_week'].map(weekday_map)

    # Step 5: Count the number of articles published per day of the week
    weekday_publication_counts = df['weekday_name'].value_counts().sort_index()

    # Step 6: Create a plot to visualize trends over the days of the week
    fig, ax = plt.subplots(figsize=(10, 6))  # Set the figure size
    weekday_publication_counts.plot(kind='bar', ax=ax, color='#6fa3ef')  # Bar plot for days of the week
    ax.set_title('Number of Articles Published per Day of the Week')
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Number of Articles')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")  # Rotate labels for readability

    # Create the 'results/descriptive_statistics' folder if it doesn't exist
    os.makedirs('results/descriptive_statistics', exist_ok=True)

    # Save the plot as an image in the specified folder
    plt.tight_layout()  # Adjust layout to avoid cutting off labels
    plt.savefig('results/descriptive_statistics/articles_per_weekday.png', dpi=300)

# Define the file path
file_path = os.path.join('cleaned_data', 'raw_analyst_ratings', 'raw_analyst_ratings.csv')

# Call the function to analyze the publication dates and save the plot
generate_headline_length_stats_image(file_path)