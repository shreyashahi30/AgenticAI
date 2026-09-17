# =========================================================
# RESUME SKILL PROMPT
# =========================================================

def resume_skill_prompt(resume_text: str) -> str:
    return f"""
You are an AI resume analyzer.

Analyze the resume and extract the candidate's technical skills,
experience level, and a short professional summary.

IMPORTANT:
Return ONLY a valid JSON object.
Do not use Markdown.
Do not use ```json.
Do not include explanations outside the JSON.

Use exactly this structure:

{{
    "skills": ["Python", "SQL"],
    "experience_level": "Beginner",
    "summary": "Short professional summary"
}}

Rules:
- skills must be an array of strings.
- experience_level must be one of:
  "Beginner", "Intermediate", or "Advanced".
- summary must be a short string.
- Return valid JSON only.

Resume:
{resume_text}
"""


# =========================================================
# MARKET DEMAND PROMPT
# =========================================================

def market_demand_prompt(target_role: str) -> str:
    return f"""
You are a job market analysis expert.

Analyze the skills generally required for the specified target role.

IMPORTANT:
Return ONLY a valid JSON object.
Do not use Markdown.
Do not use ```json.
Do not include explanations outside the JSON.

Use exactly this structure:

{{
    "required_skills": ["Python", "Docker", "AWS"],
    "trend": "High",
    "summary": "Short market demand summary"
}}

Rules:
- required_skills must be an array of strings.
- trend must be one of:
  "High", "Medium", or "Low".
- summary must be a short string.
- Return valid JSON only.

Target role:
{target_role}
"""


# =========================================================
# SKILL GAP PROMPT
# =========================================================

def skill_gap_prompt(user_skills, market_skills) -> str:
    return f"""
You are a career skill-gap analysis expert.

Compare the candidate's current skills against the skills
required by the target role.

IMPORTANT:
Return ONLY a valid JSON object.
Do not use Markdown.
Do not use ```json.
Do not include explanations outside the JSON.

Use exactly this structure:

{{
    "missing_skills": ["Docker", "Kubernetes"],
    "priority": "High"
}}

Rules:
- missing_skills must be an array of strings.
- priority must be one of:
  "High", "Medium", or "Low".
- If there are no important missing skills, return an empty array.
- Return valid JSON only.

User skills:
{user_skills}

Market skills:
{market_skills}
"""


# =========================================================
# LEARNING PATH PROMPT
# =========================================================

def learning_path_prompt(skill_gap_data) -> str:
    return f"""
You are an expert AI career mentor.

The user is missing the following skills:

{skill_gap_data}

Create a practical 30/60/90-day learning roadmap.

IMPORTANT:
Return ONLY a valid JSON object.
Do not use Markdown.
Do not use ```json.
Do not include explanations outside the JSON.

The JSON MUST follow exactly this structure:

{{
    "roadmap": {{
        "30": [
            {{
                "skill": "Skill name",
                "goal": "What the user should learn",
                "resources": "Courses, documentation, or learning resources",
                "mini_project": "A small project to practice the skill",
                "completed": false
            }}
        ],
        "60": [
            {{
                "skill": "Skill name",
                "goal": "What the user should learn",
                "resources": "Courses, documentation, or learning resources",
                "mini_project": "A small project to practice the skill",
                "completed": false
            }}
        ],
        "90": [
            {{
                "skill": "Skill name",
                "goal": "What the user should learn",
                "resources": "Courses, documentation, or learning resources",
                "mini_project": "A small project to practice the skill",
                "completed": false
            }}
        ]
    }}
}}

Rules:
- roadmap must contain exactly the keys "30", "60", and "90".
- Each key must contain an array.
- Each roadmap item must contain:
  "skill"
  "goal"
  "resources"
  "mini_project"
  "completed"
- completed must always be false for newly generated roadmap items.
- Keep the roadmap practical and career-focused.
- Return valid JSON only.
"""
