from matching import calculate_match
from feedback import generate_feedback

CUTOFF = 60

def allocate_students(students, internships):
    results = []

    for student in students:
        best_option = None
        best_score = 0
        best_internship = None

        for internship in internships:
            if internship["slots"] <= 0:
                continue

            result = calculate_match(student, internship)

            if result["match_percent"] >= CUTOFF:
                if result["match_percent"] > best_score:
                    best_score = result["match_percent"]
                    best_option = result
                    best_internship = internship

        if best_option:
            best_internship["slots"] -= 1
            feedback = generate_feedback(best_option)

            results.append({
                "student": student["name"],
                "assigned_to": best_internship["company"],
                "match_percent": best_option["match_percent"],
                "classification": best_option["classification"],
                "feedback": feedback
            })
        else:
            results.append({
                "student": student["name"],
                "assigned_to": None,
                "match_percent": 0,
                "classification": "Not Eligible",
                "feedback": "No internship met the 60% cutoff. Improve core skills."
            })

    return results