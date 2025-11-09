import os
import io
import numpy as np
import librosa
import pickle
import soundfile as sf
from tensorflow.keras.models import load_model

# --- Global Model Variables ---
# These will be loaded once when the FastAPI application starts
VOICE_MODEL = None
VOICE_SCALER = None
VOICE_LABELS = None

# --- Configuration ---
# File paths relative to the backend/ folder
MODEL_PATH = "models/voice_mood_model.h5"
SCALER_PATH = "models/voice_scaler.pkl"
LABELS_PATH = "models/voice_mood_labels.npy"
SAMPLE_RATE = 22050
MAX_PAD_LEN = 173 # Length used during training

# --- 1. Model Loading ---

def load_voice_model():
    """Loads the trained Keras model, scaler, and labels into global memory."""
    global VOICE_MODEL, VOICE_SCALER, VOICE_LABELS
    try:
        # Load Keras model
        VOICE_MODEL = load_model(MODEL_PATH)
        print("Voice Model loaded successfully.")

        # Load StandardScaler object
        with open(SCALER_PATH, 'rb') as f:
            VOICE_SCALER = pickle.load(f)
        print("Voice Scaler loaded successfully.")

        # Load labels (emotion names)
        VOICE_LABELS = np.load(LABELS_PATH, allow_pickle=True)
        print(f"Voice Labels loaded: {VOICE_LABELS}")

    except Exception as e:
        print(f"ERROR loading voice model components: {e}")
        # Critical error: ensure the process exits gracefully
        VOICE_MODEL = None 
        raise RuntimeError("Voice model failed to load. Check model/scaler file paths.")

# --- 2. Feature Extraction for Prediction ---

def extract_features_from_bytes(audio_bytes):
    """
    Extracts MFCC features from raw audio bytes (received from the API).
    """
    # Use io.BytesIO to treat the bytes as a file, then soundfile to read
    with io.BytesIO(audio_bytes) as audio_file:
        with sf.SoundFile(audio_file) as sound_file:
            X = sound_file.read(dtype="float32")
            
            # --- Feature Extraction ---
            mfccs = librosa.feature.mfcc(y=X, sr=SAMPLE_RATE, n_mfcc=40)
            mfccs = np.mean(mfccs.T, axis=0)
            
            # --- Padding/Trimming to Match Training Length ---
            if mfccs.shape[0] < MAX_PAD_LEN:
                # Pad with zeros if shorter than max length
                pad_width = MAX_PAD_LEN - mfccs.shape[0]
                mfccs = np.pad(mfccs, (0, pad_width), mode='constant')
            elif mfccs.shape[0] > MAX_PAD_LEN:
                # Trim if longer than max length
                mfccs = mfccs[:MAX_PAD_LEN]

    return mfccs

# --- 3. Prediction Function ---

def get_voice_mood(audio_bytes: bytes):
    """
    Predicts mood from live audio input bytes.
    """
    if VOICE_MODEL is None:
        return "Model Not Loaded"

    try:
        # 1. Extract and standardize features
        features = extract_features_from_bytes(audio_bytes)
        
        # Reshape and scale the single feature vector
        features = features.reshape(1, -1)
        features_scaled = VOICE_SCALER.transform(features)
        
        # Reshape for CNN model (1 sample, MAX_PAD_LEN, 1 feature channel)
        features_cnn = np.expand_dims(features_scaled, axis=2)

        # 2. Make prediction
        predictions = VOICE_MODEL.predict(features_cnn, verbose=0)
        
        # 3. Convert prediction (numerical index) back to emotion label
        predicted_index = np.argmax(predictions, axis=1)[0]
        predicted_mood = VOICE_LABELS[predicted_index]

        return predicted_mood

    except Exception as e:
        print(f"Prediction Error: {e}")
        return "Error Processing Audio"
