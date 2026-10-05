import { Link } from 'react-router-dom';
import { FileText, Brain, Users } from 'lucide-react';

export default function Home() {
  return (
    <div>
      <div className="hero-section text-center mb-5 mt-n4">
        <div className="container">
          <h1 className="display-4 fw-bold">Tell Us Once</h1>
          <p className="lead mb-4">One story. One case. Every department connected.</p>
          <div className="d-flex justify-content-center gap-3">
            <Link to="/intake" className="btn btn-light btn-lg px-4 fw-bold">Tell Your Story</Link>
            <Link to="/dashboard" className="btn btn-outline-light btn-lg px-4">View Staff Demo</Link>
          </div>
          <p className="mt-4 safety-statement text-light opacity-75">
            AI suggests. Policy decides. Humans handle the exceptions.
          </p>
        </div>
      </div>

      <div className="row g-4 text-center">
        <div className="col-md-4">
          <div className="card h-100 border-0 shadow-sm card-hover">
            <div className="card-body p-4">
              <div className="text-primary mb-3"><FileText size={48} /></div>
              <h4 className="card-title">1. Tell Your Story</h4>
              <p className="card-text text-muted">Students shouldn't have to repeat difficult situations to multiple offices. Just explain it once.</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card h-100 border-0 shadow-sm card-hover">
            <div className="card-body p-4">
              <div className="text-primary mb-3"><Brain size={48} /></div>
              <h4 className="card-title">2. AI Understands</h4>
              <p className="card-text text-muted">Our AI securely extracts required requests, assesses urgency, and flags complex risks for human review.</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card h-100 border-0 shadow-sm card-hover">
            <div className="card-body p-4">
              <div className="text-primary mb-3"><Users size={48} /></div>
              <h4 className="card-title">3. Departments Coordinate</h4>
              <p className="card-text text-muted">Deterministic policies auto-approve routine requests, while complex cases are routed to the right humans.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
