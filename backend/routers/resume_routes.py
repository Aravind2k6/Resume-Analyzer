import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.resume_parser import extract_resume_text


router = APIRouter()

UPLOAD_DIR = "backend/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/")
def resume_home():
    return {
        "message": "Resume API is working"
    }


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Check file
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )

    # Only PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # Safe filename
    filename = os.path.basename(file.filename)

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    try:

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        # Extract text
        text = extract_resume_text(file_path)

        return {
            "success": True,
            "message": "Resume uploaded successfully",
            "filename": filename,
            "text": text
        }

    except Exception as e:

        # Remove broken file
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )