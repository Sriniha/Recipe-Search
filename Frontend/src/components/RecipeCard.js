import React from 'react';

const RecipeCard = ({ recipe }) => {
  return (
    <div className="recipe-card">
      <h3>{recipe.title}</h3>
      <p>{recipe.description}</p>
      {/* Add more recipe details as needed */}
    </div>
  );
};

export default RecipeCard;
