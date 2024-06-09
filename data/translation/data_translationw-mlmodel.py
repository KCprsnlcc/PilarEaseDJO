import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm
import logging
import multiprocessing
import os

# Configure logging
logging.basicConfig(filename='translation_errors.log', level=logging.ERROR)

def translate_batch(texts, model, tokenizer):
    try:
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        return tokenizer.batch_decode(translated, skip_special_tokens=True)
    except Exception as e:
        logging.error(f"Error translating texts: {texts}\nException: {e}")
        return [None] * len(texts)

def translate_chunk(chunk, model_name, return_dict, index, progress_queue):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    translated_texts = []
    for text in chunk:
        translated_text = translate_batch([text], model, tokenizer)
        translated_texts.append(translated_text)
        progress_queue.put(1)  # Indicate that one more text has been processed
    return_dict[index] = translated_texts

def update_progress_bar(total_texts, progress_queue):
    with tqdm(total=total_texts, desc="Translating", unit=" texts") as pbar:
        for _ in range(total_texts):
            progress_queue.get()
            pbar.update(1)

def main():
    try:
        # Create a warning message in a text file
        with open('translation_in_progress.txt', 'w') as f:
            f.write("Warning: Translation process is in progress. This might take a while, feel free to leave this running while you sleep.")

        # Load the dataset from the specified file path
        dataset_path = r"C:\xampp\htdocs\PilarEaseDJO\data\scripts\combined_data\emotion_datasets_predicted.csv"
        df = pd.read_csv(dataset_path)

        # Load the translation model and tokenizer
        model_name = 'Helsinki-NLP/opus-mt-en-tl'
        num_processes = multiprocessing.cpu_count()
        chunk_size = len(df) // num_processes
        chunks = [df['text'][i:i + chunk_size].tolist() for i in range(0, len(df), chunk_size)]

        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        progress_queue = manager.Queue()
        processes = []

        print("Starting translation...")

        # Start a separate process for updating the progress bar
        pbar_process = multiprocessing.Process(target=update_progress_bar, args=(len(df), progress_queue))
        pbar_process.start()

        for index, chunk in enumerate(chunks):
            p = multiprocessing.Process(target=translate_chunk, args=(chunk, model_name, return_dict, index, progress_queue))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        # Signal the progress bar process to finish
        progress_queue.put(None)
        pbar_process.join()

        translated_texts = []
        for index in range(len(chunks)):
            translated_texts.extend(return_dict[index])

        df['text'] = [text[0] if text is not None else None for text in translated_texts]

        # Keep only the translated text and label columns
        df = df[['text', 'label']]

        export_path = r"C:\xampp\htdocs\PilarEaseDJO\data\scripts\combined_data\emotion_datasets_tagalog-predicted.csv"
        df.to_csv(export_path, index=False)

        print(f"Dataset has been successfully translated and exported to {export_path}")

        # Remove the warning message file after completion
        os.remove('translation_in_progress.txt')

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
