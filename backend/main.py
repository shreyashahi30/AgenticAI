from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

# Utils
from backend.utils.resume_parser import extract_text_from_pdf
from backend.utils.adaptive_logic import calculate_readiness

# Mock AI Agents
from backend.mock_ai.mock_agents import (
    skill_assessment_agent,
    market_demand_agent,
    skill_gap_agent,
    learning_path_agent
)

# Database
from backend.database.db import engine, SessionLocal
from backend.database import models
from backend.database.models import UserProfile, Progress

# ----------------------------------
# Create FastAPI app
# ----------------------------------
app = FastAPI(title="Agentic AI Skill Gap & Career Planner")

# ----------------------------------
# Enable CORS for React frontend
# ----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------
# Create DB Tables Automatically
# ----------------------------------
models.Base.metadata.create_all(bind=engine)

# ----------------------------------
# Health Check
# ----------------------------------
@app.get("/")
def home():
    return {"message": "Agentic AI Skill Gap Planner running (Mock Mode + DB Enabled)"}


# ----------------------------------
# Upload Resume & Analyze
# ----------------------------------
@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    target_role: str = Form(...)
):
    # 1. Extract resume text
    resume_text = extract_text_from_pdf(file.file)

    # 2. Mock AI pipeline
    student_profile = skill_assessment_agent(resume_text)
    market_profile = market_demand_agent(target_role)

    skill_gap = skill_gap_agent(
        student_profile["skills"],
        market_profile["required_skills"]
    )

    roadmap = learning_path_agent(skill_gap)

    # 3. Save to Database
    db = SessionLocal()
    user = UserProfile(
        resume_text=resume_text,
        target_role=target_role,
        skills=student_profile["skills"],
        missing_skills=skill_gap["missing_skills"],
        roadmap=roadmap
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    # 4. Return response
    return {
        "user_id": user.id,
        "target_role": target_role,
        "current_skills": student_profile["skills"],
        "missing_skills": skill_gap["missing_skills"],
        "roadmap": roadmap,
        "readiness_score": roadmap.get("career_readiness_score", 0)
    }


# ----------------------------------
# Update Progress
# ----------------------------------
@app.post("/update-progress")
def update_progress(user_id: int, skill: str, task: str):
    db = SessionLocal()

    progress = Progress(
        user_id=user_id,
        skill=skill,
        task=task,
        completed=True
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)
    db.close()

    return {
        "message": "Progress updated successfully",
        "progress_id": progress.id
    }


# ----------------------------------
# Get User Progress
# ----------------------------------
@app.get("/progress/{user_id}")
def get_user_progress(user_id: int):
    db = SessionLocal()
    progress = db.query(Progress).filter(Progress.user_id == user_id).all()
    db.close()
    return progress


# ----------------------------------
# Adaptive Roadmap Logic
# ----------------------------------
@app.get("/adaptive-roadmap/{user_id}")
def adaptive_roadmap(user_id: int):
    db = SessionLocal()

    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    progress = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.completed == True
    ).all()

    completed_tasks = len(progress)

    # Base score from roadmap
    base_score = user.roadmap.get("career_readiness_score", 50)

    # Adaptive logic
    new_score = calculate_readiness(base_score, completed_tasks)

    db.close()

    return {
        "user_id": user_id,
        "completed_tasks": completed_tasks,
        "old_score": base_score,
        "new_score": new_score,
        "message": "Roadmap adapted based on progress"
    }
