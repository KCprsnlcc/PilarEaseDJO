import os
import pandas as pd
import io
import requests
from tqdm import tqdm
import time

urls = {
    'crowdflower': 'https://raw.githubusercontent.com/crowdflower/text_emotion/master/text_emotion.csv',
    'elvis': 'https://raw.githubusercontent.com/dair-ai/emotion_dataset/master/emotion.csv',
    'goemotions': 'https://raw.githubusercontent.com/google-research/goemotions/master/data/train.tsv',
    'isear': 'https://raw.githubusercontent.com/dalopez98/isear-dataset/master/isear.csv',
    'meld': 'https://raw.githubusercontent.com/declare-lab/MELD/master/data/MELD/train_sent_emo.csv',
    'semeval': 'https://raw.githubusercontent.com/SemEval2021-TASK1/dataset/master/dataset.csv'
}

output_dir = 'combined_data'
os.makedirs(output_dir, exist_ok=True)

dfs = {}
start_time = time.time()

print("Downloading and loading datasets...")
for name, url in tqdm(urls.items(), desc="Downloading"):
    try:
        if name == 'meld':
            dfs[name] = pd.read_csv(url, sep=',')
        elif name == 'goemotions':
            dfs[name] = pd.read_csv(url, sep='\t')
        else:
            response = requests.get(url)
            if response.status_code == 200:
                dfs[name] = pd.read_csv(io.StringIO(response.text))
                print(f"{name} shape:", dfs[name].shape)
            else:
                print(f"Failed to load {name}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error loading {name}: {e}")
download_time = time.time()
print(f"Download and load time: {download_time - start_time} seconds")

if 'crowdflower' in dfs:
    print("Crowdflower DataFrame Head:")
    print(dfs['crowdflower'].head())
else:
    print("Crowdflower dataset not loaded.")

crowdflower_cols = ['text', 'anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
print("Expected columns for Crowdflower:", crowdflower_cols)

if 'crowdflower' in dfs:
    dfs['crowdflower'].columns = crowdflower_cols

all_columns = set()
for df in dfs.values():
    all_columns.update(df.columns)

# Progress bar for aligning columns across all DataFrames
print("Aligning columns across DataFrames...")
for name, df in tqdm(dfs.items(), desc="Aligning"):
    for col in all_columns:
        if col not in df.columns:
            df[col] = 0
    print(f"{name} columns after alignment:", df.columns.tolist())

processing_time = time.time()
print(f"Processing time: {processing_time - download_time} seconds")

if dfs:
    combined_df = pd.concat(dfs.values(), ignore_index=True)
    combined_df.to_csv(os.path.join(output_dir, 'combined_emotion_dataset.csv'), index=False)
    print("Combined DataFrame shape:", combined_df.shape)
else:
    print("No datasets loaded successfully.")

save_time = time.time()
print(f"Saving time: {save_time - processing_time} seconds")
print(f"Total execution time: {save_time - start_time} seconds")
