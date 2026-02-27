def generate_feedback(result):
    percent = result["match_percent"]
    classification = result["classification"]
    strong = result.get("strong_skills", [])
    weak = result.get("weak_skills", {})

    feedback = []

    feedback.append(
        f"Your profile achieved a {percent}% alignment score, categorized as {classification}."
    )

    # Strength insight
    if strong:
        feedback.append(
            f"Core strengths include {', '.join(strong[:2])}, demonstrating solid competency in key areas."
        )

    # Weakness insight
    if weak:
        sorted_weak = sorted(weak, key=weak.get, reverse=True)
        top_gaps = sorted_weak[:2]
        feedback.append(
            f"The primary improvement areas are {', '.join(top_gaps)}, which carry significant evaluation weight."
        )

    # Strategic advisory
    if percent >= 85:
        feedback.append(
            "Your profile is highly competitive and stands out strongly among typical applicants."
        )
    elif percent >= 75:
        feedback.append(
            "With minor targeted skill refinement, your candidacy can become exceptionally strong."
        )
    elif percent >= 60:
        feedback.append(
            "Focused upskilling in the highlighted areas can substantially increase your selection probability."
        )
    else:
        feedback.append(
            "Significant skill development is recommended to meet the required competency threshold."
        )

    return " ".join(feedback)