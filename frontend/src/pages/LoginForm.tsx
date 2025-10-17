import { useState } from 'react';
import {login, setToken} from '../services/auth';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState("");


  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Login submitted:', { email, password });
    
    try {
      const response = await login(email, password);
        if (response.success) {
          if (response.token) setToken(response.token);
          setMessage(response.message || "Login successful!");
        } else {
          setMessage(response.error || "Login failed.");
        }
      } catch (err) {
        console.error(err);
        setMessage("Something went wrong. Please try again.");
      }
    };
    

  return (
    <form onSubmit={onSubmit} className="max-w-md w-full p-6 bg-white rounded-lg shadow space-y-6">
      <h2 className="text-2xl font-bold text-center text-gray-800">Login</h2>

      <div>
        <label className="block text-sm font-medium text-gray-700">Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none"
          placeholder="you@example.com"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none"
          placeholder="••••••••"
          required
        />
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
      >
        Sign In
      </button>
      {message && (
        <p className="text-center text-sm text-gray-700 mt-4">{message}</p>
      )}
    </form>
  );
  
}
export default LoginForm;