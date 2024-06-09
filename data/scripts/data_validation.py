import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import logging
from plyer import notification

# Set up logging
logging.basicConfig(filename='emotion_validation_full.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Load the dataset
file_path = 'combined_data/emotion_datasets_predicted.csv'
df = pd.read_csv(file_path)

# Log the start of the process
logging.info('Starting full emotion validation process')

# Load the pre-trained emotion detection model
emotion_classifier = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base')

# Predict emotions for the text column with progress bar
predictions = []
confidence_scores = []
for text in tqdm(df['text'], desc="Processing"):
    result = emotion_classifier(text)[0]
    predictions.append(result['label'])
    confidence_scores.append(result['score'])

df['new_predicted_emotion'] = predictions
df['confidence_score'] = confidence_scores

# Compare the model's predictions with the existing labels
df['mismatch'] = df['new_predicted_emotion'] != df['label']

# Count the number of mismatched rows in the full dataset
mismatched_count_full = df['mismatch'].sum()

# Save the full dataset with predictions and mismatches for review
df.to_csv('combined_data/full_predictions_with_mismatches.csv', index=False)

# Log the completion of the process
logging.info(f"Number of mismatches in the full dataset: {mismatched_count_full}")
logging.info('Full emotion validation process completed')

# Send a desktop notification
notification.notify(
    title='Emotion Validation',
    message=f'Full emotion validation process completed with {mismatched_count_full} mismatches.',
    timeout=10
)

print(f"Number of mismatches in the full dataset: {mismatched_count_full}")
