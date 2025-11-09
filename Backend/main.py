import random
import os
import io
import asyncio
from typing import Dict, Annotated, Optional
from contextlib import asynccontextmanager 
import numpy as np

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# --- LOCAL MODULE IMPORTS (Corrected Structure) ---
# 1. Assessment Data
from assessment_data import ASSESSMENT_QUESTIONS

# 2. AI Mood Detection Logic
from mood_detector.text_model import load_text_model, get_text_mood
from mood_detector.voice_model import load_voice_model, get_voice_mood

# 3. Firebase Service for Data Storage
from firebase_service import initialize_firebase, save_mood_log 

# --- Pydantic Data Models ---

# Model for incoming answers for the psychological assessment
class AssessmentAnswers(BaseModel):
    answers: Dict[str, int]

# Model for incoming Text Input
class TextInput(BaseModel):
    text: str = Field(..., description="User's journal entry or mood message.")

# Input model for the FINAL integration endpoint (combines scores from client)
class FinalCheckinData(BaseModel):
    user_id: str = Field(..., description="Firebase user ID for logging.")
    psychological_score: int = Field(..., ge=0, le=15, description="Total score from the assessment questions.")
    text_mood: str = Field(..., description="Mood predicted by the Text API (e.g., Positive, Negative).")
    voice_mood: str = Field(..., description="Mood predicted by the Voice API (e.g., Happy, Angry, Sad).")


# --- Modern Lifespan Manager (Startup/Shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes AI models and Firebase Admin SDK."""
    print("--- Starting AI Model Loading & Firebase Initialization ---")
    
    # Load Models
    load_text_model()
    load_voice_model()
    
    # Initialize Firebase Admin SDK
    initialize_firebase()
    
    await asyncio.sleep(0.5)
    print("--- All Services Loaded Successfully. Application Ready ---")
    
    yield
    
    print("--- Application Shutting Down ---")


# --- FastAPI App Initialization ---

app = FastAPI(title="HealthIQ Mood Monitoring API", version="0.3.1", lifespan=lifespan)

# --- CORS Configuration ---

origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    "http://localhost:8501", # Default Streamlit port
    "http://127.0.0.1:8501", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Basic Health Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the HealthIQ Backend! Head to /docs for API documentation."}

@app.get("/health")
def check_health():
    """Confirms the backend is running and ready for API calls."""
    return {"status": "Backend OK", "framework": "FastAPI", "version": "0.3.1"}


# --- 1. Psychological Assessment Endpoints ---

@app.post("/api/assessment/get_questions")
def get_assessment_questions():
    """Randomly selects 5 psychological questions for the user's daily check-in."""
    try:
        questions_list = list(ASSESSMENT_QUESTIONS.values())
        selected_questions = random.sample(questions_list, 5)
    except ValueError:
        raise HTTPException(status_code=500, detail="Error: Not enough questions in the pool to sample 5.")
    
    formatted_output = [
        {"id": q['id'], "question": q['question']} 
        for q in selected_questions
    ]
    
    return formatted_output

@app.post("/api/assessment/submit_answers")
def submit_assessment_answers(answers_data: AssessmentAnswers):
    """
    Receives the user's answers (0-3 scale) and calculates the total Psychological Assessment Score.
    """
    total_score = 0
    
    # 1. Calculate the total score
    for q_id, answer_value in answers_data.answers.items():
        if q_id in ASSESSMENT_QUESTIONS:
            if 0 <= answer_value <= 3:
                total_score += answer_value
            else:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid answer value for question {q_id}. Must be between 0 and 3."
                )
        else:
            pass 

    # Calculate the max possible score 
    max_possible_score = len(answers_data.answers) * 3
    
    return {
        "status": "success",
        "total_questions_answered": len(answers_data.answers),
        "psychological_score": total_score,
        "max_possible_score": max_possible_score,
        "interpretation": "Score will be used to weight the final AI mood prediction."
    }

# --- 2. AI Mood Detection Endpoints ---

