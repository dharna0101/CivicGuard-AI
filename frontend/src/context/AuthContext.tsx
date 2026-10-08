import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import api from '../lib/api';

interface User {
  user_id: string;
  name: string;
  role: string;
  email: string;
}

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { name: string; email: string; password: string; role: string; phone?: string }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('civicguard_token');
    if (!token) {
      setLoading(false);
      return;
    }

    api
      .get('/auth/verify', { params: { token } })
      .then((response) => {
        setUser({
          user_id: response.data.user_id,
          name: response.data.name,
          role: response.data.role,
          email: response.data.email,
        });
      })
      .catch(() => {
        localStorage.removeItem('civicguard_token');
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    localStorage.setItem('civicguard_token', response.data.access_token);
    setUser({
      user_id: response.data.user_id,
      name: response.data.name,
      role: response.data.role,
      email: response.data.email,
    });
  };

  const register = async (data: { name: string; email: string; password: string; role: string; phone?: string }) => {
    const response = await api.post('/auth/register', data);
    localStorage.setItem('civicguard_token', response.data.access_token);
    setUser({
      user_id: response.data.user_id,
      name: response.data.name,
      role: response.data.role,
      email: response.data.email,
    });
  };

  const logout = () => {
    localStorage.removeItem('civicguard_token');
    setUser(null);
  };

  const value = useMemo<AuthContextValue>(() => ({ user, loading, login, register, logout }), [user, loading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
