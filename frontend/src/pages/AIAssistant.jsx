import { useState } from "react";

import Navbar from "../components/Navbar";

import { analyzeResume } from "../services/api";

function AIAssistant() {

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const handleAsk = async () => {

    const filename =
      localStorage.getItem("resume_filename");

    if (!filename) {

      setError(
        "Please upload your resume first."
      );

      return;
    }

    try {

      setLoading(true);
      setError("");

      const data = await analyzeResume(filename);

      let response =
        data.analysis ||
        data.response ||
        data.result ||
        JSON.stringify(data, null, 2);

      if (question.trim()) {
        response =
          `${response}\n\nYour question:\n${question}`;
      }

      setAnswer(response);

    } catch (err) {

      console.error(err);

      setError(
        err.response?.data?.detail ||
        "Unable to get AI response."
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
              ARTIFICIAL INTELLIGENCE
            </div>

            <h1>AI Resume Assistant</h1>

            <p>
              Get personalized feedback about your resume.
            </p>

          </div>

          {error && (
            <div className="error-message">
              ⚠ {error}
            </div>
          )}

          <div className="panel ai-panel">

            <div className="panel-icon">
              ✦
            </div>

            <h2>AI Resume Insights</h2>

            <p>
              Generate useful insights from your uploaded resume.
            </p>

            <textarea
              className="question-input"
              placeholder="Ask something about your resume..."
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
            />

            <button
              className="primary-button"
              onClick={handleAsk}
              disabled={loading}
            >
              {loading
                ? "Generating..."
                : "Ask AI"}
            </button>

            {answer && (
              <div className="result-box">

                <h3>AI Response</h3>

                <pre>
                  {answer}
                </pre>

              </div>
            )}

          </div>

        </section>

      </main>

    </div>
  );
}

export default AIAssistant;