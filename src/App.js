import React, { Component } from 'react';
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faSearch from '@fortawesome/fontawesome-free-solid/faSearch'
import Center from 'react-center';
import Wendell from './wendell2.jpg';
import Logo from './raw.jpg';
import './App.css';
import {
  BrowserRouter,
} from 'react-router-dom';
import FloorPlan from './Components/FloorPlan';

// Manages the main logic of the page
class App extends Component {
	
  constructor(props) {
    super(props);
		
    this.state = {
			rooms: [], // Contains all rooms returned by getQuery()
		};
		this.roomid = 0;		// Room-ID, Changed on Click
		this.roomidFloorList = []; // Keep track of which roomID the floor is

		this.floor = 0;	// Floor-ID for the Rooms
		this.floorList = []; // Holds onto a list of all the floors in a building
		this.floorButtonClicked = 0; // determine whether a specific floor button is clicked

		this.searchLink = ""; // A string to hold the query searched
		
		// List of all the rooms that can be displayed, used for ImageMapper
		this.roomIDRendered = [];
		
		// Default image path is set to Wendell, but changes on click
		this.imagePath = Wendell;

		// Bindings
		this.getQuery = this.getQuery.bind(this);
		this.getFloorplan = this.getFloorplan.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	// Makes an API call to return all rooms associated with the building
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
        // Update the room image pathing, if query
		if (Array.isArray(data) && data.length) {
			// for now, default to the first floor
			if (!this.floorButtonClicked) {
				this.floor = data[0].level;
				this.roomid = data[0].room_id;
			}
			this.getFloorplan();

	        console.log("New Rooms", this.state.rooms);

	        this.floorList = [];
	        this.roomidFloorList = [];
	        var currFloorID = -1;
	        // handle the number of floors there are
	        for (var i = 0; i < data.length; i++) {
	        	var entry = data[i];
	        	if (currFloorID !== entry.level) {
	        		// get the level
	        		this.floorList.push(entry.level);
	        		// get the room_id for that specific level
	        		this.roomidFloorList.push(entry.room_id);

	        		currFloorID = entry.level;
	        	}
	        }
	        console.log("All floors", this.floorList);
	        this.forceUpdate();
		}
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
				this.forceUpdate();
			})
			.catch(error => console.log(error));
	}

<<<<<<< HEAD
=======
	// Handles the click for the Polygons in the ImageMapper
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

	// Handles the changing of the floors
	changeFloor = (event, listValue) => {
		var activeFloor = event.target.id;
		console.log("Just clicked floor " + event.target.id);
		var index = -1;
		// get the index to get the correct room_id index
		for (var i = 0; i < this.floorList.length; i++) {
			if (activeFloor === this.floorList[i])
				index = i;
		}

		this.roomid = this.roomidFloorList[index];
		this.floor = activeFloor;
		this.floorButtonClicked = 1;
		this.getQuery();
	}

>>>>>>> 083ead23f5d2ed72eadf9e573e70560520770297
	// Handles the form submission by making a call to the API
	handleSubmit(event) {
		event.preventDefault();
		const data = new FormData(event.target);
		const searchData = data.get('search');
	
		/* ADD ERROR PROCESSING... Finding Room that doesn't exist */		
		this.searchLink = searchData;
		this.floorButtonClicked = 0;
		this.getQuery();
	}

	render() {
<<<<<<< HEAD
=======
		// Process the JSON received from Back-End
		var retQuery = this.state.rooms;
		var areaArray = [];
		this.roomIDRendered = [];
		var ratio = 1000.0/2550.0;
		// Iterate through all rooms in the json file
		for (var i = 0; i < retQuery.length; i++) {
			var iRoom = retQuery[i];
			// Hard-Coded to only display those on one floor
			if (iRoom.level === this.floor) {
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
		// Diplays the array of polygons loaded for debugging purposes.
		console.log("Polygons", areaArray);

		// Make the MAP to be drawn in
		var MAP = {
			name: 'my-map',
			areas: areaArray,
		};
		
>>>>>>> 083ead23f5d2ed72eadf9e573e70560520770297
		return (
			<BrowserRouter>
				<div className = "App">
					<div id = "header">
						<img id ="headerImg" src={Logo} alt="R"/>
						<p>edraw</p>
					</div>
					<div id ="formBlock">
						<form onSubmit = {this.handleSubmit}>
							<input type="text"
								placeholder="Search Room..."
								name="search"/>
							<button 
								id="submitButton" 
								type="submit">
									<FontAwesomeIcon icon = {faSearch}/>
							</button>
						</form>
					</div>
<<<<<<< HEAD
					<Center>
						<FloorPlan
						 	rooms={this.state.rooms}
							jpg={this.imagePath}
						/>
					</Center>
=======

					<div id = "mainContent">
						<Center>
							<ImageMapper	
								src={this.imagePath} 
								map={MAP} 
								fillColor="rgba(50,153,255,0.5)"
								strokeColor="rgba(255, 255, 255, 0.9)"
								width={1000} 
								onClick={(obj, num, event) => this.handleClick(obj, num, event)}
							/>
						</Center>

						<ul id = "floorButtons">
							{this.floorList.map(listValue => 
								<li>
									<input id={listValue}
									value={"Floor " + parseInt(listValue, 10)} 
									type="button"
									onClick={(event) => this.changeFloor(event)}/>
								</li>
							)}
						</ul>
					</div>


					
>>>>>>> 083ead23f5d2ed72eadf9e573e70560520770297
				</div>
			</BrowserRouter>
		);
	}
}

export default () => (
	<App/>
);