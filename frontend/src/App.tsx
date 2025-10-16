import { Routes, Route, Link } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import AllRecipesPage from './pages/AllRecipesPage';
import RecipeDetailPage from './pages/RecipeDetailPage';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow p-4">
        <nav className="flex justify-center space-x-4">
          <Link to="/login" className="text-blue-600 hover:underline">Login</Link>
          <Link to="/register" className="text-green-600 hover:underline">Register</Link>
        </nav>
      </header>

      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/" element={<HomePage />} />
        <Route path="/recipes" element={<AllRecipesPage />} />
        <Route path="/recipes/:id" element={<RecipeDetailPage />} />
      </Routes>
    </div>
  );
}

export default App;