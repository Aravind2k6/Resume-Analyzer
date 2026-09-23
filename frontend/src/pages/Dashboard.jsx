import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="app-layout">

      <Navbar />

      <main className="main-content">

        <header className="topbar">
          <div className="search">
            🔍 Search your career tools...
          </div>

          <div className="top-icons">
            🔔
            <div className="small-avatar">A</div>
          </div>
        </header>

        <section className="dashboard">

          <div className="hero">

            <div className="hero-text">

              <div className="eyebrow">
                AI POWERED CAREER PLATFORM
              </div>

              <h1>
                Understand your resume.
                <br />
                <span>Improve your career.</span>
              </h1>

              <p>
                Upload your resume and use AI to analyze your
                skills, match job descriptions and discover
                areas for improvement.
              </p>

            </div>

            <div className="hero-card">

              <div className="ai-circle">
                AI
              </div>

              <h2>Smart Resume Analysis</h2>

              <p>
                Get insights about your resume in seconds.
              </p>

            </div>

          </div>

          <div className="dashboard-actions">

            <div className="feature-card">

              <div className="feature-icon">
                ↑
              </div>

              <h2>Resume Analyzer</h2>

              <p>
                Upload your resume and analyze it using AI.
              </p>

              <button
                onClick={() => navigate("/resume-analyzer")}
              >
                Analyze Resume →
              </button>

            </div>

            <div className="feature-card">

              <div className="feature-icon">
                ✦
              </div>

              <h2>AI Assistant</h2>

              <p>
                Get personalized career suggestions.
              </p>

              <button
                onClick={() => navigate("/ai-assistant")}
              >
                Open AI Assistant
              </button>

            </div>

            <div className="feature-card">

              <div className="feature-icon">
                ◎
              </div>

              <h2>Job Matching</h2>

              <p>
                Compare your resume against a job description.
              </p>

              <button
                onClick={() => navigate("/job-match")}
              >
                Find Job Match →
              </button>

            </div>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Dashboard;