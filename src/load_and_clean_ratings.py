import gdown
import pandas as pd
from dateutil import parser
import os

def download_from_gdrive(file_id, output_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)

def load_and_clean_data():

    file_ids = {
        "raw_analyst_ratings": "1AM3ksWQGfdOklFd1H9x8h25Zra-cmWMD"
    }

    # Define local paths to save the data temporarily
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_analyst_ratings'))
    os.makedirs(base_path, exist_ok=True)  
    
    # Define file paths for each dataset
    data_path = os.path.join(base_path, 'raw_analyst_ratings.csv')

    # Download files only if they don't exist
    if not os.path.exists(data_path):
        print("Downloading data...")
        download_from_gdrive(file_ids["raw_analyst_ratings"], data_path)
    
    # Load the data (after confirming they are downloaded)
    data = pd.read_csv(data_path)

    """ 
    # Print the first few rows to verify successful load
        print(data.head())
    """

    data['date'] = data['date'].apply(lambda x: parser.parse(x, fuzzy=True, ignoretz=True))

    # Drop the Unnamed column
    data = data.drop(columns=['Unnamed: 0'])

    # Define local paths to save the data temporarily
    cleaned_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cleaned_data', 'raw_analyst_ratings'))
    os.makedirs(cleaned_path, exist_ok=True)  

    # Save the cleaned data to a new CSV file
    cleaned_data_path = os.path.join(cleaned_path, 'raw_analyst_ratings.csv')
    data.to_csv(cleaned_data_path, index=False)  # Save without the index column

    """
    # Check the data types of the columns
    print(data.dtypes)

    # Check for missing data
    print(data.isnull().sum())
    """

load_and_clean_data()
