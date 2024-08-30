import pandas as pd
from datasets import load_dataset, Dataset, DatasetDict, concatenate_datasets
from tqdm import tqdm
from datasets import ClassLabel

# Enable tqdm progress bar for Pandas apply function
tqdm.pandas()

# 1. Load ISEAR Dataset from CSV with error handling
print("Loading ISEAR dataset...")
try:
    isear_df = pd.read_csv('isear.csv', delimiter='|', on_bad_lines='skip')  # Skips problematic lines
    print("ISEAR dataset loaded successfully.")
except Exception as e:
    print(f"Error loading ISEAR dataset: {e}")
    isear_df = pd.DataFrame()  # Create an empty DataFrame if there's an error

if not isear_df.empty:
    # 2. Preprocess ISEAR Dataset
    print("Preprocessing ISEAR dataset...")
    def map_isear_label(row):
        label_mapping = {'joy': 0, 'fear': 1, 'anger': 2, 'sadness': 3, 'disgust': 4, 'shame': 5, 'guilt': 6}
        return pd.Series({'text': row['SIT'], 'label': label_mapping.get(row['EMOT'], -1)})

    # Apply the function with progress bar
    isear_df_mapped = isear_df.progress_apply(map_isear_label, axis=1)

    # Convert the processed DataFrame to a Hugging Face Dataset
    isear_dataset = Dataset.from_pandas(isear_df_mapped)
    print("ISEAR dataset preprocessing complete.")
else:
    print("ISEAR dataset is empty or could not be loaded.")
    isear_dataset = None

# 3. Load Other Available Datasets
print("Loading GoEmotions dataset...")
go_emotions = load_dataset('go_emotions')
print("GoEmotions dataset loaded.")

print("Loading Emotion dataset...")
emotion = load_dataset('dair-ai/emotion')
print("Emotion dataset loaded.")

print("Loading DailyDialog dataset...")
daily_dialog = load_dataset('daily_dialog')
print("DailyDialog dataset loaded.")

# 4. Preprocess GoEmotions
print("Preprocessing GoEmotions dataset...")
def map_go_emotions_label(example):
    example['label'] = int(example['labels'][0]) if example['labels'] else -1
    return {'text': example['text'], 'label': example['label']}


go_emotions = go_emotions['train'].map(map_go_emotions_label, remove_columns=['id', 'labels'])
print("GoEmotions dataset preprocessing complete.")

# 5. Preprocess Emotion Dataset - Convert ClassLabel to Integer
print("Preprocessing Emotion dataset...")
def map_emotion_label(example):
    label_mapping = {'sadness': 0, 'joy': 1, 'love': 2, 'anger': 3, 'fear': 4, 'surprise': 5}
    return {'text': example['text'], 'label': int(label_mapping.get(example['label'], -1))}

# Remove the ClassLabel feature and map it to int
emotion_train = emotion['train'].map(map_emotion_label, remove_columns=['label'])

# Explicitly set the label column as int64 after mapping
emotion_train = emotion_train.cast_column("label", "int64")
print("Emotion dataset preprocessing complete.")

# 6. Preprocess DailyDialog Dataset
print("Preprocessing DailyDialog dataset...")
def map_daily_dialog_label(example):
    emotion = int(example['emotion'][0]) if isinstance(example['emotion'], list) else int(example['emotion'])
    return {'text': ' '.join(example['dialog']), 'label': emotion}


daily_dialog = daily_dialog['train'].map(map_daily_dialog_label, remove_columns=['act'])
print("DailyDialog dataset preprocessing complete.")

# 7. Convert all labels to integer type
def convert_label_to_int(example):
    example['label'] = int(example['label'])
    return example

go_emotions = go_emotions.map(convert_label_to_int)
daily_dialog = daily_dialog.map(convert_label_to_int)
if isear_dataset:
    isear_dataset = isear_dataset.map(convert_label_to_int)

# 8. Combine All Datasets if ISEAR dataset is successfully loaded
print("Combining all datasets...")
if isear_dataset:
    combined_dataset = concatenate_datasets([go_emotions, emotion_train, daily_dialog, isear_dataset])
else:
    combined_dataset = concatenate_datasets([go_emotions, emotion_train, daily_dialog])
print("All datasets combined successfully.")

# Convert to DatasetDict to keep it organized
combined_dataset = DatasetDict({"train": combined_dataset})

# Save the combined dataset for later use
print("Saving combined dataset to disk...")
combined_dataset.save_to_disk('./combined_emotion_dataset')
print("Combined dataset saved successfully.")

# Inspect the combined dataset
print("Inspecting the first record of the combined dataset:")
print(combined_dataset['train'][0])
