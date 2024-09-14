import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import RecipeGrid from '../components/RecipeGrid';
import '../styles/SearchResultsPage.css';

const SearchResultsPage = () => {
  const [results, setResults] = useState([]);
  const location = useLocation();
  const query = new URLSearchParams(location.search).get('q');

  useEffect(() => {
    if (query) {
      fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => setResults(data))
        .catch(error => console.error('Error fetching search results:', error));
    }
  }, [query]);

  return (
    <div className="search-results">
      <h1>Search Results for "{query}"</h1>
      <RecipeGrid recipes={results} title="Search Results" />
    </div>
  );
};

export default SearchResultsPage;
