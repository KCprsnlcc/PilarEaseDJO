from transformers import MarianMTModel, MarianTokenizer

# Load the model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-en-tl'

# Check if the model and tokenizer are already cached
try:
    tokenizer = MarianTokenizer.from_pretrained(model_name, local_files_only=True)
    model = MarianMTModel.from_pretrained(model_name, local_files_only=True)
    print("Model and tokenizer loaded from cache.")
except:
    print("Model and tokenizer not found in cache. Ensure they are downloaded.")

