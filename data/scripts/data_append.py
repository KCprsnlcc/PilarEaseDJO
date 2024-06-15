import os
import pandas as pd
import pyodbc
from tqdm import tqdm
from datasets import load_dataset
import logging

# Updated paths and URLs of the datasets
urls = {
    'crowdflower': 'C:\\xampp\\htdocs\\PilarEaseDJO\\data\\scripts\\crowdflower.csv',
    'elvis': None,  # Will use Hugging Face datasets
    'goemotions': None,  # Will use Hugging Face datasets
    'isear': 'C:\\xampp\\htdocs\\PilarEaseDJO\\data\\scripts\\isear_databank.mdb',  # Local Access database file
    'meld': 'https://raw.githubusercontent.com/declare-lab/MELD/master/data/MELD/train_sent_emo.csv',
    'semeval': 'C:\\xampp\\htdocs\\PilarEaseDJO\\data\\scripts\\SemEvalWorkshopsem_eval_2018_task_1.txt'  # Local file
}

output_dir = 'combined_data'
os.makedirs(output_dir, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def verify_file_paths(urls):
    """Verify if the file paths are valid."""
    for name, url in urls.items():
        if url and name in ['crowdflower', 'isear', 'semeval'] and not os.path.exists(url):
            logging.error(f"File for {name} not found at {url}")
            return False
    return True

def download_and_load_datasets(urls):
    """Download and load datasets from provided URLs."""
    dfs = {}
    for name, url in tqdm(urls.items(), desc="Downloading datasets"):
        try:
            logging.info(f"Loading dataset: {name}")
            if name == 'elvis':
                dataset = load_dataset("dair-ai/emotion")
                dfs[name] = dataset['train'].to_pandas()
            elif name == 'goemotions':
                dataset = load_dataset("google-research-datasets/go_emotions")
                dfs[name] = dataset['train'].to_pandas()
            elif name == 'semeval':
                dfs[name] = pd.read_csv(url, delimiter='\t')
            elif name == 'isear':
                # Debugging: Print the connection string
                conn_str = (
                    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                    rf"DBQ={url};"
                )
                logging.info(f"Connecting to Access DB with: {conn_str}")
                conn = pyodbc.connect(conn_str)
                query = "SELECT * FROM DATA"
                dfs[name] = pd.read_sql(query, conn)
            elif name == 'meld':
                dfs[name] = pd.read_csv(url)
            elif name == 'crowdflower':
                dfs[name] = pd.read_csv(url)
            logging.info(f"{name} shape: {dfs[name].shape}")
        except Exception as e:
            logging.error(f"Error loading {name}: {e}")
    return dfs

def extract_and_categorize_text(dfs):
    """Extract text and labels from datasets and categorize them."""
    categorized_data = []

    for name, df in tqdm(dfs.items(), desc="Processing datasets"):
        logging.info(f"Processing {name} dataset")
        if name == 'crowdflower':
            for _, row in df.iterrows():
                categorized_data.append({
                    'text': row['content'], 
                    'label': row['sentiment']
                })
        elif name == 'elvis':
            for _, row in df.iterrows():
                categorized_data.append({'text': row['text'], 'label': row['label']})
        elif name == 'goemotions':
            for _, row in df.iterrows():
                categorized_data.append({'text': row['text'], 'label': row['labels']})
        elif name == 'isear':
            for _, row in df.iterrows():
                categorized_data.append({'text': row['SIT'], 'label': row['EMOT']})
        elif name == 'meld':
            for _, row in df.iterrows():
                categorized_data.append({'text': row['Utterance'], 'label': row['Emotion']})
        elif name == 'semeval':
            for _, row in df.iterrows():
                emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'love', 'optimism', 'pessimism', 'sadness', 'surprise', 'trust']
                for emotion in emotions:
                    if row[emotion]:
                        categorized_data.append({'text': row['Tweet'], 'label': emotion})

    return pd.DataFrame(categorized_data)

if __name__ == "__main__":
    logging.info("Starting dataset processing")
    if verify_file_paths(urls):
        datasets = download_and_load_datasets(urls)
        categorized_data = extract_and_categorize_text(datasets)
        combined_csv_path = os.path.join(output_dir, 'emotion_datasets_overview.csv')
        categorized_data.to_csv(combined_csv_path, index=False)
        logging.info(f"Combined dataset saved at {combined_csv_path}")
        logging.info("Dataset processing completed successfully")
    else:
        logging.error("One or more file paths are invalid. Please check the file paths and try again.")
