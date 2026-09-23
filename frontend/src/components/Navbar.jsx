import { Link, useLocation } from "react-router-dom";

function Navbar() {
  const location = useLocation();

  const menu = [
    {
      name: "Dashboard",
      path: "/",
      icon: "⌂",
    },
    {
      name: "Job Match",
      path: "/job-match",
      icon: "◎",
    },
    {
      name: "AI Assistant",
      path: "/ai-assistant",
      icon: "✦",
    },
    {
      name: "My Skills",
      path: "/resume-analyzer",
      icon: "◇",
    },
  ];

  return (
    <aside className="sidebar">

      <div className="logo">
        <div className="logo-box">R</div>
        <span>ResumeIQ</span>
      </div>

      <nav className="navigation">

        {menu.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className={
              location.pathname === item.path
                ? "nav-item active"
                : "nav-item"
            }
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.name}</span>
          </Link>
        ))}

      </nav>

      <div className="sidebar-bottom">

        <Link
          to="/settings"
          className="nav-item"
        >
          <span className="nav-icon">⚙</span>
          <span>Settings</span>
        </Link>

        <div className="user-box">

          <div className="avatar">
            A
          </div>

          <div>
            <strong>Resume User</strong>
            <small>Free Plan</small>
          </div>

        </div>

      </div>

    </aside>
  );
}

export default Navbar;