import { useEffect, useState } from 'react';
import { Activity, BarChart3, BellRing, CheckCircle2, Gauge, ShieldCheck, Users, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import api from '../lib/api';

export default function AdminDashboard() {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState<any>(null);
  const [incidents, setIncidents] = useState<any[]>([]);
  const [reports, setReports] = useState<any[]>([]);

  useEffect(() => {
    api.get('/admin/dashboard', { headers: { Authorization: `Bearer ${localStorage.getItem('civicguard_token')}` } }).then((response) => setStats(response.data)).catch(() => {});
    api.get('/admin/all-incidents', { headers: { Authorization: `Bearer ${localStorage.getItem('civicguard_token')}` } }).then((response) => setIncidents(response.data)).catch(() => {});
    api.get('/admin/all-reports', { headers: { Authorization: `Bearer ${localStorage.getItem('civicguard_token')}` } }).then((response) => setReports(response.data)).catch(() => {});
  }, []);

  const summary = [
    { label: 'Total reports', value: stats?.total_reports ?? 0, icon: <Users className="h-5 w-5" /> },
    { label: 'Total incidents', value: stats?.total_incidents ?? 0, icon: <Activity className="h-5 w-5" /> },
    { label: 'Critical', value: stats?.critical_issues ?? 0, icon: <ShieldCheck className="h-5 w-5" /> },
    { label: 'Active issues', value: stats?.active_issues ?? 0, icon: <Gauge className="h-5 w-5" /> },
  ];

  return (
    <div className="min-h-screen bg-slate-950 p-6 text-slate-50">
      <header className="mx-auto mb-6 flex max-w-7xl items-center justify-between rounded-2xl border border-slate-700 bg-slate-900/80 p-4">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-emerald-300">Admin console</p>
          <h1 className="text-2xl font-bold">CivicGuard AI Dashboard</h1>
        </div>
        <button onClick={logout} className="inline-flex items-center gap-2 rounded-xl border border-slate-700 p-2 text-sm"><LogOut className="h-4 w-4" /> Logout</button>
      </header>

      <div className="mx-auto grid max-w-7xl gap-6">
        <div className="grid gap-4 md:grid-cols-4">
          {summary.map((item) => (
            <div className="card p-4" key={item.label}>
              <div className="mb-3 inline-flex rounded-lg bg-emerald-500/10 p-2 text-emerald-300">{item.icon}</div>
              <p className="text-sm text-slate-300">{item.label}</p>
              <p className="mt-2 text-3xl font-bold">{item.value}</p>
            </div>
          ))}
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <div className="card p-6">
            <div className="mb-4 flex items-center gap-3"><BarChart3 className="h-5 w-5 text-emerald-300" /><h2 className="text-xl font-semibold">Reports by category</h2></div>
            <div className="space-y-3 text-sm">
              {['POTHOLE','ROAD_DAMAGE','STREETLIGHT','GARBAGE'].map((category, index) => (
                <div key={category}>
                  <div className="mb-1 flex justify-between"><span>{category}</span><span>{Math.max(10, 50 - index * 8)}</span></div>
                  <div className="h-2 rounded-full bg-slate-800">
                    <div className="h-2 rounded-full bg-emerald-500" style={{ width: `${55 - index * 11}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card p-6">
            <div className="mb-4 flex items-center gap-3"><BellRing className="h-5 w-5 text-emerald-300" /><h2 className="text-xl font-semibold">AI recommendations</h2></div>
            <div className="space-y-3 text-sm text-slate-300">
              <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-3">3 REPORTS → 1 ACTUAL INCIDENT</div>
              <div className="rounded-xl border border-slate-700 bg-slate-950/80 p-3">INC-001 | Pothole near Main Gate | Priority: P1 CRITICAL</div>
              <div className="rounded-xl border border-slate-700 bg-slate-950/80 p-3">Recommended department: Maintenance</div>
            </div>
          </div>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Recent incidents</h2>
            <div className="space-y-3">
              {incidents.map((incident) => (
                <div key={incident.id} className="rounded-xl border border-slate-700 bg-slate-950/80 p-3">
                  <div className="flex justify-between"><span className="font-medium">{incident.title}</span><span className="text-emerald-300">{incident.priority}</span></div>
                  <p className="mt-2 text-sm text-slate-300">{incident.location}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="card p-6">
            <h2 className="mb-4 text-xl font-semibold">Open reports</h2>
            <div className="space-y-3">
              {reports.map((report) => (
                <div key={report.id} className="rounded-xl border border-slate-700 bg-slate-950/80 p-3">
                  <div className="flex justify-between"><span>{report.category}</span><span className="text-amber-300">{report.status}</span></div>
                  <p className="mt-2 text-sm text-slate-300">{report.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
