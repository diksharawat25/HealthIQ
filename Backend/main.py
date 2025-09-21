from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the HealthIQ Backend!"}

@app.get("/health")
def check_health():
    return {"status": "ok"}