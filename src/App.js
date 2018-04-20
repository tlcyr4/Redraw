import React, { Component } from 'react';
import ImageMapper from 'react-image-mapper';
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faSearch from '@fortawesome/fontawesome-free-solid/faSearch'
import Center from 'react-center';
import Wendell from './wendell2.jpg';
import Logo from './raw.jpg';
import './App.css';
import {
  BrowserRouter,
} from 'react-router-dom';

// hold the static components
class App extends Component {
	
  constructor(props) {
    super(props);
    this.state = {
      rooms: [],
    };
		// Room-ID, Changed on Click
    this.roomid = 0;
		
		// List of all the rooms that can be displayed, used for ImageMapper
    this.roomIDRendered = []; 
		
    // the path of the image, being tested
    this.imagePath = Wendell;
		
    // hold onto the search input
    this.searchLink = "";
		
		// Binds methods to the object
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

  // Using ROOM-ID, receive floorplan filepath from Back-End.
  getFloorplan() {
		const url = '/api/floorplan/?room_id='+this.roomid;

    fetch(url, {credentials: 'same-origin'})
      .then((response) => { return response.blob(); })
			.then((data) => {
				var objectURL = URL.createObjectURL(data);
				this.imagePath = objectURL;
				console.log(this.imagePath);
				this.forceUpdate();
      })
      .catch(error => console.log(error));
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
    const searchData = data.get('search');
		
		// Needs work to parse the input query
    console.log(searchData);
		
		if (isNaN(searchData)) {
			this.searchLink = searchData;
			this.getQuery();
		}
    else {
			this.roomid = searchData; 
			this.getFloorplan();
		}
  }

  render() {
    // Process the JSON received from Back-End
    var retQuery = this.state.rooms;
    var areaArray = [];
    // used to be 2550, now is 1015********************
    var ratio = 1000.0/2550.0;
    // go through every room in the json file
    for (var i = 0; i < retQuery.length; i++) {
      var iRoom = retQuery[i];
      if (iRoom.floor_id === 36) {
        var roomCoords = [];
        var roomRaw = JSON.parse(iRoom.polygons);
				
        for (var k = 0; k < roomRaw.length; k++) {
        	var roomArray = roomRaw[k];
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
    }
    console.log(areaArray);

    // make the MAP to be drawn in
    var MAP = {
      name: 'my-map',
      areas: areaArray,
    };
		
    return (
      <BrowserRouter>

        <div className = "App">
          <div id = "header">
            <img id ="headerImg" src={Logo}/>
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
            <ImageMapper src={this.imagePath} map={MAP} fillColor="rgba(127,255,212,0.5)" width={1000} 
            onClick={(obj, num, event) => this.handleClick(obj, num, event)}/>
          </Center>
        </div>
				
      </BrowserRouter>
      );
  }
}

export default () => (
  <App/>
);