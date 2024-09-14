import React from 'react';
import TopRatedSlider from '../components/TopRatedSlider';
import CategoryGrid from '../components/CategoryGrid';
import RecipeGrid from '../components/RecipeGrid';
import '../styles/HomePage.css';

const HomePage = () => {
  return (
    <div className="home-page">
      <TopRatedSlider />
      <h2>Recipe Categories</h2>
      <CategoryGrid />
      <RecipeGrid title="Popular Recipes" endpoint="/api/popular_recipes" />
    </div>
  );
};

export default HomePage;
