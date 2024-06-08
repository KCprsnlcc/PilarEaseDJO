import os
import pandas as pd
import requests
import io
import pyodbc
from tqdm import tqdm
from datasets import load_dataset
import logging

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
                dataset = load_dataset("dair-ai/emotion", split="train", trust_remote_code=True)
                dfs[name] = dataset.to_pandas()
            elif name == 'goemotions':
                dataset = load_dataset("go_emotions", split="train")
                dfs[name] = dataset.to_pandas()
            elif name == 'semeval':
                dataset = load_dataset("SemEval2018_emotion", split="train", trust_remote_code=True)
                dfs[name] = dataset.to_pandas()
            elif name == 'isear':
                conn_str = (
                    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                    rf"DBQ={url};"
                )
                conn = pyodbc.connect(conn_str)
                query = "SELECT * FROM DATA"  # Ensure we query the correct table
                dfs[name] = pd.read_sql(query, conn)
            elif name == 'meld':
                dfs[name] = pd.read_csv(url)
            else:
                dfs[name] = pd.read_csv(url)
            logging.info(f"{name} shape: {dfs[name].shape}")
            logging.info(f"{name} columns: {dfs[name].columns.tolist()}")
        except Exception as e:
            logging.error(f"Error loading {name}: {e}")
    return dfs

def extract_and_categorize_text(dfs):
    """Extract text and labels from datasets and categorize them."""
    categorized_data = []

    for name, df in dfs.items():
        logging.info(f"Processing {name} dataset")
        if name == 'crowdflower':
            for _, row in df.iterrows():
                categorized_data.append({
                    'text': row['text'], 
                    'label': 'anger' if row['anger'] else 
                             'disgust' if row['disgust'] else 
                             'fear' if row['fear'] else 
                             'joy' if row['joy'] else 
                             'neutral' if row['neutral'] else 
                             'sadness' if row['sadness'] else 
                             'surprise' if row['surprise'] else 'unknown'
                })
        elif name == 'elvis':
            for _, row in df.iterrows():
                categorized_data.append({'text': row['text'], 'label': row['label']})
        elif name == 'goemotions':
            for _, row in df.iterrows():
                for label in row['labels']:
                    categorized_data.append({'text': row['text'], 'label': label})
        elif name == 'isear':
            for _, row in df.iterrows():
                categorized_data.append({'text': row['SIT'], 'label': row['EMOT']})
        elif name == 'meld':
            for _, row in df.iterrows():
                categorized_data.append({'text': row['Utterance'], 'label': row['Emotion']})
        elif name == 'semeval':
            for _, row in df.iterrows():
                categorized_data.append({'text': row['Tweet'], 'label': row['Affect Dimension']})

    return pd.DataFrame(categorized_data)

if __name__ == "__main__":
    datasets = download_and_load_datasets(urls)
    categorized_data = extract_and_categorize_text(datasets)
    categorized_data.to_csv(os.path.join(output_dir, 'emotion_datasets_overview.csv'), index=False)
    logging.info("Combined dataset saved.")
