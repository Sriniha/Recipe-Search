import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import RecipeDetailsPage from './pages/RecipeDetailsPage';
import CategoryPage from './pages/CategoryPage';
import SearchResultsPage from './pages/SearchResultsPage.js';
import './styles/global.css';

const App = () => {
  return (
    <Router>
      <div className="App">
        <Header />
        <Switch>
          <Route exact path="/" component={HomePage} />
          <Route path="/recipe/:id" component={RecipeDetailsPage} />
          <Route path="/category/:category" component={CategoryPage} />
          <Route path="/search" component={SearchResultsPage} />
        </Switch>
      </div>
    </Router>
  );
};

export default App;