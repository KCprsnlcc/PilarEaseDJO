import os
import pandas as pd
from datasets import load_dataset
from deep_translator import GoogleTranslator
from tqdm import tqdm

try:
    # Load the "emotion" dataset from Hugging Face
    dataset = load_dataset("emotion", split="train", trust_remote_code=True)

    # Define the id2label mapping
    id2label = {
        0: "anger",
        1: "disgust",
        2: "fear",
        3: "joy",
        4: "neutral",
        5: "sadness",
        6: "surprise"
    }

    # Convert the dataset to a Pandas DataFrame
    df = pd.DataFrame(dataset)

    # Map the labels to the corresponding string values using id2label
    df['label'] = df['label'].map(id2label)

    # Initialize the translator
    translator = GoogleTranslator(source='en', target='tl')

    # Translate each text entry to Tagalog with progress monitoring
    print("Starting translation...")
    df['text_tl'] = [translator.translate(text) for text in tqdm(df['text'], desc="Translating", unit=" texts")]
    print("Translation completed.")

    # Define the export path
    export_path = "emotion_dataset_tl.csv"

    # Export the DataFrame to a CSV file
    df.to_csv(export_path, index=False)

    print(f"Dataset has been successfully translated and exported to {export_path}")

except Exception as e:
    print(f"An error occurred: {e}")
