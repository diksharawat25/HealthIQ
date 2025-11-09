import numpy as np
import os
import glob
import librosa
import soundfile as sf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import tensorflow as tf # Changed import style for better compatibility
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import pickle

# --- Configuration ---
# RAVDESS data is assumed to be extracted inside the 'backend/data/' folder.
DATA_PATH = "data/"
MODEL_SAVE_PATH = "models/voice_mood_model.h5"
MAX_TIME_STEPS = 173 # Fixed size for padding based on common audio lengths

# Dictionary to map the RAVDESS emotion codes (part of the filename) to actual emotions
EMOTION_MAP = {
    '01': 'neutral', '02': 'calm', '03': 'happy', '04': 'sad',
    '05': 'angry', '06': 'fearful', '07': 'disgust', '08': 'surprised'
}
OBSERVE_EMOTIONS = ['happy', 'sad', 'angry', 'neutral', 'fearful'] # Focusing on these 5 key emotions

# --- 1. Feature Extraction Function ---

def extract_features(file_name, max_time_steps):
    """
    Extracts MFCC features and pads them to a fixed size.
    """
    try:
        with sf.SoundFile(file_name) as sound_file:
            X = sound_file.read(dtype="float32")
            sample_rate = sound_file.samplerate

            # Extract MFCC features
            mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40)
            
            # Transpose and take the mean, but ensure fixed shape:
            mfccs = mfccs.T
            
            # --- Padding Logic (Fixes the ValueError) ---
            if mfccs.shape[0] < max_time_steps:
                # Pad with zeros if too short
                pad_width = max_time_steps - mfccs.shape[0]
                mfccs = np.pad(mfccs, pad_width=((0, pad_width), (0, 0)), mode='constant')
            elif mfccs.shape[0] > max_time_steps:
                # Truncate if too long
                mfccs = mfccs[:max_time_steps, :]
            # --- End Padding Logic ---

    except Exception as e:
        print(f"Error processing file {file_name}: {e}")
        return None

    return mfccs

# --- 2. Data Loading and Processing ---

def load_data(max_time_steps):
    """
    Loads data from RAVDESS directory structure.
    """
    X, y = [], []
    
    # Check if the base data path exists
    if not os.path.isdir(DATA_PATH):
        raise FileNotFoundError(f"Data path not found: {DATA_PATH}. Ensure RAVDESS is extracted inside 'data/' folder.")
        
    print("Starting data loading and feature extraction...")
    
    # Iterate through actor directories
    for actor_dir in glob.glob(os.path.join(DATA_PATH, 'Actor_*')):
        
        # Iterate through audio files
        for file in glob.glob(os.path.join(actor_dir, '*.wav')):
            
            file_name = os.path.basename(file)
            emotion_code = file_name.split("-")[2]
            emotion = EMOTION_MAP.get(emotion_code)

            if emotion in OBSERVE_EMOTIONS:
                
                # Extract features with fixed size
                feature = extract_features(file, max_time_steps)
                
                if feature is not None:
                    X.append(feature)
                    y.append(emotion)
    
    print(f"\nFinished extraction. Total samples loaded: {len(X)}")
    return np.array(X), np.array(y)

# --- 3. Model Training ---

def train_and_save_model():
    """
    Main function to load data, preprocess, train the CNN model, and save it.
    """
    # 3.1 Load and Prepare Data
    try:
        X, y = load_data(MAX_TIME_STEPS)
    except FileNotFoundError as e:
        print(e)
        return

    # Check if data was loaded successfully
    if len(X) == 0:
        print("ERROR: No audio files found or loaded successfully. Check your data folder structure.")
        return
        
    # 3.2 Label Encoding (Convert emotion names to numbers)
    encoder = OneHotEncoder()
    y_encoded = encoder.fit_transform(y.reshape(-1, 1)).toarray()
    
    # Save the encoder for later use in prediction
    np.save('models/voice_mood_labels.npy', encoder.categories_[0])
    print("Emotion labels saved to models/voice_mood_labels.npy")

    # 3.3 Splitting Data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # 3.4 Feature Scaling (Standardization)
    # The scaler must be fitted on the 2D data before reshaping
    scaler = StandardScaler()
    
    # Reshape 3D to 2D for scaling (samples * time_steps, features)
    X_train_2d = X_train.reshape(-1, X_train.shape[-1])
    X_train_scaled_2d = scaler.fit_transform(X_train_2d)
    
    # Reshape back to 3D (samples, time_steps, features)
    X_train_scaled = X_train_scaled_2d.reshape(X_train.shape)
    
    # Apply transformation to test set
    X_test_2d = X_test.reshape(-1, X_test.shape[-1])
    X_test_scaled_2d = scaler.transform(X_test_2d)
    X_test_scaled = X_test_scaled_2d.reshape(X_test.shape)
    
    # Save the scaler object for prediction on live audio input
    with open('models/voice_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print("Scaler object saved to models/voice_scaler.pkl")
    
    # Determine input shape for the model
    input_shape = (X_train_scaled.shape[1], X_train_scaled.shape[2])
    num_classes = y_encoded.shape[1]
    
    # 3.5 Build the CNN Model
    model = Sequential([
        # First Conv Layer
        Conv1D(filters=128, kernel_size=5, activation='relu', input_shape=input_shape),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        Dropout(0.3),
        
        # Second Conv Layer
        Conv1D(filters=128, kernel_size=5, activation='relu'),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        Dropout(0.3),
        
        # Classifier (Flatten the sequence output)
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    
    # 3.6 Define Callbacks
    checkpoint = ModelCheckpoint(MODEL_SAVE_PATH, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min', restore_best_weights=True)

    # 3.7 Train the Model
    print("\nStarting model training...")
    history = model.fit(
        X_train_scaled, y_train,
        epochs=100,
        batch_size=32,
        validation_data=(X_test_scaled, y_test),
        callbacks=[checkpoint, early_stopping],
        verbose=1
    )
    
    print(f"\nTraining finished. Best model saved to {MODEL_SAVE_PATH}")
    
# --- Execution ---
if __name__ == "__main__":
    # Ensure the models directory exists
    os.makedirs('models', exist_ok=True)
    
    train_and_save_model()