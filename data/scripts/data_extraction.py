import os
import pandas as pd
from datasets import load_dataset

try:
    # Load the "emotion" dataset from Hugging Face
    dataset = load_dataset("emotion", split="train")

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

    # Define the export path
    export_path = "emotion_dataset.csv"

    # Export the DataFrame to a CSV file
    df.to_csv(export_path, index=False)

    print(f"Dataset has been successfully exported to {export_path}")

except Exception as e:
    print(f"An error occurred: {e}")
