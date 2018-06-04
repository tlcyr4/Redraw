import React from 'react';

import IoAndroidExpand from 'react-icons/lib/io/android-expand';
import IoMan from 'react-icons/lib/io/man';


// heart icons
import FaHeart from 'react-icons/lib/fa/heart';
import FaHeartO from 'react-icons/lib/fa/heart-o';

import ButlerCrest from './images/crests/butler.png'
import ForbesCrest from './images/crests/forbes.png'
import MatheyCrest from './images/crests/mathey.png'
import RockyCrest from './images/crests/rocky.png'
import PrincetonCrest from './images/crests/princeton.png'
import WhitmanCrest from './images/crests/whitman.png'
import WilsonCrest from './images/crests/wilson.png'

// Import relevant json files
import buildings from './json/buildings.json';
import name2Num from './json/name2num.json';


const IMAGES = {
    'Butler'     :   ButlerCrest,
    'Forbes'     :   ForbesCrest,
    'Independent':   PrincetonCrest,
    'Mathey'     :   MatheyCrest,
    'Rockefeller':   RockyCrest,
    'Spelman'    :   PrincetonCrest,
    'Upperclass' :   PrincetonCrest,
    'Whitman'    :   WhitmanCrest,
    'Wilson'     :   WilsonCrest,
}


function getBuilding(buildingName) {
	return buildings[name2Num[buildingName]];
}

function RoomCard(props) {
    let room = props.room;
    let draw = room.draws_in;
    let crest = IMAGES[draw];
    let shortName = getBuilding(room.building_name).shortName;
    let Heart;
    if (props.isFavorite) {
        Heart = FaHeart;
    }
    else {
        Heart = FaHeartO;
    }
	return (
		<li
              onClick={e => 
                props.getPolygons(
                  room.building_name, 
                  room.level, 
                  room.room_id
              )}
            >
                <div style={{"float":"left","height":"100%"}}>
                    <img 
                    src={crest} 
                    alt={draw}
                    style={{"float":"left","height":"100%"}}
                    />
                </div>
                <span style={{"vertical-align":"middle","font-size":"100%"}}> {shortName + " " + room.number}</span>
                <div style={{"float":"right","height":"100%"}}>
                    <Heart height="100%"
                        onClick={e => {
                            props.updateFavorites(room);
                            e.stopPropagation();
                        }}
                        color="DeepPink"
                    />
                </div>
                <div 
                  style={{"float":"right","height":"100%","margin":"0px 10px 0px 10px"}}>
                        <IoMan style={{"margin-right":"-8px"}}/> {'\u00d7' + room.num_occupants}
                </div> 
            </li>
	)
}


export default RoomCard;