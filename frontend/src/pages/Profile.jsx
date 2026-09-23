import Navbar from "../components/Navbar";

function Profile() {
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
              ACCOUNT
            </div>

            <h1>Profile</h1>

            <p>
              Manage your ResumeIQ profile.
            </p>
          </div>

          <div className="panel profile-panel">

            <div className="large-avatar">
              A
            </div>

            <h2>Resume User</h2>

            <p>Free Plan</p>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Profile;