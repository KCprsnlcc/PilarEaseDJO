import pandas as pd
from tqdm import tqdm

# Define the target emotions, mapping 'joy' to 'happiness'
target_emotions = {
    'anger': 'anger',
    'disgust': 'disgust',
    'fear': 'fear',
    'joy': 'happiness',  # Map 'joy' to 'happiness'
    'sadness': 'sadness',
    'surprise': 'surprise',
    'neutral': 'neutral'
}

def process_goemotions(input_file, output_file):
    # Load the GoEmotions dataset from Hugging Face in Parquet format
    df = pd.read_parquet(input_file)
    
    # Initialize an empty list to store the filtered data
    filtered_data = []

    # Set up progress bar for iteration
    print("Processing dataset...")
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Rows processed", unit="row"):
        # Check each target emotion column in the row
        for emotion, label in target_emotions.items():
            if row[emotion] > 0:  # If emotion is present
                # Append a dictionary with Text and Label to the filtered data
                filtered_data.append({'Text': row['text'], 'Label': label})
                break  # Only take the first matching emotion

    # Convert filtered data to DataFrame
    filtered_df = pd.DataFrame(filtered_data)
    
    # Save the filtered data to CSV
    filtered_df.to_csv(output_file, index=False)
    print(f"\nFiltered dataset saved to {output_file}")
    print(f"Processing complete! {len(filtered_data)} rows matched the specified emotions.")

# Example usage
input_file = "hf://datasets/google-research-datasets/go_emotions/raw/train-00000-of-00001.parquet"
output_file = "filtered_goemotions.csv"

# Process and save the filtered GoEmotions data
process_goemotions(input_file, output_file)
