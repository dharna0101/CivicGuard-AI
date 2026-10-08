import { useEffect, useState } from 'react';
import { CircleAlert, FilePlus, MapPin, ShieldAlert, Bell, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import api from '../lib/api';
import { useAuth } from '../context/AuthContext';

interface Report {
  id: string;
  category: string;
  description: string;
  location: string;
  incident_id?: string | null;
  is_duplicate?: boolean;
  ai_summary?: string;
}

export default function CitizenDashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [reports, setReports] = useState<Report[]>([]);
  const [form, setForm] = useState({
    category: 'POTHOLE',
    description: '',
    location: 'Main Gate, Campus',
    latitude: '12.9716',
    longitude: '77.5946',
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    api.get('/reports/my-reports').then((response) => setReports(response.data)).catch(() => {});
  }, []);

  const submitReport = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = new FormData();
    payload.append('category', form.category);
    payload.append('description', form.description);
    payload.append('location', form.location);
    payload.append('latitude', form.latitude);
    payload.append('longitude', form.longitude);
    const response = await api.post('/reports/submit', payload, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    setReports((prev) => [response.data, ...prev]);
    setMessage('Report submitted successfully and AI clustering has been processed.');
    setForm({ ...form, description: '', location: 'Main Gate, Campus' });
  };

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-6 text-slate-50">
      <header className="mx-auto mb-6 flex max-w-7xl items-center justify-between rounded-2xl border border-slate-700 bg-slate-900/80 p-4">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-emerald-300">Citizen area</p>
          <h1 className="text-2xl font-bold">Welcome {user?.name}</h1>
        </div>
        <button onClick={logout} className="inline-flex items-center gap-2 rounded-xl border border-slate-700 p-2 text-sm"><LogOut className="h-4 w-4" /> Logout</button>
      </header>

      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-6">
          <section className="card p-6">
            <div className="mb-4 flex items-center gap-3"><FilePlus className="h-5 w-5 text-emerald-300" /><h2 className="text-xl font-semibold">Report issue</h2></div>
            <form onSubmit={submitReport} className="space-y-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm text-slate-300">Category</label>
                  <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3">
                    {['POTHOLE','ROAD_DAMAGE','STREETLIGHT','GARBAGE','WATER_LEAKAGE','DRAINAGE','ELECTRICAL_HAZARD','BROKEN_EQUIPMENT','OTHER'].map((item) => (
                      <option key={item} value={item}>{item.replace('_', ' ')}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="mb-2 block text-sm text-slate-300">Location</label>
                  <input value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3" />
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm text-slate-300">Description</label>
                <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} rows={4} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3" placeholder="Describe the issue and any safety risks" required />
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label className="mb-2 block text-sm text-slate-300">Latitude</label>
                  <input type="number" step="0.0001" value={form.latitude} onChange={(e) => setForm({ ...form, latitude: e.target.value })} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3" />
                </div>
                <div>
                  <label className="mb-2 block text-sm text-slate-300">Longitude</label>
                  <input type="number" step="0.0001" value={form.longitude} onChange={(e) => setForm({ ...form, longitude: e.target.value })} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3" />
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm text-slate-300">Photo upload</label>
                <input type="file" className="w-full rounded-xl border border-dashed border-slate-700 bg-slate-950 p-3" />
              </div>

              <button type="submit" className="rounded-xl bg-emerald-500 px-4 py-3 font-semibold text-slate-950">Submit report</button>
              {message && <p className="mt-3 text-sm text-emerald-300">{message}</p>}
            </form>
          </section>

          <section className="card p-6">
            <div className="mb-4 flex items-center gap-3"><MapPin className="h-5 w-5 text-emerald-300" /><h2 className="text-xl font-semibold">Nearby incident map</h2></div>
            <MapContainer center={[12.9716, 77.5946]} zoom={15} scrollWheelZoom>
              <TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
              <Marker position={[12.9716, 77.5946]}><Popup>Incident cluster near Main Gate</Popup></Marker>
            </MapContainer>
          </section>
        </div>

        <aside className="space-y-6">
          <div className="card p-6">
            <div className="mb-4 flex items-center gap-3"><ShieldAlert className="h-5 w-5 text-amber-300" /><h2 className="text-xl font-semibold">My reports</h2></div>
            <div className="space-y-3">
              {reports.length === 0 ? <p className="text-slate-300">No reports yet.</p> : reports.map((report) => (
                <div key={report.id} className="rounded-xl border border-slate-700 bg-slate-950/80 p-3">
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{report.category}</span>
                    <span className="rounded-full bg-emerald-500/10 px-2 py-1 text-xs text-emerald-300">{report.incident_id ? 'Linked' : 'Open'}</span>
                  </div>
                  <p className="mt-2 text-sm text-slate-300">{report.description}</p>
                  {report.ai_summary && <p className="mt-2 text-xs text-amber-300">AI: {report.ai_summary}</p>}
                </div>
              ))}
            </div>
          </div>

          <div className="card p-6">
            <div className="mb-4 flex items-center gap-3"><Bell className="h-5 w-5 text-emerald-300" /><h2 className="text-xl font-semibold">Notifications</h2></div>
            <div className="space-y-3 text-sm text-slate-300">
              <div className="rounded-xl bg-slate-950/70 p-3">Your report was merged into incident INC-001.</div>
              <div className="rounded-xl bg-slate-950/70 p-3">Admin reviewed the priority and assigned maintenance team.</div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
