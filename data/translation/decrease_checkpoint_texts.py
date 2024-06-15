import pickle
import os
from shutil import copyfile

def decrease_checkpoint_progress(checkpoint_file, decreased_checkpoint_file, num_texts_to_remove):
    try:
        with open(checkpoint_file, 'rb') as f:
            return_dict, processed_chunks, total_translated_texts = pickle.load(f)
        print("Checkpoint loaded successfully.")
        print(f"Total texts loaded from checkpoint: {total_translated_texts}")
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        return

    original_total_texts = total_translated_texts

    # Decrease the progress by removing the specified number of recent translated texts
    for _ in range(num_texts_to_remove):
        if total_translated_texts > 0:
            total_translated_texts -= 1
            print("Removed one translated text.")
        else:
            print("No more translated texts to remove.")
            break

    print(f"Original total translated texts: {original_total_texts}")
    print(f"Updated total translated texts: {total_translated_texts}")

    # Save the modified checkpoint
    try:
        temp_file = decreased_checkpoint_file + '.tmp'
        with open(temp_file, 'wb') as f:
            pickle.dump((dict(return_dict), list(processed_chunks), total_translated_texts), f)
        os.replace(temp_file, decreased_checkpoint_file)
        copyfile(decreased_checkpoint_file, 'decreased_backup_' + decreased_checkpoint_file)
        print("Decreased checkpoint updated successfully.")
    except Exception as e:
        print(f"Error saving updated checkpoint: {e}")

# File paths
CHECKPOINT_FILE = 'translation_checkpoint.pkl'
DECREASED_CHECKPOINT_FILE = 'translation_texts_decrease.pkl'
NUM_TEXTS_TO_REMOVE = 12  # Adjust this number as needed to remove the required number of translated texts

# Decrease the progress in the checkpoint file by removing translated texts
decrease_checkpoint_progress(CHECKPOINT_FILE, DECREASED_CHECKPOINT_FILE, NUM_TEXTS_TO_REMOVE)
