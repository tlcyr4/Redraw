import React, { Component } from 'react';
import Home from './Home';
import Image1 from './Image1';
import './App.css';
import {
  Route, 
  Switch,
  Link,
  BrowserRouter,
} from 'react-router-dom';

// hold the static components
class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      rooms: [],
    };
  }

  componentDidMount() {
    const url = 'https:predraw.herokuapp.com/api/search/?building=FISHER&number=A101';
    fetch(url, {
      headers : { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
       }
      })
      .then((response) => {
        return response;
      })
      .then(data => {
        this.setState({
          rooms: data
        });
        console.log("HI");
        console.log(data);
      })
      .catch((error) => console.log(error));
  }

  render(){
    return (
      <BrowserRouter>
        <div className = "App">
          <Switch>
            <Route path="/login" component = {Login} />
            <Route exact path="/home" component = {Main} />
            <Route path="/image1" component = {Back} />
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
        <Link to="/accounts/login">
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


const Main = () => (
  <div>
    <form><input
          type="text"
          placeholder="Search Room"/>
    </form>
    <Link to="/image1"> <Home /> </Link>
  </div>
)

const Back = () => (
  <div>
    <Link to="/home"> <Image1 /> </Link>
  </div>
)

export default App;
