import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <nav>
      <NavLink to="/courses" className={({isActive}) => `nav-link ${isActive ? "active" : ""}`}>
        Courses
      </NavLink>
      <NavLink to="/students" className={({isActive}) => `nav-link ${isActive ? "active" : ""}`}>
        Students
      </NavLink>
    </nav>
  );
}
