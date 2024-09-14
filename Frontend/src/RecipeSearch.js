import React, { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar';
import FilterPanel from './FilterPanel';

const RecipeSearch = () => {
  const [filters, setFilters] = useState({
    calories: '',
    dietary: [],
  });
  const [availableFilters, setAvailableFilters] = useState({
    calories_range: { min: 0, max: 1000 },
    dietary: [],
  });

  useEffect(() => {
    fetchFilters();
  }, []);

  const fetchFilters = async () => {
    try {
      const response = await fetch('/api/filters');
      const data = await response.json();
      setAvailableFilters(data);
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  };

  const handleFilterChange = (name, value) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [name]: value
    }));
  };

  const handleSearch = (searchParams) => {
    // Implement search logic here
    console.log('Searching with params:', searchParams);
  };

  return (
    <div className="recipe-search">
      <SearchBar 
        filters={filters} 
        onFilterChange={handleFilterChange} 
        onSearch={handleSearch}
      />
      <FilterPanel 
        filters={filters} 
        availableFilters={availableFilters} 
        onFilterChange={handleFilterChange}
      />
    </div>
  );
};

export default RecipeSearch;
