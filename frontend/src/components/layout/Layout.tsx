import { Link, NavLink, Outlet } from "react-router-dom";
import { useI18n } from "../../lib/i18n";

export function Layout() {
  const { t, toggleLocale } = useI18n();

  return (
    <div className="layout">
      <nav className="nav">
        <div className="nav-inner">
          <Link to="/" className="nav-brand">
            HotPulse
          </Link>
          <div className="nav-links">
            <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
              {t("nav.home")}
            </NavLink>
            <NavLink to="/explore" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
              {t("nav.explore")}
            </NavLink>
            <NavLink to="/saved" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
              {t("nav.saved")}
            </NavLink>
            <button className="lang-toggle" onClick={toggleLocale}>
              {t("lang.toggle")}
            </button>
          </div>
        </div>
      </nav>

      <div className="container">
        <Outlet />
      </div>

      <footer className="footer">{t("footer.text")}</footer>
    </div>
  );
}
