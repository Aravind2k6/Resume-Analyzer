import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "gemma3:1b"


def ask_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return "Ollama is not running. Start Ollama using: ollama serve"

    except requests.exceptions.Timeout:
        return "Ollama request timed out. Please try again."

    except Exception as e:
        return f"Ollama error: {str(e)}"


def generate_ai_analysis(resume_text: str) -> str:

    prompt = f"""
You are an AI resume analyzer.

Analyze the following resume and provide useful career feedback.

Resume:
----------------
{resume_text}
----------------

Give the answer in this format:

RESUME SUMMARY:
Give a short summary.

STRENGTHS:
- List 3 to 5 strengths.

SKILLS:
- List the important technical skills.

AREAS TO IMPROVE:
- List 3 to 5 improvements.

ATS SUGGESTIONS:
- Give practical ATS optimization suggestions.

CAREER SUGGESTION:
- Suggest suitable software/technology roles.

Keep the response simple and practical.
"""

    return ask_ollama(prompt)


def extract_skills_with_ai(resume_text: str) -> str:

    prompt = f"""
Extract technical skills from this resume.

Resume:
----------------
{resume_text}
----------------

Return only the skills grouped like this:

PROGRAMMING:
Java, Python, C++

WEB:
HTML, CSS, JavaScript, React

DATABASE:
MySQL, PostgreSQL

CLOUD:
AWS, Azure, GCP

AI / ML:
Machine Learning, Generative AI

TOOLS:
Git, GitHub, Docker

Only include skills that are actually present in the resume.
"""

    return ask_ollama(prompt)


def analyze_job_match(resume_text: str, job_description: str) -> str:

    prompt = f"""
You are an AI job matching assistant.

RESUME:
----------------
{resume_text}
----------------

JOB DESCRIPTION:
----------------
{job_description}
----------------

Compare the resume with the job description.

Return:

MATCH PERCENTAGE:
Give an estimated percentage.

MATCHED SKILLS:
- List skills present in both.

MISSING SKILLS:
- List skills required by the job but missing from the resume.

STRENGTHS FOR THIS JOB:
- Explain why the candidate matches.

IMPROVEMENTS:
- Explain what should be added or improved.

FINAL SUGGESTION:
Give a short practical recommendation.

Keep the answer clear and simple.
"""

    return ask_ollama(prompt)