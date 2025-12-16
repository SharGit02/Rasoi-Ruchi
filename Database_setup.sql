
CREATE DATABASE IF NOT EXISTS recipe_app;

CREATE USER IF NOT EXISTS 'recipe_user'@'localhost' IDENTIFIED BY 'SharRecipeBook';

GRANT ALL PRIVILEGES ON recipe_app.* TO 'recipe_user'@'localhost';

FLUSH PRIVILEGES;


DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS instructions;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS recipes;

CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    cuisine VARCHAR(100),
    course VARCHAR(100),
    diet_type VARCHAR(50),
    prep_time_minutes INT,
    cook_time_minutes INT,
    image_path VARCHAR(255) NULL -- Stores the path to the uploaded image file
);

CREATE TABLE ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE instructions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT,
    step_number INT,
    description TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE TABLE recipe_ingredients (
    recipe_id INT,
    ingredient_id INT,
    quantity VARCHAR(50),
    unit VARCHAR(50),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
    PRIMARY KEY (recipe_id, ingredient_id) -- Ensures an ingredient is listed only once per recipe
);


CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT NOT NULL,
    author VARCHAR(100) DEFAULT 'Anonymous',
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

