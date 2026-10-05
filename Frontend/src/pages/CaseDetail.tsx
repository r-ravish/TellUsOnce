import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, ShieldAlert, CheckCircle, BrainCircuit } from 'lucide-react';

export default function CaseDetail() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchCase = async () => {
    try {
      const res = await api.get(`/api/cases/${id}`);
      setData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCase();
  }, [id]);

  const handleAction = async (reqId: number, action: string) => {
    try {
      await api.post(`/api/requests/${reqId}/action`, { action, note: 'Processed by staff' });
      fetchCase();
    } catch (err) {
      alert('Error updating request');
    }
  };

  if (loading) return <div className="text-center mt-5"><div className="spinner-border text-primary" /></div>;
  if (!data) return <div className="alert alert-danger">Case not found</div>;

  return (
    <div>
      <Link to="/dashboard" className="btn btn-link px-0 text-decoration-none mb-3"><ArrowLeft size={16} /> Back to Dashboard</Link>
      
      <div className="d-flex justify-content-between align-items-start mb-4">
        <div>
          <h2 className="fw-bold mb-1">Case #TUO-{data.id}</h2>
          <p className="text-muted mb-0">Student: <strong>{data.student_reference}</strong></p>
        </div>
        <div>
          {data.risk_flag && <span className="badge bg-danger fs-6 p-2 me-2"><ShieldAlert size={16} className="me-1"/> HIGH RISK</span>}
          <span className="badge bg-dark fs-6 p-2">Confidence: {(data.confidence * 100).toFixed(0)}%</span>
        </div>
      </div>

      <div className="row g-4">
        <div className="col-lg-8">
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-body p-4">
              <h5 className="fw-bold mb-3">Original Story (Masked)</h5>
              <p className="bg-light p-3 rounded">{data.masked_story}</p>
              
              <h5 className="fw-bold mb-3 mt-4">AI Summary</h5>
              <p>{data.summary}</p>
            </div>
          </div>

          <h4 className="fw-bold mb-3">Requests & Decisions</h4>
          {data.requests.map((req: any) => (
            <div className={`card border-0 shadow-sm mb-3 ${req.status === 'Escalated' ? 'border-start border-4 border-danger' : 'border-start border-4 border-primary'}`} key={req.id}>
              <div className="card-body p-4">
                <div className="d-flex justify-content-between align-items-start mb-3">
                  <div>
                    <h5 className="fw-bold mb-1">{req.request_type}</h5>
                    <span className="text-muted">Department: <strong>{req.department}</strong></span>
                  </div>
                  <span className={`badge ${req.status === 'Auto Approved' ? 'bg-success' : req.status === 'Escalated' ? 'bg-danger' : 'bg-primary'}`}>
                    {req.status}
                  </span>
                </div>
                
                <div className="row bg-light rounded p-3 mb-3 mx-0">
                  <div className="col-md-6 mb-2 mb-md-0">
                    <small className="text-muted d-block text-uppercase fw-bold">AI Suggestion</small>
                    <span className="d-flex align-items-center"><BrainCircuit size={16} className="me-2 text-primary" /> {req.ai_suggested_action}</span>
                  </div>
                  <div className="col-md-6">
                    <small className="text-muted d-block text-uppercase fw-bold">Days Requested</small>
                    <span>{req.days_requested || 'N/A'}</span>
                  </div>
                  <div className="col-12 mt-3">
                    <small className="text-muted d-block text-uppercase fw-bold">AI Reason</small>
                    <span>{req.ai_reason}</span>
                  </div>
                </div>

                <div className="d-flex justify-content-between align-items-center mt-4 pt-3 border-top">
                  <div>
                    <small className="text-muted fw-bold d-block">DECISION RATIONALE</small>
                    {req.status === 'Auto Approved' ? (
                      <span className="text-success"><CheckCircle size={16} className="me-1"/> Policy met, documents present, high confidence, no risk.</span>
                    ) : (
                      <span className="text-secondary">Requires manual policy check or human intervention.</span>
                    )}
                  </div>
                  
                  <div className="btn-group">
                    {req.status !== 'Auto Approved' && req.status !== 'Done' && (
                      <>
                        <button className="btn btn-sm btn-outline-success" onClick={() => handleAction(req.id, 'accept')}>Accept</button>
                        <button className="btn btn-sm btn-success" onClick={() => handleAction(req.id, 'complete')}>Complete</button>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="col-lg-4">
          <div className="card border-0 shadow-sm mb-4">
            <div className="card-body">
              <h5 className="fw-bold mb-4">Audit Trail</h5>
              <div className="timeline-container">
                {data.audit_logs.map((log: any) => (
                  <div className="timeline-item" key={log.id}>
                    <strong className="d-block">{log.event_type}</strong>
                    <span className="text-muted small d-block mb-1">{new Date(log.created_at).toLocaleString()}</span>
                    <p className="mb-0 small">{log.details}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
