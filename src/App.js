import React, { Component } from 'react';
import { Document } from 'react-pdf';
//import ImageMapper from 'react-image-mapper';
import Home from './Home';
import Image1 from './Image1';
import Test1 from './spoon5.jpg';
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
    this.roomid = 0;
    this.imagePath = "/home";
    this.getQuery = this.getQuery.bind(this)
  }

  getQuery() {
    const url = '/api/search/?building=WITHERSPOON&number=509';

    fetch(url, {credentials: "same-origin"})
      .then(response => {
        return response.json();
      })
      .then(data => {
        this.setState({
          rooms: data
        });
        this.roomid = data[0].room_id;
        console.log(this.roomid);
        console.log(data);
      })
      .catch(error => console.log(error));
  }

  getFloorplan() {
    if (this.roomid === 0)
      this.imagePath = "./spoon5.jpg";
    else
      this.imagePath = './spoon5.jpg';
  }

  render() {
    return (
      <BrowserRouter>
        <div className = "App">
          <form>
            <input type="text"
              placeholder="Search Room"
              onChange={this.getQuery}
              onSubmit={this.getFloorplan}/>
          </form>
          <img usemap="#test_map" src={Test1}/>

          <map name="test_map">
            <area shape="poly" coords="3671,3587,3670,4476,4202,4476,4203,4498,4460,4498,4461,4227,4405,4225,4405,3824,4461,3822,4461,3587,4051,3587,4050,3755,4044,3587" href="google.com"/>
          </map>
        </div>
      </BrowserRouter>
      );
  }
}
/* 


*/






/*
<Switch>
  <Route path={this.imagePath} component = {Main} />
</Switch>
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
*/

const Main = () => (
  <div>
    <Link to="/image1"> <Home /> </Link>
  </div>
)

const Back = () => (
  <div>
    <Link to="/home"> <Image1 /> </Link>
  </div>
)

export default App;
