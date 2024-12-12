# Kaim Week 1

This repository contains the work for **Kaim Week 1**, focusing on data analysis, financial modeling, and sentiment analysis tasks. The project is divided into multiple tasks that progressively build a data-driven dashboard for analyzing stock market movements and their correlation with news sentiment.

## Folder Structure

```
kaim-week-1/
├── data/                # Contains datasets (stock prices, news headlines, etc.)
├── notebooks/           # Jupyter notebooks for analysis and development
├── scripts/             # Python scripts for task automation
├── requirements.txt     # List of Python dependencies
└── README.md            # Project documentation
```

## Tasks

### Task 1: Exploratory Data Analysis (EDA)
- Perform initial data exploration and visualization to understand stock price trends and distributions.
- Tools: `pandas`, `matplotlib`, `seaborn`.

### Task 2: Quantitative Analysis Using PyNance and TA-Lib
- Calculate and visualize financial indicators such as Moving Averages, RSI, and MACD.
- Tools: `TA-Lib`, `pynance`, `matplotlib`.

### Task 3: Correlation Between News and Stock Movement
- Conduct sentiment analysis on news headlines and correlate sentiment scores with stock price movements.
- Tools: `nltk`, `TextBlob`, `scipy`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/kaim-week-1.git
   cd kaim-week-1
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Getting Started

1. Ensure your environment is activated.
2. Fetch stock data using `yfinance` or load the provided datasets in the `data/` directory.
3. Run the Jupyter notebooks or scripts to perform the tasks.

## Requirements

- Python 3.8+
- Libraries:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `scipy`
  - `statsmodels`
  - `nltk`
  - `TextBlob`
  - `spacy`
  - `scikit-learn`
  - `TA-Lib`
  - `pynance`
  - `plotly`
  - `mplfinance`
  - `jupyterlab`
  - `yfinance`

## Contribution Guidelines

1. Create a new branch for each task:
   ```bash
   git checkout -b task-name
   ```
2. Commit changes with descriptive messages.
3. Push changes and create a Pull Request (PR).

## License

This project is licensed under the MIT License.
