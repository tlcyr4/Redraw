import React, { Component } from 'react';
import Home from './Home';
import Image1 from './Image1';
/*import './App.css';*/
import {
  Route, 
  Switch, 
  Link,
  BrowserRouter
} from 'react-router-dom';

class App extends Component {
  render(){
    return (
      <BrowserRouter>
        <div className = "App">
          <Switch>
            <Route exact path="/" component = {Main} /> 
            <Route path = "/image1" component = {Back} />
          </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

const Main = () => (
  <div>
    <Link to="/image1"> <Home /> </Link>
  </div>
)

const Back = () => (
  <div>
    <Link to="/"> <Image1 /> </Link>
  </div>
)

export default App;
