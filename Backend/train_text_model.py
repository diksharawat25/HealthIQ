import pandas as pd
import numpy as np
import pickle
import os
import re

# Scikit-learn imports for Model and Vectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# --- Configuration ---
# Data file ka path (jahan aapne CSV rakhi hai)
DATA_FILE_PATH = 'data/training.1600000.processed.noemoticon.csv'

# Models ko save karne ka path
MODEL_DIR = 'models'
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
MODEL_PATH = os.path.join(MODEL_DIR, 'text_sentiment_model.pkl')

# Column names in the Sentiment140 CSV file
COLUMNS = ['target', 'ids', 'date', 'flag', 'user', 'text']
# Target labels: 0 -> Negative, 4 -> Positive. We will map 4 to 1 for simplicity.
TARGET_MAP = {0: 0, 4: 1} # 0: Negative, 1: Positive

def preprocess_text(text):
    """Simple function to clean the tweets/text data."""
    if isinstance(text, str):
        # Remove mentions (@user) and URLs (http...)
        text = re.sub(r'@\w+|https?://\S+|www\.\S+', '', text).lower()
        # Remove special characters and numbers (keeping only letters and spaces)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text.strip()
    return ""

def train_and_save_model():
    """Main function to load data, train the model, and save assets."""
    print("--- Starting Text Sentiment Model Training ---")
    
    # 1. Data Load
    try:
        # Load only the 'target' and 'text' columns and skip the header
        data = pd.read_csv(
            DATA_FILE_PATH, 
            encoding='ISO-8859-1', 
            names=COLUMNS, 
            usecols=['target', 'text']
        )
    except FileNotFoundError:
        print(f"\nERROR: Data file not found at {DATA_FILE_PATH}")
        print("Please ensure the CSV file is correctly placed inside the 'backend/data/' folder.")
        return

    # 2. Data Preprocessing
    # Map 0 (Negative) and 4 (Positive) to 0 and 1
    data['target'] = data['target'].map(TARGET_MAP)
    # Clean the text
    data['text'] = data['text'].apply(preprocess_text)
    
    # Remove any rows where text became empty after cleaning
    data = data[data['text'].str.strip() != ""]
    
    X = data['text']
    y = data['target']
    
    # Use a small sample to reduce training time drastically (100,000 samples)
    if len(X) > 100000:
        X_sample, _, y_sample, _ = train_test_split(X, y, test_size=1 - (100000/len(X)), stratify=y, random_state=42)
        X = X_sample
        y = y_sample

    print(f"Data loaded and sampled: {len(X)} records.")

    # 3. Vectorizer Training and Saving (TF-IDF)
    # This converts text into numerical features
    print("Training TfidfVectorizer...")
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_vectorized = tfidf.fit_transform(X)

    # Save the FITTED Vectorizer
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(VECTORIZER_PATH, 'wb') as f:
        pickle.dump(tfidf, f)
    print(f"Vectorizer saved successfully at: {VECTORIZER_PATH}")


    # 4. Model Training and Saving (Logistic Regression)
    # Splitting data for internal testing
    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)
    
    print("Training Logistic Regression Model...")
    model = LogisticRegression(max_iter=1000, n_jobs=-1)
    model.fit(X_train, y_train)

    # Evaluate (Optional, but good practice)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Training Complete. Test Accuracy: {accuracy:.4f}")

    # Save the Trained Model
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved successfully at: {MODEL_PATH}")

    print("\n--- Training Process Finished. You can now use the models in the API. ---")


if __name__ == '__main__':
    train_and_save_model()