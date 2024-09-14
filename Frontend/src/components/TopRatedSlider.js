import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import '../styles/TopRatedSlider.css';

const TopRatedSlider = () => {
  const [topRatedRecipes, setTopRatedRecipes] = useState([]);

  useEffect(() => {
    fetch('/api/top_rated')
      .then(response => response.json())
      .then(data => setTopRatedRecipes(data))
      .catch(error => console.error('Error fetching top rated recipes:', error));
  }, []);

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 4000,
  };

  return (
    <div className="top-rated-slider">
      <h2>Top Rated Recipes</h2>
      <Slider {...settings}>
        {topRatedRecipes.map(recipe => (
          <div key={recipe.id} className="slide">
            <Link to={`/recipe/${recipe.id}`}>
              <img src={recipe.image} alt={recipe.title} />
              <h3>{recipe.title}</h3>
              <p>Rating: {recipe.rating}</p>
            </Link>
          </div>
        ))}
      </Slider>
    </div>
  );
};

export default TopRatedSlider;
