import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm
import logging
import multiprocessing
import os
import pickle
from shutil import copyfile
import time
import signal
import traceback
<<<<<<< HEAD
=======
import threading
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5

# Configure logging
logging.basicConfig(filename='translation_errors.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Constants
CHECKPOINT_FILE = 'translation_checkpoint.pkl'
BACKUP_CHECKPOINT_FILE = 'translation_checkpoint_backup.pkl'
CACHE_DIR = './model_cache'
CHECKPOINT_INTERVAL = 90  # Save checkpoint every 90 seconds

# Global variables for process references
checkpoint_process = None
pbar_process = None
chunk_pbar_process = None
progress_queue = None
processed_chunks_queue = None
return_dict = None
processed_chunks = None
total_translated_texts = 0
<<<<<<< HEAD
=======
error_log = []
terminate_signal_received = multiprocessing.Event()

def validate_checkpoint(checkpoint):
    """ Validate the checkpoint structure and content. """
    try:
        if not isinstance(checkpoint, tuple) or len(checkpoint) != 3:
            raise ValueError("Checkpoint is not a valid tuple of length 3.")
        return_dict, processed_chunks, total_translated_texts = checkpoint
        if not isinstance(return_dict, dict):
            raise ValueError("return_dict is not a dictionary.")
        if not isinstance(processed_chunks, list):
            raise ValueError("processed_chunks is not a list.")
        if not isinstance(total_translated_texts, int):
            raise ValueError("total_translated_texts is not an integer.")
        return True
    except Exception as e:
        logging.error(f"Checkpoint validation failed: {e}")
        return False
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5

def save_checkpoint(return_dict, processed_chunks, total_translated_texts):
    try:
        temp_file = CHECKPOINT_FILE + '.tmp'
        with open(temp_file, 'wb') as f:
            pickle.dump((dict(return_dict), list(processed_chunks), total_translated_texts), f)
        os.replace(temp_file, CHECKPOINT_FILE)
        copyfile(CHECKPOINT_FILE, BACKUP_CHECKPOINT_FILE)
        logging.info(f"Checkpoint saved: {len(processed_chunks)} chunks processed.")
        logging.info(f"Total texts saved in checkpoint: {total_translated_texts}")
        logging.debug(f"Checkpoint content saved: return_dict keys={list(return_dict.keys())}, processed_chunks={list(processed_chunks)}, total_translated_texts={total_translated_texts}")
    except Exception as e:
        logging.error(f"Error saving checkpoint: {e}\nTraceback: {traceback.format_exc()}")

def load_checkpoint():
    try:
        if os.path.exists(CHECKPOINT_FILE) and os.path.getsize(CHECKPOINT_FILE) > 0:
            with open(CHECKPOINT_FILE, 'rb') as f:
                checkpoint = pickle.load(f)
<<<<<<< HEAD
                print(f"Checkpoint content: {checkpoint}")
                logging.info("Checkpoint loaded successfully.")
                logging.info(f"Total texts loaded from checkpoint: {checkpoint[2]}")
                logging.debug(f"Checkpoint content loaded: {checkpoint}")
                return checkpoint
        logging.warning("Checkpoint file does not exist or is empty.")
        return None, [], 0
    except (EOFError, pickle.UnpicklingError) as e:
        logging.error(f"Primary checkpoint file is corrupted: {e}\nTrying to load backup checkpoint.")
=======
                if validate_checkpoint(checkpoint):
                    logging.info("Checkpoint loaded successfully.")
                    logging.info(f"Total texts loaded from checkpoint: {checkpoint[2]}")
                    logging.debug(f"Checkpoint content loaded: {checkpoint}")
                    return checkpoint
                else:
                    raise ValueError("Invalid checkpoint structure.")
        logging.warning("Checkpoint file does not exist or is empty.")
        return None, [], 0
    except (EOFError, pickle.UnpicklingError, ValueError) as e:
        logging.error(f"Primary checkpoint file is corrupted or invalid: {e}\nTrying to load backup checkpoint.")
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
        if os.path.exists(BACKUP_CHECKPOINT_FILE) and os.path.getsize(BACKUP_CHECKPOINT_FILE) > 0:
            try:
                with open(BACKUP_CHECKPOINT_FILE, 'rb') as f:
                    checkpoint = pickle.load(f)
<<<<<<< HEAD
                    print(f"Backup checkpoint content: {checkpoint}")
                    logging.info("Backup checkpoint loaded successfully.")
                    logging.info(f"Total texts loaded from backup checkpoint: {checkpoint[2]}")
                    logging.debug(f"Backup checkpoint content loaded: {checkpoint}")
                    return checkpoint
            except (EOFError, pickle.UnpicklingError) as e:
                logging.error(f"Backup checkpoint file is also corrupted: {e}")
=======
                    if validate_checkpoint(checkpoint):
                        logging.info("Backup checkpoint loaded successfully.")
                        logging.info(f"Total texts loaded from backup checkpoint: {checkpoint[2]}")
                        logging.debug(f"Backup checkpoint content loaded: {checkpoint}")
                        return checkpoint
                    else:
                        raise ValueError("Invalid backup checkpoint structure.")
            except (EOFError, pickle.UnpicklingError, ValueError) as e:
                logging.error(f"Backup checkpoint file is also corrupted or invalid: {e}")
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
        return None, [], 0

def translate_batch(texts, model, tokenizer, return_dict, processed_chunks, total_translated_texts):
    try:
<<<<<<< HEAD
=======
        if texts is None:
            raise ValueError("Input texts are None.")
        
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        translations = tokenizer.batch_decode(translated, skip_special_tokens=True)
        logging.info(f"Translated batch: {translations}")
        
        for text in translations:
<<<<<<< HEAD
            total_translated_texts += 1
            return_dict[total_translated_texts] = text
=======
            if text is not None:  # Check for None before adding to return_dict
                total_translated_texts += 1
                return_dict[total_translated_texts] = text
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
        
        logging.debug(f"Batch translated: {translations}")
        logging.debug(f"Total translated texts after batch: {total_translated_texts}")

        save_checkpoint(return_dict, processed_chunks, total_translated_texts)
        logging.debug(f"Checkpoint saved after batch with total translated texts: {total_translated_texts}")
        
        return translations
<<<<<<< HEAD
=======
    except ValueError as ve:
        logging.error(f"ValueError in translate_batch: {ve}")
        return [None] * len(texts)
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
    except Exception as e:
        logging.error(f"Error translating texts: {texts}\nException: {e}\nTraceback: {traceback.format_exc()}")
        return [None] * len(texts)

def translate_chunk(chunk, model_name, return_dict, index, progress_queue, processed_chunks, total_translated_texts):
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name, cache_dir=CACHE_DIR)
        model = MarianMTModel.from_pretrained(model_name, cache_dir=CACHE_DIR)
        batch_size = 32  # Adjust batch size based on performance needs
        translated_texts = []
        for i in range(0, len(chunk), batch_size):
