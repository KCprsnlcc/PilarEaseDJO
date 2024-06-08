import pandas as pd
from datasets import load_dataset
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm

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

    df = pd.DataFrame(dataset)

    df['label'] = df['label'].map(id2label)

    model_name = 'Helsinki-NLP/opus-mt-en-tl'
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    def translate_to_tagalog(text):
        translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))
        return tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

    print("Starting translation...")
    df['text_tl'] = [translate_to_tagalog(text) for text in tqdm(df['text'], desc="Translating", unit=" texts")]
    print("Translation completed.")

    export_path = "emotion_dataset_tl-w-ml.csv"

    df.to_csv(export_path, index=False)

    print(f"Dataset has been successfully translated and exported to {export_path}")

except Exception as e:
    print(f"An error occurred: {e}")