@app.post("/api/mood/text")
def analyze_mood_text(data: TextInput):
    """
    Predicts mood from user-provided text using the trained Text Sentiment Model.
    """
    if not data.text:
        raise HTTPException(status_code=400, detail="Text input cannot be empty.")
        
    prediction_result = get_text_mood(data.text)
    
    if "error" in prediction_result:
        raise HTTPException(status_code=500, detail=prediction_result["error"])

    return prediction_result

@app.post("/api/mood/voice")
async def analyze_mood_voice(audio_file: Annotated[UploadFile, File(description="The audio file (.wav, .mp3) to analyze.")]):
    """
    Analyzes an uploaded audio file (e.g., recorded voice memo) using the trained
    Voice Emotion Recognition Model.
    """
    if audio_file.content_type not in ["audio/wav", "audio/mp3", "audio/mpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an audio file (WAV or MP3).")
        
    try:
        # Read the file bytes asynchronously
        audio_bytes = await audio_file.read()
        
        # Get prediction from the voice model logic
        prediction_result = get_voice_mood(audio_bytes)

        if "error" in prediction_result:
             raise HTTPException(status_code=500, detail=prediction_result["error"])
        
        return prediction_result
        
    except Exception as e:
        print(f"Voice Prediction Error: {e}")
        raise HTTPException(status_code=500, detail="Error processing audio file.")


# --- 3. Final Integration and Data Persistence Endpoint ---

@app.post("/api/mood/final_checkin")
def finalize_mood(data: FinalCheckinData):
    """
    Combines predictions (Text Mood, Voice Mood) and the Psychological Score 
    to provide the single, final, most accurate mood and saves the log to Firestore.
    """
    
    # --- 1. Final Mood Determination Logic ---
    
    # Score the AI inputs (Positive=1, Negative=-1, Neutral=0)
    ai_scores = []
    
    # Text Scoring
    if data.text_mood == "Positive":
        ai_scores.append(1)
    elif data.text_mood == "Negative":
        ai_scores.append(-1)
    
    # Voice Scoring (Simplifying emotions for final consensus)
    if data.voice_mood in ["happy", "calm"]:
        ai_scores.append(1)
    elif data.voice_mood in ["sad", "angry", "fearful"]:
        ai_scores.append(-1)
    
    # Calculate Final AI Consensus Score
    ai_consensus_score = sum(ai_scores)
    
    final_mood = "Neutral"
    suggestion = "Continue to track your mood and prioritize sleep."
    
    # --- 2. Applying Consensus and Psychological Weight ---
    
    # Case 1: Strong Positive Consensus and Low Distress
    if ai_consensus_score > 0 and data.psychological_score < 5:
        final_mood = "Positive"
        suggestion = "Great job! Maintain your current healthy routines."
    
    # Case 2: Negative Consensus and High Distress (Critical)
    elif ai_consensus_score < 0 and data.psychological_score > 8:
        final_mood = "Distressed"
        suggestion = "We detect high distress. Focus on stress-reducing activities like meditation or connecting with a friend."
        
    # Case 3: Very High Self-Reported Distress (Overrules AI)
    elif data.psychological_score > 10:
        final_mood = "High Anxiety"
        suggestion = "Your self-assessment indicates severe difficulty. Please consider speaking with a mental health professional."
        
    else:
        final_mood = "Mixed/Stable"
        suggestion = "Your mood indicators are mixed. Pay close attention to your sleep and activity levels today."
    
    
    # --- 3. Data Saving to Firestore (THIS IS THE NEW LOGIC) ---
    
    log_status = save_mood_log(
        user_id=data.user_id,
        log_data={
            "final_status": final_mood,
            "suggestion_text": suggestion,
            "text_mood": data.text_mood,
            "voice_mood": data.voice_mood,
            "psych_score": data.psychological_score,
            "ai_consensus_score": ai_consensus_score,
        }
    )

    if not log_status:
        # Raise a 500 error if the database failed to save the calculated result
        raise HTTPException(status_code=500, detail="Final mood calculated, but failed to save data to Firestore. Check Firebase logs.")

    # --- 4. Return Final Decision ---
    return {
        "user_id": data.user_id,
        "final_mood_status": final_mood,
        "final_suggestion": suggestion,
        "raw_scores_used": {
            "ai_consensus": ai_consensus_score,
            "psych_score": data.psychological_score
        }
    }