<<<<<<< HEAD
=======
            if terminate_signal_received.is_set():
                logging.info(f"Termination signal received. Stopping translation for chunk {index}.")
                return
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
            batch = chunk[i:i + batch_size]
            translated_text = translate_batch(batch, model, tokenizer, return_dict, processed_chunks, total_translated_texts)
            translated_texts.extend(translated_text)
            for _ in batch:
                progress_queue.put(1)
                logging.debug(f"Text processed: {translated_text}")
<<<<<<< HEAD
        return_dict[index] = translated_texts
=======
        if translated_texts:  # Ensure we don't add empty or None values
            return_dict[index] = translated_texts
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
        processed_chunks.append(index)
        logging.info(f"Chunk {index} translated successfully.")
    except Exception as e:
        logging.error(f"Error in translate_chunk for index {index}: {e}\nTraceback: {traceback.format_exc()}")
        return_dict[index] = [None] * len(chunk)
        for _ in chunk:
            progress_queue.put(1)

def update_progress_bar(total_texts, progress_queue, processed_count):
    with tqdm(total=total_texts, desc="Translating", unit=" texts") as pbar:
        pbar.update(processed_count)
        while True:
            try:
                item = progress_queue.get()
                if item is None:
                    break
                pbar.update(1)
            except Exception as e:
                logging.error(f"Error updating progress bar: {e}\nTraceback: {traceback.format_exc()}")
        pbar.close()

def update_chunk_progress_bar(total_chunks, processed_chunks_queue, processed_chunks_count):
    with tqdm(total=total_chunks, desc="Chunks Processed", unit=" chunks") as pbar:
        pbar.update(processed_chunks_count)
        while True:
            try:
                item = processed_chunks_queue.get()
                if item is None:
                    break
                pbar.update(1)
                logging.info(f"Chunk {item} processed and added to checkpoint.")
            except Exception as e:
                logging.error(f"Error updating chunk progress bar: {e}\nTraceback: {traceback.format_exc()}")
        pbar.close()

def regular_checkpoint_saving(return_dict, processed_chunks, processed_chunks_queue, total_translated_texts):
<<<<<<< HEAD
    while True:
