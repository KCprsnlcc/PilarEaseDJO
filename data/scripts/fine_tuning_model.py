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


# import torch
# from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
# from datasets import load_dataset, load_metric
# from sklearn.metrics import accuracy_score, precision_recall_fscore_support
# import numpy as np

# # 1. Load and Preprocess Dataset
# dataset = load_dataset('emotion')
# train_testvalid = dataset['train'].train_test_split(test_size=0.2)
# test_valid = train_testvalid['test'].train_test_split(test_size=0.5)
# train_dataset = train_testvalid['train']
# valid_dataset = test_valid['train']
# test_dataset = test_valid['test']

# # 2. Load Pre-trained Model and Tokenizer
# model_name = "roberta-large"
# tokenizer = RobertaTokenizer.from_pretrained(model_name)
# model = RobertaForSequenceClassification.from_pretrained(model_name, num_labels=len(dataset['train'].features['label'].names))

# # 3. Advanced Tokenization with Padding
# def tokenize_function(examples):
#     return tokenizer(examples['text'], truncation=True, padding=True, max_length=128)

# train_dataset = train_dataset.map(tokenize_function, batched=True)
# valid_dataset = valid_dataset.map(tokenize_function, batched=True)
# test_dataset = test_dataset.map(tokenize_function, batched=True)

# # 4. Data Collator for Dynamic Padding
# data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# # 5. Fine-Tuning Hyperparameters and Trainer Setup
# training_args = TrainingArguments(
#     output_dir='./results',
#     evaluation_strategy="epoch",
#     learning_rate=2e-5,
#     per_device_train_batch_size=8,  # Reduce batch size to fit large model in memory
#     per_device_eval_batch_size=16,
#     num_train_epochs=5,  # Reduced number of epochs due to larger model size
#     weight_decay=0.01,
#     save_total_limit=3,
#     load_best_model_at_end=True,
#     metric_for_best_model="accuracy",
#     logging_dir='./logs',
#     logging_steps=10,
# )

# def compute_metrics(eval_pred):
#     logits, labels = eval_pred
#     predictions = np.argmax(logits, axis=-1)
#     accuracy = accuracy_score(labels, predictions)
#     precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='weighted')
#     return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}

# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=valid_dataset,
#     tokenizer=tokenizer,
#     data_collator=data_collator,
#     compute_metrics=compute_metrics
# )

# # 6. Model Training with Early Stopping and Gradient Accumulation
# trainer.train()

# # 7. Evaluate Model on Test Set
# eval_results = trainer.evaluate(eval_dataset=test_dataset)
# print(f"Test Accuracy: {eval_results['eval_accuracy']:.4f}")
# print(f"Test F1-Score: {eval_results['eval_f1']:.4f}")

# # 8. Post-Processing - Adjust Decision Thresholds for Multi-class Classification
# def adjust_thresholds(model, eval_dataset, target_f1=0.9):
#     logits = trainer.predict(eval_dataset).predictions
#     probabilities = torch.nn.functional.softmax(torch.tensor(logits), dim=-1)
#     thresholds = np.arange(0.1, 1.0, 0.1)
#     best_f1 = 0
#     best_threshold = 0.5

#     for threshold in thresholds:
#         predictions = (probabilities > threshold).int()
#         f1 = precision_recall_fscore_support(eval_dataset['label'], predictions.numpy(), average='weighted')[2]
#         if f1 > best_f1:
#             best_f1 = f1
#             best_threshold = threshold

#     return best_threshold, best_f1

# best_threshold, best_f1 = adjust_thresholds(model, test_dataset)
# print(f"Best Threshold: {best_threshold}, Best F1: {best_f1}")

# # 9. Model Calibration (e.g., Platt Scaling) - Improves Calibration of Probabilities
# # Placeholder for implementation, Platt scaling usually needs a separate logistic regression step.

# # 10. Save the Fine-Tuned Model and Tokenizer
# model.save_pretrained('./fine_tuned_roberta_large_model')
# tokenizer.save_pretrained('./fine_tuned_roberta_large_model')

# # 11. (Optional) Continual Learning - Incorporate Additional Data Over Time
# # Add new data and incrementally train the model using the trainer instance.
