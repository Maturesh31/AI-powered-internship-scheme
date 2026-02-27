from flask import Flask, request, jsonify
import pdfplumber
from docx import Document
import re
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# -------- Skill Categories -------- #
TECH_CATEGORIES = {
    "Programming Languages": ["Python", "Java", "C++", "C", "JavaScript"],
    "Web Development": ["HTML", "CSS", "React", "Django", "Flask", "Node.js"],
    "Data Science": ["Machine Learning", "TensorFlow", "Pandas", "NumPy", "SQL"],
    "Tools": ["Git", "Docker", "AWS", "Linux"]
}

# -------- Text Extraction -------- #
def extract_text(file):
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif file.filename.endswith(".docx"):
        doc = Document(file)
        return "\n".join(para.text for para in doc.paragraphs)

    else:
        return ""

# -------- Information Parsing -------- #
def extract_email(text):
    match = re.findall(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    return match[0] if match else None

def extract_phone(text):
    match = re.findall(r"\+?\d[\d -]{8,15}\d", text)
    return match[0] if match else None

def extract_name(text):
    lines = text.split("\n")
    
    # Check first 10 lines only
    top_section = " ".join(lines[:10])
    
    doc = nlp(top_section)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    
    # Filter out common skill words
    invalid_names = ["Java", "Python", "C", "C++"]
    
    for name in persons:
        if name not in invalid_names and len(name.split()) >= 2:
            return name
    
    return None

def extract_education(text):
    keywords = ["Bachelor", "Master", "B.Tech", "M.Tech", "BSc", "MSc", "PhD"]
    return [line.strip() for line in text.split("\n")
            if any(k.lower() in line.lower() for k in keywords)]

def extract_skills(text):
    found = []
    for category in TECH_CATEGORIES.values():
        for skill in category:
            if skill.lower() in text.lower():
                found.append(skill)
    return list(set(found))

def categorize_skills(skills):
    categorized = {}
    for category, skill_list in TECH_CATEGORIES.items():
        categorized[category] = [s for s in skills if s in skill_list]
    return categorized

# -------- API Endpoint -------- #
@app.route("/upload", methods=["POST"])
def upload_resume():
    file = request.files["resume"]
    text = extract_text(file)

    skills = extract_skills(text)

    response = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "skills": skills,
        "categorized_skills": categorize_skills(skills)
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)