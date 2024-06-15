import pandas as pd
import pickle
import os

CHECKPOINT_FILE = 'translation_checkpoint.pkl'

def save_progress(df, translated_texts):
    checkpoint_data = {
        'df': df,
        'translated_texts': translated_texts
    }
    with open(CHECKPOINT_FILE, 'wb') as f:
        pickle.dump(checkpoint_data, f)
    print("Progress saved.")

def load_progress():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'rb') as f:
            checkpoint_data = pickle.load(f)
        return checkpoint_data['df'], checkpoint_data['translated_texts']
    return None, None

# Example usage:
# Call save_progress() periodically within your existing script to save current progress.
