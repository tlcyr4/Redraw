// library imports
import React, { Component } from 'react';
import FontAwesomeIcon from '@fortawesome/react-fontawesome';
import faSearch from '@fortawesome/fontawesome-free-solid/faSearch';
import faBed from '@fortawesome/fontawesome-free-solid/faBed';
import Center from 'react-center';
import { DiscreteColorLegend } from 'react-vis';
import { RingLoader } from 'react-spinners';
import ImageMapper from './ImageMapper';

// material imports
import Tabs, { Tab } from 'material-ui/Tabs';
// Expansion panel section
import ExpansionPanel, {
	ExpansionPanelSummary,
	ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from 'material-ui/Typography';
import { withStyles, } from 'material-ui/styles';

// heart icons
import FaHeart from 'react-icons/lib/fa/heart';
import FaHeartO from 'react-icons/lib/fa/heart-o';

// Imports for AutoSuggestion
import buildings from './buildings';
import DownshiftInput from './Downshift';
import { Form, Field } from 'react-final-form';

// Image Import
import HomeMap from './images/homeMap.png';
import Logo from './images/raw.jpg';
import BrokenDoor from './images/404Door.png';

// Team profile picture import
import DChae from './images/squadpic/DC.png';
import Tigar from './images/squadpic/Tigar.png';
import Kesin from './images/squadpic/Kesin.png';
import ChooChoo from './images/squadpic/Chuchu.png';

// Style import
import './styling/App.css';
import './styling/styles.css';

// Import relevant json files
import BuildingCoordData from './json/building_polygons.json';
import BuildingQueryName from './json/buildings.json';

/*===========================================================================*/
/* Change up the styling!                                                    */
/*===========================================================================*/
const materialStyle = theme => ({
	// a root styling
	root: {
	    flexGrow: 1,
	    width: '100%',
	    backgroundColor: theme.palette.background.paper,
	},

	expansionSlot: {
		height: window.innerHeight*0.3,
	},

	expPanel: {
		margin: '0',
	},

	headerLabels: {
		fontSize: '16'
	}
});

/*===========================================================================*/
/*===========================================================================*/
/*===========================================================================*/

// Manages the main logic of the page
class App extends Component {
	
  constructor(props) {
    super(props);
		
    this.state = {
			search_results: [],  // All rooms returned by a specific query
			rooms_displayed: [], // The rooms which should be renderd over a floorplan
			favorites: [], 
			loading: false, 	// for the loading wheel
			pageNum: -1, 			// decides which page is loaded
		};
		
		this.roomid = 0;		// Room-ID representing the floor
		this.roomidFloorList = []; // Keep track of which roomID the floor is
		
		this.floorNameLabel = (<p></p>);
		this.floor = 0;	// Floor-ID for the Rooms
		this.floorList = []; // Holds onto a list of all the floors in a building
		this.floorListB2M = []; // Just holds HOME button!
		this.floorButtonClicked = 0; // determine whether a specific floor button is clicked

		this.searchLink = ""; // A string to hold the query searched
		this.building = "";
		
		// List of all the rooms that can be displayed, used for ImageMapper
		this.roomIDRendered = [];

		// List of all the buildings that are clickable, used for ImageMapper
		this.buildingIDRendered = [];
		this.buildingPolygons = [];
		this.start = 0; // check startup
		
		// Default Background Image is a Campus Map
		this.imagePath = HomeMap;

		// Holds of all the information of the room!
		this.roomClicked = -1;
		this.currRoom = [];	

		this.favoritesList = []; // favorites
		this.loadFavorites = 0; // load the favorites when you open up the website

		this.searchSwitch = 0; // this would allow us to make suren ot to reset roomClicked in getPolygons

		// Create a legend! (one time thing!)
		this.items = [
			{title: 'Rockefeller', color: '#97c574'},
			{title: 'Mathey', color: '#b3604d'},
			{title: 'Whitman', color: '#a9d6e3'},
			{title: 'Wilson', color: '#f7b164'},
			{title: 'Butler', color: '#5B8fbe'},
			{title: 'Forbes', color: '#f3766d'},
			{title: 'Upperclass', color: '#a4a2a0'}
		];

		// Methods that begin with 'get' make calls to API
		this.getQuery = this.getQuery.bind(this);
		this.getPolygons = this.getPolygons.bind(this);
		this.getFloorplan = this.getFloorplan.bind(this);
		
		// Methods related to favorites
		this.updateFavorites = this.updateFavorites.bind(this);
		this.getFavorites = this.getFavorites.bind(this);
		
		// Methods that are related to user search
		this.formSubmit = this.formSubmit.bind(this);
		this.formValidate = this.formValidate.bind(this);
		
		this.processBuildingJSON = this.processBuildingJSON.bind(this);
	}

	// getPolygons: updates the rooms_displayed state variable.
	getPolygons() {
		const url = '/api/search/?building=' + this.building;

	    fetch(url, {credentials: "same-origin"})
	      .then(response => {
	        return response.json();
	      })
	      .then(data => {
	        this.setState({
	          rooms_displayed: data,
	          loading: true,
	        });
	        	this.forceUpdate();
				if (Array.isArray(data) && data.length) {
					this.roomClicked = -1;
					// Default to the first floor
					if (!this.floorButtonClicked) {
						var alphabet = parseInt([0].level, 10);
						if (isNaN(alphabet))
							this.floor = data[0].level;
						else
							this.floor = alphabet;
						this.roomid = data[0].room_id;
					}
					this.getFloorplan(this.roomid);
					
					this.floorList = [];
					this.roomidFloorList = [];
					this.floorListB2M = [];
					var currFloorID = -1;
					
					// Handle the number of floors there are
					for (var i = 0; i < data.length; i++) {
						var entry = data[i];
						if (currFloorID !== entry.level) {
							var alphabet2 = parseInt(entry.level, 10);
							if (isNaN(alphabet2))
								this.floorList.push(entry.level);
							else
								this.floorList.push(alphabet2);

							// get the room_id for that specific level
							this.roomidFloorList.push(entry.room_id);
							currFloorID = entry.level;
						}
					}
					this.floorListB2M.push("H");
					this.floorNameLabel = (
						<div id="floorLabel">
							<p id="floorBuildingName" class=".centerLabel">{this.building}</p>
							<p id="floorNumberName" class=".centerLabel">{"Floor " + this.floor}</p>
						</div>
					);
					this.forceUpdate();
				}
				this.state.loading = false;
			})
		.catch(error => console.log(error));
	}

	// Returns a series of rooms based on a search query
	getQuery() {
    const url = '/api/search/?' + this.searchLink;

    fetch(url, {credentials: "same-origin"})
      .then(response => {
        return response.json();
      })
      .then(data => {
        this.setState({
          search_results: data,
          loading: false,
        });
      })
      .catch(error => console.log(error));
  	}

	// getFloorplan: fetch a new floorplan filepath from Back-End.
	getFloorplan(roomID) {
		const url = '/api/floorplan/?room_id=' + roomID;
		
		fetch(url, {credentials: 'same-origin'})
			.then((response) => { return response.blob(); })
			.then((data) => {
				var objectURL = URL.createObjectURL(data);
				this.imagePath = objectURL;
				this.forceUpdate();
			})
			.catch(error => console.log(error));
	}

	// On-Click Event, fetch a new floorplan filepath from Back-End.
	handleFloorplanSwitch = (event) => {
		/* We need to check if this is necessary or not */
		const url = '/api/floorplan/?room_id=' + event.target.id;
		
		this.building = event.target.getAttribute('bldg');
		this.roomid = event.target.id;
		this.roomClicked = event.target.id;
		this.floorButtonClicked = 1;
		
		// alphabet capitalizing
		var alphabet = parseInt(event.target.getAttribute('floor'), 10);
		if (isNaN(alphabet))
			this.floor = event.target.getAttribute('floor');
		else
			this.floor = alphabet;
		
		this.state.loading = true;
		this.forceUpdate()
		// fetch data
		fetch(url, {credentials: 'same-origin'})
			.then((response) => { return response.blob(); })
			.then((data) => {
				var objectURL = URL.createObjectURL(data);
				this.imagePath = objectURL;
				
				const url = '/api/search/?building=' + this.building;
			    fetch(url, {credentials: "same-origin"})
			      .then(res => {
			        return res.json();
			      })
			      .then(data2 => {
				        this.setState({
				          rooms_displayed: data2,
				          loading: true,
				        });
						if (Array.isArray(data2) && data2.length) {
							
							this.getFloorplan(this.roomid);
							
							this.floorList = [];
							this.roomidFloorList = [];
							this.floorListB2M = [];
							var currFloorID = -1;
							
							// Handle the number of floors there are
							for (var i = 0; i < data2.length; i++) {
								var entry = data2[i];
								if (currFloorID !== entry.level) {
									var alphabet2 = parseInt(entry.level, 10);
									if (isNaN(alphabet2))
										this.floorList.push(entry.level);
									else
										this.floorList.push(alphabet2);
											
									// get the room_id for that specific level
									this.roomidFloorList.push(entry.room_id);
									currFloorID = entry.level;
								}
							}
							this.floorListB2M.push("H");
							this.floorNameLabel = (
								<div id="floorLabel">
									<p id="floorBuildingName" class=".centerLabel">{this.building}</p>
									<p id="floorNumberName" class=".centerLabel">{"Floor " + this.floor}</p>
								</div>
							);
							this.forceUpdate();
						}
						var query = data2;
				    for (var i = 0; i < query.length; i++) {
				      var iRoom = query[i];
				      // make sure there is a match
				      if (iRoom.room_id == this.roomid) {
								
				      	// update the room info
				      	this.roomClicked = iRoom.room_id;
				      	var checkAlpha = parseInt(iRoom.level, 10);
				      	if (isNaN(checkAlpha))
				      		this.currRoom.floor = iRoom.level;
				      	else
				      		this.currRoom.floor = checkAlpha;
									
				      	this.currRoom.roomNum = iRoom.number;
								
				      	// make sure that the entry is not undefined
				      	if (iRoom.num_rooms === null) { this.currRoom.num_rooms = iRoom.num_occupants; }
				      	else { this.currRoom.num_rooms = iRoom.num_rooms; }
									
				      	this.currRoom.num_occupants = iRoom.num_occupants;
				      	this.currRoom.sqft = iRoom.sqft;
				      	this.currRoom.drawType = iRoom.draws_in.toLowerCase();
				      	this.currRoom.drawType = this.currRoom.drawType.charAt(0).toUpperCase() 
				      		+ this.currRoom.drawType.slice(1);
				      	this.state.loading = false;
				      	this.forceUpdate();
				        break;
				      }
						}
					})
					.catch(error => console.log(error));
			})
			.catch(error => console.log(error));
	}

	// update the favorites list
	updateFavorites() {
		const url = '/api/favorites/?room_id='+this.roomClicked; 
		fetch(url, {credentials: 'same-origin'})
				.then(response => {
					return response.json();
				})
				.then((data) => {
					this.getFavorites();
				})
				.catch(error => console.log(error));
	}

	// get the favorites from the server so we can preserve the order
	getFavorites() {
		const url = '/api/favorites/?room_id=0'; 

		fetch(url, {credentials: 'same-origin'})
			.then(response => {
					return response.json();
				})
			.then((faveData) => {
				this.state.loading = true;
				this.favoritesList = [];
				if (Array.isArray(faveData) && faveData.length) {
					for (var i = 0; i < faveData.length; i++) {
						var entry = faveData[i];
						this.favoritesList.push({
							level: entry.level,
							buildingName: entry.building_name,
							RoomNum: entry.number, 
							RoomID: entry.room_id
						});
					}
				}
				this.state.loading = false;
				// force update so that we can update buttons
				if (this.loadFavorites > 0) {
					this.forceUpdate();
				}
				if (this.loadFavorites === 0) {
					this.loadFavorites = 1;
				}
			})  
			.catch(error => console.log(error));
	}
	
	handleExpansion = () => { this.forceUpdate(); }
	
	// when the favorites button is clicked, handle the case
	handleFavoritesClick = (obj, num, event) => {
		this.updateFavorites();
		this.forceUpdate();
	}

	// Handles the click for the Polygons in the ImageMapper
	handleClick = (obj, num, event) => {
		if (this.imagePath === HomeMap) {
			var buildingQ = this.buildingIDRendered[num].id;
			this.building = BuildingQueryName[buildingQ].name;
			this.getPolygons();
		}
		else {
		    var query = this.state.rooms_displayed;
		    for (var i = 0; i < query.length; i++) {
		      var iRoom = query[i];
		      // print how many sqft the room is on the console
		      if (iRoom.room_id == this.roomIDRendered[num]) {
		      	// update the room info
		      	this.roomClicked = iRoom.room_id;
		      	var checkAlpha = parseInt(iRoom.level, 10);
		      	if (isNaN(checkAlpha))
		      		this.currRoom.floor = iRoom.level;
		      	else
		      		this.currRoom.floor = checkAlpha;
							
		      	this.currRoom.roomNum = iRoom.number;
						
		      	// make sure that the entry is not undefined
		      	if (iRoom.num_rooms === null) { this.currRoom.num_rooms = iRoom.num_occupants; }
		      	else { this.currRoom.num_rooms = iRoom.num_rooms; }
							
		      	this.currRoom.num_occupants = iRoom.num_occupants;
		      	this.currRoom.sqft = iRoom.sqft;
		      	this.currRoom.drawType = iRoom.draws_in.toLowerCase();
		      	this.currRoom.drawType = this.currRoom.drawType.charAt(0).toUpperCase() 
		      		+ this.currRoom.drawType.slice(1);
		      	this.forceUpdate();
		        break;
		      }
		    }
	    }
	}

	// Handles the changing of the floors
	changeFloor = (event) => {
		var activeFloor = event.target.id;
		var index = -1;

		// get the index to get the correct room_id index
		for (var i = 0; i < this.floorList.length; i++) {
			if (activeFloor == this.floorList[i])
				index = i;
		}

		this.roomid = this.roomidFloorList[index];
		this.floor = activeFloor;
		this.floorButtonClicked = 1;
		this.roomClicked = -1;
		this.getPolygons();
	}

	// Handles the form submission by making a call to the API
	formSubmit = async values => {
		var searchData = "";
		var numField = 0;
		Object.keys(values).map( function(key, index) {
				if (values[key]) {
					if (numField > 0) { searchData += "&"; }
					searchData += (key + "=" + values[key]);
					numField++;
				}
		});	
		this.searchLink = searchData;
		this.floorButtonClicked = 0;
		this.searchSwitch = 1;
		this.getQuery();
	}
	
	/* validate: process the values returned when a form is submitted.
			If something is invalid, then return an error array. */
	formValidate = (values) => {
		const errArray = {};
	  if (values.building) {
			if (values.building.length > 30) { errArray.building = 'Name is too long'; }
			else {
				var valid = false;
				for (var i = 0; i < buildings.length; i++) {
					if (buildings[i]['value'] == values.building) { valid=true; break; }
				}
				if (!valid) { errArray.building = 'Does not exist' }
			}
		}
	  return errArray;
	}
	
	// handle change of page!
	handlePage = (event, value) => {
		this.setState({ pageNum: value });
	};

	// Process for The Start Screen
	processBuildingJSON() {
		const imageWidthScaled = window.innerWidth*0.43;
		var ratio = imageWidthScaled/1166.0;

		for (var i = 0; i < BuildingCoordData.length; i++) {
			var oneBuild = BuildingCoordData[i];
			var oneBuildPoly = oneBuild.geometry.coordinates;
			var buildingCoords = [];

			for (var j = 0; j < oneBuildPoly.length; j++) {
				var gpsCoor = oneBuildPoly[j];
				var buildX = parseInt(gpsCoor[0],10) * ratio;
				var buildY = parseInt(gpsCoor[1],10) * ratio;
				buildingCoords.push(buildX);
				buildingCoords.push(buildY);
			}
			this.buildingPolygons.push({
				_id: oneBuild.properties.id,
				shape: 'poly', 
				coords: buildingCoords, 
				tooltip: {name: oneBuild.properties.name, moreInfo: oneBuild.properties.type} 
			})
			// hold onto the order in which the buildings are added
			this.buildingIDRendered.push(oneBuild.properties);
		}
		this.start = 1;

		return imageWidthScaled;
	}

/*====================================================================*/

	render() {
		const { classes } = this.props;
		const { value } = this.state;

		if (this.loadFavorites === 0) {
			this.getFavorites(); 
		}

		/*=====================================================================*/
		/* Default to to error message, should theoretically never happen      */
		/*=====================================================================*/
		var content = (
				<div>
					<img id="brokenDoor" src={BrokenDoor} alt="404 Error" height={window.innerHeight*0.8}/>
					<div id="pageNotFound">
						<h1>Page Not Found</h1>
						<h2>Oh no!</h2>
						<p>Something went terribly wrong!</p>
						<p>Please navigate out of the page and report the issue.</p>
					</div>
				</div>
			);

		/*================================================================*/
		/* Change to the default mapping — main screen !                  */
		/*================================================================*/
		if (this.state.pageNum < 0) {		
			// Process the JSON received from Back-End
			var retQuery = this.state.rooms_displayed;
			var areaArray = [];
			this.roomIDRendered = [];
			var imageWidthScaled = window.innerWidth*0.6;
			var ratio = imageWidthScaled/2550.0;

			// Run Only Once
			if (this.start === 0) {
				imageWidthScaled = this.processBuildingJSON();
			}
			
			// Iterate through all rooms in the json file
			for (var i = 0; i < retQuery.length; i++) {
				var iRoom = retQuery[i];
				
				// Hard-Coded to only display those on one floor
				var temp = parseInt(iRoom.level, 10);
				if (isNaN(temp))
					temp = iRoom.level;

				if (temp == this.floor) {
					var roomRaw = JSON.parse(iRoom.polygons);
					
					for (var k = 0; k < roomRaw.length; k++) {
						var roomCoords = [];
						var roomArray = roomRaw[k];
						
						for (var j = 0; j < roomArray.length; j++) {
							roomCoords.push(parseInt(parseInt(roomArray[j][0], 10)/4*ratio, 10));
							roomCoords.push(parseInt(parseInt(roomArray[j][1], 10)/4*ratio, 10));
						}

						var residentPlurality = " Residents";
						if (iRoom.num_occupants === 1)
							residentPlurality = " Resident";

						areaArray.push({ 
							_id: iRoom.room_id, 
							shape: 'poly', 
							coords: roomCoords, 
							tooltip: {name: "Room "+ iRoom.number, moreInfo: iRoom.num_occupants + residentPlurality}
						});
						// hold onto the order of the polygons wrt to the rooms
						// useful for when handling click
						this.roomIDRendered.push(iRoom.room_id);
					}
				}
			}

			// Make the MAP to be drawn over the floor plans.
			var MAP = {
				name: 'my-map',
				areas: areaArray,
			};
			var fillColor = "rgba(255, 165, 0, 0.7)";
			var borderColor = "rgba(255, 255, 255, 0)";

			var info = (
					<div id="roomInfo">
						<div id="roomNotClicked">
							Click a Room!
						</div>
					</div>
				);
			
			// overwrite for cases when home screen
			if (this.imagePath === HomeMap) {
				// map of polygons
				MAP = {
					name: 'my-map',
					areas: this.buildingPolygons,
				};
				fillColor = "rgba(255, 0, 255, 0.85)";
				borderColor = "rgba(200,200,250, 1)";

				// bottom right
				info = (
					<div id = "buildingInfo">
						<div id = "roomNotClicked">
							<h3>Click a Building!</h3>
						</div>
						<div id = "legendDiv">
							<DiscreteColorLegend
							    height={window.innerHeight*0.35}
							    width={window.innerWidth*0.1}
							    items={this.items}
							/>
						</div>
					</div>
				);
			}

			// if the room is clicked, then display the information
			if (parseInt(this.roomClicked, 10) >= 0) {
				var subFree = "No";
				if (this.currRoom.sub_free)
					subFree = "Yes";

				// change the icon if it is favorited 
				var heartIcon = (<div style={{color: 'DeepPink'}}><FaHeartO size={30} /></div>);
				for (var l = 0; l < this.favoritesList.length; l++) {
					if(this.roomClicked == this.favoritesList[l].RoomID) {
						heartIcon = (<div style={{color: 'DeepPink'}}><FaHeart size={30} /></div>);
					    break; 
					}
				}
				info = (
					<div id="roomInfo">
						<div id="roomClicked">
							<h4>{this.building}</h4>
							<h5>{"Floor " + this.currRoom.floor}</h5>
							<button id="heartButton" onClick={(obj, num, event)=>this.handleFavoritesClick(obj, num, event)}> 
								{heartIcon} 
							</button>
							<ul>
								<li class="roomContent"><p>{"Room Number: " + this.currRoom.roomNum}</p></li>
								<li class="roomContent"><p>{"Room Size: " + this.currRoom.sqft + " sqft"}</p></li>
								<li class="roomContent"><p>{"Occupant Size: " + this.currRoom.num_occupants}</p></li>
								<li class="roomContent"><p>{"Number of Rooms: " + this.currRoom.num_rooms}</p></li>
								<li class="roomContent"><p>{"Draw Type: " + this.currRoom.drawType}</p></li>
								<li class="roomContent"><p>{"Sub Free: " + subFree}</p></li>
							</ul>
						</div>
					</div>
				);
			}

			// for displaying the search results, as needed
			var resultsContent = (<div></div>);
			if (this.searchSwitch > 0) {
				resultsContent = (
					<div>
						<ul id="roomSearchButtons">
							{this.state.search_results.map( r => 
								<li>
									<input 
										id={r['room_id']}
										bldg={r['building_name']}
										floor={r['level']}
										type="button"
										value={r['building_name'] + " " + r['number']}
										onClick={ (e) => this.handleFloorplanSwitch(e) }
									/>
								</li>
								)}
						</ul>
						<p>{this.state.search_results.length + " Results Found"}</p>
					</div>);
			}
		/*================================================================*/
		/* The Content Block                                              */
		/*================================================================*/
		content = (
				<div>
					<div id="formBlock">
						<Form
							onSubmit={this.formSubmit}
							validate={this.formValidate}
							render={({ handleSubmit, pristine, submitting, values }) => (
								<form id="searchForm" onSubmit={handleSubmit}>
									<div id="buildingNameLabel">
										<label>Building Name</label>
									</div>
									<div id="buildingNameSearch">
										<Field
											name="building"
											items={buildings}
											component={DownshiftInput}
											placeholder="Search for Building..."
										/>
									</div>
									<div id="floorSearch">
										<label>Floor</label>
										<Field name="level" component="select" placeholder="#">
											<option />
											<option value="A">A</option>
											<option value="00">0</option>
											<option value="01">1</option>
											<option value="02">2</option>
											<option value="03">3</option>
											<option value="04">4</option>
											<option value="05">5</option>
										</Field>
									</div>
									<div id="drawLabel">
										<label>Draw Section</label>
									</div>
									<div id="drawSearch">
										<Field name="draws_in_id" component="select">
											<option />
											<option value="1">Butler</option>
											<option value="2">Forbes</option>
											<option value="3">Independent</option>
											<option value="4">Mathey</option>
											<option value="5">Rockefeller</option>
											<option value="6">Upperclass</option>
											<option value="7">Whitman</option>
											<option value="8">Wilson</option>
										</Field>
									</div>
									<div id="sizeSearch">
										<label>Minimum Size</label>
										<Field
											name="sqft__gte"
											component="input"
											type="number"
											min="0" 
											max="1150"
											placeholder="###"
										/>
									</div>
									<div id="divSubmitButton" className="buttons">
										<button
											id="submitButton" 
											type="submit"
											disabled={submitting || pristine}>
												<FontAwesomeIcon icon = {faSearch}/>
										</button>
									</div>
								</form>
							)}
						/>
					</div>
					
					<div id="leftContent">
						<ExpansionPanel onClick={this.handleExpansion} className = "expPanel">
									<ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
											<Typography variant="subheading">Favorites</Typography>
									</ExpansionPanelSummary>
									<ul id="favoriteButtons">
										{this.favoritesList.map((room, index)=>(
											<li>
											<ExpansionPanelDetails>
												<input
													id={room.RoomID}
													floor={room.level}
													bldg={room.buildingName}
													onClick={ (e) => this.handleFloorplanSwitch(e) }
													type="button"
													value = {room.buildingName + " " + room.RoomNum}/> 
											</ExpansionPanelDetails>
											</li>
										))}
									</ul>
						</ExpansionPanel>
						{resultsContent}
					</div>
					
					<div id="centerContent">
						<Center>
							<ImageMapper
								src={this.imagePath} 
								map={MAP} 
								fillColor={fillColor}
								strokeColor={borderColor}
								width={imageWidthScaled}
								onClick={(obj, num, event) => this.handleClick(obj, num, event)}
								lineWidth='3'
							/>
						</Center>
					</div>

					<div id="rightContent">
						{this.floorNameLabel}
						<ul id="floorButtons">
							{this.floorListB2M.map(listValue =>
								<li class="backToMap">
									<a href="/">
									<input id={listValue}
									value="Back To Map"
									type="button"/></a>
								</li>
							)}
							{this.floorList.map(listValue => 
								<li>
									<input 
										id={listValue}
										value={"Floor " + listValue} 
										type="button"
										onClick={(event) => this.changeFloor(event)}
									/>
								</li>
							)}
						</ul>
						{info}
					</div>

					<div id="loading">
						<RingLoader
							color={'#ffa500'} 
							loading={this.state.loading} 
						/>
					</div>
				</div>
			);
		}
		/*================================================================*/
		/* The About Page                                                 */
		/*================================================================*/
		else if (this.state.pageNum === 0) {
			content = (
					<div id = "aboutDiv">
						<div id = "aboutInfoDiv">
							<h1 id="aboutHeader">Room Draw Made Easy</h1>
							<p class="aboutInfo">
								Interact directly with rooms and buildings to find rooms on campus. 
								We emphasize simplicity and clean visualizations to help you find the perfect room for you.
							</p>
							<p class ="aboutInfo">
								Redraw is a final project for COS 333: Advanced Programming Techniques, 
								taught by Professor Brian Kernighan in Spring 2018. The team is advised by Jérémie Lumbroso. 
								Special acknowledgement for all who have helped us along the way.
							</p>
						</div>

						<div id = "squadImages">
							<h1 id = "aboutSquad">Meet The Team</h1>
							<div id = "TC" class = "squad">
								<div class = "squadInfoB">
									<img src = {Tigar} class = "picSquad" alt="Tigar"/>
									<p class = "nameBigger">Tigar Cyr</p>
									<p class = "basicFont">Backend Developer & Team Manager</p>
									<p class = "majorItalics">Computer Science BSE</p>
									<p class = "basicFont">Class of 2020</p>
								</div>
							</div>
							<div id = "DC" class = "squad">
								<div class = "squadInfoO">
									<img src = {DChae} class = "picSquad" alt="DChae"/>
									<p class = "nameBigger">Daniel Chae</p>
									<p class = "basicFont">Full Stack Developer</p>
									<p class = "majorItalics">Computer Science BSE</p>
									<p class = "basicFont">Class of 2020</p>
								</div>
							</div>
							<div id = "KD" class = "squad">
								<div class = "squadInfoB">
									<img src = {Kesin} class = "picSquad" alt="Kesin"/>
									<p class = "nameBigger">Kesin Ryan Dehejia</p>
									<p class = "basicFont">Frontend Developer</p>
									<p class = "majorItalics">Computer Science BSE</p>
									<p class = "basicFont">Class of 2020</p>
								</div>
							</div>
							<div id = "CC" class = "squad">
								<div class = "squadInfoO">
									<img src = {ChooChoo} class = "picSquad" alt="ChuChu"/>
									<p class = "nameBigger">Chris Chu</p>
									<p class = "basicFont">Frontend Developer</p>
									<p class = "majorItalics">Civil and Environmental Engineering</p>
									<p class = "basicFont">Class of 2019</p>
								</div>
							</div>
						</div>
					</div>
				);
		}
		else if (this.state.pageNum === 1) {
			// has the same styling as the content in About page, therefore reusing the id names
			content = (
				<div id = "aboutDiv">
					<div id = "aboutInfoDiv">
						<h1 id = "aboutHeader">Feedback</h1>
						<p class = "aboutInfo">
							We value any feedback you give to us, as we are always trying to improve.
						</p>
						<p class = "aboutInfo">
							Please send an email to <a href="mailto:tcyr@princeton.edu">the team</a> with your feedback and we will 
							be sure to get back to you, as needed!
						</p>
						<p class = "aboutInfo">
							Or take <a href="https://goo.gl/forms/2dHxJSRLhcgi2wjM2">this survey</a> to give us an evaluation of the site!
							 We take your input very seriously and are always striving to improve the site.
						</p>
						<p class = "aboutInfo">
							Thank you!
						</p>
						<p class = "aboutInfo">
							~ Redraw Team
						</p>

					</div>
				</div>
			);
		}
		else if (this.state.pageNum === 2) {
			content = (
					<div></div>
				);
			window.location.replace("/accounts/logout");
		}
		
		// return with the known header and different content, as needed
		return (
				<div className="App" id="AppBackground">
					
					<div id="header">
						<a href="/"><img id ="headerImg" src={Logo} alt="Logo"/><p>edraw</p></a>

						<div id = "tabs">
							<Tabs value={value} onChange={this.handlePage} scrollable scrollButtons="off" indicatorColor="primary">
								<Tab label = "About" className={classes.headerLabels}/>
								<Tab label = "Feedback" className={classes.headerLabels}/>
								<Tab label = "Logout" className={classes.headerLabels}/>
							</Tabs>
						</div>
					</div>
				
				{content}
				
			</div>
		);
	}
}

export default withStyles(materialStyle)(App);
