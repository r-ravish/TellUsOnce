import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Activity, AlertOctagon, CheckCircle2, RotateCcw } from 'lucide-react';

export default function Dashboard() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchCases = async () => {
    try {
      const res = await api.get('/api/cases');
      setCases(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCases();
    const interval = setInterval(fetchCases, 5000);
    return () => clearInterval(interval);
  }, []);

  const resetDemo = async () => {
    if (window.confirm('Reset database to demo data?')) {
      setLoading(true);
      await api.post('/api/demo/reset');
      fetchCases();
    }
  };

  if (loading && cases.length === 0) return <div className="text-center mt-5"><div className="spinner-border text-primary" /></div>;

  const escalated = cases.filter((c: any) => c.status === 'Escalated').length;

  const getStatusBadge = (status: string) => {
    const map: any = {
      'Auto Approved': 'bg-success',
      'Routed': 'bg-primary',
      'In Progress': 'bg-info',
      'Needs Documents': 'bg-warning text-dark',
      'Escalated': 'bg-danger',
      'Done': 'bg-secondary'
    };
    return `badge status-badge ${map[status] || 'bg-secondary'}`;
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold mb-0">Staff Dashboard</h2>
          <p className="text-muted safety-statement mb-0">AI suggests. Policy decides. Humans handle exceptions.</p>
        </div>
        <button className="btn btn-outline-secondary" onClick={resetDemo}>
          <RotateCcw size={16} className="me-2" /> Reset Demo
        </button>
      </div>

      <div className="row g-4 mb-4">
        <div className="col-md-4">
          <div className="card bg-primary text-white border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="text-white-50 text-uppercase fw-bold">Active Cases</h6>
                  <h2 className="display-5 fw-bold mb-0">{cases.length}</h2>
                </div>
                <Activity size={48} className="opacity-50" />
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card bg-danger text-white border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="text-white-50 text-uppercase fw-bold">Escalated</h6>
                  <h2 className="display-5 fw-bold mb-0">{escalated}</h2>
                </div>
                <AlertOctagon size={48} className="opacity-50" />
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card bg-success text-white border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <div>
                  <h6 className="text-white-50 text-uppercase fw-bold">System Status</h6>
                  <h2 className="h4 fw-bold mb-0 mt-2">All Clear</h2>
                </div>
                <CheckCircle2 size={48} className="opacity-50" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="card border-0 shadow-sm">
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-hover align-middle mb-0">
              <thead className="bg-light">
                <tr>
                  <th className="px-4 py-3">Case ID</th>
                  <th className="py-3">Student</th>
                  <th className="py-3">Summary</th>
                  <th className="py-3">Urgency</th>
                  <th className="py-3">Status</th>
                  <th className="px-4 py-3 text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                {cases.map((c: any) => (
                  <tr key={c.id}>
                    <td className="px-4 fw-bold text-muted">TUO-{c.id}</td>
                    <td className="fw-bold">{c.student_reference}</td>
                    <td className="text-truncate" style={{ maxWidth: '300px' }}>{c.summary}</td>
                    <td>
                      <span className={`badge ${c.urgency === 'high' ? 'bg-danger' : c.urgency === 'medium' ? 'bg-warning text-dark' : 'bg-info'}`}>
                        {c.urgency.toUpperCase()}
                      </span>
                      {c.risk_flag && <AlertOctagon size={16} className="text-danger ms-2" />}
                    </td>
                    <td><span className={getStatusBadge(c.status)}>{c.status}</span></td>
                    <td className="px-4 text-end">
                      <Link to={`/dashboard/cases/${c.id}`} className="btn btn-sm btn-primary">View Case</Link>
                    </td>
                  </tr>
                ))}
                {cases.length === 0 && (
                  <tr>
                    <td colSpan={6} className="text-center py-5 text-muted">No cases found. Create one or load demo data.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
