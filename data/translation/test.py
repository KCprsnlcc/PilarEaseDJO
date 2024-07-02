from transformers import pipeline
from tqdm import tqdm
from plyer import notification
from langdetect import detect
import re
from collections import defaultdict
import time

# Load the translation model for Tagalog to English from local path
translator = pipeline("translation", model="translationmodel/")

# Load the J-Hartmann model for emotion classification from local path
emotion_classifier = pipeline("text-classification", model="predictivemodel/")

# Define all emotions we are interested in
all_emotions = ['anger', 'sadness', 'disgust', 'joy', 'neutral', 'surprise', 'fear']

def split_text_into_chunks(text, max_length=1024, overlap=100):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > max_length:
            if len(current_chunk) > 0:
                chunks.append(current_chunk)
                current_chunk = sentence[-overlap:]  # Overlap with new sentence start
            else:
                chunks.append(sentence)
                current_chunk = ""
        else:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def translate_text(text):
    text_chunks = split_text_into_chunks(text)
    translated_chunks = []
    for chunk in tqdm(text_chunks, desc="Translating", unit="chunk"):
        translated_chunk = translator(chunk)
        translated_chunks.append(translated_chunk[0]['translation_text'])
    translated_text = " ".join(translated_chunks)
    return translated_text

def analyze_emotion(text):
    text_chunks = split_text_into_chunks(text, max_length=512, overlap=0)
    emotion_results = []
    for chunk in tqdm(text_chunks, desc="Analyzing Emotion", unit="chunk"):
        emotion_results.append(emotion_classifier(chunk))
    
    detailed_results = []
    for chunk_result in emotion_results:
        chunk_emotions = {result['label'].lower(): result['score'] for result in chunk_result}
        detailed_results.append(chunk_emotions)
    
    return detailed_results

def process_text(text):
    try:
        notification.notify(
            title="Text Classification Analysis",
            message="Detecting language...",
            timeout=5
        )
        detected_language = detect(text)
        
        if detected_language != 'en':
            notification.notify(
                title="Text Classification Analysis",
                message="Translating text from Tagalog to English...",
                timeout=5
            )
            english_text = translate_text(text)
        else:
            english_text = text
        
        notification.notify(
            title="Text Classification Analysis",
            message="Analyzing emotion...",
            timeout=5
        )
        start_time = time.time()
        emotion_result = analyze_emotion(english_text)
        end_time = time.time()
        computation_time = end_time - start_time
        return english_text, emotion_result, computation_time
    except Exception as e:
        notification.notify(
            title="Error",
            message=str(e),
            timeout=5
        )
        return None, None, None

def main():
    while True:
        tagalog_text = input("Enter text (or type 'exit' to quit): ")
        
        if tagalog_text.lower() == 'exit':
            print("Exiting the program.")
            break
        
        notification.notify(
            title="Text Classification Analysis",
            message="Starting translation and emotion analysis...",
            timeout=5
        )
        
        with tqdm(total=2, desc="Processing", unit="step") as pbar:
            english_text, emotion_result, computation_time = process_text(tagalog_text)
            if english_text and emotion_result:
                pbar.update(2)
        
        notification.notify(
            title="Text Classification Analysis",
            message="Translation and emotion analysis completed!",
            timeout=5
        )
        
        if english_text and emotion_result:
            print("\nTranslated Text:", english_text)
            print("Emotion Analysis Result:")
            print(f"Computation time on CPU: {computation_time:.6f} s")
            for idx, result in enumerate(emotion_result):
                print(f"Chunk {idx + 1}:")
                for emotion in all_emotions:
                    print(f"  {emotion}: {result.get(emotion, 0.0):.6f}")
            print()

if __name__ == "__main__":
    main()
