import { useState } from "react";

import Navbar from "../components/Navbar";

import { matchJob } from "../services/api";

function JobMatcher() {

  const [jobDescription, setJobDescription] = useState(
`Job Title: Software Developer
Company: TechNova Solutions
Job Type: Full-Time

We are looking for a Software Developer with knowledge of Java,
Python, SQL, REST APIs and Git.

Requirements:
- Java programming
- Python
- SQL
- REST API development
- Git and GitHub
- Problem solving
- Good communication skills`
  );

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleMatch = async () => {

    const filename =
      localStorage.getItem("resume_filename");

    if (!filename) {

      setError(
        "Please upload your resume first from Resume Analyzer."
      );

      return;
    }

    if (!jobDescription.trim()) {

      setError(
        "Please enter a job description."
      );

      return;
    }

    try {

      setLoading(true);
      setError("");
      setResult(null);

      const data = await matchJob(
        filename,
        jobDescription
      );

      setResult(data);

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
        "Job matching failed."
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
              CAREER MATCHING
            </div>

            <h1>Job Match</h1>

            <p>
              Compare your uploaded resume with a target
              job description.
            </p>

          </div>

          {error && (
            <div className="error-message">
              ⚠ {error}
            </div>
          )}

          <div className="job-grid">

            <div className="panel">

              <div className="panel-icon">
                ◎
              </div>

              <h2>Target Job</h2>

              <p>
                Paste the job description below.
              </p>

              <textarea
                value={jobDescription}
                onChange={(e) =>
                  setJobDescription(e.target.value)
                }
                className="job-textarea"
              />

              <button
                className="primary-button"
                onClick={handleMatch}
                disabled={loading}
              >
                {loading
                  ? "Analyzing..."
                  : "Analyze Job Match →"}
              </button>

            </div>

            {result && (

              <div className="panel">

                <div className="panel-icon">
                  ✓
                </div>

                <h2>Match Result</h2>

                <div className="match-result">

                  {result.match_percentage !== undefined && (
                    <div className="match-score">
                      {result.match_percentage}%
                    </div>
                  )}

                  {result.score !== undefined && (
                    <div className="match-score">
                      {result.score}%
                    </div>
                  )}

                  <pre>
                    {typeof result === "string"
                      ? result
                      : JSON.stringify(
                          result,
                          null,
                          2
                        )}
                  </pre>

                </div>

              </div>

            )}

          </div>

        </section>

      </main>

    </div>
  );
}

export default JobMatcher;