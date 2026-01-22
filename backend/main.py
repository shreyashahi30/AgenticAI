import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.utils.resume_parser import extract_text_from_pdf
from backend.ai.agents import (
    skill_assessment_agent,
    market_demand_agent,
    skill_gap_agent,
    learning_path_agent
)
from backend.utils.adaptive_logic import calculate_readiness

from backend.database.db import engine, SessionLocal
from backend.database import models
from backend.database.models import UserProfile, Progress


# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------- DB INIT ----------------
models.Base.metadata.create_all(bind=engine)


# ---------------- APP ----------------
app = FastAPI(title="Agentic AI Skill Gap & Career Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- COST CONTROL ----------------
MAX_RESUME_CHARS = 5000
MAX_CALLS_PER_REQUEST = 4


@app.get("/")
def home():
    return {"message": "Agentic AI Skill Gap Planner running (Real AI Pipeline)"}


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    target_role: str = Form(...)
):
    try:
        logger.info("Received resume upload")

        # 1. Extract text
        resume_text = extract_text_from_pdf(file.file)
        resume_text = resume_text[:MAX_RESUME_CHARS]
        logger.info(f"Resume extracted. Length: {len(resume_text)} chars")

        # 2. AI Pipeline
        logger.info("Calling skill_assessment_agent")
        student_profile = skill_assessment_agent(resume_text)

        logger.info("Calling market_demand_agent")
        market_profile = market_demand_agent(target_role)

        logger.info("Calling skill_gap_agent")
        skill_gap = skill_gap_agent(
            student_profile.skills,
            market_profile.required_skills
        )

        logger.info("Calling learning_path_agent")
        roadmap = learning_path_agent(skill_gap)

        # 3. Save to DB
        db = SessionLocal()
        user = UserProfile(
            resume_text=resume_text,
            target_role=target_role,
            skills=student_profile.skills,
            missing_skills=skill_gap.missing_skills,
            roadmap=roadmap.model_dump()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()

        logger.info(f"User {user.id} saved successfully")

        return {
             "user_id": user.id,
             "target_role": target_role,
             "current_skills": student_profile.skills,
             "missing_skills": skill_gap.missing_skills,
             "readiness_score": roadmap.career_readiness_score if hasattr(roadmap, "career_readiness_score") else 30,
             "roadmap": {
                 "30": roadmap.roadmap[:4],
                 "60": roadmap.roadmap[4:8],
                 "90": roadmap.roadmap[8:12],
                }
        }
    
    except Exception as e:
        logger.error(f"AI Pipeline failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="AI service unavailable, try again later"
        )

@app.get("/progress/{user_id}")
def get_user_progress(user_id: int):
    db = SessionLocal()

    completed = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.completed == True
    ).count()

    total = 12  # total roadmap tasks (4 for 30, 4 for 60, 4 for 90)

    db.close()

    percentage = int((completed / total) * 100) if total > 0 else 0

    return {
        "completed_tasks": completed,
        "total_tasks": total,
        "completion_percentage": percentage
    }


@app.post("/update-progress")
def update_progress(payload: dict):
    db = SessionLocal()

    progress = Progress(
        user_id=payload["user_id"],
        skill=payload["period"],
        task=f"Task index {payload['task_index']}",
        completed=True
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)
    db.close()

    return {"message": "Progress updated"}

@app.get("/adaptive-roadmap/{user_id}")
def adaptive_roadmap(user_id: int):
    db = SessionLocal()

    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    completed = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.completed == True
    ).count()

    base = user.roadmap.get("career_readiness_score", 30)
    new_score = calculate_readiness(base, completed)

    db.close()

    return {
        "readiness_score": new_score,
        "roadmap": user.roadmap
    }

