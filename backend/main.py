from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Form,
    Depends
)

from pathlib import Path
import shutil
import json

from sqlalchemy.orm import Session

from services.resume_parser import extract_text_from_pdf
from services.skill_matcher import (
    extract_skills,
    calculate_match
)

from services.ai_assistant import generate_ai_analysis

from database.database import (
    engine,
    Base,
    get_db
)

from database import models


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

Base.metadata.create_all(
    bind=engine
)


# --------------------------------------------------
# FASTAPI
# --------------------------------------------------

app = FastAPI(
    title="AI Resume Analyzer API",
    description="AI Resume Analyzer and Job Assistant",
    version="1.0"
)


# --------------------------------------------------
# UPLOAD FOLDER
# --------------------------------------------------

UPLOAD_FOLDER = Path(
    "uploads/resumes"
)

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message":
        "AI Resume Analyzer backend is running successfully"
    }


# --------------------------------------------------
# UPLOAD RESUME
# --------------------------------------------------

@app.post("/upload-resume")
def upload_resume(
    resume: UploadFile = File(...)
):

    file_extension = Path(
        resume.filename
    ).suffix.lower()

    if file_extension != ".pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_path = (
        UPLOAD_FOLDER /
        resume.filename
    )

    with file_path.open("wb") as buffer:

        shutil.copyfileobj(
            resume.file,
            buffer
        )

    return {
        "filename": resume.filename,
        "message": "Resume uploaded successfully"
    }


# --------------------------------------------------
# EXTRACT SKILLS
# --------------------------------------------------

@app.post("/extract-skills")
def extract_resume_skills(
    resume: UploadFile = File(...)
):

    file_extension = Path(
        resume.filename
    ).suffix.lower()

    if file_extension != ".pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_path = (
        UPLOAD_FOLDER /
        resume.filename
    )

    with file_path.open("wb") as buffer:

        shutil.copyfileobj(
            resume.file,
            buffer
        )

    resume_text = extract_text_from_pdf(
        file_path
    )

    skills = extract_skills(
        resume_text
    )

    return {
        "filename": resume.filename,
        "skills": skills
    }


# --------------------------------------------------
# MATCH RESUME WITH JOB + AI ANALYSIS
# --------------------------------------------------

@app.post("/match-job")
def match_resume_with_job(

    resume: UploadFile = File(...),

    job_description: str = Form(...),

    db: Session = Depends(get_db)
):

    # Check file type
    file_extension = Path(
        resume.filename
    ).suffix.lower()

    if file_extension != ".pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Save resume
    file_path = (
        UPLOAD_FOLDER /
        resume.filename
    )

    with file_path.open("wb") as buffer:

        shutil.copyfileobj(
            resume.file,
            buffer
        )

    # Extract resume text
    resume_text = extract_text_from_pdf(
        file_path
    )

    # Extract skills
    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    # Calculate matching
    result = calculate_match(
        resume_skills,
        job_skills
    )

    # Generate AI analysis
    ai_analysis = generate_ai_analysis(
        resume_text
    )

    # Create database record
    analysis = models.ResumeAnalysis(

        filename=resume.filename,

        resume_skills=json.dumps(
            resume_skills
        ),

        job_skills=json.dumps(
            job_skills
        ),

        matched_skills=json.dumps(
            result["matched_skills"]
        ),

        missing_skills=json.dumps(
            result["missing_skills"]
        ),

        match_percentage=str(
            result["match_percentage"]
        ),

        ai_analysis=ai_analysis
    )

    # Save to database
    db.add(analysis)

    db.commit()

    db.refresh(analysis)

    # Return result
    return {

        "id": analysis.id,

        "filename": resume.filename,

        "resume_skills": resume_skills,

        "job_skills": job_skills,

        "matched_skills":
            result["matched_skills"],

        "missing_skills":
            result["missing_skills"],

        "match_percentage":
            result["match_percentage"],

        "ai_analysis":
            ai_analysis,

        "message":
            "Complete analysis saved successfully"
    }


# --------------------------------------------------
# AI ANALYSIS ONLY
# --------------------------------------------------

@app.post("/ai-analysis")
def ai_resume_analysis(

    resume: UploadFile = File(...)
):

    file_extension = Path(
        resume.filename
    ).suffix.lower()

    if file_extension != ".pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_path = (
        UPLOAD_FOLDER /
        resume.filename
    )

    with file_path.open("wb") as buffer:

        shutil.copyfileobj(
            resume.file,
            buffer
        )

    resume_text = extract_text_from_pdf(
        file_path
    )

    analysis = generate_ai_analysis(
        resume_text
    )

    return {
        "filename": resume.filename,
        "ai_analysis": analysis
    }


# --------------------------------------------------
# GET SAVED ANALYSES
# --------------------------------------------------

@app.get("/analyses")
def get_analyses(
    db: Session = Depends(get_db)
):

    analyses = db.query(
        models.ResumeAnalysis
    ).all()

    return analyses