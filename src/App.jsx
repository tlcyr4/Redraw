// library imports
import React, { Component } from 'react';
import Center from 'react-center';
import ImageMapper from './ImageMapper';

// material imports

import { withStyles, } from 'material-ui/styles';


// Image Import
import HomeMap from './images/homeMap.png';

// Style import
import './styling/App.css';
import './styling/styles.css';

// Import relevant json files
import buildings from './json/buildings.json';
import name2Num from './json/name2num.json';

// local imports
import AboutPage from './About'
import FeedbackPage from './Feedback'
import {Search, SearchResults} from './Search'
import Favorites from './Favorites'
import Error from './Error'
import {MapInfo, RoomInfo, DefaultInfo} from './Info'
import Header from './Header'
import Loader from './Loader'
import CampusMap from './CampusMap'
import Floorplan from './Floorplan'


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

const pageEnum = {
	MAP		 : -2,
	FLOORPLAN: -1,
	ABOUT    :  0,
	FEEDBACK :  1,
	LOGOUT   :  2
}
export {pageEnum};

function BackToMap(props) {
	return (
		<li class="backToMap">
			<a href="/">
				<input 
					id={'H'}
					value="Back To Map"
					type="button"
				/>
			</a>
		</li>
	);
}



function FloorButtons(props) {
	return (
		<ul id="floorButtons">
			{!props.isMap && <BackToMap />}	
			{props.floorList.map(level => 
				<li>
					<input 
					  id={level}
					  value={'Floor ' + level} 
					  type="button"
					  onClick={(event) => props.changeFloor(event)}
					/>
				</li>
			)}
		</ul>
	);
}


function FloorLabel(props) {
	return (
		<div id="floorLabel">
			<p 
			  id="floorBuildingName" 
			  class=".centerLabel">
				{props.building}
			</p>
			<p 
			  id="floorNumberName" 
			  class=".centerLabel">
				{"Floor " + props.level}
			</p>
		</div>
	);
}


function getBuildingID(buildingName) {
	return name2Num[buildingName]
}
function getBuilding(buildingName) {
	return buildings[name2Num[buildingName]];
}

// Manages the main logic of the page
class App extends Component {
	
    constructor(props) {

		// cut off leading zeroes
		Object.values(buildings).map(b => {b['floors'] = b['floors'].map(f => f.slice(-1))});
        super(props);
		
		this.state = {
			search_results: [],  // All rooms returned by a specific query
			rooms_displayed: [], // The rooms which should be renderd over a floorplan
			loading: false, 	// for the loading wheel
			pageNum: -1, 			// decides which page is rendered
			building: '',
			floorList: [],
			floor: '',
			roomClicked: null,
			imagePath: HomeMap,
			favoritesList: [],
			roomIDRendered: [],
			areaArray: [],
			buildingIDRendered: [],
		};

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
		
		this.imageWidthScaled = window.innerWidth * 0.43;
		this.getFavorites();

		
	}

	// getPolygons: updates the rooms_displayed state variable.
	getPolygons(building, level = null, roomClickedID = null) {
		this.setState({
			pageNum: pageEnum.FLOORPLAN,
			loading: true
		});

		// Set default
		if (level === null)
			level = getBuilding(building)['floors'][0];
		
		this.getFloorplan(building, level);
		
		var ratio = this.imageWidthScaled / 2550.0 / 4;
		
		let url = '/api/search/?building=' + building;
	    fetch(url, {credentials: 'same-origin'})
	      .then(response => response.json())
	      .then(data => {
			let rooms_displayed = data.filter(room => room.level === level);

			var areaArray = [];
			var polygonIDs = [];
			
			rooms_displayed.forEach(room => {
				let polygons = JSON.parse(room.polygons);
				polygons.forEach(() => polygonIDs.push(room.room_id));

				polygons.forEach(polygon => {
					let occ = room.num_occupants;
					let coordsJoined = [].concat.apply([],polygon);
					let coords = coordsJoined.map(coord => coord * ratio);
					areaArray.push({
						_id: room.room_id, 
						shape: 'poly', 
						coords: coords, 
						tooltip: {
							name: 'Room '+ room.number, 
							moreInfo: occ + ' Resident' + (occ > 1 ? 's' : '')
						}
					})
				});
			})
			var roomClicked;
			if (roomClickedID !== null) {
				roomClicked = data.find(r => r.room_id === roomClickedID);
			}
			else {
				roomClicked = null;
			}

			let floors = getBuilding(building)['floors']
			this.setState({
				roomIDRendered 	:	polygonIDs,
				areaArray		:	areaArray,
				rooms_displayed	:	rooms_displayed,
				building		:	building,
				floorList		:	floors,
				floor			:	level,
				roomClicked		:	roomClicked,
				loading			:	false
			});
		})
		.catch(error => console.log(error));
	}


	// Returns a series of rooms based on a search query
	getQuery(query) {
		const url = '/api/search/?' + query;
		fetch(url, {credentials: 'same-origin'})
			.then(response => response.json())
			.then(data => 
				this.setState({
					search_results: data,
					loading: false,
				}))
			.catch(error => console.log(error));
  	}

