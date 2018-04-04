import React, { Component } from 'react';
import Home from './Home';
import Image1 from './Image1';
import './App.css';
import {
  Route, 
  Switch,
  Link,
  Redirect,
  BrowserRouter,
} from 'react-router-dom';

class App extends Component {
  render(){
    return (
      <BrowserRouter>
        <div className = "App">
          <Switch>
            <Route path="/login" component = {Login} />
            <PrivateRoute exact path="/" component = {Main} />
            <PrivateRoute path="/image1" component = {Back} />
          </Switch>
        </div>
      </BrowserRouter>
    );
  }
}

class Login extends Component {
  state = {
    redirectToRefferrer: false
  }; 

  login = () => {
    fakeAuth.authenticate(() => {
      this.setState({ redirectToRefferrer: true});
    });
  };

  render () {
    return (
      <div className="Login-page">
        <h1 className="Welcome-page">Welcome to Redraw!</h1> 
        <h2 className="Description">
          Making room draw a more enjoyable experience
        </h2>
        <Link to="/">
          <button className="Login-button" onClick = {this.login}>
             Click Here to Login 
          </button>
        </Link>
      </div>
    );
  }
}

const fakeAuth = {
  isAuthenticated: false,
  authenticate(cb) {
    this.isAuthenticated = true; 
    setTimeout(cb, 100);
  }, 
  signout(cb) {
    this.isAuthenticated = false;
    setTimeout(cb, 100);
  }
}

const PrivateRoute = ({ component: Component, ...rest}) => (
  <Route 
    {...rest} 
    render={props =>
      fakeAuth.isAuthenticated ? (
        <Component {...props} />
      ) : (
        <Redirect 
          to = {{
            pathname: "/login",
            state: {from: props.location}
          }}
        />
      )
    }
  />
);

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
