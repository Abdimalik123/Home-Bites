import { useEffect, useState } from "react";
import { Link } from "react-router-dom"; // Add this if you want navigation
import { API_URL } from "../services/auth";

interface Author {
    first_name: string;
    last_name: string;
}

interface Ingredients {
    name: string;
    quantity: string;
    unit: string;
}

interface Recipe {
    author: Author;
    recipe_id: number;
    instructions: string;
    ingredients: Ingredients[];
    created_at: string;
    title: string;
}

function AllRecipesPage() { 
    const [recipes, setRecipes] = useState<Recipe[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    useEffect(() => {
        const fetchRecipes = async () => {
            try {
                const res = await fetch(`${API_URL}/recipes`);
                if (!res.ok) {
                    throw new Error("Failed to fetch recipes");
                }
                const data = await res.json(); 
                setRecipes(data);
            } catch (error) {
                console.error("Error fetching recipes:", error);
                setError("Failed to load recipes. Please try again later.");
            } finally {
                setLoading(false);
            }
        };
        fetchRecipes();
    }, []);

    // Format date helper
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">All Recipes</h1>
            
            {loading ? (
                <p>Loading recipes...</p>
            ) : error ? (
                <p className="text-red-600">{error}</p>
            ) : recipes.length === 0 ? (
                <p className="text-gray-600">No recipes found. Be the first to add one!</p>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {recipes.map((recipe) => (
                        <Link 
                            key={recipe.recipe_id} 
                            to={`/recipes/${recipe.recipe_id}`}
                            className="border rounded p-4 shadow hover:shadow-lg transition-shadow"
                        >
                            <h2 className="text-xl font-semibold">{recipe.title}</h2>
                            <p className="text-gray-600">
                                By {recipe.author.first_name} {recipe.author.last_name}
                            </p>
                            <p className="text-sm text-gray-500 mt-1">
                                {formatDate(recipe.created_at)}
                            </p>
                            <p className="mt-2 text-gray-700 line-clamp-3">
                                {recipe.instructions}
                            </p>
                            <div className="mt-2">
                                <p className="text-sm font-medium text-gray-700">
                                    Ingredients ({recipe.ingredients.length}):
                                </p>
                                <ul className="mt-1 list-disc list-inside text-sm text-gray-600">
                                    {recipe.ingredients.slice(0, 3).map((ing, index) => (
                                        <li key={index}>
                                            {ing.quantity} {ing.unit} {ing.name}
                                        </li>
                                    ))}
                                    {recipe.ingredients.length > 3 && (
                                        <li className="text-gray-500">
                                            +{recipe.ingredients.length - 3} more...
                                        </li>
                                    )}
                                </ul>
                            </div>
                        </Link>
                    ))}
                </div>
            )}
        </div>
    );
}

export default AllRecipesPage;