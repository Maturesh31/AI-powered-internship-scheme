from matching import calculate_match
from feedback import generate_feedback

CUTOFF = 60
SKILL_WEIGHT = 0.7
PREFERENCE_WEIGHT = 0.3
MAX_PREFERENCES = 5

def get_preference_score(rank):
    return ((MAX_PREFERENCES - rank + 1) / MAX_PREFERENCES) * 100


def allocate_students(students, internships):
    results = []

    for student in students:
        ranking = []

        for rank, company_name in enumerate(student["preferences"], start=1):
            internship = next(
                (i for i in internships if i["company"] == company_name),
                None
            )

            if not internship:
                continue

            match_result = calculate_match(student, internship)

            if match_result["match_percent"] < CUTOFF:
                continue

            preference_score = get_preference_score(rank)

            final_score = (
                match_result["match_percent"] * SKILL_WEIGHT +
                preference_score * PREFERENCE_WEIGHT
            )

            ranking.append({
                "company": company_name,
                "match_percent": match_result["match_percent"],
                "final_score": round(final_score, 2),
                "classification": match_result["classification"]
            })

        # Sort by final_score descending
        ranking.sort(key=lambda x: x["final_score"], reverse=True)

        assigned_company = None
        feedback = "No internship met the 60% cutoff."

        for option in ranking:
            internship = next(
                (i for i in internships if i["company"] == option["company"]),
                None
            )

            if internship and internship["slots"] > 0:
                internship["slots"] -= 1
                assigned_company = option["company"]

                # Generate feedback using best match
                best_match_result = calculate_match(student, internship)
                feedback = generate_feedback(best_match_result)
                break

        results.append({
            "student": student["name"],
            "assigned_to": assigned_company,
            "ranking": ranking,
            "feedback": feedback
        })

    return results