	// getFloorplan: fetch a new floorplan filepath from Back-End.
	getFloorplan(buildingName, level) {
		let buildingID = getBuildingID(buildingName);
		let url = '/api/floorplan/?building=' + buildingID + '&level=' + level;
		
		fetch(url, {credentials: 'same-origin'})
			.then(response => response.blob())
			.then(data => this.setState({imagePath:URL.createObjectURL(data)}))
			.catch(error => console.log(error));
	}

	// On-Click Event, fetch a new floorplan filepath from Back-End.
	handleFloorplanSwitch = (event) => {
		let buildingName = event.target.getAttribute('bldg');
		let level = event.target.getAttribute('level');
		let roomID = parseInt(event.target.id, 10);
		
		this.getPolygons(buildingName, level, roomID);
	}

	// update the favorites list
	updateFavorites(roomID) {
		const url = '/api/favorites/?room_id=' + roomID;
		fetch(url, {credentials: 'same-origin'})
			.then(response => response.json())
			.then(faveData => this.setState({favoritesList : faveData}))
			.catch(error => console.log(error));
	}

	// Just retrieve favorites from backend
	getFavorites() {this.updateFavorites(0)}

	// Handles the click for the Polygons in the ImageMapper
	handleClick = (obj, num, event) => {
		let roomsDisplayed = this.state.rooms_displayed;
		let roomID = this.state.roomIDRendered[num];
		let room = roomsDisplayed.find(r => r.room_id === roomID);
		this.setState({roomClicked : room})
	}

	// Handles the changing of the floors
	changeFloor = (event) => {
		let level = event.target.id;
		let buildingName = this.state.building;
		this.getPolygons(buildingName, level, null);
	}

	// Handles the form submission by making a call to the API
	formSubmit = async values => {
		let pairs = Object.entries(values);
		let queries = pairs.map(pair => pair.join('='));
		this.getQuery(queries.join('&'));
	}
	
	/* validate: process the values returned when a form is submitted.
			If something is invalid, then return an error array. */
	formValidate = (values) => {
		var errArray = {};
		if (values.building) {
			let buildingName = values.building;
			if (buildingName.length > 30) {
				errArray.building = 'Name is too long';
			}
			else if (!name2Num.hasOwnProperty(buildingName)) {
				errArray.building = 'Does not exist';
			}
		}
	  return errArray;
	}
	
	// handle change of page!
	handlePage = (event, value) => {
		this.setState({ pageNum: value });
	};

/*====================================================================*/

	render() {
		const { classes } = this.props;
		const { value } = this.state;

		
		
		var imageWidthScaled = this.imageWidthScaled;
		var ratio = imageWidthScaled/2550.0;
		var content;
		

		if (this.state.pageNum === pageEnum.ABOUT) {
			content = <AboutPage />
		}
		else if (this.state.pageNum === pageEnum.FEEDBACK) {
			content = <FeedbackPage />
		}
		else if (this.state.pageNum === pageEnum.LOGOUT) {
			content = <div></div>;
			window.location.replace('/accounts/logout');
		}
		else if (this.state.pageNum === pageEnum.FLOORPLAN) {
			var isMap = this.state.imagePath === HomeMap;		
			

			var info = <DefaultInfo />;
			
			// overwrite for cases when home screen
			if (isMap) {
				info = <MapInfo window={window} />
			}

			// if the room is clicked, then display the information
			if (this.state.roomClicked !== null) {
				let roomID = this.state.roomClicked.room_id;
				let favorites = this.state.favoritesList;
				let isFavorite = favorites.some(r => r.room_id === roomID);
				info = (
					<RoomInfo 
					  room={this.state.roomClicked} 
					  updateFavorites={this.updateFavorites}
					  isFavorite={isFavorite}
					/>
				);
			}
		var searchBar = (
			<Search 
			  formSubmit={this.formSubmit} 
			  formValidate={this.formValidate}
			/>
		);
		var leftPanel = (
			<div id="leftContent">
				<Favorites 
				  handleFloorplanSwitch={this.handleFloorplanSwitch} 
				  favoritesList={this.state.favoritesList}
				/>
				<SearchResults 
				  results={this.state.search_results} 
				  handleFloorplanSwitch={this.handleFloorplanSwitch}
				/>
			</div>
		);
		var centerImage;
		if(isMap) {
			centerImage = <CampusMap getPolygons={this.getPolygons} />;
		}
		else {
			centerImage = 
				<Floorplan 
				  areaArray={this.state.areaArray} 
				  imagePath={this.state.imagePath}
				  handleClick={this.handleClick}
				/>;
		}
		var rightContent = (
			<div id="rightContent">
				{(!isMap &&
					<FloorLabel 
						building={this.state.building} 
						level={this.state.floor}
					/>
				)}
				<FloorButtons 
					isMap={this.state.imagePath === HomeMap}
					floorList={this.state.floorList}
					changeFloor={this.changeFloor}
				/>
				
				{info}
			</div>
		)
		/*================================================================*/
		/* The Content Block                                              */
		/*================================================================*/
		content = (
				<div>
					{searchBar}
					{leftPanel}
					{centerImage}
					{rightContent}	
					<Loader loading={this.state.loading}/>
				</div>
			);
		}
		else {
			content = <Error window={window} />;
		}
		
		
		// return with the known header and different content, as needed
		return (
			<div className="App" id="AppBackground">
				<Header 
				  handlePage={this.handlePage} 
				  classes={this.props} 
				  value={this.state}
				/>
				{content}
			</div>
		);
	}
}

export default withStyles(materialStyle)(App);
