const API_URL= 'https://localhost:5000'; // backend url

export async function login(email: string, password: string) {
  const res = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  return res.json();
}

export async function register(data: { firstname: string, lastname: string, email: string, password: string, confirm_password: string}) {
  const res = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}

// optional: store and get JWT from localStorage
export function setToken(token: string) { localStorage.setItem('jwt', token); }
export function getToken() { return localStorage.getItem('jwt'); }
export function clearToken() { localStorage.removeItem('jwt'); }
