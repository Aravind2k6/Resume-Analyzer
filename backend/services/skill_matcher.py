import re


SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "react",
    "angular",
    "node.js",
    "node",
    "html",
    "css",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "fastapi",
    "flask",
    "django",
    "spring",
    "spring boot",
    "rest api",
    "rest",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "google cloud",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "scikit-learn",
    "generative ai",
    "artificial intelligence",
    "nlp",
    "linux",
    "mongodb",
]


def normalize_text(text: str) -> str:

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def extract_skills(text: str):

    normalized = normalize_text(text)

    found = []

    for skill in SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, normalized):

            if skill not in found:
                found.append(skill)

    return sorted(found)


def match_resume_to_job(
    resume_text: str,
    job_description: str
):

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_description)
    )

    if not job_skills:

        return {
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": [],
            "resume_skills": sorted(resume_skills),
            "job_skills": [],
            "message": "No recognized skills were found in the job description."
        }

    matched = sorted(
        resume_skills.intersection(job_skills)
    )

    missing = sorted(
        job_skills.difference(resume_skills)
    )

    percentage = (
        len(matched) / len(job_skills)
    ) * 100

    percentage = round(
        percentage,
        2
    )

    return {
        "match_percentage": percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills)
    }