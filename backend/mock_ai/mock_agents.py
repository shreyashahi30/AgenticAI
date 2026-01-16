def skill_assessment_agent(resume_text):
    return {
        "skills": ["Python", "HTML", "Basic SQL"],
        "experience_level": "Beginner"
    }


def market_demand_agent(target_role):
    roles = {
        "data analyst": ["Python", "SQL", "Power BI", "Statistics", "Excel"],
        "backend developer": ["Python", "FastAPI", "PostgreSQL", "Docker", "Git"]
    }
    return {
        "required_skills": roles.get(target_role.lower(), ["Python", "Git"])
    }


def skill_gap_agent(student_skills, required_skills):
    missing = list(set(required_skills) - set(student_skills))
    strengths = list(set(student_skills) & set(required_skills))

    return {
        "missing_skills": missing,
        "strengths": strengths
    }


def learning_path_agent(skill_gap):
    roadmap = []
    day = 1
    for skill in skill_gap["missing_skills"]:
        roadmap.append({
            "day": day,
            "skill": skill,
            "task": f"Learn basics of {skill}",
            "practice": f"Build a mini project using {skill}"
        })
        day += 2

    return {
        "estimated_days": len(roadmap) * 2,
        "roadmap": roadmap
    }
