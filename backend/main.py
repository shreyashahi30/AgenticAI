from fastapi import FastAPI
from backend.mock_ai.mock_agents import (
    skill_assessment_agent,
    market_demand_agent,
    skill_gap_agent,
    learning_path_agent
)

app = FastAPI(title="Agentic AI Skill Gap & Career Planner")

@app.get("/")
def home():
    return {"message": "Agentic AI Skill Gap Planner running (Mock Mode)"}


@app.post("/analyze")
def analyze(resume_text: str, target_role: str):
    student_profile = skill_assessment_agent(resume_text)
    market_profile = market_demand_agent(target_role)
    skill_gap = skill_gap_agent(
        student_profile["skills"],
        market_profile["required_skills"]
    )
    roadmap = learning_path_agent(skill_gap)

    return {
        "student_profile": student_profile,
        "market_profile": market_profile,
        "skill_gap": skill_gap,
        "learning_roadmap": roadmap
    }
