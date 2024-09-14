import React from 'react';
import { Link } from 'react-router-dom';
import SearchBar from './SearchBar';
import '../styles/Header.css';

const Header = () => {
  return (
    <header className="header">
      <Link to="/" className="logo">Recipe Finder</Link>
      <SearchBar />
      <button className="filter-btn">Filters</button>
      <Link to="/profile" className="profile-icon">Profile</Link>
    </header>
  );
};

export default Header;
