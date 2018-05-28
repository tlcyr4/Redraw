import React from 'react';


// heart icons
import FaHeart from 'react-icons/lib/fa/heart';
import FaHeartO from 'react-icons/lib/fa/heart-o';


import { DiscreteColorLegend } from 'react-vis';

// Create a legend! (one time thing!)
const items = [
	{title: 'Rockefeller', color: '#97c574'},
	{title: 'Mathey', color: '#b3604d'},
	{title: 'Whitman', color: '#a9d6e3'},
	{title: 'Wilson', color: '#f7b164'},
	{title: 'Butler', color: '#5B8fbe'},
	{title: 'Forbes', color: '#f3766d'},
	{title: 'Upperclass', color: '#a4a2a0'}
];

function MapInfo(props) {
	return (
		<div id = "buildingInfo">
			<div id = "roomNotClicked">
				<h3>Click a Building!</h3>
			</div>
			<div id = "legendDiv">
				<DiscreteColorLegend
					height={props.window.innerHeight*0.35}
					width={props.window.innerWidth*0.1}
					items={items}
				/>
			</div>
		</div>
	)
}

function RoomInfo(props) {
	return (
	<div id="roomInfo">
		<div id="roomClicked">
			<h4>{props.room.building_name}</h4>
			<h5>{"Floor " + props.room.level}</h5>
			<button id="heartButton" onClick={()=>props.updateFavorites(props.room.room_id)}> 
				{
				(<div style={{color:'DeepPink'}}>
				{props.isFavorite ? <FaHeart size={30}/> : <FaHeartO size={30}/>}
				</div>)
				} 
			</button>
			<ul>
				<li class="roomContent"><p>{"Room Number: " + props.room.number}</p></li>
				<li class="roomContent"><p>{"Room Size: " + props.room.sqft + " sqft"}</p></li>
				<li class="roomContent"><p>{"Occupant Size: " + props.room.num_occupants}</p></li>
				<li class="roomContent"><p>{"Number of Rooms: " + props.room.num_rooms}</p></li>
				<li class="roomContent"><p>{"Draw Type: " + props.room.draws_in}</p></li>
				<li class="roomContent"><p>{"Sub Free: " + (props.room.sub_free ? "Yes" : "No")}</p></li>
			</ul>
		</div>
	</div>
	)
}

function DefaultInfo(props) {
	return (
		<div id="roomInfo">
			<div id="roomNotClicked">
				Click a Room!
			</div>
		</div>
	)
}
export {MapInfo, RoomInfo, DefaultInfo};