import { useState, useEffect } from 'react';
import api from '../services/api';
import { AlertCircle } from 'lucide-react';

export default function Gaps() {
  const [gaps, setGaps] = useState<any>(null);

  useEffect(() => {
    const fetchGaps = async () => {
      try {
        const res = await api.get('/api/gaps');
        setGaps(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchGaps();
  }, []);

  if (!gaps) return <div className="text-center mt-5"><div className="spinner-border text-primary" /></div>;

  return (
    <div>
      <h2 className="fw-bold mb-4">System Gaps & Attention Needed</h2>
      
      <div className="row g-4">
        <div className="col-md-6">
          <div className="card border-0 shadow-sm h-100 border-top border-4 border-danger">
            <div className="card-body">
              <h5 className="fw-bold"><AlertCircle className="text-danger me-2" /> Escalated Cases</h5>
              <p className="display-4 fw-bold text-danger">{gaps.escalated_cases?.length || 0}</p>
              <p className="text-muted">Cases requiring immediate human intervention.</p>
            </div>
          </div>
        </div>
        
        <div className="col-md-6">
          <div className="card border-0 shadow-sm h-100 border-top border-4 border-warning">
            <div className="card-body">
              <h5 className="fw-bold"><AlertCircle className="text-warning me-2" /> Unowned Requests</h5>
              <p className="display-4 fw-bold text-warning">{gaps.unowned_requests?.length || 0}</p>
              <p className="text-muted">Requests that are routed but haven't been accepted by department staff yet.</p>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card border-0 shadow-sm h-100 border-top border-4 border-info">
            <div className="card-body">
              <h5 className="fw-bold"><AlertCircle className="text-info me-2" /> Complex Cases</h5>
              <p className="display-4 fw-bold text-info">{gaps.multi_department_cases?.length || 0}</p>
              <p className="text-muted">Cases involving 3 or more departments that may require central coordination.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
