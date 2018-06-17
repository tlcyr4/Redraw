import React from 'react';

import Center from 'react-center';
import ImageMapper from './ImageMapper';
import HomeMap from './images/homeMap.png';


import BuildingCoordData from './json/building_polygons.json';
import buildings from './json/buildings.json';





class CampusMap extends React.Component {
    constructor(props) {
        super(props);
        this.imageWidthScaled = window.innerWidth * 0.43;
        this.buildingPolygons = [];
        this.buildingIDRendered = [];
        // console.log(this.buildingIDRendered);
        this.processBuildingJSON();
        // console.log(this.buildingIDRendered)
        this.MAP = {
            name: 'my-map',
            areas: this.buildingPolygons
        };
        this.fillColor = 'rgba(255, 0, 255, 0.85)';
        this.borderColor = 'rgba(200,200,250, 1)';

        this.handleClick = this.handleClick.bind(this);
    }


    // Process for The Start Screen
    processBuildingJSON() {
        const imageWidthScaled = window.innerWidth * 0.43;
        var ratio = imageWidthScaled/1166.0;
        BuildingCoordData.forEach(building => {
            var polygon = building.geometry.coordinates;
            let coordsJoined = [].concat.apply([],polygon);
            let coords = coordsJoined.map(x => parseInt(x, 10) * ratio)
            this.buildingPolygons.push({
                _id: building.properties.id,
                shape: 'poly', 
                coords: coords, 
                tooltip: {
                    name: building.properties.name, 
                    moreInfo: building.properties.type
                } 
            })
            // hold onto the order in which the buildings are added
            this.buildingIDRendered.push(building.properties);
        })

        return imageWidthScaled;
    }
    handleClick(obj, num, event) {
        let buildingNum = this.buildingIDRendered[num].id;
        this.props.getPolygons(buildings[buildingNum].name, null, null);
    }


    render() {
    return (
        <div id="centerContent">
            <Center>
                <ImageMapper
                    src={HomeMap} 
                    map={this.MAP} 
                    fillColor={this.fillColor}
                    strokeColor={this.borderColor}
                    width={this.imageWidthScaled}
                    onClick={this.handleClick}
                    lineWidth="3"
                />
            </Center>
        </div>
    )}
}

export default CampusMap;