from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import random
from .assessment_data import ASSESSMENT_QUESTIONS 

# Pydantic Model for incoming answers
# The Dict type hint requires Python 3.9+, otherwise use typing.Dict
class AssessmentAnswers(BaseModel):
    answers: Dict[str, int]


app = FastAPI(title="HealthIQ Mood Monitoring API")

# --- CORS Configuration ---

origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    "http://localhost:8501", # Default Streamlit port
    "http://127.0.0.1:8501", 
    # Add your deployed frontend URL here later
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
    return {"status": "Backend OK", "framework": "FastAPI", "version": "0.1.0"}


# --- Psychological Assessment Endpoints ---

@app.post("/api/assessment/get_questions")
def get_assessment_questions():
    """
    Randomly selects 5 psychological questions to present to the user 
    for their daily check-in assessment.
    """
    try:
        # Select 5 random questions from the pool
        questions_list = list(ASSESSMENT_QUESTIONS.values())
        selected_questions = random.sample(questions_list, 5)
    except ValueError:
        raise HTTPException(status_code=500, detail="Error: Not enough questions in the pool to sample 5.")
    
    # Format the output to clearly show the ID and the question text
    formatted_output = [
        {"id": q['id'], "question": q['question']} 
        for q in selected_questions
    ]
    
    return formatted_output

# submit answer.py
@app.post("/api/assessment/submit_answers")
def submit_assessment_answers(answers_data: AssessmentAnswers):
    """
    Receives the user's answers (0-3 scale) and calculates the total Psychological Assessment Score.
    This score is crucial for adjusting the final AI mood prediction.
    """
    total_score = 0
    
    # 1. Iterate through each question ID and the corresponding answer value
    for q_id, answer_value in answers_data.answers.items():
        
        # 2. Validation Check: Does the question ID exist in our pool?
        if q_id in ASSESSMENT_QUESTIONS:
            
            # 3. Validation Check: Is the answer value within the valid range (0-3)?
            if 0 <= answer_value <= 3:
                # Add the valid score to the total
                total_score += answer_value
            else:
                # Raise an error if the score value is invalid
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid answer value for question {q_id}. Must be between 0 and 3."
                )
        else:
            # Skip unknown IDs but rely on the frontend to send correct data
            pass 

    # Calculate the max possible score based on the number of questions sent (assumed 5)
    # Note: We assume the client sent answers for 5 questions
    max_possible_score = len(answers_data.answers) * 3

    
    # 4. Return the result to the frontend
    return {
        "status": "success",
        "total_questions_answered": len(answers_data.answers),
        "psychological_score": total_score,
        "max_possible_score": max_possible_score,
        "interpretation": "Score will be used to weight the final AI mood prediction."
    }