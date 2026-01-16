from fastapi import FastAPI

app = FastAPI(title="Agentic AI Skill Gap & Career Planner")

@app.get("/")
def home():
    return {"message": "Backend is running successfully"}