=======
    while not terminate_signal_received.is_set():
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
        try:
            time.sleep(CHECKPOINT_INTERVAL)
            save_checkpoint(return_dict, processed_chunks, total_translated_texts)
            logging.info(f"Regular checkpoint saved with {total_translated_texts} texts and {len(processed_chunks)} chunks.")
            for chunk in list(processed_chunks):
                processed_chunks_queue.put(chunk)
            processed_chunks_queue.put(None)  # Notify chunk progress bar that checkpoint has been updated
        except Exception as e:
            logging.error(f"Error in regular_checkpoint_saving: {e}\nTraceback: {traceback.format_exc()}")

def finalize_progress_bars(progress_queue, processed_chunks_queue):
<<<<<<< HEAD
    progress_queue.put(None)
    processed_chunks_queue.put(None)

def signal_handler(signum, frame):
    global checkpoint_process, pbar_process, chunk_pbar_process, progress_queue, processed_chunks_queue, return_dict, processed_chunks, total_translated_texts
=======
    if progress_queue:
        progress_queue.put(None)
    if processed_chunks_queue:
        processed_chunks_queue.put(None)

def signal_handler(signum, frame):
    global terminate_signal_received
    terminate_signal_received.set()
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
    logging.info("Termination signal received. Saving current state and exiting gracefully...")
    save_checkpoint(return_dict, processed_chunks, total_translated_texts)
    finalize_progress_bars(progress_queue, processed_chunks_queue)
    if checkpoint_process:
        checkpoint_process.terminate()
    if pbar_process:
        pbar_process.terminate()
    if chunk_pbar_process:
        chunk_pbar_process.terminate()
    logging.info("Graceful termination complete.")
<<<<<<< HEAD
    exit(0)

def main():
    global checkpoint_process, pbar_process, chunk_pbar_process, progress_queue, processed_chunks_queue, return_dict, processed_chunks, total_translated_texts
=======
    os._exit(0)

def main():
    global checkpoint_process, pbar_process, chunk_pbar_process, progress_queue, processed_chunks_queue, return_dict, processed_chunks, total_translated_texts, error_log
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        with open('translation_in_progress.txt', 'w') as f:
            f.write("Warning: Translation process is in progress. This might take a while, feel free to leave this running while you sleep.")

        dataset_path = r'emotion_datasets_predicted.csv'
        df = pd.read_csv(dataset_path)

        model_name = 'Helsinki-NLP/opus-mt-en-tl'
        num_processes = multiprocessing.cpu_count()
        chunk_size = len(df) // num_processes
        chunks = [df['text'][i:i + chunk_size].tolist() for i in range(0, len(df), chunk_size)]

        return_dict, processed_chunks, processed_count = load_checkpoint()
        if return_dict is None:
            manager = multiprocessing.Manager()
            return_dict = manager.dict()
            progress_queue = manager.Queue()
            processed_chunks = manager.list()
            processed_count = 0
        else:
            manager = multiprocessing.Manager()
            progress_queue = manager.Queue()
            processed_chunks = manager.list(processed_chunks)
            # Calculate processed_count from the loaded return_dict
<<<<<<< HEAD
            processed_count = sum([len(return_dict[key]) for key in return_dict])
=======
            processed_count = sum([len(return_dict[key]) for key in return_dict if return_dict[key] is not None])
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
            total_translated_texts = processed_count
            logging.info(f"Resuming translation from checkpoint: {len(processed_chunks)} chunks processed.")
            logging.info(f"Total texts processed so far: {processed_count}")
            logging.debug(f"Loaded return_dict keys: {list(return_dict.keys())}")
            logging.debug(f"Loaded processed_chunks: {processed_chunks}")

        pbar_process = multiprocessing.Process(target=update_progress_bar, args=(len(df), progress_queue, processed_count))
        pbar_process.start()

        processed_chunks_queue = manager.Queue()
        chunk_pbar_process = multiprocessing.Process(target=update_chunk_progress_bar, args=(len(chunks), processed_chunks_queue, len(processed_chunks)))
        chunk_pbar_process.start()

        checkpoint_process = multiprocessing.Process(target=regular_checkpoint_saving, args=(return_dict, processed_chunks, processed_chunks_queue, total_translated_texts))
        checkpoint_process.start()

        logging.info("Starting translation...")

        processes = []

        for index, chunk in enumerate(chunks):
            if index in processed_chunks or index in return_dict:
                logging.info(f"Skipping chunk {index}, already processed.")
                continue
            try:
                logging.info(f"Starting process for chunk {index}.")
                p = multiprocessing.Process(target=translate_chunk, args=(chunk, model_name, return_dict, index, progress_queue, processed_chunks, total_translated_texts))
                p.start()
                processes.append(p)
            except Exception as e:
