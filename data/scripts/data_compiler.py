import os
import pandas as pd
import io
import requests
from tqdm import tqdm
import time
import logging

# Updated URLs of the datasets (these should be verified for correctness)
urls = {
    'crowdflower': 'https://example.com/valid_crowdflower_url.csv',
    'elvis': 'https://example.com/valid_elvis_url.csv',
    'goemotions': 'https://example.com/valid_goemotions_url.tsv',
    'isear': 'https://example.com/valid_isear_url.csv',
    'meld': 'https://raw.githubusercontent.com/declare-lab/MELD/master/data/MELD/train_sent_emo.csv',
    'semeval': 'https://example.com/valid_semeval_url.csv'
}

output_dir = 'combined_data'
os.makedirs(output_dir, exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_and_load_datasets(urls):
    """Download and load datasets from provided URLs."""
    dfs = {}
    for name, url in tqdm(urls.items(), desc="Downloading"):
        try:
            if name in ['meld', 'goemotions']:
                sep = ',' if name == 'meld' else '\t'
                dfs[name] = pd.read_csv(url, sep=sep)
            else:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                dfs[name] = pd.read_csv(io.StringIO(response.text))
            logging.info(f"{name} shape: {dfs[name].shape}")
        except Exception as e:
            logging.error(f"Error loading {name}: {e}")
    return dfs

def rename_columns(df, expected_columns):
    """Rename columns of the 'crowdflower' DataFrame."""
    if len(df.columns) == len(expected_columns):
        df.columns = expected_columns
    else:
        logging.warning("Crowdflower dataset does not have the expected number of columns.")
    return df

def align_columns(dfs):
    """Align columns across all DataFrames."""
    all_columns = set()
    for df in dfs.values():
        all_columns.update(df.columns)
    
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
    
    for name, df in dfs.items():
        presence = ['Yes' if col in df.columns else '-' for col in emotion_columns]
        summary_data.append([dataset_names.get(name, name)] + presence)
    
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
        crowdflower_cols = ['text', 'anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
        dfs['crowdflower'] = rename_columns(dfs['crowdflower'], crowdflower_cols)
    else:
        logging.warning("Crowdflower dataset not loaded.")
    
    logging.info("Aligning columns across DataFrames...")
    dfs = align_columns(dfs)
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
