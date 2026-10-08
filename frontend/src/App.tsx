import { Navigate, Route, Routes } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import CitizenDashboard from './pages/CitizenDashboard';
import WorkerDashboard from './pages/WorkerDashboard';
import AdminDashboard from './pages/AdminDashboard';

function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-100">Loading CivicGuard AI...</div>;
  }

  return (
    <Routes>
      <Route path="/" element={user ? <Navigate to={`/${user.role}`} replace /> : <Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/student" element={user && user.role === 'student' ? <CitizenDashboard /> : <Navigate to="/login" replace />} />
      <Route path="/worker" element={user && user.role === 'worker' ? <WorkerDashboard /> : <Navigate to="/login" replace />} />
      <Route path="/admin" element={user && user.role === 'admin' ? <AdminDashboard /> : <Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
