import React from 'react';
import Center from 'react-center';
import ImageMapper from './ImageMapper';

class Floorplan extends React.Component {
    constructor(props) {
        super(props);
        this.width = window.innerWidth * 0.43;
        this.fillColor = 'rgba(255, 165, 0, 0.7)' // orange
        this.borderColor = 'rgba(255, 255, 255, 0)' // white\
    }

    render() {
        let MAP =  {
            name: 'my-map',
            areas: this.props.areaArray
        };
        return (
            <div id="centerContent">
				<Center>
					<ImageMapper
					  src={this.props.imagePath} 
					  map={MAP} 
					  fillColor={this.fillColor}
					  strokeColor={this.borderColor}
					  width={this.width}
                      onClick={(obj, num, event) => 
                        this.props.handleClick(obj, num, event)}
					  lineWidth="3"
					/>
				</Center>
			</div>
        )
    }
}

export default Floorplan;