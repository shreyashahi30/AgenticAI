def calculate_readiness(base_score, completed_tasks):
    score = base_score + (completed_tasks * 5)
    return min(score, 100)
