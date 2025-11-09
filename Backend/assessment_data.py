# backend/assessment_data.py
# Psychological questions based on common mood scales.
# Answers will be on a Likert scale (0=Not at all, 3=Nearly every day).

ASSESSMENT_QUESTIONS = {
    "Q1": {
        "id": "Q1",
        "question": "Over the last two weeks, how often have you felt little interest or pleasure in doing things?",
        "scale": "PHQ"
    },
    "Q2": {
        "id": "Q2",
        "question": "Over the last two weeks, how often have you felt down, depressed, or hopeless?",
        "scale": "PHQ"
    },
    "Q3": {
        "id": "Q3",
        "question": "Are you feeling easily annoyed, irritable, or restless lately?",
        "scale": "GAD"
    },
    "Q4": {
        "id": "Q4",
        "question": "Have you been worrying too much about different things?",
        "scale": "GAD"
    },
    "Q5": {
        "id": "Q5",
        "question": "Do you often feel bothered by feeling tired or having little energy?",
        "scale": "General"
    },
    "Q6": {
        "id": "Q6",
        "question": "Do you find yourself sleeping much less or much more than usual?",
        "scale": "General"
    },
    "Q7": {
        "id": "Q7",
        "question": "How often have you felt difficulty relaxing or winding down?",
        "scale": "Stress"
    },
    "Q8": {
        "id": "Q8",
        "question": "Have you felt afraid, as if something awful might happen?",
        "scale": "Anxiety"
    },
    "Q9": {
        "id": "Q9",
        "question": "How often have you found it hard to concentrate on things, such as reading or watching TV?",
        "scale": "Focus"
    },
    "Q10": {
        "id": "Q10",
        "question": "Have you noticed any significant changes in your appetite or weight?",
        "scale": "General"
    }
}