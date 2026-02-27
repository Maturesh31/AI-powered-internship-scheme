def generate_feedback(result):
    percent = result["match_percent"]
    gap = result["skill_gap"]
    classification = result["classification"]

    if percent < 60:
        if gap:
            weak_skills = sorted(gap, key=gap.get, reverse=True)[:2]
            return f"You achieved {percent}% match. Improve {', '.join(weak_skills)} to meet eligibility."
        return f"You achieved {percent}% match. Strengthen required skills."

    if classification == "Strong Match":
        return f"Excellent profile alignment with {percent}% match. You are well suited for this role."

    return f"You achieved {percent}% match. Improving high-weighted weak skills can increase competitiveness."