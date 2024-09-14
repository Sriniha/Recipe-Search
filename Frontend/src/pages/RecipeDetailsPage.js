import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/RecipeDetailsPage.css';

const RecipeDetailsPage = () => {
  const [recipe, setRecipe] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    fetch(`/api/recipe/${id}`)
      .then(response => response.json())
      .then(data => setRecipe(data))
      .catch(error => console.error('Error fetching recipe:', error));
  }, [id]);

  if (!recipe) return <div>Loading...</div>;

  return (
    <div className="recipe-details">
      <h1>{recipe.title}</h1>
      <img src={recipe.image} alt={recipe.title} className="recipe-image" />
      <div className="recipe-info">
        <p>Rating: {recipe.rating}</p>
        <p>Calories: {recipe.calories}</p>
        <p>Protein: {recipe.protein}g</p>
        <p>Fat: {recipe.fat}g</p>
        <p>Sodium: {recipe.sodium}mg</p>
        <p>Tags: {recipe.tags.join(', ')}</p>
      </div>
      {/* Add more details as needed */}
    </div>
  );
};

export default RecipeDetailsPage;
