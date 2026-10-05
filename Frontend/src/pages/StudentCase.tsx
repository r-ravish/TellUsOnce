import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { FileText, Clock, AlertTriangle, CheckCircle } from 'lucide-react';

export default function StudentCase() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
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
    fetchCase();
  }, [id]);

  if (loading) return <div className="text-center mt-5"><div className="spinner-border text-primary" /></div>;
  if (!data) return <div className="alert alert-danger">Case not found</div>;

  const getStatusBadge = (status: string) => {
    const map: any = {
      'Auto Approved': 'bg-success',
      'Routed': 'bg-primary',
      'In Progress': 'bg-info',
      'Needs Documents': 'bg-warning text-dark',
      'Escalated': 'bg-danger',
      'Done': 'bg-secondary'
    };
    return `badge ${map[status] || 'bg-secondary'}`;
  };

  return (
    <div className="row">
      <div className="col-12 mb-4">
        <h2 className="fw-bold">Your Support Plan</h2>
        <p className="text-muted">Case #{data.id} • {data.student_reference}</p>
      </div>

      <div className="col-md-8">
        <div className="card border-0 shadow-sm mb-4">
          <div className="card-header bg-white border-bottom-0 pt-4 pb-0">
            <h5 className="fw-bold"><FileText className="me-2" size={20} /> What we understood</h5>
          </div>
          <div className="card-body">
            <p className="mb-0">{data.summary}</p>
            {data.risk_flag && (
              <div className="alert alert-warning mt-3 mb-0 d-flex align-items-center">
                <AlertTriangle className="me-2" /> 
                <strong>Note:</strong> We have prioritized your case for human review to ensure you get the best support.
              </div>
            )}
          </div>
        </div>

        <h5 className="fw-bold mb-3">Requests Created</h5>
        <div className="row g-3">
          {data.requests.map((req: any) => (
            <div className="col-md-6" key={req.id}>
              <div className="card h-100 border-0 shadow-sm border-start border-4 border-primary">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-start mb-2">
                    <h6 className="fw-bold mb-0">{req.request_type}</h6>
                    <span className={getStatusBadge(req.status)}>{req.status}</span>
                  </div>
                  <p className="text-muted small mb-0">Handled by: <strong>{req.department}</strong></p>
                  {req.status === 'Needs Documents' && req.documents_mentioned?.length > 0 && (
                    <div className="mt-2 text-warning fw-bold small">
                      <Clock size={14} className="me-1" /> Missing: {req.documents_mentioned.join(', ')}
                    </div>
                  )}
                  {req.status === 'Auto Approved' && (
                    <div className="mt-2 text-success fw-bold small">
                      <CheckCircle size={14} className="me-1" /> Approved
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="col-md-4">
        <div className="card border-0 shadow-sm sticky-top" style={{ top: '20px' }}>
          <div className="card-body">
            <h5 className="fw-bold mb-4">Timeline</h5>
            <div className="timeline-container">
              {data.timeline.map((event: any) => (
                <div className="timeline-item" key={event.id}>
                  <strong className="d-block">{event.event_type.replace(/_/g, ' ')}</strong>
                  <span className="text-muted small d-block mb-1">{new Date(event.created_at).toLocaleString()}</span>
                  <p className="mb-0 small">{event.message}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
