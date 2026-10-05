import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Send, Loader2 } from 'lucide-react';

export default function Intake() {
  const [reference, setReference] = useState('STUDENT-001');
  const [story, setStory] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const res = await api.post('/api/intake', {
        student_reference: reference,
        story
      });
      navigate(`/case/${res.data.case.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred during submission.');
      setLoading(false);
    }
  };

  const loadDemoRoutine = () => {
    setStory("My father was hospitalized. I need a 5 day fee extension because I am unable to manage the payment this week. I have the supporting letter.");
  };

  const loadDemoComplex = () => {
    setStory("My father is hospitalized. I need a 10 day fee extension, I missed my mid-term exam, I need attendance consideration, and I'll return to the hostel late next week.");
  };

  const loadDemoRisk = () => {
    setStory("I am feeling extremely overwhelmed and depressed. I can't take this anymore, I just want to drop out or disappear. Nothing is working.");
  };

  return (
    <div className="row justify-content-center">
      <div className="col-lg-8">
        <div className="card shadow-sm border-0">
          <div className="card-body p-5">
            <h2 className="mb-4 fw-bold">Tell us what happened.</h2>
            <p className="text-muted mb-4">We'll make sure this gets to all the right departments so you don't have to repeat yourself.</p>
            
            {error && <div className="alert alert-danger">{error}</div>}

            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label fw-bold">Student Reference</label>
                <input 
                  type="text" 
                  className="form-control" 
                  value={reference} 
                  onChange={(e) => setReference(e.target.value)} 
                  required 
                />
              </div>
              <div className="mb-4">
                <label className="form-label fw-bold">Your Story</label>
                <textarea 
                  className="form-control" 
                  rows={8} 
                  placeholder="Tell us what happened and what support you need..."
                  value={story}
                  onChange={(e) => setStory(e.target.value)}
                  required
                ></textarea>
                <div className="form-text text-muted mt-2">
                  <small>Demo autofill: 
                    <button type="button" className="btn btn-link btn-sm p-0 ms-1 me-2" onClick={loadDemoRoutine}>Routine</button>| 
                    <button type="button" className="btn btn-link btn-sm p-0 ms-2 me-2" onClick={loadDemoComplex}>Complex</button>| 
                    <button type="button" className="btn btn-link btn-sm p-0 ms-2" onClick={loadDemoRisk}>Risk</button>
                  </small>
                </div>
              </div>

              <button 
                type="submit" 
                className="btn btn-primary btn-lg w-100 fw-bold d-flex align-items-center justify-content-center"
                disabled={loading || !story.trim()}
              >
                {loading ? <><Loader2 className="me-2" size={20} /> Understanding your situation...</> : <><Send className="me-2" size={20} /> Submit My Story</>}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
