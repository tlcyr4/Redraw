import React, { Component } from 'react';
import ImageMapper from 'react-image-mapper';
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faSearch from '@fortawesome/fontawesome-free-solid/faSearch'
import Center from 'react-center';
import Spoon5 from './wendell2.jpg';
import Logo from './raw.jpg';

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
    // roomid 
    this.roomid = 0;
    // list of all the rooms in the list, used for ImageMapper
    this.roomIDRendered = [];
    // the path of the image, NOT USED CURRENTLY
    this.imagePath = "/api/floorplan/?room_id";
    // hold onto the search input
    this.searchLink = "";
    this.getQuery = this.getQuery.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  // get query from the url
  getQuery() {
    const url = '/api/search/?building='+this.searchLink;

    fetch(url, {credentials: "same-origin"})
      .then(response => {
        return response.json();
      })
      .then(data => {
        this.setState({
          rooms: data
        });
        this.roomid = data[0].room_id;
        console.log(this.state.rooms);
        this.forceUpdate();
      })
      .catch(error => console.log(error));
  }

  // get the floorplan
  getFloorplan() {
    if (this.roomid === 0)
      this.imagePath = "/home";
    else
      this.imagePath = '/api/floorplan/?room_id'+this.roomid;
    console.log("HELLO");
  }

  // handle the clicking on image mapper
  handleClick = (obj, num, event) => {
    var query = this.state.rooms;
    for (var i = 0; i < query.length; i++) {
      var iRoom = query[i];
      // print how many sqft the room is on the console
      if (iRoom.room_id === this.roomIDRendered[num]) {
        console.log("Room " + iRoom.room_id + " is " + iRoom.sqft + " sqft.");
        break;
      }
    }
  }

  // handle submission of the search query
  handleSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.target);
    this.searchLink = data.get('search');
    console.log(this.searchLink);
    this.getQuery();
  }

  render() {
    // process the json file
    var witherspoonQuery = this.state.rooms;
    var areaArray = [];
    var ratio = 1000.0/2550.0;
    // go through every room in the json file
    for (var i = 0; i < witherspoonQuery.length; i++) {
      var iRoom = witherspoonQuery[i];
      if (iRoom.floor_id === 568) {
        var roomCoords = [];
        var roomRaw = JSON.parse(iRoom.polygons);
        //console.log(roomRaw);
        //console.log(roomRaw.length);
        for (var k = 0; k < roomRaw.length; k++)
        var roomArray = roomRaw[0]; // over a for loop FIX FIX
        for (var j = 0; j < roomArray.length; j++) {
          roomCoords.push(parseInt(parseInt(roomArray[j][0], 10)/4*ratio, 10));
          roomCoords.push(parseInt(parseInt(roomArray[j][1], 10)/4*ratio, 10));
        }
        areaArray.push({shape: 'poly', coords: roomCoords});
        // hold onto the order of the polygons wrt to the rooms
        // useful for when handling click
        this.roomIDRendered.push(iRoom.room_id);
      }
    }
    console.log(areaArray);

    // make the MAP to be drawn in
    var MAP = {
      name: 'my-map',
      areas: areaArray,
    };
    //var URL = 'spoon5.jpg';
    return (
      <BrowserRouter>

        <div className = "App">
          <div id = "header">
            <img id = "headerImg" src={Logo}/>
            <p>edraw</p>
          </div>
          <div id = "formBlock">
            <form onSubmit = {this.handleSubmit}>
              <input type="text"
                placeholder="Search Room..."
                name="search"/>
              <button name="submitButton" type="submit"><FontAwesomeIcon icon = {faSearch}/></button>
            </form>
          </div>
          <Center>
            <ImageMapper src={Spoon5} map={MAP} fillColor="rgba(127,255,212,0.5)" width={1000} 
            onClick={(obj, num, event) => this.handleClick(obj, num, event)}/>
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

export default () => (
  <App/>
);
