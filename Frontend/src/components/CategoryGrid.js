import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/CategoryGrid.css';

const CategoryGrid = () => {
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchCategories();
  }, []);

  async function fetchCategories() {
    try {
      const response = await fetch('/api/categories');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const categoriesData = await response.json();
      setCategories(categoriesData);
    } catch (error) {
      console.error('There was a problem fetching the categories:', error);
    }
  }

  return (
    <div className="category-grid">
      {categories.map((category) => (
        <Link to={`/category/${category.name}`} key={category.name} className="category-item">
          <img src={category.image} alt={category.name} />
          <h3>{category.name}</h3>
        </Link>
      ))}
    </div>
  );
};

export default CategoryGrid;
