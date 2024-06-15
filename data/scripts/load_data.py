import pandas as pd

combined_csv_path = 'combined_data/emotion_datasets_overview.csv'
df = pd.read_csv(combined_csv_path)

print(df.head())

print(f"Combined dataset shape: {df.shape}")
