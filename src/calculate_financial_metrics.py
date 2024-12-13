import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_financial_metrics(file_path, output_folder):
    """
    Calculate financial metrics, print values to console, create plots, and save as PNG images.

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

    # Calculate returns
    df['Returns'] = df['Close'].pct_change()

    # Calculate financial metrics
    daily_returns = df['Returns'].dropna()
    mean_return = daily_returns.mean()
    volatility = daily_returns.std()
    annualized_return = mean_return * 252  # Assuming 252 trading days in a year
    annualized_volatility = volatility * np.sqrt(252)
    
    # Sharpe Ratio (assuming risk-free rate is 0)
    sharpe_ratio = annualized_return / annualized_volatility

    # Sortino Ratio (assuming target return of 0)
    downside_returns = daily_returns[daily_returns < 0]
    sortino_ratio = annualized_return / (downside_returns.std() * np.sqrt(252))

    # Max Drawdown
    cumulative_returns = (1 + daily_returns).cumprod()
    running_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()

    # Store metrics
    financial_metrics = {
        'Sharpe Ratio': sharpe_ratio,
        'Sortino Ratio': sortino_ratio,
        'Annualized Volatility': annualized_volatility,
        'Max Drawdown': max_drawdown
    }

    # Print metrics to the console
    stock_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"\nMetrics for {stock_name}:")
    for metric, value in financial_metrics.items():
        print(f"{metric}: {value:.4f}")

    # Convert metrics to a DataFrame
    metrics_df = pd.DataFrame.from_dict(financial_metrics, orient='index', columns=['Value'])

    # Determine the stock name and create a subfolder for the stock
    stock_output_folder = os.path.join(output_folder, stock_name)
    os.makedirs(stock_output_folder, exist_ok=True)

    # Create a plot for the metrics
    fig, ax = plt.subplots(figsize=(8, 6))
    metrics_df.plot(kind='bar', legend=False, ax=ax, color='skyblue')
    ax.set_title(f'{stock_name} - Financial Metrics')
    ax.set_ylabel('Value')
    ax.set_xlabel('Metric')
    plt.xticks(rotation=45, ha='right')

    # Save the plot as a PNG file
    output_file = os.path.join(stock_output_folder, f'{stock_name}_financial_metrics.png')
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"Financial metrics plotted and saved to {output_file}")

# Define the folder paths
input_folder = os.path.join('cleaned_data', 'yfinance_data')
output_folder = os.path.join('results', 'financial_metrics')

# Apply the function to all files in the input folder
stock_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

for stock_file in stock_files:
    file_path = os.path.join(input_folder, stock_file)
    calculate_financial_metrics(file_path, output_folder)