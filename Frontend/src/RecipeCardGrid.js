import React from 'react';
import RecipeCard from './components/RecipeCard';  // Import the RecipeCard component
import '../styles/RecipeStyles.css';  // Import the CSS file

const RecipeCardGrid = ({ recipes }) => {
  // Ensure we only display up to 5 recipes
  const displayedRecipes = recipes.slice(0, 5);

  return (
    <div className="recipe-card-grid">
      {displayedRecipes.map(recipe => (
        <RecipeCard key={recipe.id} recipe={recipe} />
      ))}
    </div>
  );
};

export default RecipeCardGrid;
