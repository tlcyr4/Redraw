import React, { Component } from 'react';
import ImageMapper from 'react-image-mapper';
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faSearch from '@fortawesome/fontawesome-free-solid/faSearch'
import Center from 'react-center';
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
    this.imagePath = "/api/floorplan/?room_id";
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
      this.imagePath = "/home";
    else
      this.imagePath = '/api/floorplan/?room_id'+this.roomid;
    console.log("HELLO");
  }

  handleClick = () => {
    console.log("HELLO");
  }

  render() {
    var MAP = {
      name: 'my-map',
      areas: [
        {shape: 'poly', coords: [50,66,54,600,256,480,256,188]},
        {shape: 'poly', coords: [438,236,440,420,566,420,568,238]},
        {shape: 'poly', coords: [762,482,766,188,462*2,53*2,457*2,282*2]},
        {shape: 'poly', coords: [245*2,285*2,290*2,285*2,274*2,239*2,249*2,238*2]},
      ]
    };
    var URL = 'https://c1.staticflickr.com/5/4052/4503898393_303cfbc9fd_b.jpg';
    return (
      <BrowserRouter>

        <div className = "App">
          <form>
            <input type="text"
              placeholder="Search Room..."
              onChange={this.getQuery}
              onSubmit={this.getFloorplan}/>
            <button id="submitButton" type="submit"><FontAwesomeIcon icon = {faSearch}/></button>
          </form>
        <Center>
          <ImageMapper src={URL} map={MAP} width={1000} onClick={(obj, num, event) => this.handleClick(obj, num, event)}/>
        </Center>

        </div>
      </BrowserRouter>
      );
  }
}
/* 
<img usemap="#test_map" src={this.imagePath}/>

          <map name="test_map">
            <area shape="poly" coords="3671,3587,3670,4476,4202,4476,4203,4498,4460,4498,4461,4227,4405,4225,4405,3824,4461,3822,4461,3587,4051,3587,4050,3755,4044,3587" href="google.com"/>
          </map>
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

export default App;
