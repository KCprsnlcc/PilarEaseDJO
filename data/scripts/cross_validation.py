import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import logging
from plyer import notification

# Set up logging
logging.basicConfig(filename='emotion_validation.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Load the dataset
file_path = 'combined_data/emotion_datasets_predicted.csv'
df = pd.read_csv(file_path)

# Log the start of the process
logging.info('Starting emotion validation process')

# Load the pre-trained emotion detection model
emotion_classifier = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base')

# Apply the model to a subset of the dataset for validation
subset_size = 1000  # Subset size for demonstration
df_subset = df.head(subset_size)

# Predict emotions for the text column with progress bar
predictions = []
confidence_scores = []
for text in tqdm(df_subset['text'], desc="Processing"):
    result = emotion_classifier(text)[0]
    predictions.append(result['label'])
    confidence_scores.append(result['score'])

df_subset['new_predicted_emotion'] = predictions
df_subset['confidence_score'] = confidence_scores

# Compare the model's predictions with the existing labels
df_subset['mismatch'] = df_subset['new_predicted_emotion'] != df_subset['label']

# Count the number of mismatched rows in the subset
mismatched_count_subset = df_subset['mismatch'].sum()

# Save the subset with predictions and mismatches for review
df_subset.to_csv('combined_data/subset_predictions_with_mismatches.csv', index=False)

# Log the completion of the process
logging.info(f"Number of mismatches in the subset: {mismatched_count_subset}")
logging.info('Emotion validation process completed')

# Display mismatched rows for manual review
mismatched_rows_subset = df_subset[df_subset['mismatch']]

# Send a desktop notification
notification.notify(
    title='Emotion Validation',
    message=f'Emotion validation process completed with {mismatched_count_subset} mismatches.',
    timeout=10
)

import ace_tools as tools; tools.display_dataframe_to_user(name="Subset Predictions with Mismatches", dataframe=mismatched_rows_subset)
