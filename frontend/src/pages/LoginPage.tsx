import { useNavigate } from 'react-router-dom';
import { ArrowRight, FileText, MapPinned, ShieldCheck, UserRound } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login, user } = useAuth();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const email = String(form.get('email'));
    const password = String(form.get('password'));
    await login(email, password);
    if (user) {
      navigate(`/${user.role}`);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 px-6 py-10 text-slate-50">
      <div className="mx-auto max-w-6xl grid gap-8 lg:grid-cols-2 items-center">
        <div>
          <div className="mb-6 inline-flex items-center rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-sm text-emerald-300">From Complaints to Action.</div>
          <h1 className="text-5xl font-bold tracking-tight">CivicGuard AI</h1>
          <p className="mt-4 max-w-xl text-slate-300 text-lg">AI-powered infrastructure complaint and incident management for colleges, campuses, and cities.</p>
          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            <FeatureCard icon={<FileText className="h-5 w-5" />} title="Smart clustering" text="Multiple reports become one incident." />
            <FeatureCard icon={<MapPinned className="h-5 w-5" />} title="Geo-aware" text="Map-driven visibility for teams." />
            <FeatureCard icon={<ShieldCheck className="h-5 w-5" />} title="Priority engine" text="AI grading with transparent rationale." />
            <FeatureCard icon={<UserRound className="h-5 w-5" />} title="Role-based access" text="Student, worker, and admin workflows." />
          </div>
        </div>

        <div className="card p-8">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-2xl font-semibold">Login</h2>
            <button className="text-sm text-emerald-300" onClick={() => navigate('/register')}>Create account</button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="mb-2 block text-sm text-slate-300">Email</label>
              <input name="email" type="email" defaultValue="student@civicguard.ai" className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-emerald-400" />
            </div>
            <div>
              <label className="mb-2 block text-sm text-slate-300">Password</label>
              <input name="password" type="password" defaultValue="student123" className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-emerald-400" />
            </div>
            <button type="submit" className="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-emerald-400">
              Sign in <ArrowRight className="h-4 w-4" />
            </button>
          </form>

          <div className="mt-6 rounded-xl border border-slate-700 bg-slate-950/80 p-4 text-sm text-slate-300">
            Demo accounts: <br />
            Student: student@civicguard.ai / student123 <br />
            Worker: worker@civicguard.ai / worker123 <br />
            Admin: admin@civicguard.ai / admin123
          </div>
        </div>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, text }: { icon: React.ReactNode; title: string; text: string }) {
  return (
    <div className="card p-4">
      <div className="mb-3 inline-flex rounded-lg bg-emerald-500/10 p-2 text-emerald-300">{icon}</div>
      <h3 className="font-semibold">{title}</h3>
      <p className="mt-1 text-sm text-slate-300">{text}</p>
    </div>
  );
}
