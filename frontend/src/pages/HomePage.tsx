import {Link} from 'react-router-dom';

function HomePage() {
    return (
        <div className="container mx-auto p-4">
            <nav>
                <Link to="/login" className="mr-4 text-blue-600 hover:underline">
                    Login
                </Link>
                <Link to="/register" className="text-green-600 hover:underline">
                    Register
                </Link>
            <h1 className="text-3xl font-bold mb-4">Welcome to the Recipe App</h1>
            <p className="mb-4">Discover and share amazing recipes from around the world!</p>
            <Link to="/recipes" className="text-blue-600 hover:underline">
                View All Recipes
            </Link>
            </nav>
        </div>
    );
}
export default HomePage;