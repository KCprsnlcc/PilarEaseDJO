import pandas as pd
import random
from tqdm import tqdm
import itertools

# Base phrases for each emotion
base_phrases = {
    "anger": [
        "I'm absolutely furious with how things turned out.",
        "She hit the ceiling when she found out.",
        "He's fuming about the decision."
    ],
    "disgust": [
        "The taste left me feeling nauseous.",
        "She was disgusted by the sight.",
        "His behavior was utterly repulsive."
    ],
    "fear": [
        "I felt a chill run down my spine.",
        "She was terrified of the dark.",
        "The eerie silence filled me with dread."
    ],
    "joy": [
        "I couldn't stop smiling all day.",
        "She was flying high after the promotion.",
        "He felt an overwhelming sense of happiness."
    ],
    "neutral": [
        "I went to the store yesterday.",
        "He is reading a book.",
        "The weather is quite average today."
    ],
    "sadness": [
        "She felt down in the dumps.",
        "He couldn't shake off the sadness.",
        "The news left me heartbroken."
    ],
    "surprise": [
        "I was completely taken aback.",
        "Her sudden arrival was a surprise.",
        "He couldn't believe his eyes."
    ]
}

# Synonym lists for generating variations
synonyms = {
    "furious": ["angry", "enraged", "infuriated"],
    "ceiling": ["roof", "sky"],
    "fuming": ["seething", "irate"],
    "disgusted": ["revolted", "repulsed", "sickened"],
    "nauseous": ["queasy", "sick"],
    "terrified": ["scared", "afraid"],
    "chill": ["shiver", "tremor"],
    "happy": ["joyful", "elated", "thrilled"],
    "smiling": ["grinning", "beaming"],
    "high": ["ecstatic", "elated"],
    "store": ["shop", "market"],
    "book": ["novel", "text"],
    "average": ["typical", "ordinary"],
    "sadness": ["sorrow", "grief"],
    "heartbroken": ["devastated", "crushed"],
    "surprise": ["shock", "astonishment"],
    "taken aback": ["stunned", "shocked"]
}

# Function to generate variations
def generate_variations(phrase, synonyms):
    words = phrase.split()
    variations = set()
    for i, word in enumerate(words):
        if word in synonyms:
            for synonym in synonyms[word]:
                new_words = words.copy()
                new_words[i] = synonym
                variations.add(" ".join(new_words))
    return list(variations)

# Generate unique phrases for each emotion
unique_phrases = {"text": [], "label": []}
n_phrases_per_emotion = 1500

for emotion, phrases in base_phrases.items():
    emotion_phrases = set()
    variations_set = set()
    for phrase in phrases:
        variations = generate_variations(phrase, synonyms)
        variations_set.update(variations)
    with tqdm(total=n_phrases_per_emotion, desc=f"Generating phrases for {emotion}") as pbar:
        for variation in itertools.cycle(variations_set):
            if len(emotion_phrases) >= n_phrases_per_emotion:
                break
            if variation not in emotion_phrases:
                emotion_phrases.add(variation)
                pbar.update(1)
    unique_phrases["text"].extend(emotion_phrases)
    unique_phrases["label"].extend([emotion] * n_phrases_per_emotion)

# Convert to DataFrame
new_data_df = pd.DataFrame(unique_phrases)

# Load existing dataset
csv_file_path = 'english_emotion_dataset.csv'
existing_df = pd.read_csv(csv_file_path)

# Combine datasets
combined_df = pd.concat([existing_df, new_data_df], ignore_index=True)

# Save the updated dataset
updated_csv_file_path = 'large_extended_emotion_dataset.csv'
combined_df.to_csv(updated_csv_file_path, index=False)

import ace_tools as tools; tools.display_dataframe_to_user(name="Large Extended Emotion Dataset", dataframe=combined_df)

updated_csv_file_path
