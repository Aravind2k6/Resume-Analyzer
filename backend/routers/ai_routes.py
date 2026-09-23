import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.resume_parser import extract_resume_text
from backend.services.ai_assistant import (
    generate_ai_analysis,
    extract_skills_with_ai
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "uploads"
)


class ResumeRequest(BaseModel):
    filename: str


def get_filename(data: ResumeRequest):

    filename = data.filename.strip()

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume or provide a filename."
        )

    return filename


def get_resume_text(filename: str):

    file_path = os.path.join(
        UPLOAD_DIR,
        os.path.basename(filename)
    )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Resume file not found: {filename}"
        )

    try:
        return extract_resume_text(file_path)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not read resume: {str(e)}"
        )


@router.post("/analysis")
def ai_analysis(data: ResumeRequest):

    filename = get_filename(data)

    resume_text = get_resume_text(filename)

    result = generate_ai_analysis(resume_text)

    return {
        "success": True,
        "filename": filename,
        "analysis": result
    }


@router.post("/extract-skills")
def extract_skills(data: ResumeRequest):

    filename = get_filename(data)

    resume_text = get_resume_text(filename)

    result = extract_skills_with_ai(resume_text)

    return {
        "success": True,
        "filename": filename,
        "skills": result
    }