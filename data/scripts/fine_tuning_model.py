import os
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, pipeline
from datasets import Dataset
from sklearn.metrics import classification_report
from tqdm import tqdm

def preprocess_data(examples, tokenizer):
    return tokenizer(examples['text'], truncation=True, padding=True)

dataset_path = 'tagalog_dataset.csv'
df = pd.read_csv(dataset_path)

train_df = df.sample(frac=0.8, random_state=42)
val_df = df.drop(train_df.index)

train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)

model_name = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)

train_dataset = train_dataset.map(lambda x: preprocess_data(x, tokenizer), batched=True)
val_dataset = val_dataset.map(lambda x: preprocess_data(x, tokenizer), batched=True)

train_dataset = train_dataset.map(lambda examples: {'labels': examples['label']}, batched=True)
val_dataset = val_dataset.map(lambda examples: {'labels': examples['label']}, batched=True)

def data_collator(features):
    return {key: tf.convert_to_tensor([f[key] for f in features]) for key in features[0]}

learning_rates = [1e-5, 2e-5, 3e-5]
batch_sizes = [8, 16, 32]
num_epochs_list = [3, 5]

def fine_tune_and_evaluate(learning_rate, batch_size, num_epochs):
    model = TFAutoModelForSequenceClassification.from_pretrained(model_name, num_labels=7)
    
    train_tf_dataset = train_dataset.to_tf_dataset(
        columns=['input_ids', 'attention_mask', 'labels'],
        shuffle=True,
        batch_size=batch_size,
        collate_fn=data_collator
    )
    
    val_tf_dataset = val_dataset.to_tf_dataset(
        columns=['input_ids', 'attention_mask', 'labels'],
        shuffle=False,
        batch_size=batch_size,
        collate_fn=data_collator
    )
    
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss=model.compute_loss, metrics=['accuracy'])
    
    model.fit(train_tf_dataset, validation_data=val_tf_dataset, epochs=num_epochs)
    
    predictions = []
    true_labels = []

    for batch in val_tf_dataset:
        logits = model(batch['input_ids'], attention_mask=batch['attention_mask']).logits
        predictions.extend(tf.argmax(logits, axis=-1).numpy())
        true_labels.extend(batch['labels'].numpy())
    
    id2label = {
        0: "anger",
        1: "disgust",
        2: "fear",
        3: "joy",
        4: "neutral",
        5: "sadness",
        6: "surprise"
    }
    true_labels_mapped = [id2label[label] for label in true_labels]
    predicted_labels_mapped = [id2label[label] for label in predictions]
    
    report = classification_report(true_labels_mapped, predicted_labels_mapped, target_names=list(id2label.values()), output_dict=True, zero_division=0)
    
    report_df = pd.DataFrame(report).transpose()
    
    print(report_df)
    
    save_directory = f'fine-tuned-model/lr-{learning_rate}_bs-{batch_size}_epochs-{num_epochs}'
    model.save_pretrained(save_directory)
    tokenizer.save_pretrained(save_directory)
    
    return report_df

results = []
for lr in learning_rates:
    for bs in batch_sizes:
        for epochs in num_epochs_list:
            print(f"Training with learning_rate={lr}, batch_size={bs}, num_epochs={epochs}")
            result = fine_tune_and_evaluate(lr, bs, epochs)
            results.append((lr, bs, epochs, result))

for lr, bs, epochs, result in results:
    print(f"Results for learning_rate={lr}, batch_size={bs}, num_epochs={epochs}:")
    print(result)

results_df = pd.DataFrame([(lr, bs, epochs, result) for lr, bs, epochs, result in results],
                          columns=['learning_rate', 'batch_size', 'num_epochs', 'report'])
results_df.to_csv('fine-tuning-results.csv', index=False)
