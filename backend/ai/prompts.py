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


def learning_path_prompt(skill_gap_data):
    return f"""
You are an expert AI career mentor.

The user is missing these skills:

{skill_gap_data}

Generate a structured roadmap grouped into 30/60/90 days.

Return STRICT JSON ONLY:

{{
  "roadmap": {{
    "30": [
      {{
        "skill": "Skill name",
        "goal": "What to learn",
        "resources": "Courses/docs",
        "mini_project": "Mini project",
        "completed": false
      }}
    ],
    "60": [
      {{
        "skill": "...",
        "goal": "...",
        "resources": "...",
        "mini_project": "...",
        "completed": false
      }}
    ],
    "90": [
      {{
        "skill": "...",
        "goal": "...",
        "resources": "...",
        "mini_project": "...",
        "completed": false
      }}
    ]
  }}
}}

Rules:
- No markdown
- No explanation
- JSON only
"""
