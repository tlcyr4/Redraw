import React, { Component } from 'react';
import Home from './Home';
import Image1 from './Image1';
/*import './App.css';*/
import {
  Route, 
  NavLink, 
  BrowserRouter
} from 'react-router-dom';

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div className = "App">
          <NavLink to="/image1"> <Home /> </NavLink>
          <Route exact path="/image1" component = {Image1} />
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
