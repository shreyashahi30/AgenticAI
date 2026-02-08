from pydantic import BaseModel
from typing import List, Dict


# ---------------- SKILL PROFILE ----------------
class SkillProfile(BaseModel):
    skills: List[str]
    experience_level: str
    summary: str


# ---------------- MARKET PROFILE ----------------
class MarketProfile(BaseModel):
    required_skills: List[str]
    trend: str
    summary: str


# ---------------- SKILL GAP PROFILE ----------------
class SkillGapProfile(BaseModel):
    missing_skills: List[str]
    priority: str


# ---------------- ROADMAP ITEM ----------------
class RoadmapItem(BaseModel):
    skill: str
    goal: str
    resources: str
    mini_project: str
    completed: bool = False


# ---------------- LEARNING PATH PROFILE ----------------
class LearningPathProfile(BaseModel):
    roadmap: Dict[str, List[RoadmapItem]]
