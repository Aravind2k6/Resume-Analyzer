import ollama


def generate_ai_analysis(resume_text):

    prompt = f"""
You are an AI Resume Analyzer.

Analyze the following resume carefully.

Provide the response using these sections:

## 1. Resume Strengths
Identify the main strengths of the resume.

## 2. Resume Weaknesses
Identify areas that can be improved.

## 3. Missing or Recommended Skills
Suggest useful technical skills based on the resume.

## 4. Resume Improvement Suggestions
Give practical suggestions to improve the resume.

## 5. Recommended Learning Areas
Suggest technologies or topics the candidate should learn.

## 6. Interview Questions
Give 5 relevant interview questions based on the resume.

Keep the response simple, clear and useful for a student or job seeker.

Resume:
{resume_text}
"""

    response = ollama.chat(
        model="gemma3:1b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]