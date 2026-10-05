import { Link } from 'react-router-dom';
import { ShieldCheck } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container">
        <Link className="navbar-brand d-flex align-items-center" to="/">
          <ShieldCheck className="me-2" /> Tell Us Once
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/intake">Student Intake</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/dashboard">Staff Dashboard</Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/gaps">System Gaps</Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}
