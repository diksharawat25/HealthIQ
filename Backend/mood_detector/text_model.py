import pickle
import re
from pathlib import Path

# --- Configuration (Path Fixing) ---
# Get the absolute path to the current directory (mood_detector)
BASE_DIR = Path(__file__).resolve().parent

# Set model file paths relative to the BASE_DIR (one level up to the 'models' folder)
MODEL_PATH = BASE_DIR.parent / "models" / "text_sentiment_model.pkl"
VECTORIZER_PATH = BASE_DIR.parent / "models" / "tfidf_vectorizer.pkl"

# Global variables to store the loaded model and vectorizer
TEXT_MODEL = None
TEXT_VECTORIZER = None
# Labels defined during training: 0 for Negative, 1 for Positive
TEXT_LABELS = {0: "Negative", 1: "Positive"}

# --- 1. Model Loading ---

def load_text_model():
    """
    Loads the trained Logistic Regression model and TfidfVectorizer into memory.
    """
    global TEXT_MODEL, TEXT_VECTORIZER

    try:
        # Load the Vectorizer
        with open(VECTORIZER_PATH, 'rb') as f:
            TEXT_VECTORIZER = pickle.load(f)
        
        # Load the Model
        with open(MODEL_PATH, 'rb') as f:
            TEXT_MODEL = pickle.load(f)
        
        return {"status": True, "message": "Text Model loaded successfully."}
    
    except FileNotFoundError:
        # This error occurs if train_text_model.py was not run correctly
        return {"status": False, "error": "Text model files not found. Please ensure they are in 'backend/models/'."}
    
    except Exception as e:
        return {"status": False, "error": f"An error occurred during text model loading: {e}"}


# --- 2. Prediction Logic ---

def preprocess_text(text):
    """Cleans text (removes mentions, links, special chars)."""
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'@[A-Za-z0-9_]+', '', text) # Remove mentions
        text = re.sub(r'https?://\S+', '', text) # Remove links
        text = re.sub(r'[^a-z\s]', '', text) # Remove special characters
        return text.strip()
    return ""

def get_text_mood(text: str):
    """
    Predicts the sentiment/mood of the given text using the loaded models.
    """
    if TEXT_MODEL is None or TEXT_VECTORIZER is None:
        return {"error": "Text model is not loaded. Check server startup logs."}

    try:
        cleaned_text = preprocess_text(text)
        if not cleaned_text:
            return {"mood": "Neutral", "confidence": 0.5, "label_code": 2} # Return neutral if input is empty
            
        # 1. Vectorize: Use the fitted vectorizer to transform the new text
        text_vectorized = TEXT_VECTORIZER.transform([cleaned_text])
        
        # 2. Predict: Get the prediction probability
        prediction_prob = TEXT_MODEL.predict_proba(text_vectorized)
        
        # 3. Get the predicted class (0 or 1)
        predicted_class = TEXT_MODEL.predict(text_vectorized)[0]
        
        # 4. Get the mood label and confidence
        mood = TEXT_LABELS.get(predicted_class, "Neutral")
        confidence = prediction_prob[0][predicted_class]

        return {
            "mood": mood,
            "confidence": round(float(confidence), 4),
            "label_code": int(predicted_class)
        }
    
    except Exception as e:
        return {"error": f"Prediction failed during processing: {e}"}
