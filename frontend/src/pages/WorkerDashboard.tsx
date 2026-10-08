import { useEffect, useState } from 'react';
import { BellRing, BriefcaseBusiness, ClipboardCheck, MapPinned, LogOut, PlayCircle, UploadCloud } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import api from '../lib/api';

export default function WorkerDashboard() {
  const { user, logout } = useAuth();
  const [incidents, setIncidents] = useState<any[]>([]);

  useEffect(() => {
    api.get('/worker/assigned-incidents').then((response) => setIncidents(response.data)).catch(() => {});
  }, []);

  const startWork = async (incidentId: string) => {
    await api.post(`/worker/start-work/${incidentId}`);
    setIncidents((prev) => prev.map((item) => item.id === incidentId ? { ...item, status: 'IN_PROGRESS' } : item));
  };

  const submitResolution = async (incidentId: string) => {
    const form = new FormData();
    form.append('resolution_notes', 'Repair completed and verified.');
    await api.post(`/worker/submit-resolution/${incidentId}`, form, { headers: { 'Content-Type': 'multipart/form-data' } });
  };

  return (
    <div className="min-h-screen bg-slate-950 p-6 text-slate-50">
      <header className="mx-auto mb-6 flex max-w-7xl items-center justify-between rounded-2xl border border-slate-700 bg-slate-900/80 p-4">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-amber-300">Worker dashboard</p>
          <h1 className="text-2xl font-bold">Welcome {user?.name}</h1>
        </div>
        <button onClick={logout} className="inline-flex items-center gap-2 rounded-xl border border-slate-700 p-2 text-sm"><LogOut className="h-4 w-4" /> Logout</button>
      </header>

      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-3">
        {incidents.map((incident) => (
          <div key={incident.id} className="card p-5">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-semibold">{incident.title}</h3>
              <span className="rounded-full bg-amber-500/10 px-2 py-1 text-xs text-amber-300">{incident.priority}</span>
            </div>
            <p className="mt-3 text-sm text-slate-300">{incident.description}</p>
            <div className="mt-4 space-y-2 text-sm text-slate-300">
              <div className="flex items-center gap-2"><MapPinned className="h-4 w-4 text-emerald-300" />{incident.location}</div>
              <div className="flex items-center gap-2"><BriefcaseBusiness className="h-4 w-4 text-emerald-300" />Department: {incident.department}</div>
              <div className="flex items-center gap-2"><ClipboardCheck className="h-4 w-4 text-emerald-300" />Status: {incident.status}</div>
            </div>

            <div className="mt-4 flex gap-2">
              <button onClick={() => startWork(incident.id)} className="flex-1 rounded-lg bg-amber-500 px-3 py-2 font-medium text-slate-950">Start work</button>
              <button onClick={() => submitResolution(incident.id)} className="flex-1 rounded-lg border border-slate-700 px-3 py-2">Submit</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
