import os
import pandas as pd
import matplotlib.pyplot as plt
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, pipeline
from datasets import load_dataset
from sklearn.metrics import classification_report
from tqdm import tqdm

try:
    # Load the model and tokenizer from Hugging Face
    model_name = "j-hartmann/emotion-english-distilroberta-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

    # Create a pipeline for emotion classification
    classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=None)

    # Load the "emotion" dataset for evaluation
    dataset = load_dataset("emotion", split="test")

    # Print dataset information
    print("Dataset Info:", dataset)

    # Get the texts and labels
    texts = dataset["text"]
    true_labels = dataset["label"]

    # Define the id2label mapping expected by the model
    id2label = {
        0: "anger",
        1: "disgust",
        2: "fear",
        3: "joy",
        4: "neutral",
        5: "sadness",
        6: "surprise"
    }

    # Print the unique labels in the dataset
    unique_labels = set(true_labels)
    print("Unique Labels in Dataset:", unique_labels)

    # Ensure that the true labels are mapped to their string representations
    true_labels_mapped = [id2label[label] for label in true_labels]

    # Initialize the progress bar
    print("Starting model evaluation...")
    predictions = []
    for text in tqdm(texts, desc="Evaluating", unit="texts"):
        predictions.append(classifier(text))

    # Debugging: Print the first prediction to inspect its structure
    print("First prediction:", predictions[0])

    # Extract the predicted labels from the predictions
    predicted_labels = [max(pred[0], key=lambda x: x["score"])["label"] for pred in predictions]

    # Debugging: Inspect a sample of predictions
    for i in range(10):
        print(f"Text: {texts[i]}")
        print(f"True label: {true_labels_mapped[i]}")
        print(f"Predicted: {predicted_labels[i]}")
        print()

    # Generate the classification report
    report = classification_report(true_labels_mapped, predicted_labels, target_names=list(id2label.values()), output_dict=True, zero_division=0)

    # Convert the report to a DataFrame
    report_df = pd.DataFrame(report).transpose()

    # Print the report DataFrame
    print(report_df)

    # Create the reports directory if it does not exist
    reports_dir = 'reports'
    os.makedirs(reports_dir, exist_ok=True)

    # Visualize the classification report
    plt.figure(figsize=(10, 6))
    plt.title("Classification Report")
    plt.axis('off')
    plt.table(cellText=report_df.values, colLabels=report_df.columns, rowLabels=report_df.index, cellLoc='center', loc='center')
    plt.savefig(os.path.join(reports_dir, 'classification_report.png'), bbox_inches='tight')

    print("Model evaluation completed. The classification report has been saved to 'reports/classification_report.png'.")

except ImportError as e:
    print(f"Error: {e}")
    print("Make sure to install the required packages with: pip install transformers datasets scikit-learn pandas matplotlib tqdm")
except Exception as e:
    print(f"An error occurred: {e}")
