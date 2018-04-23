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
		this.floor_id = 0;	// Floor-ID for the Rooms
		this.floorList = []; // Holds onto a list of all the floors in a building
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
			this.roomid = data[0].room_id;
			this.getFloorplan();
			this.floor_id = data[0].floor_id;
	        console.log("New Rooms", this.state.rooms);

	        this.floorList = [];
	        var currFloorID = -1;
	        // handle the number of floors there are
	        for (var i = 0; i < data.length; i++) {
	        	var entry = data[i];
	        	if (currFloorID !== entry.floor_id) {
	        		this.floorList.push(entry.level);
	        		currFloorID = entry.floor_id;
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

	// Handles the form submission by making a call to the API
	handleSubmit(event) {
		event.preventDefault();
		const data = new FormData(event.target);
		const searchData = data.get('search');
	
		/* ADD ERROR PROCESSING... Finding Room that doesn't exist */		
		this.searchLink = searchData;
		this.getQuery();
	}

	render() {
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
					<Center>
						<FloorPlan
						 	rooms={this.state.rooms}
							jpg={this.imagePath}
						/>
					</Center>
				</div>
			</BrowserRouter>
		);
	}
}

export default () => (
	<App/>
);