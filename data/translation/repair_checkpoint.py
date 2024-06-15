import pickle
import os
from shutil import copyfile

def load_checkpoint(checkpoint_file):
    try:
        with open(checkpoint_file, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        return None

def analyze_corrupted_data(return_dict):
    corrupted_texts = []
    corrupted_chunks = []
    
    for key, value in return_dict.items():
        if value is None or any(text is None for text in value):
            corrupted_texts.append(key)
            corrupted_chunks.append(processed_chunks.index(key))
    
    return corrupted_texts, corrupted_chunks

def repair_corrupted_data(return_dict, corrupted_texts):
    for text_index in corrupted_texts:
        # Implement logic to repair the corrupted data, if possible
        pass

def remove_corrupted_data(return_dict, corrupted_texts, processed_chunks):
    for text_index in corrupted_texts:
        del return_dict[text_index]
        processed_chunks.remove(text_index)

def save_repaired_checkpoint(repaired_checkpoint_file, return_dict, processed_chunks, total_translated_texts):
    try:
        with open(repaired_checkpoint_file, 'wb') as f:
            pickle.dump((return_dict, processed_chunks, total_translated_texts), f)
        print("Repaired checkpoint saved successfully.")
    except Exception as e:
        print(f"Error saving repaired checkpoint: {e}")

# File paths
CHECKPOINT_FILE = 'translation_checkpoint.pkl'
REPAIRED_CHECKPOINT_FILE = 'repaired_translation_checkpoint.pkl'

# Load checkpoint
checkpoint_data = load_checkpoint(CHECKPOINT_FILE)
if checkpoint_data is not None:
    return_dict, processed_chunks, total_translated_texts = checkpoint_data

    # Analyze corrupted data
    corrupted_texts, corrupted_chunks = analyze_corrupted_data(return_dict)

    if corrupted_texts:
        # Repair or remove corrupted data
        # Uncomment one of the following lines based on your choice
        # repair_corrupted_data(return_dict, corrupted_texts)
        remove_corrupted_data(return_dict, corrupted_texts, processed_chunks)

        # Save repaired checkpoint
        save_repaired_checkpoint(REPAIRED_CHECKPOINT_FILE, return_dict, processed_chunks, total_translated_texts)
    else:
        print("No corrupted data found in the checkpoint.")
else:
    print("Checkpoint data could not be loaded.")

