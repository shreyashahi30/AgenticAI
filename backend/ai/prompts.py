def resume_skill_prompt(resume_text: str) -> str:
    return f"""
You are an AI resume analyzer.
Extract skills and experience.

Return ONLY valid JSON:

{{
  "skills": ["Python", "SQL"],
  "experience_level": "Beginner | Intermediate | Advanced",
  "summary": "Short professional summary"
}}

Resume:
{resume_text}
"""


def market_demand_prompt(target_role: str) -> str:
    return f"""
You are a job market expert.

Return ONLY valid JSON:

{{
  "required_skills": ["Python", "Docker", "AWS"],
  "trend": "High / Medium / Low",
  "summary": "Market demand summary"
}}

Target role:
{target_role}
"""


def skill_gap_prompt(user_skills, market_skills) -> str:
    return f"""
Compare user skills and market skills.

Return ONLY valid JSON:

{{
  "missing_skills": ["Docker", "Kubernetes"],
  "priority": "High / Medium / Low"
}}

User skills: {user_skills}
Market skills: {market_skills}
"""


def learning_path_prompt(skill_gap) -> str:
    return f"""
You are an expert career coach AI.

STRICT RULES:
- Output ONLY valid JSON
- Do NOT use markdown
- Do NOT use ```json
- Do NOT explain anything
- Do NOT add text outside JSON
- Every string must be quoted
- No trailing commas

Format:

{{
  "roadmap": [
    {{"week": 1, "skill": "Docker", "task": "Learn Docker basics"}},
    {{"week": 2, "skill": "Docker", "task": "Build containers"}},
    {{"week": 3, "skill": "Kubernetes", "task": "Deploy app"}}
  ],
  "career_readiness_score": 70
}}

Skill gap data:
{skill_gap}
"""
