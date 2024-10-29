import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    Trainer, 
    TrainingArguments,
    TrainerCallback
)
from datasets import Dataset
from sklearn.utils import resample
from tqdm import tqdm
import logging
import plotly.graph_objects as go

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load dataset
df = pd.read_csv('filtered_goemotions.csv')
logging.info("Loaded dataset successfully.")

# Data Balancing with Up-Sampling
def balance_data(df):
    logging.info("Starting data balancing with up-sampling.")
    max_size = df['label'].value_counts().max()
    lst = [df]
    for label in df['label'].unique():
        samples = df[df['label'] == label]
        upsampled = resample(samples, replace=True, n_samples=max_size, random_state=123)
        lst.append(upsampled)
    logging.info("Completed data balancing.")
    return pd.concat(lst)

df = balance_data(df)

# Data Augmentation with Synonym Replacement
def synonym_replacement(text):
    words = text.split()
    num_replacements = random.randint(1, max(1, len(words) // 3))
    for _ in range(num_replacements):
        word_idx = random.randint(0, len(words) - 1)
        words[word_idx] = words[word_idx][::-1]  # Simple mock-up; use actual NLP synonym replacement
    return ' '.join(words)

# Apply data augmentation with progress bar
logging.info("Starting data augmentation with synonym replacement.")
df['text'] = [synonym_replacement(text) for text in tqdm(df['text'], desc="Data Augmentation")]
logging.info("Completed data augmentation.")

# Map emotions to integer labels
label_map = {'anger': 0, 'disgust': 1, 'fear': 2, 'happiness': 3, 'neutral': 4, 'sadness': 5, 'surprise': 6}
df['label'] = df['label'].map(label_map)

# Convert to Hugging Face Dataset format
dataset = Dataset.from_pandas(df)
dataset = dataset.train_test_split(test_size=0.2)
logging.info("Converted dataset to Hugging Face format and split into train/test sets.")

# Load tokenizer and tokenize dataset with progress bar
tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")

def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True)

logging.info("Tokenizing dataset.")
dataset = dataset.map(tokenize, batched=True)
logging.info("Tokenization completed.")

# Hyperparameter Tuning Setup
def model_init():
    return AutoModelForSequenceClassification.from_pretrained(
        "j-hartmann/emotion-english-distilroberta-base", 
        num_labels=7
    )

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="f1",
)

# Track Metrics for Plotly Visualization
training_metrics = {'accuracy': [], 'precision': [], 'recall': [], 'f1': []}

# Define custom evaluation metrics
def compute_metrics(pred):
    labels = pred.label_ids
    preds = np.argmax(pred.predictions, axis=1)
    report = classification_report(labels, preds, target_names=label_map.keys(), output_dict=True)
    # Append metrics to the list for plotting
    training_metrics['accuracy'].append(report["accuracy"])
    training_metrics['precision'].append(report["weighted avg"]["precision"])
    training_metrics['recall'].append(report["weighted avg"]["recall"])
    training_metrics['f1'].append(report["weighted avg"]["f1-score"])
    return {
        "accuracy": report["accuracy"],
        "precision": report["weighted avg"]["precision"],
        "recall": report["weighted avg"]["recall"],
        "f1": report["weighted avg"]["f1-score"],
    }

# Initialize Trainer with progress logging callback
class ProgressCallback(TrainerCallback):
    def on_train_begin(self, args, state, control, **kwargs):
        logging.info("Training started.")
    
    def on_epoch_begin(self, args, state, control, **kwargs):
        logging.info(f"Epoch {state.epoch + 1} started.")
    
    def on_epoch_end(self, args, state, control, **kwargs):
        logging.info(f"Epoch {state.epoch + 1} completed.")

    def on_train_end(self, args, state, control, **kwargs):
        logging.info("Training finished.")

trainer = Trainer(
    model_init=model_init,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    compute_metrics=compute_metrics,
    callbacks=[ProgressCallback()]  # Add the progress callback
)

# Run Hyperparameter Tuning
logging.info("Starting hyperparameter tuning.")
best_run = trainer.hyperparameter_search(
    direction="maximize",
    n_trials=5,
    hp_space=lambda _: {
        "learning_rate": random.uniform(1e-5, 5e-5),
        "num_train_epochs": random.choice([3, 4, 5]),
        "per_device_train_batch_size": random.choice([8, 16]),
    }
)

# Apply best hyperparameters and re-train
trainer.args.learning_rate = best_run.hyperparameters['learning_rate']
trainer.args.num_train_epochs = best_run.hyperparameters['num_train_epochs']
trainer.args.per_device_train_batch_size = best_run.hyperparameters['per_device_train_batch_size']

logging.info(f"Best hyperparameters: {best_run.hyperparameters}")
logging.info("Starting final training with best hyperparameters.")
trainer.train()

# Evaluation on test set
logging.info("Evaluating the model on test set.")
eval_results = trainer.evaluate()
logging.info(f"Final Evaluation Metrics: {eval_results}")

# Plotting Metrics with Plotly
def plot_metrics(metrics):
    epochs = list(range(1, len(metrics['accuracy']) + 1))
    fig = go.Figure()

    # Plot each metric
    fig.add_trace(go.Scatter(x=epochs, y=metrics['accuracy'], mode='lines+markers', name='Accuracy'))
    fig.add_trace(go.Scatter(x=epochs, y=metrics['precision'], mode='lines+markers', name='Precision'))
    fig.add_trace(go.Scatter(x=epochs, y=metrics['recall'], mode='lines+markers', name='Recall'))
    fig.add_trace(go.Scatter(x=epochs, y=metrics['f1'], mode='lines+markers', name='F1 Score'))

    fig.update_layout(
        title="Training Metrics Over Epochs",
        xaxis_title="Epoch",
        yaxis_title="Score",
        legend_title="Metrics",
        template="plotly_dark"
    )
    fig.show()

plot_metrics(training_metrics)

# Save the final model
trainer.save_model("./fine_tuned_emotion_model")
tokenizer.save_pretrained("./fine_tuned_emotion_model")
logging.info("Model and tokenizer saved successfully.")
