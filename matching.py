def calculate_match(student, internship):
    required = internship["required_skills"]
    weights = internship["weights"]
    student_skills = student["skills"]

    total_score = 0
    skill_gap = {}
    strong_skills = []
    weak_skills = {}

    for skill, required_level in required.items():
        weight = weights.get(skill, 0)
        student_level = student_skills.get(skill, 0)

        # Normalized score (cap at 1)
        normalized = min(student_level / required_level, 1)
        total_score += normalized * weight

        # Gap calculation
        if student_level < required_level:
            skill_gap[skill] = (required_level - student_level) * weight
            
        if student_level >= required_level:
            strong_skills.append(skill)
        else:
            weak_skills[skill] = (required_level - student_level) * weight

    match_percent = round(total_score * 100, 2)

    # Classification
    if match_percent >= 80:
        classification = "Strong Match"
    elif match_percent >= 60:
        classification = "Moderate Match"
    else:
        classification = "Skill Gap Alert"

    return {
        "match_percent": match_percent,
        "classification": classification,
        "strong_skills": strong_skills,
        "weak_skills": weak_skills
    }