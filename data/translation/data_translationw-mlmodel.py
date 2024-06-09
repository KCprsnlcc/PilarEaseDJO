import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm
import logging
import multiprocessing
import os
import pickle

# Configure logging
logging.basicConfig(filename='translation_errors.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Checkpoint file path
CHECKPOINT_FILE = 'translation_checkpoint.pkl'

def save_checkpoint(return_dict, processed_chunks):
    temp_file = CHECKPOINT_FILE + '.tmp'
    with open(temp_file, 'wb') as f:
        pickle.dump((dict(return_dict), processed_chunks), f)
    os.replace(temp_file, CHECKPOINT_FILE)
    logging.info(f"Checkpoint saved: {len(processed_chunks)} chunks processed.")

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE) and os.path.getsize(CHECKPOINT_FILE) > 0:
        try:
            with open(CHECKPOINT_FILE, 'rb') as f:
                checkpoint = pickle.load(f)
                logging.info("Checkpoint loaded successfully.")
                return checkpoint
        except (EOFError, pickle.UnpicklingError) as e:
            logging.error(f"Checkpoint file is corrupted: {e}")
            return None, []
    return None, []

def translate_batch(texts, model, tokenizer):
    try:
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        return tokenizer.batch_decode(translated, skip_special_tokens=True)
    except Exception as e:
        logging.error(f"Error translating texts: {texts}\nException: {e}")
        return [None] * len(texts)

def translate_chunk(chunk, model_name, return_dict, index, progress_queue):
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        translated_texts = []
        for text in chunk:
            translated_text = translate_batch([text], model, tokenizer)
            translated_texts.append(translated_text[0])
            progress_queue.put((index, 1))
        return_dict[index] = translated_texts
    except Exception as e:
        logging.error(f"Error in translate_chunk for index {index}: {e}")
        return_dict[index] = [None] * len(chunk)
        for _ in chunk:
            progress_queue.put((index, 1))

def update_progress_bar(total_texts, progress_queue):
    with tqdm(total=total_texts, desc="Translating", unit=" texts") as pbar:
        completed_chunks = set()
        while True:
            item = progress_queue.get()
            if item is None:
                break
            index, count = item
            if index not in completed_chunks:
                pbar.update(count)
                completed_chunks.add(index)
                logging.info(f"Chunk {index} completed.")

def main():
    try:
        with open('translation_in_progress.txt', 'w') as f:
            f.write("Warning: Translation process is in progress. This might take a while, feel free to leave this running while you sleep.")

        dataset_path = r'C:\xampp\htdocs\PilarEaseDJO\data\scripts\combined_data\emotion_datasets_predicted.csv'
        df = pd.read_csv(dataset_path)

        model_name = 'Helsinki-NLP/opus-mt-en-tl'
        num_processes = multiprocessing.cpu_count()
        chunk_size = len(df) // num_processes
        chunks = [df['text'][i:i + chunk_size].tolist() for i in range(0, len(df), chunk_size)]

        return_dict, processed_chunks = load_checkpoint()
        if return_dict is None:
            manager = multiprocessing.Manager()
            return_dict = manager.dict()
            progress_queue = manager.Queue()
            processed_chunks = []
        else:
            manager = multiprocessing.Manager()
            progress_queue = manager.Queue()
            logging.info(f"Resuming translation from checkpoint: {len(processed_chunks)} chunks processed.")

        processes = []

        total_processed_texts = len(processed_chunks) * chunk_size

        pbar_process = multiprocessing.Process(target=update_progress_bar, args=(len(df), progress_queue))
        pbar_process.start()

        print("Starting translation...")

        for index, chunk in enumerate(chunks):
            if index in processed_chunks:
                continue
            try:
                p = multiprocessing.Process(target=translate_chunk, args=(chunk, model_name, return_dict, index, progress_queue))
                p.start()
                processes.append(p)
                processed_chunks.append(index)
                save_checkpoint(return_dict, processed_chunks)
                total_processed_texts += len(chunk)
            except Exception as e:
                logging.error(f"Error starting process for chunk {index}: {e}")

        for p in processes:
            p.join()

        if pbar_process:
            progress_queue.put(None)
            pbar_process.join()

        translated_texts = []
        for index in range(len(chunks)):
            if index in return_dict:
                translated_texts.extend(return_dict[index])
            else:
                logging.error(f"Chunk {index} missing in return_dict.")

        if len(translated_texts) != len(df):
            raise ValueError(f"Length of translated texts ({len(translated_texts)}) does not match length of original texts ({len(df)})")

        df['text'] = translated_texts

        df = df[['text', 'label']]

        export_path = r'C:\xampp\htdocs\PilarEaseDJO\data\scripts\combined_data\emotion_datasets_tagalog-predicted.csv'
        df.to_csv(export_path, index=False)

        print(f"Dataset has been successfully translated and exported to {export_path}")

        os.remove('translation_in_progress.txt')
        if os.path.exists(CHECKPOINT_FILE):
            os.remove(CHECKPOINT_FILE)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
