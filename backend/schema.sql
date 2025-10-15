-- =========================
-- Recipe & Ingredient Web App Schema (Normalized)
-- =========================

-- 1️⃣ Users table (keep your existing users)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    first_name TEXT,
    last_name TEXT
);

-- 2️⃣ Recipes table
CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    instructions TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 3️⃣ Ingredient master table (list of unique ingredients)
CREATE TABLE IF NOT EXISTS ingredient_master (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- 4️⃣ Recipe ingredients (linking recipes to ingredients with quantity and unit)
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipe_id INT NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_id INT NOT NULL REFERENCES ingredient_master(id) ON DELETE CASCADE,
    quantity NUMERIC NOT NULL,
    unit TEXT,
    PRIMARY KEY (recipe_id, ingredient_id)
);

-- 5️⃣ Categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- 6️⃣ Join table for recipes and categories (many-to-many)
CREATE TABLE IF NOT EXISTS recipe_categories (
    recipe_id INT NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    category_id INT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (recipe_id, category_id)
);

-- 7️⃣ Comments table
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    recipe_id INT NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 8️⃣ Likes table (many-to-many)
CREATE TABLE IF NOT EXISTS likes (
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipe_id INT NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, recipe_id)
);

-- 9️⃣ Favorites table (many-to-many)
CREATE TABLE IF NOT EXISTS favorites (
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipe_id INT NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, recipe_id)
);

-- 🔹 Optional Indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_recipes_title ON recipes(title);
CREATE INDEX IF NOT EXISTS idx_ingredient_master_name ON ingredient_master(name);
CREATE INDEX IF NOT EXISTS idx_recipe_categories_category_id ON recipe_categories(category_id);
