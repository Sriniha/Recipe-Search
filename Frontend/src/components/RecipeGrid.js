import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/RecipeGrid.css';

const RecipeGrid = ({ title = "Popular Recipes", endpoint = "/api/popular_recipes" }) => {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    fetch(endpoint)
      .then(response => response.json())
      .then(data => setRecipes(data))
      .catch(error => console.error(`Error fetching recipes from ${endpoint}:`, error));
  }, [endpoint]);

  return (
    <div className="recipe-grid-container">
      <h2>{title}</h2>
      <div className="recipe-grid">
        {recipes.map(recipe => (
          <Link to={`/recipe/${recipe.id}`} key={recipe.id} className="recipe-card">
            <img src={recipe.image} alt={recipe.title} className="recipe-image" />
            <div className="recipe-info">
              <h3>{recipe.title}</h3>
              <p>Rating: {recipe.rating}</p>
              <p>Calories: {recipe.calories}</p>
              <p>Tags: {recipe.tags.join(', ')}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default RecipeGrid;
