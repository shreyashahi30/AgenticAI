from sqlalchemy import Column, Integer, String, JSON, Boolean, ForeignKey
from backend.database.db import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    resume_text = Column(String)
    target_role = Column(String)
    skills = Column(JSON)
    missing_skills = Column(JSON)
    roadmap = Column(JSON)

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    skill = Column(String)
    task = Column(String)
    completed = Column(Boolean, default=False)