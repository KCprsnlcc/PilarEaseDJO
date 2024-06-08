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
            if 'text' in df.columns and 'anger' in df.columns:
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
            else:
                logging.warning(f"Expected columns not found in {name}")
        elif name == 'elvis':
            if 'text' in df.columns and 'label' in df.columns:
                for _, row in df.iterrows():
                    categorized_data.append({'text': row['text'], 'label': row['label']})
            else:
                logging.warning(f"Expected columns not found in {name}")
        elif name == 'goemotions':
            if 'text' in df.columns and 'labels' in df.columns:
                for _, row in df.iterrows():
                    for label in row['labels']:
                        categorized_data.append({'text': row['text'], 'label': label})
            else:
                logging.warning(f"Expected columns not found in {name}")
        elif name == 'isear':
            if 'SIT' in df.columns and 'EMOT' in df.columns:
                for _, row in df.iterrows():
                    categorized_data.append({'text': row['SIT'], 'label': row['EMOT']})
            else:
                logging.warning(f"Expected columns not found in {name}")
        elif name == 'meld':
            if 'Utterance' in df.columns and 'Emotion' in df.columns:
                for _, row in df.iterrows():
                    categorized_data.append({'text': row['Utterance'], 'label': row['Emotion']})
            else:
                logging.warning(f"Expected columns not found in {name}")
        elif name == 'semeval':
            if 'Tweet' in df.columns and 'Affect Dimension' in df.columns:
                for _, row in df.iterrows():
                    categorized_data.append({'text': row['Tweet'], 'label': row['Affect Dimension']})
            else:
                logging.warning(f"Expected columns not found in {name}")

    return pd.DataFrame(categorized_data)

if __name__ == "__main__":
    datasets = download_and_load_datasets(urls)
    categorized_data = extract_and_categorize_text(datasets)
    combined_csv_path = os.path.join(output_dir, 'emotion_datasets_overview.csv')
    categorized_data.to_csv(combined_csv_path, index=False)
    logging.info(f"Combined dataset saved at {combined_csv_path}")
