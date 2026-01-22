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
    roadmap = {
        "30_days": [],
        "60_days": [],
        "90_days": []
    }

    for skill in skill_gap["missing_skills"]:
        roadmap["30_days"].append({
            "skill": skill,
            "goal": f"Learn basics of {skill}",
            "resources": [
                f"YouTube: {skill} tutorial",
                f"Coursera: Intro to {skill}"
            ],
            "project": f"Mini project using {skill}"
        })

        roadmap["60_days"].append({
            "skill": skill,
            "goal": f"Build intermediate projects with {skill}",
            "resources": [
                f"Official docs of {skill}",
                "Medium tutorials"
            ],
            "project": f"Intermediate project using {skill}"
        })

        roadmap["90_days"].append({
            "skill": skill,
            "goal": f"Master {skill} for job readiness",
            "resources": [
                "System design practice",
                "Mock interviews"
            ],
            "project": f"Capstone project using {skill}"
        })

    readiness_score = max(20, 100 - len(skill_gap["missing_skills"]) * 15)

    return {
        "roadmap": roadmap,
        "career_readiness_score": readiness_score
    }
