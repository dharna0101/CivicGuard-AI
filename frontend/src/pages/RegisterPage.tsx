import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function RegisterPage() {
  const navigate = useNavigate();
  const { register } = useAuth();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    await register({
      name: String(form.get('name')),
      email: String(form.get('email')),
      password: String(form.get('password')),
      role: String(form.get('role')), 
      phone: String(form.get('phone') || ''),
    });
    navigate('/student');
  };

  return (
    <div className="min-h-screen bg-slate-950 px-6 py-12 text-slate-50">
      <div className="mx-auto max-w-xl card p-8">
        <h2 className="text-3xl font-bold">Register</h2>
        <p className="mt-2 text-slate-300">Create an account to report a civic issue.</p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label className="mb-2 block text-sm">Name</label>
            <input name="name" className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3" required />
          </div>
          <div>
            <label className="mb-2 block text-sm">Email</label>
            <input type="email" name="email" className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3" required />
          </div>
          <div>
            <label className="mb-2 block text-sm">Password</label>
            <input type="password" name="password" className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3" required />
          </div>
          <div>
            <label className="mb-2 block text-sm">Role</label>
            <select name="role" className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3" defaultValue="student">
              <option value="student">Student / Citizen</option>
              <option value="worker">Worker</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div>
            <label className="mb-2 block text-sm">Phone (optional)</label>
            <input name="phone" className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3" />
          </div>

          <button type="submit" className="w-full rounded-xl bg-emerald-500 px-4 py-3 font-semibold text-slate-950">Register</button>
        </form>
        <button className="mt-4 text-sm text-emerald-300" onClick={() => navigate('/login')}>Back to login</button>
      </div>
    </div>
  );
}
