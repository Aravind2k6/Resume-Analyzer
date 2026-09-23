import Navbar from "../components/Navbar";

function Settings() {
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
              SETTINGS
            </div>

            <h1>Settings</h1>

            <p>
              Manage your ResumeIQ preferences.
            </p>

          </div>

          <div className="panel">

            <h2>Application Settings</h2>

            <div className="setting-row">
              <span>AI Analysis</span>
              <span className="setting-status">
                Enabled
              </span>
            </div>

            <div className="setting-row">
              <span>Resume Storage</span>
              <span className="setting-status">
                Local
              </span>
            </div>

            <div className="setting-row">
              <span>AI Provider</span>
              <span className="setting-status">
                Ollama
              </span>
            </div>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Settings;