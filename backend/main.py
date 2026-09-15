from fastapi import FastAPI

app = FastAPI(
    title ="AI Resume Analyzer API",
    description ="Backend for Ai Resume Analyzer and Job Description",
    version ="1.0"
)
@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer backend is running successfully"
    }
