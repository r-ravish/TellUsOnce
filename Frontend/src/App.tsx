import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Intake from './pages/Intake';
import StudentCase from './pages/StudentCase';
import Dashboard from './pages/Dashboard';
import CaseDetail from './pages/CaseDetail';
import Gaps from './pages/Gaps';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="container mt-4 mb-5">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/intake" element={<Intake />} />
          <Route path="/case/:id" element={<StudentCase />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard/cases/:id" element={<CaseDetail />} />
          <Route path="/gaps" element={<Gaps />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
