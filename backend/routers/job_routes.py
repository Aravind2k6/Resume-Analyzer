from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import re

from backend.services.resume_parser import extract_resume_text

router = APIRouter()


class JobMatchRequest(BaseModel):
    filename: str
    job_description: str


@router.post("/match-job")
async def match_job(data: JobMatchRequest):

    if not data.filename:
        raise HTTPException(
            status_code=400,
            detail="Resume filename is required."
        )

    if not data.job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description is required."
        )

    # Resume location
    resume_path = os.path.join(
        "backend",
        "uploads",
        data.filename
    )

    if not os.path.exists(resume_path):

        # Try absolute/current upload location
        alternative_path = os.path.join(
            "uploads",
            data.filename
        )

        if os.path.exists(alternative_path):
            resume_path = alternative_path
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Resume not found: {data.filename}"
            )

    try:
        resume_text = extract_resume_text(resume_path)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not read resume: {str(e)}"
        )

    # Convert both texts to lowercase
    resume_lower = resume_text.lower()
    jd_lower = data.job_description.lower()

    # Common technical skills
    skills = [
        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "node.js",
        "fastapi",
        "django",
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "gcp",
        "machine learning",
        "deep learning",
        "html",
        "css",
        "rest api",
        "spring boot",
        "c++",
        "c"
    ]

    required_skills = []

    for skill in skills:
        if skill.lower() in jd_lower:
            required_skills.append(skill)

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill.lower() in resume_lower:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if required_skills:

        match_percentage = round(
            (len(matched_skills) / len(required_skills)) * 100,
            2
        )

    else:
        match_percentage = 0

    return {
        "success": True,
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "required_skills": required_skills,
        "message": "Job matching completed successfully."
    }