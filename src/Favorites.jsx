import React from 'react';


// Expansion panel section
import ExpansionPanel, {
	ExpansionPanelSummary,
	ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from 'material-ui/Typography';

import RoomCard from './RoomCard'




function Favorites(props) {
    return (
<ExpansionPanel 
    className = "expPanel" 
    defaultExpanded={true}>
    <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
        <Typography variant="subheading">Favorites</Typography>
    </ExpansionPanelSummary>
    <ul id="favoriteButtons">
        {props.favoritesList.map(room => (
            <RoomCard 
              room={room} 
              getPolygons={props.getPolygons} 
              updateFavorites={props.updateFavorites}
              isFavorite={true}
            />
        ))}
    </ul>
</ExpansionPanel>
    )
}


export default Favorites;
