import pandas as pd
import os
import matplotlib.pyplot as plt
from collections import Counter

def analyze_publishers(file_path, publisher_column='publisher', email_column=None, category_column=None):
    """
    Analyzes publisher contributions to the news feed and identifies trends based on publisher type.

    Args:
        file_path (str): Path to the CSV file containing the data.
        publisher_column (str): Column name containing publisher names.
        email_column (str, optional): If publishers are email addresses, the column with emails.
        category_column (str, optional): Column name containing news categories or types.

    Returns:
        None
    """
    # Create the 'results/publisher_analysis' folder if it doesn't exist
    os.makedirs('results/publisher_analysis', exist_ok=True)

    # Load the dataset
    df = pd.read_csv(file_path)

    # Check if the necessary columns exist
    if publisher_column not in df.columns:
        print(f"Error: '{publisher_column}' column not found in the dataset.")
        return

    # 1. Identify Top Publishers (Most Frequent Publications) using Counter
    print("Identifying top publishers using Counter...")
    publisher_counts = Counter(df[publisher_column])
    top_publishers = publisher_counts.most_common(10)  # Get the top 10 publishers
    print("Top Publishers:\n", top_publishers)

    # Convert publisher counts into a pandas Series for plotting
    publisher_series = pd.Series(dict(top_publishers))

    # Plot the top publishers by count
    plt.figure(figsize=(12, 6))
    publisher_series.plot(kind='bar', color='skyblue', title='Top Publishers by Publication Count')
    plt.xlabel('Publisher')
    plt.ylabel('Number of Articles')
    plt.tight_layout()
    plt.savefig('results/publisher_analysis/top_publishers_by_count.png', dpi=300)

    # 2. Identify Types of News Reported by Each Publisher (if category_column exists)
    if category_column and category_column in df.columns:
        print("Analyzing the types of news each publisher reports...")
        publisher_categories = df.groupby([publisher_column, category_column]).size().unstack(fill_value=0)
        print("Publisher-Category Breakdown:\n", publisher_categories)

        # Plot publisher vs. category
        publisher_categories.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='viridis', title='Publisher vs Category')
        plt.xlabel('Publisher')
        plt.ylabel('Number of Articles by Category')
        plt.tight_layout()
        plt.savefig('results/publisher_analysis/publisher_vs_category.png', dpi=300)

    # 3. If email addresses are used as publisher names, identify unique domains using Counter
    if email_column and email_column in df.columns:
        print("Extracting unique email domains from publishers using Counter...")
        df['domain'] = df[email_column].str.extract(r'@([A-Za-z0-9.-]+)')[0]
        
        # Count the occurrences of each domain using Counter
        domain_counts = Counter(df['domain'])
        top_domains = domain_counts.most_common(10)  # Get the top 10 domains
        print("Top Email Domains:\n", top_domains)

        # Convert domain counts into a pandas Series for plotting
        domain_series = pd.Series(dict(top_domains))

        # Plot the email domains contributing to the publications
        plt.figure(figsize=(12, 6))
        domain_series.plot(kind='bar', color='lightcoral', title='Top Email Domains by Publication Count')
        plt.xlabel('Domain')
        plt.ylabel('Number of Articles')
        plt.tight_layout()
        plt.savefig('results/publisher_analysis/top_email_domains_by_count.png', dpi=300)


# Define the file path
file_path = os.path.join('cleaned_data', 'raw_analyst_ratings', 'raw_analyst_ratings.csv')

# Example function call for publishers
analyze_publishers(file_path, publisher_column='publisher', email_column='publisher_email', category_column='category')