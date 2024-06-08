import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

combined_csv_path = 'combined_data/emotion_datasets_overview.csv'
df = pd.read_csv(combined_csv_path)

logging.info("Loading the emotion detection model...")
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)
logging.info("Model loaded successfully.")

def predict_emotion(text):
    try:
        max_length = 512
        tokens = text.split()
        if len(tokens) > max_length:
            chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]
            results = [emotion_classifier(' '.join(chunk))[0]['label'] for chunk in chunks]
            # Aggregate results, here using the most common label as a simple approach
            result = max(set(results), key=results.count)
        else:
            result = emotion_classifier(text)[0]['label']
        return result
    except Exception as e:
        logging.error(f"Error predicting emotion for text: {text[:30]}... - {e}")
        return None

logging.info("Starting the prediction process...")
tqdm.pandas(desc="Predicting emotions")
df['label'] = df['text'].progress_apply(predict_emotion)

recategorized_csv_path = 'combined_data/emotion_datasets_predicted.csv'
df.to_csv(recategorized_csv_path, index=False)
logging.info(f"Recategorized dataset with predicted labels saved at {recategorized_csv_path}")
