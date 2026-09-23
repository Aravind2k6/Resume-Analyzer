import { useState } from "react";

import Navbar from "../components/Navbar";

import {
  uploadResume,
  extractSkills,
  analyzeResume,
} from "../services/api";

function ResumeAnalyzer() {

  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");

  const [skills, setSkills] = useState([]);
  const [analysis, setAnalysis] = useState("");

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = (event) => {

    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    if (selectedFile.type !== "application/pdf") {

      setError("Please select a PDF resume.");

      return;
    }

    setFile(selectedFile);
    setFilename(selectedFile.name);

    setMessage("Resume selected successfully.");
    setError("");

  };

  const handleUpload = async () => {

    if (!file) {

      setError("Please select a resume first.");

      return;
    }

    try {

      setLoading(true);
      setError("");
      setMessage("");

      const data = await uploadResume(file);

      const returnedFilename =
        data.filename ||
        data.file_name ||
        data.name ||
        file.name;

      setFilename(returnedFilename);

      localStorage.setItem(
        "resume_filename",
        returnedFilename
      );

      setMessage("Resume uploaded successfully.");

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
        "Resume upload failed. Make sure the backend is running."
      );

    } finally {

      setLoading(false);

    }
  };

  const handleSkills = async () => {

    const savedFilename =
      filename ||
      localStorage.getItem("resume_filename");

    if (!savedFilename) {

      setError(
        "Please upload a resume before extracting skills."
      );

      return;
    }

    try {

      setLoading(true);
      setError("");
      setMessage("");

      const data = await extractSkills(savedFilename);

      let extracted = [];

      if (Array.isArray(data)) {
        extracted = data;
      } else if (Array.isArray(data.skills)) {
        extracted = data.skills;
      } else if (data.skills) {
        extracted = String(data.skills)
          .split(",")
          .map((skill) => skill.trim())
          .filter(Boolean);
      }

      setSkills(extracted);

      setMessage("Skills extracted successfully.");

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
        "Unable to extract skills."
      );

    } finally {

      setLoading(false);

    }
  };

  const handleAIAnalysis = async () => {

    const savedFilename =
      filename ||
      localStorage.getItem("resume_filename");

    if (!savedFilename) {

      setError(
        "Please upload a resume before using AI analysis."
      );

      return;
    }

    try {

      setLoading(true);
      setError("");
      setMessage("");
      setAnalysis("");

      const data = await analyzeResume(savedFilename);

      const result =
        data.analysis ||
        data.result ||
        data.response ||
        data.message ||
        JSON.stringify(data, null, 2);

      setAnalysis(result);

      setMessage("AI analysis completed.");

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
        "AI analysis failed. Make sure Ollama is running."
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="app-layout">

      <Navbar />

      <main className="main-content">

        <header className="topbar">
          <div className="search">
            🔍 Search your career tools...
          </div>
        </header>

        <section className="page">

          <div className="page-heading">

            <div className="eyebrow">
              RESUME INTELLIGENCE
            </div>

            <h1>Resume Analyzer</h1>

            <p>
              Upload your resume and use AI to understand
              your skills and improve your profile.
            </p>

          </div>

          {message && (
            <div className="success-message">
              ✓ {message}
            </div>
          )}

          {error && (
            <div className="error-message">
              ⚠ {error}
            </div>
          )}

          <div className="analyzer-grid">

            <div className="panel">

              <div className="panel-icon">
                ↑
              </div>

              <h2>Upload your resume</h2>

              <p>
                PDF files only. Your resume will be analyzed
                securely.
              </p>

              <input
                id="resume-file"
                type="file"
                accept=".pdf,application/pdf"
                onChange={handleFileChange}
                className="file-input"
              />

              <label
                htmlFor="resume-file"
                className="choose-button"
              >
                Choose Resume
              </label>

              {file && (
                <div className="selected-file">
                  ✓ {file.name}
                </div>
              )}

              <button
                className="primary-button"
                onClick={handleUpload}
                disabled={loading || !file}
              >
                {loading ? "Uploading..." : "Upload Resume"}
              </button>

            </div>

            <div className="panel">

              <div className="panel-icon">
                ✦
              </div>

              <h2>AI Resume Analysis</h2>

              <p>
                Get AI-powered feedback about your resume.
              </p>

              <button
                className="primary-button"
                onClick={handleAIAnalysis}
                disabled={loading || !filename}
              >
                {loading ? "Analyzing..." : "Analyze with AI"}
              </button>

              {analysis && (
                <div className="result-box">

                  <h3>AI Analysis</h3>

                  <pre>
                    {analysis}
                  </pre>

                </div>
              )}

            </div>

            <div className="panel">

              <div className="panel-icon yellow">
                ⚡
              </div>

              <h2>Skill Extraction</h2>

              <p>
                Automatically identify technical skills
                from your resume.
              </p>

              <button
                className="secondary-button"
                onClick={handleSkills}
                disabled={loading || !filename}
              >
                {loading ? "Extracting..." : "Extract Skills"}
              </button>

              {skills.length > 0 && (

                <div className="skills-container">

                  <h3>Detected Skills</h3>

                  <div className="skills-list">

                    {skills.map((skill, index) => (
                      <span
                        className="skill-tag"
                        key={index}
                      >
                        {skill}
                      </span>
                    ))}

                  </div>

                </div>

              )}

            </div>

          </div>

        </section>

      </main>

    </div>
  );
}

export default ResumeAnalyzer;