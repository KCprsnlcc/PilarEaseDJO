import pandas as pd
import requests
import io
from datasets import load_dataset
import pyodbc
import os

# Define the URLs of the datasets
urls = {
    'crowdflower': 'https://query.data.world/s/cx25qqyvwdn4os2ljtbs2tm6p3apr5?dws=00000',
    'elvis': 'https://huggingface.co/datasets/dair-ai/emotion',
    'goemotions': 'https://huggingface.co/datasets/google-research-datasets/go_emotions',
    'isear': r'C:\xampp\htdocs\PilarEaseDJO\data\scripts\isear_databank.mdb',  # Local Access database file
    'meld': 'https://raw.githubusercontent.com/declare-lab/MELD/master/data/MELD/train_sent_emo.csv',
    'semeval': 'https://huggingface.co/datasets/SemEvalWorkshop/sem_eval_2018_task_1'
}

# Define the required columns
required_columns = ['text', 'anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']

def download_and_load_datasets(urls):
    dfs = {}
    for name, url in urls.items():
        try:
            if name in ['elvis', 'goemotions', 'semeval']:
                dataset = load_dataset(url)
                dfs[name] = dataset['train'].to_pandas()
            elif name == 'isear':
                conn_str = (
                    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                    rf"DBQ={url};"
                )
                conn = pyodbc.connect(conn_str)
                query = "SELECT * FROM DATA"  # Adjust the table name as needed
                dfs[name] = pd.read_sql(query, conn)
            else:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                dfs[name] = pd.read_csv(io.StringIO(response.text))
            print(f"{name} dataset loaded with shape: {dfs[name].shape}")
        except Exception as e:
            print(f"Error loading {name} dataset: {e}")
    return dfs

def process_datasets(dfs, required_columns):
    for name, df in dfs.items():
        # Check if the required columns exist in the dataset
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Missing columns in {name} dataset: {missing_columns}")
            # Add missing columns with default values if necessary
            for col in missing_columns:
                df[col] = 0
        # Ensure only the required columns are present
        dfs[name] = df[required_columns]
    return dfs

def main():
    output_dir = r'C:\xampp\htdocs\PilarEaseDJO\data\scripts\combined_data'
    os.makedirs(output_dir, exist_ok=True)

    # Download and load datasets
    dfs = download_and_load_datasets(urls)

    # Process datasets to ensure they have the required columns
    dfs = process_datasets(dfs, required_columns)

    # Combine all datasets into a single DataFrame
    combined_df = pd.concat(dfs.values(), ignore_index=True)
    
    # Save the combined DataFrame to a new CSV file
    output_path = os.path.join(output_dir, 'updated_combined_emotion_dataset.csv')
    combined_df.to_csv(output_path, index=False)
    print(f"Updated dataset saved to {output_path}")

if __name__ == "__main__":
    main()