<<<<<<< HEAD
=======
                error_log.append(f"Error starting process for chunk {index}: {e}\nTraceback: {traceback.format_exc()}")
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
                logging.error(f"Error starting process for chunk {index}: {e}\nTraceback: {traceback.format_exc()}")

        for p in processes:
            try:
                p.join()
                logging.info(f"Process {p.pid} joined successfully.")
            except Exception as e:
<<<<<<< HEAD
=======
                error_log.append(f"Error joining process {p.pid}: {e}\nTraceback: {traceback.format_exc()}")
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
                logging.error(f"Error joining process {p.pid}: {e}\nTraceback: {traceback.format_exc()}")

        finalize_progress_bars(progress_queue, processed_chunks_queue)

        if pbar_process:
            pbar_process.join()

        if chunk_pbar_process:
            chunk_pbar_process.join()

        if checkpoint_process:
            checkpoint_process.terminate()

        translated_texts = []
        missing_chunks = []
        untranslated_texts = []
        for index in range(len(chunks)):
            if index in return_dict:
<<<<<<< HEAD
                translated_texts.extend(return_dict[index])
                if None in return_dict[index]:
                    untranslated_texts.extend([chunks[index][i] for i, text in enumerate(return_dict[index]) if text is None])
=======
                if return_dict[index] is not None:
                    try:
                        chunk_texts = return_dict[index]
                        if chunk_texts is not None and isinstance(chunk_texts, list):
                            if None in chunk_texts:
                                untranslated_texts.extend([chunks[index][i] for i, text in enumerate(chunk_texts) if text is None])
                            translated_texts.extend([text for text in chunk_texts if text is not None])
                        else:
                            logging.error(f"Chunk {index} in return_dict is not a list or is None. Skipping.")
                            missing_chunks.append(index)
                    except TypeError as e:
                        error_log.append(f"Error processing chunk {index} in return_dict: {e}\nTraceback: {traceback.format_exc()}")
                        logging.error(f"Error processing chunk {index} in return_dict: {e}\nTraceback: {traceback.format_exc()}")
                        missing_chunks.append(index)
                else:
                    logging.error(f"Chunk {index} in return_dict is None. Skipping.")
                    missing_chunks.append(index)
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
            else:
                logging.error(f"Chunk {index} missing in return_dict. Skipping.")
                missing_chunks.append(index)

<<<<<<< HEAD
        if len(translated_texts) != len(df):
            logging.error(f"Length of translated texts ({len(translated_texts)}) does not match length of original texts ({len(df)})")
            raise ValueError(f"Length of translated texts ({len(translated_texts)}) does not match length of original texts ({len(df)})")

        df['translated_text'] = translated_texts
=======
        if len(translated_texts) + len(untranslated_texts) != len(df):
            error_log.append(f"Length of translated texts ({len(translated_texts)}) + untranslated texts ({len(untranslated_texts)}) does not match length of original texts ({len(df)})")
            logging.error(f"Length of translated texts ({len(translated_texts)}) + untranslated texts ({len(untranslated_texts)}) does not match length of original texts ({len(df)})")
            raise ValueError(f"Length of translated texts ({len(translated_texts)}) + untranslated texts ({len(untranslated_texts)}) does not match length of original texts ({len(df)})")

        df['translated_text'] = translated_texts + [''] * (len(df) - len(translated_texts))
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5

        df = df[['text', 'translated_text', 'label']]

        export_path = r'emotion_datasets_tagalog-predicted.csv'
        df.to_csv(export_path, index=False)

        logging.info(f"Dataset has been successfully translated and exported to {export_path}")

        os.remove('translation_in_progress.txt')
        if os.path.exists(CHECKPOINT_FILE):
            os.remove(CHECKPOINT_FILE)
        if os.path.exists(BACKUP_CHECKPOINT_FILE):
            os.remove(BACKUP_CHECKPOINT_FILE)

        logging.info(f"Missing chunks: {missing_chunks}")
        logging.info(f"Untranslated texts: {untranslated_texts}")
<<<<<<< HEAD

    except Exception as e:
=======
        logging.info(f"Errors encountered during translation: {error_log}")

    except Exception as e:
        error_log.append(f"An error occurred in main: {e}\nTraceback: {traceback.format_exc()}")
>>>>>>> 7106f13252543654f23333fb3ac38060345826b5
        logging.error(f"An error occurred in main: {e}\nTraceback: {traceback.format_exc()}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
