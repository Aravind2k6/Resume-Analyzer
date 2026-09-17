SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "docker",
    "kubernetes",
    "fastapi",
    "django",
    "flask"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def calculate_match(resume_skills, job_skills):

    resume_skills = set(resume_skills)
    job_skills = set(job_skills)

    if not job_skills:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "match_percentage": 0
        }

    matched_skills = resume_skills.intersection(job_skills)

    missing_skills = job_skills - resume_skills

    match_percentage = (
        len(matched_skills) / len(job_skills)
    ) * 100

    return {
        "matched_skills": sorted(list(matched_skills)),
        "missing_skills": sorted(list(missing_skills)),
        "match_percentage": round(match_percentage, 2)
    }