import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import RecipeCard from '../components/RecipeCard';
import '../styles/CategoryPage.css';

const CategoryPage = () => {
  const [recipes, setRecipes] = useState([]);
  const { category } = useParams();

  useEffect(() => {
    const fetchCategoryRecipes = async () => {
      try {
        const response = await fetch(`/api/category/${category}`);
        const data = await response.json();
        setRecipes(data);
      } catch (error) {
        console.error('Error fetching category recipes:', error);
      }
    };

    fetchCategoryRecipes();
  }, [category]);

  return (
    <div className="category-page">
      <h1>{category} Recipes</h1>
      <div className="recipe-grid">
        {recipes.map(recipe => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
    </div>
  );
};

export default CategoryPage;
