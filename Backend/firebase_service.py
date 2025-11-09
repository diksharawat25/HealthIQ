import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
from typing import Dict, Any

# --- Configuration (CRITICAL: Firebase Admin Key must be here) ---
# Ensure your downloaded key file is named 'serviceAccountKey.json' and is in the Backend folder
SERVICE_ACCOUNT_KEY_PATH = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

# App ID (This should ideally be fetched from environment variables in a real scenario)
APP_ID = "healthiq-app"

# Global database reference
db = None

# --- Initialization Functions ---

def initialize_firebase():
    """Initializes the Firebase Admin SDK using the service account key."""
    global db
    if firebase_admin._apps:
        # Check if app is already initialized
        db = firestore.client()
        print("Firebase already initialized.")
        return

    try:
        # 1. Load the Admin Credentials
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        
        # 2. Initialize the app
        firebase_admin.initialize_app(cred)
        
        # 3. Get Firestore client instance
        db = firestore.client()
        print("Firebase Admin SDK initialized successfully.")
    except FileNotFoundError:
        print(f"ERROR: Service account key not found at {SERVICE_ACCOUNT_KEY_PATH}")
    except Exception as e:
        print(f"ERROR: Failed to initialize Firebase: {e}")

# --- Data Saving Functions ---

def save_mood_log(user_id: str, log_data: Dict[str, Any]) -> bool:
    """
    Saves the final mood analysis log to Firestore under the user's private path.
    Path: /artifacts/{appId}/users/{userId}/mood_logs/{timestamp}
    """
    if db is None:
        print("ERROR: Firestore client not available. Cannot save data.")
        return False

    try:
        # 1. Define the collection path using the structure required by Firebase Security Rules
        collection_path = f"artifacts/{APP_ID}/users/{user_id}/mood_logs"
        
        # 2. Add current timestamp and user ID to the log data
        full_log = {
            "timestamp": datetime.now(),
            "user_id": user_id,
            "date_string": datetime.now().isoformat(),
            **log_data  # Merge the final prediction data
        }
        
        # 3. Add the document to the collection
        db.collection(collection_path).add(full_log)
        
        print(f"SUCCESS: Mood log saved for user {user_id} at {collection_path}")
        return True
    
    except Exception as e:
        print(f"ERROR: Failed to save mood log for user {user_id}: {e}")
        return False