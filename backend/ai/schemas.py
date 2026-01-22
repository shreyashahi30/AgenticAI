from pydantic import BaseModel
from typing import List, Dict


class SkillProfile(BaseModel):
    skills: List[str]
    experience_level: str
    summary: str


class MarketProfile(BaseModel):
    required_skills: List[str]
    trend: str
    summary: str


class SkillGapProfile(BaseModel):
    missing_skills: List[str]
    priority: str


class LearningPathProfile(BaseModel):
    roadmap: List[Dict]
    career_readiness_score: int
