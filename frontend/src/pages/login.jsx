import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { Coffee } from 'lucide-react';

const Login = () => {
  // CORRECCIÓN: Inicializamos con valores definidos para evitar errores de "undefined"
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/token/', {
        username: form.username,
        password: form.password
      });
      
      localStorage.setItem('access', response.data.access);
      window.location.href = '/dashboard';
    } catch (err) {
      setError('Usuario o contraseña incorrectos.');
      console.error("Error al iniciar sesión", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo">
          <Coffee size={32} />
          <h1>Buen Apetito</h1>
          <p>Panel de administración</p>
        </div>

        <form onSubmit={handleLogin} className="login-form">
          <div className="form-group">
            <label>Usuario</label>
            <input
              type="text"
              // Usamos || '' para asegurar que siempre haya una cadena de texto
              value={form.username || ''} 
              onChange={e => setForm({ ...form, username: e.target.value })}
              placeholder="tu_usuario"
              required
            />
          </div>
          <div className="form-group">
            <label>Contraseña</label>
            <input
              type="password"
              value={form.password || ''}
              onChange={e => setForm({ ...form, password: e.target.value })}
              placeholder="••••••••"
              required
            />
          </div>
          
          {error && <div className="alert alert--error">{error}</div>}
          
          <button type="submit" className="btn btn--primary btn--full" disabled={loading}>
            {loading ? 'Entrando...' : 'Iniciar sesión'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;