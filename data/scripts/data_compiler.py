import os
import pandas as pd
import io
import requests
from tqdm import tqdm
import time
import logging
from datasets import load_dataset
import pyodbc

# Updated URLs of the datasets
urls = {
    'crowdflower': 'crowdflower.csv',
    'elvis': None,  # Will use Hugging Face datasets
    'goemotions': None,  # Will use Hugging Face datasets
    'isear': 'C:\\xampp\\htdocs\\PilarEaseDJO\\data\\scripts\\isear_databank.mdb',  # Local Access database file
    'meld': 'https://raw.githubusercontent.com/declare-lab/MELD/master/data/MELD/train_sent_emo.csv',
    'semeval': None  # Will use Hugging Face datasets
}

output_dir = 'combined_data'
os.makedirs(output_dir, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_and_load_datasets(urls):
    """Download and load datasets from provided URLs."""
    dfs = {}
    for name, url in tqdm(urls.items(), desc="Downloading"):
        try:
            if name == 'elvis':
                dataset = load_dataset("dair-ai/emotion")
                dfs[name] = dataset['train'].to_pandas()
            elif name == 'goemotions':
                dataset = load_dataset("google-research-datasets/go_emotions")
                dfs[name] = dataset['train'].to_pandas()
            elif name == 'semeval':
                dataset = load_dataset("SemEvalWorkshop/sem_eval_2018_task_1", "subtask5.english", trust_remote_code=True)
                dfs[name] = dataset['train'].to_pandas()
            elif name == 'isear':
                conn_str = (
                    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                    rf"DBQ={url};"
                )
                conn = pyodbc.connect(conn_str)
                query = "SELECT * FROM DATA"  # Adjust the table name as needed
                dfs[name] = pd.read_sql(query, conn)
            elif name == 'meld':
                dfs[name] = pd.read_csv(url)
            else:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                dfs[name] = pd.read_csv(io.StringIO(response.text))
            logging.info(f"{name} shape: {dfs[name].shape}")
        except Exception as e:
            logging.error(f"Error loading {name}: {e}")
    return dfs

def align_columns(dfs, all_columns):
    """Align columns across all DataFrames."""
    for name, df in tqdm(dfs.items(), desc="Aligning"):
        for col in all_columns:
            if col not in df.columns:
                df[col] = 0
        logging.info(f"{name} columns after alignment: {df.columns.tolist()}")
    return dfs

def create_summary_table(dfs):
    """Create a summary table indicating the presence of emotion columns in each dataset."""
    emotion_columns = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
    summary_data = []
    
    dataset_names = {
        'crowdflower': 'Crowdflower (2016)',
        'elvis': 'Emotion Dataset, Elvis et al. (2018)',
        'goemotions': 'GoEmotions, Demszky et al. (2020)',
        'isear': 'ISEAR, Vikash (2018)',
        'meld': 'MELD, Poria et al. (2019)',
        'semeval': 'SemEval-2018, EI-reg, Mohammad et al. (2018)'
    }
    
    for name in dataset_names.keys():
        presence = ['Yes' if name == 'semeval' and col in ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise'] else '-' for col in emotion_columns]
        summary_data.append([dataset_names[name]] + presence)
    
    summary_df = pd.DataFrame(summary_data, columns=['Name'] + emotion_columns)
    return summary_df

def save_combined_dataframe(dfs, output_path):
    """Combine all DataFrames and save the result."""
    if dfs:
        combined_df = pd.concat(dfs.values(), ignore_index=True)
        combined_df.to_csv(output_path, index=False)
        logging.info(f"Combined DataFrame shape: {combined_df.shape}")
    else:
        logging.warning("No datasets loaded successfully.")

def main():
    start_time = time.time()
    
    logging.info("Downloading and loading datasets...")
    dfs = download_and_load_datasets(urls)
    download_time = time.time()
    logging.info(f"Download and load time: {download_time - start_time} seconds")
    
    if 'crowdflower' in dfs:
        logging.info("Crowdflower DataFrame Head:")
        logging.info(dfs['crowdflower'].head())
    
    all_columns = set()
    for df in dfs.values():
        all_columns.update(df.columns)
    
    logging.info("Aligning columns across DataFrames...")
    dfs = align_columns(dfs, all_columns)
    processing_time = time.time()
    logging.info(f"Processing time: {processing_time - download_time} seconds")
    
    logging.info("Creating summary table...")
    summary_df = create_summary_table(dfs)
    summary_df.to_csv(os.path.join(output_dir, 'emotion_columns_summary.csv'), index=False)
    logging.info("Summary table created:")
    logging.info(summary_df)
    
    logging.info("Saving combined DataFrame...")
    save_combined_dataframe(dfs, os.path.join(output_dir, 'combined_emotion_dataset.csv'))
    save_time = time.time()
    logging.info(f"Saving time: {save_time - processing_time} seconds")
    logging.info(f"Total execution time: {save_time - start_time} seconds")

if __name__ == "__main__":
    main()
